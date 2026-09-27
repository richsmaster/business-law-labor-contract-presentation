import React from 'react';
import { motion } from 'framer-motion';
import { Scale } from 'lucide-react';

interface BookFrontCoverProps {
  onOpenBook: () => void;
}

// Royal Illuminated Islamic Corner Arabesque (زخرفة تذهيب ركنية أندلسية متصلة)
const RoyalManuscriptCorner: React.FC<{ position: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' }> = ({ position }) => (
  <svg className={`cover-corner-ornament ${position}`} viewBox="0 0 96 96">
    <defs>
      <linearGradient id={`goldCornerGrad-${position}`} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#fffdf0" />
        <stop offset="35%" stopColor="#f5d36e" />
        <stop offset="70%" stopColor="#d4af37" />
        <stop offset="100%" stopColor="#8c6410" />
      </linearGradient>
      <radialGradient id={`starRosetteBg-${position}`}>
        <stop offset="0%" stopColor="rgba(255, 235, 160, 0.4)" />
        <stop offset="70%" stopColor="rgba(212, 175, 55, 0.15)" />
        <stop offset="100%" stopColor="transparent" />
      </radialGradient>
      <filter id={`filigreeGlow-${position}`} x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="0" stdDeviation="2.5" floodColor="#d4af37" floodOpacity="0.8" />
      </filter>
    </defs>

    {/* Elegant Diagonal Scalloped Arch connecting the two margins */}
    <path
      d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z"
      fill={`url(#starRosetteBg-${position})`}
      stroke={`url(#goldCornerGrad-${position})`}
      strokeWidth="1.6"
      filter={`url(#filigreeGlow-${position})`}
    />

    {/* Inner Arabesque Lace Outline */}
    <path
      d="M10,10 L76,10 Q76,26 64,38 Q52,50 38,64 Q26,76 10,76 Z"
      fill="none"
      stroke={`url(#goldCornerGrad-${position})`}
      strokeWidth="1"
      strokeDasharray="3 2"
      opacity="0.9"
    />

    {/* 8-Pointed Islamic Star Medallion in Corner (نجمة أندلسية مذهبة) */}
    <g transform="translate(30, 30)">
      <rect x="-10" y="-10" width="20" height="20" fill="rgba(212, 175, 55, 0.4)" stroke={`url(#goldCornerGrad-${position})`} strokeWidth="1.2" />
      <rect x="-10" y="-10" width="20" height="20" transform="rotate(45)" fill="rgba(212, 175, 55, 0.4)" stroke={`url(#goldCornerGrad-${position})`} strokeWidth="1.2" />
      <circle cx="0" cy="0" r="3.5" fill="#ffffff" stroke="#997314" strokeWidth="0.8" />
    </g>

    {/* Flowing Arabesque Spirals & Palmette Leaves */}
    <path
      d="M12,12 Q40,14 48,22 Q54,30 46,38 Q38,46 30,54 Q22,48 14,40"
      fill="none"
      stroke={`url(#goldCornerGrad-${position})`}
      strokeWidth="1.2"
    />
    <path
      d="M16,24 Q32,24 38,30 Q44,36 38,42 Q32,48 24,42"
      fill="none"
      stroke={`url(#goldCornerGrad-${position})`}
      strokeWidth="1"
      opacity="0.85"
    />

    {/* Jewel Dots on Border Finials */}
    <circle cx="8" cy="8" r="3" fill="#ffffff" stroke="#997314" strokeWidth="0.9" />
    <circle cx="84" cy="6" r="2.2" fill="#ffd700" />
    <circle cx="6" cy="84" r="2.2" fill="#ffd700" />
    <circle cx="60" cy="60" r="2" fill="#fce8a6" />
  </svg>
);

// Royal Top Headpiece Arch (تاج إسلامي سلطاني مذهب)
const RoyalTopHeadpiece: React.FC = () => (
  <div className="cover-top-headpiece">
    <svg viewBox="0 0 460 36" className="headpiece-svg">
      <defs>
        <linearGradient id="headpieceGold" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="transparent" />
          <stop offset="20%" stopColor="#997314" />
          <stop offset="50%" stopColor="#fff8e7" />
          <stop offset="80%" stopColor="#997314" />
          <stop offset="100%" stopColor="transparent" />
        </linearGradient>
      </defs>
      {/* Islamic Pointed Mihrab Arch */}
      <path
        d="M20,32 Q130,32 185,16 Q210,6 230,2 Q250,6 275,16 Q330,32 440,32"
        fill="none"
        stroke="url(#headpieceGold)"
        strokeWidth="2.2"
      />
      <path
        d="M50,28 Q140,28 190,14 Q210,6 230,4 Q250,6 270,14 Q320,28 410,28"
        fill="none"
        stroke="url(#headpieceGold)"
        strokeWidth="1"
        strokeDasharray="4 3"
      />
      {/* Central Diamond Starburst Finial */}
      <polygon points="230,-2 237,6 230,14 223,6" fill="#fffdfa" stroke="#d4af37" strokeWidth="1.2" />
      <circle cx="230" cy="6" r="2" fill="#aa8216" />
      <circle cx="195" cy="15" r="2.2" fill="#fce8a6" />
      <circle cx="265" cy="15" r="2.2" fill="#fce8a6" />
    </svg>
  </div>
);

// Calligraphic Medallion Seal (شمسة إسلامية مذهبة مع ميزان العدالة)
// Calligraphic Medallion Seal (شمسة إسلامية مذهبة مع ميزان العدالة)
const RoyalShamsehSeal: React.FC = () => (
  <motion.div 
    className="cover-shamseh-seal"
    initial={{ scale: 0.88, opacity: 0 }}
    animate={{ 
      scale: 1, 
      opacity: 1,
      y: [0, -5, 0]
    }}
    transition={{ 
      scale: { duration: 0.7, ease: [0.22, 1, 0.36, 1] },
      opacity: { duration: 0.7 },
      y: { repeat: Infinity, duration: 4.5, ease: "easeInOut" }
    }}
  >
    <svg viewBox="0 0 90 90" className="shamseh-svg">
      <defs>
        <linearGradient id="shamsehGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#fffdf0" />
          <stop offset="35%" stopColor="#f5d36e" />
          <stop offset="70%" stopColor="#d4af37" />
          <stop offset="100%" stopColor="#7a550a" />
        </linearGradient>
        <radialGradient id="shamsehCenterGlow">
          <stop offset="0%" stopColor="rgba(212, 175, 55, 0.4)" />
          <stop offset="70%" stopColor="rgba(30, 18, 10, 0.92)" />
          <stop offset="100%" stopColor="rgba(12, 7, 3, 0.98)" />
        </radialGradient>
      </defs>
      {/* Outer 16-point radiating ring */}
      <circle cx="45" cy="45" r="42" fill="none" stroke="url(#shamsehGoldGrad)" strokeWidth="1.3" strokeDasharray="3 3" />
      <circle cx="45" cy="45" r="39" fill="url(#shamsehCenterGlow)" stroke="url(#shamsehGoldGrad)" strokeWidth="1.8" />
      
      {/* Double 8-Pointed Star Rosette */}
      <rect x="20" y="20" width="50" height="50" fill="none" stroke="url(#shamsehGoldGrad)" strokeWidth="1.4" opacity="0.95" />
      <rect x="20" y="20" width="50" height="50" transform="rotate(45 45 45)" fill="none" stroke="url(#shamsehGoldGrad)" strokeWidth="1.4" opacity="0.95" />
      
      {/* Inner Decorative Circle */}
      <circle cx="45" cy="45" r="23" fill="rgba(212, 175, 55, 0.18)" stroke="url(#shamsehGoldGrad)" strokeWidth="1.2" />
    </svg>
    <motion.div 
      className="shamseh-icon-overlay"
      animate={{ rotate: [-2, 2, -2] }}
      transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
    >
      <Scale size={26} color="#fff8e7" />
    </motion.div>
  </motion.div>
);

// Royal Calligraphic Flourish Divider (فاصل تذهيبي للمخطوطات)
const CalligraphicFlourish: React.FC = () => (
  <motion.div 
    className="calligraphic-flourish"
    initial={{ opacity: 0, scaleX: 0.85 }}
    animate={{ opacity: 1, scaleX: 1 }}
    transition={{ duration: 0.8, delay: 0.45, ease: [0.22, 1, 0.36, 1] }}
  >
    <span className="flourish-line right"></span>
    <span className="flourish-leaf">✤</span>
    <motion.span 
      className="flourish-diamond"
      animate={{ 
        scale: [1, 1.25, 1],
        filter: [
          "drop-shadow(0 0 6px rgba(212, 175, 55, 0.6))",
          "drop-shadow(0 0 14px rgba(255, 235, 160, 0.95))",
          "drop-shadow(0 0 6px rgba(212, 175, 55, 0.6))"
        ]
      }}
      transition={{ repeat: Infinity, duration: 3.6, ease: "easeInOut" }}
    >
      ❖
    </motion.span>
    <span className="flourish-leaf">✤</span>
    <span className="flourish-line left"></span>
  </motion.div>
);

export const BookFrontCover: React.FC<BookFrontCoverProps> = ({ onOpenBook }) => {
  return (
    <motion.div
      data-component="BookFrontCover"
      initial={{ scale: 0.94, opacity: 0, rotateY: 15 }}
      animate={{ scale: 1, opacity: 1, rotateY: 0 }}
      exit={{ 
        rotateY: -115, 
        opacity: 0,
        x: -140,
        transition: { duration: 1.15, ease: [0.65, 0, 0.35, 1] } 
      }}
      className="book-cover-wrapper"
    >
      <motion.div 
        className="book-leather-cover clickable-cover"
        onClick={onOpenBook}
        whileHover={{ 
          scale: 1.012, 
          borderColor: '#ffd700',
          boxShadow: 'inset 0 0 85px rgba(0, 0, 0, 0.98), inset 0 0 50px rgba(212, 175, 55, 0.55), 0 0 55px rgba(212, 175, 55, 0.35)' 
        }}
        whileTap={{ scale: 0.992 }}
        transition={{ duration: 0.35, ease: [0.2, 0.8, 0.2, 1] }}
        title="انقر على الكتاب للفتح وبدء تصفح التقرير الأكاديمي"
      >
        {/* Ornate Gold Foil Interior Border */}
        <div className="book-ornate-border">
          {/* Authentic Illuminated Corner Ornaments Integrated directly into Frame */}
          <RoyalManuscriptCorner position="top-right" />
          <RoyalManuscriptCorner position="top-left" />
          <RoyalManuscriptCorner position="bottom-right" />
          <RoyalManuscriptCorner position="bottom-left" />

          {/* Leather Book Spine Line with Stamped Shadow */}
          <div className="book-spine-line"></div>

          {/* Top Royal Crown Arch */}
          <RoyalTopHeadpiece />

          {/* Knowledge University Brain Watermark on Book Front Cover */}
          <div className="cover-brain-watermark" aria-hidden="true">
            <img src="/knowledge_brain_watermark.png" alt="Knowledge University Brain Watermark" />
          </div>

          {/* Central Illumination & Calligraphic Title Area */}
          <div className="cover-center-content qomra-font">
            {/* Islamic Shamseh Seal with Scales of Justice */}
            <RoyalShamsehSeal />

            {/* Illuminated Title Frame & Grand Calligraphic Title */}
            <motion.div 
              className="cover-title-container"
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.75, delay: 0.15, ease: [0.22, 1, 0.36, 1] }}
            >
              <h1 className="thuluth-cover-title qomra-font">
                <motion.span 
                  className="title-row-1"
                  initial={{ opacity: 0, y: 16, filter: 'blur(3px)' }}
                  animate={{ 
                    opacity: 1, 
                    y: 0, 
                    filter: 'blur(0px)',
                    textShadow: [
                      "0 4px 20px rgba(0, 0, 0, 0.95), 0 0 35px rgba(212, 175, 55, 0.7), 0 0 70px rgba(212, 175, 55, 0.35)",
                      "0 4px 24px rgba(0, 0, 0, 0.95), 0 0 55px rgba(255, 235, 160, 0.95), 0 0 95px rgba(212, 175, 55, 0.65)",
                      "0 4px 20px rgba(0, 0, 0, 0.95), 0 0 35px rgba(212, 175, 55, 0.7), 0 0 70px rgba(212, 175, 55, 0.35)"
                    ]
                  }}
                  transition={{ 
                    opacity: { duration: 0.7, delay: 0.2 },
                    y: { duration: 0.7, delay: 0.2, ease: [0.22, 1, 0.36, 1] },
                    filter: { duration: 0.7, delay: 0.2 },
                    textShadow: { repeat: Infinity, duration: 4.8, ease: "easeInOut" }
                  }}
                >
                  إنهاء عقد العمل
                </motion.span>
                <motion.span 
                  className="title-row-2"
                  initial={{ opacity: 0, y: 12, filter: 'blur(3px)' }}
                  animate={{ 
                    opacity: 1, 
                    y: 0, 
                    filter: 'blur(0px)',
                    textShadow: [
                      "0 4px 18px rgba(0, 0, 0, 0.95), 0 0 28px rgba(212, 175, 55, 0.6)",
                      "0 4px 20px rgba(0, 0, 0, 0.95), 0 0 45px rgba(252, 232, 166, 0.85)",
                      "0 4px 18px rgba(0, 0, 0, 0.95), 0 0 28px rgba(212, 175, 55, 0.6)"
                    ]
                  }}
                  transition={{ 
                    opacity: { duration: 0.7, delay: 0.35 },
                    y: { duration: 0.7, delay: 0.35, ease: [0.22, 1, 0.36, 1] },
                    filter: { duration: 0.7, delay: 0.35 },
                    textShadow: { repeat: Infinity, duration: 4.8, ease: "easeInOut", delay: 0.8 }
                  }}
                >
                  بإرادة أحد طرفيه أو كليهما
                </motion.span>
              </h1>
            </motion.div>

            {/* Royal Calligraphic Flourish Divider */}
            <CalligraphicFlourish />
          </div>

          {/* Bottom Academic Year & Seal */}
          <motion.div 
            className="cover-bottom-year"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.55 }}
          >
            <span style={{ color: 'var(--gold-bright)', marginLeft: 8 }}>❖</span>
            العام الأكاديمي 2026 — كلية القانون / إدارة الأعمال — أربيل / بغداد
            <span style={{ color: 'var(--gold-bright)', marginRight: 8 }}>❖</span>
          </motion.div>
        </div>
      </motion.div>

      {/* 3D Gilded Book Pages Edge */}
      <div className="book-pages-gilded-edge"></div>
    </motion.div>
  );
};
