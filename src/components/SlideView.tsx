import React from 'react';
import { motion, AnimatePresence, Variants } from 'framer-motion';
import { SlideItem } from '../data/slidesData';

interface SlideViewProps {
  slide: SlideItem;
  direction: number;
  language?: 'ar' | 'ku';
}

// Ultra-Luxurious Royal Islamic Arabesque Pattern Component
const ArabesqueSidePattern: React.FC<{ side: 'right' | 'left' }> = ({ side }) => (
  <div className={`side-arabesque-ornament ${side}`}>
    <svg className="arabesque-pattern-svg" viewBox="0 0 38 600" preserveAspectRatio="none">
      <defs>
        <linearGradient id={`goldGrad-${side}`} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#fff2cc" />
          <stop offset="40%" stopColor="#d4af37" />
          <stop offset="75%" stopColor="#aa8216" />
          <stop offset="100%" stopColor="#e5c158" />
        </linearGradient>
        <filter id={`goldGlow-${side}`} x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="0" stdDeviation="2.5" floodColor="#d4af37" floodOpacity="0.5" />
        </filter>
      </defs>

      {/* Outer Border Pinstripes */}
      <line x1={side === 'right' ? '3' : '35'} y1="10" x2={side === 'right' ? '3' : '35'} y2="590" stroke={`url(#goldGrad-${side})`} strokeWidth="1.5" strokeOpacity="0.85" />
      <line x1={side === 'right' ? '7' : '31'} y1="20" x2={side === 'right' ? '7' : '31'} y2="580" stroke={`url(#goldGrad-${side})`} strokeWidth="0.8" strokeDasharray="4 3" strokeOpacity="0.7" />

      {/* Repeating 8-Pointed Star Rosettes & Interlace Lattice */}
      {[50, 130, 210, 290, 370, 450, 530].map((cy, idx) => (
        <g key={idx} filter={`url(#goldGlow-${side})`}>
          {/* Connecting Diamond Ribbon */}
          <path
            d={`M19,${cy - 36} L26,${cy - 22} L19,${cy - 8} L12,${cy - 22} Z`}
            fill="none"
            stroke={`url(#goldGrad-${side})`}
            strokeWidth="1.2"
          />
          <circle cx="19" cy={cy - 22} r="2" fill="#fff5d0" />

          {/* 8-Pointed Islamic Star (نجمة إسلامية ثمانية) */}
          {/* Square 1 */}
          <rect
            x="11"
            y={cy - 8}
            width="16"
            height="16"
            fill="rgba(212, 175, 55, 0.15)"
            stroke={`url(#goldGrad-${side})`}
            strokeWidth="1.3"
          />
          {/* Square 2 rotated 45 deg */}
          <rect
            x="11"
            y={cy - 8}
            width="16"
            height="16"
            transform={`rotate(45 19 ${cy})`}
            fill="rgba(212, 175, 55, 0.15)"
            stroke={`url(#goldGrad-${side})`}
            strokeWidth="1.3"
          />
          {/* Star Center Pearl */}
          <circle cx="19" cy={cy} r="3" fill="#fffbf0" stroke="#997314" strokeWidth="0.8" />

          {/* Floral Arabesque Winglets (توريقات نباتية) */}
          <path
            d={`M19,${cy + 10} Q28,${cy + 18} 19,${cy + 26} Q10,${cy + 18} 19,${cy + 10}`}
            fill="none"
            stroke={`url(#goldGrad-${side})`}
            strokeWidth="1.1"
          />
          <circle cx="19" cy={cy + 18} r="1.5" fill="#fce8a6" />
        </g>
      ))}

      {/* Top & Bottom Crown Finials */}
      <path d="M19,15 L26,26 L12,26 Z" fill={`url(#goldGrad-${side})`} />
      <circle cx="19" cy="11" r="2.5" fill="#fff5d0" />

      <path d="M19,585 L26,574 L12,574 Z" fill={`url(#goldGrad-${side})`} />
      <circle cx="19" cy="589" r="2.5" fill="#fff5d0" />
    </svg>
  </div>
);

// High-Detail Corner Arabesque Filigree with Medallion
const CornerFiligree: React.FC<{ position: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' }> = ({ position }) => (
  <svg className={`corner-filigree ${position}`} viewBox="0 0 64 64">
    <defs>
      <linearGradient id={`cornerGrad-${position}`} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#fff5d0" />
        <stop offset="50%" stopColor="#d4af37" />
        <stop offset="100%" stopColor="#8a6712" />
      </linearGradient>
    </defs>
    {/* Outer Corner Frame */}
    <path
      d="M4,4 L44,4 Q56,4 56,16 L56,56 Q56,4 4,4"
      fill="none"
      stroke={`url(#cornerGrad-${position})`}
      strokeWidth="1.8"
    />
    {/* Inner Arabesque Spiral */}
    <path
      d="M10,10 Q32,10 42,20 Q52,30 52,52"
      fill="none"
      stroke={`url(#cornerGrad-${position})`}
      strokeWidth="1.2"
    />
    <path
      d="M10,10 Q10,32 20,42 Q30,52 52,52"
      fill="none"
      stroke={`url(#cornerGrad-${position})`}
      strokeWidth="1.2"
    />
    {/* Floral Swirl */}
    <path
      d="M22,22 Q32,14 40,24 Q48,34 38,40 Q28,46 22,34 Z"
      fill="rgba(212, 175, 55, 0.2)"
      stroke={`url(#cornerGrad-${position})`}
      strokeWidth="1"
    />
    {/* Jewel Dots */}
    <circle cx="14" cy="14" r="3" fill="#fffdfa" stroke="#aa8216" strokeWidth="1" />
    <circle cx="48" cy="48" r="2.5" fill="#fce8a6" />
    <circle cx="30" cy="30" r="3.5" fill="#ffd700" stroke="#7a580a" strokeWidth="1" />
  </svg>
);

export const SlideView: React.FC<SlideViewProps> = ({ slide, direction, language = 'ar' }) => {
  const isKurdish = language === 'ku';
  const currentTitle = isKurdish ? (slide.titleKu || slide.title) : slide.title;
  const currentPoints = isKurdish ? (slide.pointsKu || slide.points) : slide.points;

  // Ultra-Smooth 3D Page Fold / Page Flip Transition (طية صفحة كتاب ثلاثية الأبعاد سلسة وفخمة)
  const pageFoldVariants: Variants = {
    initial: (dir: number) => ({
      rotateY: dir > 0 ? 82 : -82,
      opacity: 0,
      scale: 0.95,
      transformOrigin: dir > 0 ? 'right center' : 'left center',
      boxShadow: '0 35px 85px rgba(0,0,0,0.92), -40px 0 75px rgba(0,0,0,0.85)'
    }),
    animate: {
      rotateY: 0,
      opacity: 1,
      scale: 1,
      transformOrigin: 'right center',
      boxShadow: '0 25px 65px rgba(0,0,0,0.7), 0 0 45px rgba(212, 175, 55, 0.3)',
      transition: {
        rotateY: { duration: 0.75, ease: [0.22, 1, 0.36, 1] },
        scale: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
        opacity: { duration: 0.3 },
        when: 'beforeChildren',
        staggerChildren: 0.08
      }
    },
    exit: (dir: number) => ({
      rotateY: dir > 0 ? -92 : 92,
      opacity: 0,
      scale: 0.94,
      transformOrigin: dir > 0 ? 'right center' : 'left center',
      boxShadow: '0 35px 85px rgba(0,0,0,0.92), 40px 0 75px rgba(0,0,0,0.85)',
      transition: {
        rotateY: { duration: 0.6, ease: [0.55, 0, 0.8, 0.5] },
        scale: { duration: 0.5 },
        opacity: { duration: 0.25 }
      }
    })
  };

  // Staggered points animation with smooth entrance
  const itemVariants: Variants = {
    initial: { opacity: 0, x: 35, y: 5 },
    animate: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: { type: 'spring' as const, stiffness: 300, damping: 24 }
    }
  };

  return (
    <div className="book-open-spread" data-component="SlideView">
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={slide.id}
          data-component="SlideView"
          data-slide-id={slide.id}
          custom={direction}
          variants={pageFoldVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          className="book-page-leaf"
          style={{ perspective: 2500, backgroundColor: '#000000' }}
        >
          {/* Subtle Page Spine Fold Crease */}
          <div className="page-spine-crease"></div>

          {/* Side Islamic Arabesque Ornaments (Right & Left Margins) */}
          <ArabesqueSidePattern side="right" />
          <ArabesqueSidePattern side="left" />

          {/* Corner Filigrees on All Four Edges */}
          <CornerFiligree position="top-right" />
          <CornerFiligree position="top-left" />
          <CornerFiligree position="bottom-right" />
          <CornerFiligree position="bottom-left" />

          {/* First Page (Slide 1) Brain Background Watermark */}
          {slide.id === 1 && (
            <div className="slide-bg-brain-watermark" aria-hidden="true">
              <img src="/knowledge_brain_watermark.png" alt="Knowledge Brain Watermark" />
            </div>
          )}

          <div className="slide-grid">
            {/* Left Column: Enlarged Typography & Exactly 4-5 Concise Lines */}
            <div className="slide-content-col">
              {/* Title in Authentic Thuluth/Qomra (Arabic) or AlJazeera (Kurdish) */}
              <motion.h1
                initial={{ opacity: 0, y: -16, filter: 'blur(3px)' }}
                animate={{ 
                  opacity: 1, 
                  y: 0, 
                  filter: 'blur(0px)',
                  textShadow: [
                    "0 4px 18px rgba(0, 0, 0, 0.9), 0 0 25px rgba(212, 175, 55, 0.6)",
                    "0 4px 22px rgba(0, 0, 0, 0.9), 0 0 45px rgba(255, 235, 160, 0.85)",
                    "0 4px 18px rgba(0, 0, 0, 0.9), 0 0 25px rgba(212, 175, 55, 0.6)"
                  ]
                }}
                transition={{ 
                  opacity: { duration: 0.6, delay: 0.15 },
                  y: { duration: 0.6, delay: 0.15, ease: [0.22, 1, 0.36, 1] },
                  filter: { duration: 0.6, delay: 0.15 },
                  textShadow: { repeat: Infinity, duration: 5, ease: "easeInOut" }
                }}
                className={`slide-title-thuluth ${isKurdish ? 'jazeera-font' : 'qomra-font'}`}
              >
                {currentTitle}
              </motion.h1>

              {/* Exactly 4 to 5 Concise Bullet Points in Qomra / Al Jazeera Font */}
              <div className="points-list">
                {currentPoints.map((point, index) => {
                  const colonIndex = point.indexOf(':');
                  const hasPrefix = colonIndex !== -1 && colonIndex < 35;
                  const prefix = hasPrefix ? point.substring(0, colonIndex + 1) : '';
                  const body = hasPrefix ? point.substring(colonIndex + 1) : point;

                  return (
                    <motion.div
                      key={index}
                      variants={itemVariants}
                      className="point-card"
                    >
                      <div className="point-number-rosette">
                        <svg viewBox="0 0 32 32" className="point-star-svg">
                          <rect x="6" y="6" width="20" height="20" fill="rgba(212, 175, 55, 0.25)" stroke="#d4af37" strokeWidth="1.2" />
                          <rect x="6" y="6" width="20" height="20" transform="rotate(45 16 16)" fill="rgba(212, 175, 55, 0.25)" stroke="#d4af37" strokeWidth="1.2" />
                        </svg>
                        <span className="point-digit">{index + 1}</span>
                      </div>
                      <div className={`point-text ${isKurdish ? 'jazeera-font' : 'qomra-font'}`}>
                        {hasPrefix ? (
                          <>
                            <strong className="point-gold-prefix">{prefix}</strong>
                            <span>{body}</span>
                          </>
                        ) : (
                          point
                        )}
                      </div>
                    </motion.div>
                  );
                })}
              </div>


            </div>

            {/* Right Column: Erbil Landmark & Authentic Iraqi Legal Contract Image */}
            <div className="slide-media-col">
              <motion.div
                initial={{ opacity: 0, scale: 0.93 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.55, delay: 0.2 }}
                className="image-card-wrapper"
              >
                <img
                  src={slide.image}
                  alt={slide.title}
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    if (target.src.startsWith('/')) {
                      target.src = target.src.substring(1);
                    }
                  }}
                />
              </motion.div>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
