import React from 'react';
import { motion } from 'framer-motion';
import { RotateCcw, ShieldCheck } from 'lucide-react';

interface BookBackCoverProps {
  onReopenBook: () => void;
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
      <div className="book-leather-cover back-cover">
        {/* Gold Corner Protectors */}
        <div className="gold-corner top-right"></div>
        <div className="gold-corner top-left"></div>
        <div className="gold-corner bottom-right"></div>
        <div className="gold-corner bottom-left"></div>

        <div className="book-ornate-border">
          <div className="cover-center-content">
            <div className="gold-medallion">
              <ShieldCheck size={48} color="#d4af37" />
            </div>

            <h1 className="thuluth-cover-title" style={{ fontSize: '2.5rem' }}>
              تم بحمد الله وتوفيقه
            </h1>

            <div className="cover-gold-divider">
              <span className="divider-diamond">◆</span>
            </div>

            <p className="cover-sub-text" style={{ fontSize: '1.2rem', color: '#f8fafc' }}>
              خاتمة دراسة إنهاء عقد العمل في قانون الأعمال
            </p>



            <div className="author-item" style={{ marginTop: '1.5rem' }}>
              <span className="author-role">إشراف وتوجيه:</span>
              <span className="author-name" style={{ fontSize: '1.1rem' }}>
                الأستاذة م.م. هالة رحمن (Ass.L. Hala Rahman)
              </span>
            </div>

            {/* Reopen Action Button */}
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: "0 0 35px rgba(212, 175, 55, 0.7)" }}
              whileTap={{ scale: 0.96 }}
              onClick={onReopenBook}
              className="btn-open-book"
              style={{ marginTop: '2rem' }}
            >
              <RotateCcw size={20} />
              <span>إعادة فتح الكتاب من البداية</span>
            </motion.button>
          </div>

          <div className="cover-bottom-year">
            جميع الحقوق محفوظة © 2026 — كلية القانون / إدارة الأعمال
          </div>
        </div>
      </div>

      <div className="book-pages-gilded-edge"></div>
    </motion.div>
  );
};
