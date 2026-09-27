import React, { useState, useEffect, useCallback } from 'react';
import { slides } from './data/slidesData';
import { SlideView } from './components/SlideView';
import { BookFrontCover } from './components/BookFrontCover';
import { BookBackCover } from './components/BookBackCover';
import { AnimatePresence } from 'framer-motion';
import { Layers } from 'lucide-react';
import { VisualEditor } from './components/VisualEditor';
import { playPageTurnSound } from './utils/audio';

export type BookState = 'closed-front' | 'reading' | 'closed-back';

export const App: React.FC = () => {
  const [bookState, setBookState] = useState<BookState>('closed-front');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isVisualEditorActive, setIsVisualEditorActive] = useState<boolean>(() => {
    try {
      return localStorage.getItem('visual-editor-enabled') === 'on';
    } catch {
      return false;
    }
  });

  useEffect(() => {
    const handleStateChange = (e: Event) => {
      const detail = (e as CustomEvent).detail;
      setIsVisualEditorActive(detail?.enabled ?? false);
    };
    window.addEventListener('visualEditorStateChange', handleStateChange);
    return () => window.removeEventListener('visualEditorStateChange', handleStateChange);
  }, []);

  const totalSlides = slides.length;

  const openBook = () => {
    playPageTurnSound(true);
    setBookState('reading');
    setCurrentIndex(0);
    setDirection(1);
  };

  const closeBookAtEnd = () => {
    playPageTurnSound(true);
    setBookState('closed-back');
    setIsPlaying(false);
  };

  const reopenBook = () => {
    playPageTurnSound(true);
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
        playPageTurnSound(false);
        setDirection(1);
        setCurrentIndex((prev) => prev + 1);
      } else {
        closeBookAtEnd();
      }
    }
  }, [bookState, currentIndex, totalSlides]);

  const goToPrev = useCallback(() => {
    if (bookState === 'closed-back') {
      playPageTurnSound(false);
      setBookState('reading');
      setCurrentIndex(totalSlides - 1);
      setDirection(-1);
      return;
    }

    if (bookState === 'reading') {
      if (currentIndex - 1 >= 0) {
        playPageTurnSound(false);
        setDirection(-1);
        setCurrentIndex((prev) => prev - 1);
      } else {
        playPageTurnSound(true);
        setBookState('closed-front');
      }
    }
  }, [bookState, currentIndex, totalSlides]);

  const goToSlide = (index: number) => {
    if (index !== currentIndex || bookState !== 'reading') {
      playPageTurnSound(false);
    }
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
      document.documentElement.requestFullscreen().catch(err => {
        console.error(err);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  };

  const currentSlide = slides[currentIndex];

  return (
    <div className="presentation-container">
      {/* Top Header Bar */}
      <header className="top-bar" style={{ justifyContent: 'flex-end' }}>
        <button
          className="btn-guide-link"
          style={{
            background: isVisualEditorActive ? 'rgba(16, 185, 129, 0.22)' : 'rgba(255, 255, 255, 0.08)',
            borderColor: isVisualEditorActive ? '#10b981' : 'rgba(212, 175, 55, 0.45)',
            color: isVisualEditorActive ? '#34d399' : undefined,
            boxShadow: isVisualEditorActive ? '0 0 15px rgba(16, 185, 129, 0.35)' : 'none',
            cursor: 'pointer'
          }}
          onClick={() => {
            window.dispatchEvent(new CustomEvent('visualEditorToggle'));
          }}
          title="تشغيل/إيقاف المحرر المرئي وفاحص العناصر مثل clincsa (Ctrl+Shift+D)"
        >
          <Layers size={18} />
          <span>{isVisualEditorActive ? 'المحرر المرئي (نشط)' : 'المحرر المرئي'}</span>
        </button>
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



      {/* Visual Editor & Element Inspector (identical to clincsa DevInspector) */}
      <VisualEditor />
    </div>
  );
};

export default App;
