import React, { useState, useEffect, useCallback } from 'react';
import { slides } from './data/slidesData';
import { SlideView } from './components/SlideView';
import { BookFrontCover } from './components/BookFrontCover';
import { BookBackCover } from './components/BookBackCover';
import { AnimatePresence } from 'framer-motion';
import { 
  ChevronRight, 
  ChevronLeft, 
  Maximize2, 
  Minimize2, 
  Play, 
  Pause, 
  Scale, 
  RotateCcw,
  BookMarked,
  FileText,
  Download
} from 'lucide-react';

export type BookState = 'closed-front' | 'reading' | 'closed-back';

export const App: React.FC = () => {
  const [bookState, setBookState] = useState<BookState>('closed-front');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const totalSlides = slides.length;

  const openBook = () => {
    setBookState('reading');
    setCurrentIndex(0);
    setDirection(1);
  };

  const closeBookAtEnd = () => {
    setBookState('closed-back');
    setIsPlaying(false);
  };

  const reopenBook = () => {
    setBookState('reading');
    setCurrentIndex(0);
    setDirection(1);
  };

  const goToNext = useCallback(() => {
    if (bookState === 'closed-front') {
      openBook();
      return;
    }

    if (bookState === 'reading') {
      if (currentIndex + 1 < totalSlides) {
        setDirection(1);
        setCurrentIndex((prev) => prev + 1);
      } else {
        closeBookAtEnd();
      }
    }
  }, [bookState, currentIndex, totalSlides]);

  const goToPrev = useCallback(() => {
    if (bookState === 'closed-back') {
      setBookState('reading');
      setCurrentIndex(totalSlides - 1);
      setDirection(-1);
      return;
    }

    if (bookState === 'reading') {
      if (currentIndex - 1 >= 0) {
        setDirection(-1);
        setCurrentIndex((prev) => prev - 1);
      } else {
        setBookState('closed-front');
      }
    }
  }, [bookState, currentIndex, totalSlides]);

  const goToSlide = (index: number) => {
    setBookState('reading');
    setDirection(index > currentIndex ? 1 : -1);
    setCurrentIndex(index);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft' || e.key === ' ' || e.key === 'PageDown') {
        goToNext();
      } else if (e.key === 'ArrowRight' || e.key === 'PageUp') {
        goToPrev();
      } else if (e.key === 'Home') {
        goToSlide(0);
      } else if (e.key === 'End') {
        closeBookAtEnd();
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullscreen();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [goToNext, goToPrev]);

  // Autoplay slideshow
  useEffect(() => {
    let interval: any = null;
    if (isPlaying && bookState === 'reading') {
      interval = setInterval(() => {
        goToNext();
      }, 7500);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, bookState, goToNext]);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().then(() => {
        setIsFullscreen(true);
      }).catch(err => {
        console.error(err);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().then(() => {
          setIsFullscreen(false);
        });
      }
    }
  };

  const currentSlide = slides[currentIndex];

  return (
    <div className="presentation-container">
      {/* Top Header Bar */}
      <header className="top-bar">
        <div className="top-bar-left">
          <div className="course-badge">
            <Scale size={18} />
            <span>Business Law | قانون الأعمال</span>
          </div>
          <div className="supervisor-text qomra-font">
            <span>إشراف الأستاذة: </span>
            <span className="supervisor-name">م.م. هالة رحمن (Ass.L. Hala Rahman)</span>
          </div>
        </div>

        <div className="top-bar-right">
          <a
            href="/دليل_شرح_التقرير_الشامل.html"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-guide-link"
            title="فتح الشرح الأكاديمي الشامل للتقرير في جذر المشروع"
          >
            <FileText size={18} />
            <span>شرح التقرير الشامل</span>
          </a>

          <a
            href="/تقرير_انهاء_عقد_العمل_6_صفحات.pdf"
            target="_blank"
            download
            className="btn-guide-link"
            style={{ background: 'rgba(255, 255, 255, 0.08)', borderColor: 'rgba(212, 175, 55, 0.45)' }}
            title="تحميل وثيقة التقرير الرسمية PDF (6 صفحات)"
          >
            <Download size={18} />
            <span>وثيقة التقرير PDF</span>
          </a>

          {bookState === 'reading' && (
            <>
              <span className="slide-counter">
                {currentSlide.slideNumber}
              </span>
              <button 
                className="btn-close-book-nav" 
                onClick={closeBookAtEnd}
                title="إغلاق الكتاب"
              >
                <BookMarked size={16} />
                <span>إغلاق الكتاب</span>
              </button>
            </>
          )}

          <button 
            className="btn-control" 
            onClick={toggleFullscreen} 
            title={isFullscreen ? "إنهاء ملء الشاشة (F)" : "ملء الشاشة (F)"}
          >
            {isFullscreen ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
          </button>
        </div>
      </header>

      {/* Main 3D Book Stage */}
      <main className="slide-stage">
        <AnimatePresence mode="wait">
          {bookState === 'closed-front' && (
            <BookFrontCover key="front-cover" onOpenBook={openBook} />
          )}

          {bookState === 'reading' && (
            <SlideView 
              key={`slide-${currentSlide.id}`} 
              slide={currentSlide} 
              direction={direction} 
            />
          )}

          {bookState === 'closed-back' && (
            <BookBackCover key="back-cover" onReopenBook={reopenBook} />
          )}
        </AnimatePresence>
      </main>

      {/* Bottom Controls Bar */}
      <footer className="bottom-bar">
        {bookState === 'reading' ? (
          <>
            {/* Slide Indicator Dots */}
            <div className="slide-dots">
              {slides.map((_, idx) => (
                <button
                  key={idx}
                  className={`slide-dot ${idx === currentIndex ? 'active' : ''}`}
                  onClick={() => goToSlide(idx)}
                  title={`الصفحة ${idx + 1}`}
                />
              ))}
            </div>

            {/* Navigation Controls with 3D Page Turn */}
            <div className="controls-group">
              <button 
                className="btn-control" 
                onClick={() => setBookState('closed-front')} 
                title="الرجوع لغلاف الكتاب"
              >
                <RotateCcw size={16} />
              </button>

              <button 
                className="btn-control" 
                onClick={goToPrev} 
                title="طي الصفحة للخلف (السهم الأيمن)"
              >
                <ChevronRight size={22} />
              </button>

              <button 
                className="btn-action-primary" 
                onClick={() => setIsPlaying(!isPlaying)}
                title={isPlaying ? "إيقاف التصفح التلقائي" : "بدء التصفح التلقائي"}
              >
                {isPlaying ? <Pause size={18} /> : <Play size={18} />}
                <span className="qomra-font">{isPlaying ? "إيقاف" : "تصفح تلقائي"}</span>
              </button>

              <button 
                className="btn-control" 
                onClick={goToNext} 
                title="طي الصفحة للأمام (السهم الأيسر أو مسافة)"
              >
                <ChevronLeft size={22} />
              </button>
            </div>
          </>
        ) : (
          <div className="cover-footer-note qomra-font">
            {bookState === 'closed-front' ? 
              "اضغط على زر (افتح الكتاب) أو استخدم مسافة/الأسهم لبدء تصفح صفحات التقرير" :
              "تم استعراض كامل صفحات المبحث الثاني — انقر لإعادة الفتح أو استخدام الأسهم"
            }
          </div>
        )}

        {/* Keyboard hints */}
        <div className="keyboard-hint qomra-font">
          <span>التنقل بالصفحات:</span>
          <span className="key-cap">◀</span>
          <span className="key-cap">▶</span>
          <span className="key-cap">Space</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
