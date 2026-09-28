import React, { useState, useEffect, useCallback } from 'react';
import { slides } from './data/slidesData';
import { SlideView } from './components/SlideView';
import { BookFrontCover } from './components/BookFrontCover';
import { BookBackCover } from './components/BookBackCover';
import { AnimatePresence } from 'framer-motion';
import { GoldenStarsCursor } from './components/GoldenStarsCursor';
import { playPageTurnSound } from './utils/audio';

export type BookState = 'closed-front' | 'reading' | 'closed-back';

export const App: React.FC = () => {
  const [bookState, setBookState] = useState<BookState>('closed-front');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [language, setLanguage] = useState<'ar' | 'ku'>('ar');

  useEffect(() => {
    document.documentElement.setAttribute('data-lang', language);
  }, [language]);

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
      } else if (e.key.toLowerCase() === 'l') {
        setLanguage((prev) => (prev === 'ar' ? 'ku' : 'ar'));
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
      <header className="top-bar">
        <div className="top-bar-right">
          <div 
            className="slide-university-badge" 
            title={language === 'ku' ? "Knowledge University — زانکۆی نۆلج" : "Knowledge University — جامعة نولج"}
          >
            <img 
              src="/knowledge_logo_gold.png" 
              alt="Knowledge University Logo" 
              className="univ-logo-img" 
            />
            <span className={`univ-badge-text ${language === 'ku' ? 'kurdish-font' : 'qomra-font'}`}>
              {language === 'ku' ? "Knowledge University — زانکۆی نۆلج" : "Knowledge University — جامعة نولج"}
            </span>
          </div>
        </div>
      </header>

      {/* Main 3D Book Stage */}
      <main className="slide-stage">
        <AnimatePresence mode="wait">
          {bookState === 'closed-front' && (
            <BookFrontCover key={`front-cover-${language}`} language={language} onOpenBook={openBook} />
          )}

          {bookState === 'reading' && (
            <SlideView 
              key={`slide-${currentSlide.id}-${language}`} 
              slide={currentSlide} 
              direction={direction} 
              language={language}
            />
          )}

          {bookState === 'closed-back' && (
            <BookBackCover key={`back-cover-${language}`} language={language} onReopenBook={reopenBook} />
          )}
        </AnimatePresence>
      </main>



      {/* Golden Stardust Mouse Trail (Hardware Accelerated) */}
      <GoldenStarsCursor />
    </div>
  );
};

export default App;
