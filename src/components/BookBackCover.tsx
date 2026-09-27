import React from 'react';
import { motion } from 'framer-motion';

interface BookBackCoverProps {
  onReopenBook?: () => void;
  language?: 'ar' | 'ku';
}

export const BookBackCover: React.FC<BookBackCoverProps> = ({ onReopenBook, language = 'ar' }) => {
  const isKurdish = language === 'ku';

  return (
    <motion.div
      data-component="BookBackCover"
      initial={{ rotateY: 110, opacity: 0, x: 120 }}
      animate={{ 
        rotateY: 0, 
        opacity: 1, 
        x: 0, 
        transition: { duration: 1.1, ease: [0.65, 0, 0.35, 1] } 
      }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="book-cover-wrapper"
    >
      <div 
        className="book-leather-cover back-cover"
        onClick={onReopenBook}
        style={{ cursor: onReopenBook ? 'pointer' : 'default' }}
        title={onReopenBook ? (isKurdish ? "کرتە لەسەر کتێبەکە بکە بۆ سەرلەنوێ کردنەوەی لە سەرەتاوە" : "انقر لإعادة فتح الكتاب من البداية") : undefined}
      >
        {/* Gold Corner Protectors */}
        <div className="gold-corner top-right"></div>
        <div className="gold-corner top-left"></div>
        <div className="gold-corner bottom-right"></div>
        <div className="gold-corner bottom-left"></div>

        <div 
          className="book-ornate-border back-cover-border"
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100%',
            padding: '2.5rem 1.5rem',
            boxSizing: 'border-box'
          }}
        >
          <div 
            className={`cover-center-content back-cover-center ${isKurdish ? 'kurdish-font' : 'qomra-font'}`}
            style={{
              margin: 0,
              padding: 0,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              gap: '1.75rem',
              width: '100%',
              maxWidth: '860px'
            }}
          >
            <h1 
              className={`thuluth-cover-title back-cover-title ${isKurdish ? 'kurdish-font' : 'qomra-font'}`}
              style={{
                fontSize: '3.1rem',
                margin: 0,
                textAlign: 'center',
                lineHeight: 1.3
              }}
            >
              {isKurdish ? "بە سپاس و ستایشەوە کۆتایی هات" : "تم بحمد الله وتوفيقه"}
            </h1>

            <div className="cover-gold-divider" style={{ margin: '0 auto' }}>
              <span className="divider-diamond">◆</span>
            </div>

            <p 
              className={`cover-sub-text back-cover-sub ${isKurdish ? 'kurdish-font' : 'qomra-font'}`}
              style={{
                fontSize: '1.45rem',
                color: '#fce8a6',
                textAlign: 'center',
                margin: '0 auto',
                maxWidth: '750px',
                lineHeight: 1.6
              }}
            >
              {isKurdish ? "کۆتایی توێژینەوەی کۆتاییهێنان بە گرێبەستی کار لە یاسای کاردا" : "خاتمة دراسة إنهاء عقد العمل في قانون الأعمال"}
            </p>

            <div 
              className="author-item back-cover-author"
              style={{
                margin: '0.4rem auto 0',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <span className="author-role back-author-role">
                {isKurdish ? "سەرپەرشتی و ڕێنوێنی:" : "إشراف وتوجيه:"}
              </span>
              <span className="author-name back-author-name">
                {isKurdish ? "مامۆستای یاریدەدەر م.ی. هالة رحمن (Ass.L. Hala Rahman)" : "الأستاذة م.م. هالة رحمن (Ass.L. Hala Rahman)"}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="book-pages-gilded-edge"></div>
    </motion.div>
  );
};
