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

        <div className="book-ornate-border">
          <div className={`cover-center-content ${isKurdish ? 'jazeera-font' : 'qomra-font'}`}>
            <h1 className={`thuluth-cover-title ${isKurdish ? 'jazeera-font' : 'qomra-font'}`} style={{ fontSize: '2.5rem' }}>
              {isKurdish ? "بە سپاس و ستایشەوە کۆتایی هات" : "تم بحمد الله وتوفيقه"}
            </h1>

            <div className="cover-gold-divider">
              <span className="divider-diamond">◆</span>
            </div>

            <p className={`cover-sub-text ${isKurdish ? 'jazeera-font' : 'qomra-font'}`} style={{ fontSize: '1.2rem', color: '#f8fafc' }}>
              {isKurdish ? "کۆتایی توێژینەوەی کۆتاییهێنان بە گرێبەستی کار لە یاسای کاردا" : "خاتمة دراسة إنهاء عقد العمل في قانون الأعمال"}
            </p>

            <div className="author-item back-cover-author">
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
