import React from 'react';
import { motion } from 'framer-motion';

interface BookBackCoverProps {
  onReopenBook?: () => void;
}

export const BookBackCover: React.FC<BookBackCoverProps> = ({ onReopenBook }) => {
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
        title={onReopenBook ? "انقر لإعادة فتح الكتاب من البداية" : undefined}
      >
        {/* Gold Corner Protectors */}
        <div className="gold-corner top-right"></div>
        <div className="gold-corner top-left"></div>
        <div className="gold-corner bottom-right"></div>
        <div className="gold-corner bottom-left"></div>

        <div className="book-ornate-border">
          <div className="cover-center-content">
            <h1 className="thuluth-cover-title" style={{ fontSize: '2.5rem' }}>
              تم بحمد الله وتوفيقه
            </h1>

            <div className="cover-gold-divider">
              <span className="divider-diamond">◆</span>
            </div>

            <p className="cover-sub-text" style={{ fontSize: '1.2rem', color: '#f8fafc' }}>
              خاتمة دراسة إنهاء عقد العمل في قانون الأعمال
            </p>



            <div className="author-item back-cover-author">
              <span className="author-role back-author-role">إشراف وتوجيه:</span>
              <span className="author-name back-author-name">
                الأستاذة م.م. هالة رحمن (Ass.L. Hala Rahman)
              </span>
            </div>


          </div>
        </div>
      </div>

      <div className="book-pages-gilded-edge"></div>
    </motion.div>
  );
};
