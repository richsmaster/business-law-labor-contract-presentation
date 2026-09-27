import React, { useEffect, useRef } from 'react';

interface StarParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  maxSize: number;
  color: string;
  glowColor: string;
  alpha: number;
  decay: number;
  rotation: number;
  vRot: number;
  spikes: number;
  sparkleSpeed: number;
  age: number;
}

const GOLD_PALETTE = [
  { fill: '#fffdf2', glow: '#fde047' }, // Diamond White-Gold
  { fill: '#fde047', glow: '#d4af37' }, // Radiant 24k Gold
  { fill: '#eab308', glow: '#b45309' }, // Warm Imperial Gold
  { fill: '#fef08a', glow: '#ca8a04' }, // Champagne Sparkle
  { fill: '#d4af37', glow: '#f59e0b' }, // Classical Arabic Gold
];

export const GoldenStarsCursor: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    let animationFrameId: number | null = null;
    let isRunning = false;
    let lastTime = 0;
    let lastX = -100;
    let lastY = -100;

    const MAX_PARTICLES = 36;
    const particles: StarParticle[] = [];

    // Resize canvas to match display size with device pixel ratio
    const handleResize = () => {
      if (!canvas) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      ctx.scale(dpr, dpr);
    };

    handleResize();
    window.addEventListener('resize', handleResize, { passive: true });

    // Draw a single 4-point or 5-point star
    const drawSparkleStar = (
      p: StarParticle
    ) => {
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation);

      // Dynamic twinkle oscillation
      const twinkle = 0.8 + 0.2 * Math.sin(p.age * p.sparkleSpeed);
      const currentAlpha = Math.max(0, Math.min(1, p.alpha * twinkle));
      ctx.globalAlpha = currentAlpha;

      // Outer gold glow
      ctx.shadowColor = p.glowColor;
      ctx.shadowBlur = Math.max(4, p.size * 2);

      const spikes = p.spikes;
      const outerRadius = p.size;
      const innerRadius = p.size * 0.32;
      const step = Math.PI / spikes;

      ctx.beginPath();
      let rot = -Math.PI / 2;
      for (let i = 0; i < spikes; i++) {
        ctx.lineTo(Math.cos(rot) * outerRadius, Math.sin(rot) * outerRadius);
        rot += step;
        ctx.lineTo(Math.cos(rot) * innerRadius, Math.sin(rot) * innerRadius);
        rot += step;
      }
      ctx.closePath();
      ctx.fillStyle = p.color;
      ctx.fill();

      // Bright center core for sparkle sensation
      ctx.beginPath();
      ctx.arc(0, 0, Math.max(0.6, p.size * 0.2), 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.fill();

      ctx.restore();
    };

    // Animation Loop: only runs when particles exist to save battery & CPU
    const loop = () => {
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];

        // Physics: gentle falling gravity + air drag + subtle breeze
        p.vy += 0.055; // gravity pulling star downward
        p.vx *= 0.985; // subtle air drag
        p.vy *= 0.985;
        p.x += p.vx;
        p.y += p.vy;

        p.rotation += p.vRot;
        p.alpha -= p.decay;
        p.size *= 0.988;
        p.age += 1;

        if (p.alpha <= 0.02 || p.size <= 0.4) {
          particles.splice(i, 1);
          continue;
        }

        drawSparkleStar(p);
      }

      if (particles.length > 0) {
        animationFrameId = requestAnimationFrame(loop);
      } else {
        isRunning = false;
        animationFrameId = null;
      }
    };

    const addStar = (x: number, y: number) => {
      if (particles.length >= MAX_PARTICLES) {
        particles.shift(); // remove oldest to keep smooth 60fps
      }

      const palette = GOLD_PALETTE[Math.floor(Math.random() * GOLD_PALETTE.length)];
      const size = Math.random() * 3.8 + 2.4;
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 1.2 + 0.4;

      particles.push({
        x: x + (Math.random() - 0.5) * 6,
        y: y + (Math.random() - 0.5) * 6,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 0.7, // initial tiny upward burst before falling
        size,
        maxSize: size,
        color: palette.fill,
        glowColor: palette.glow,
        alpha: Math.random() * 0.25 + 0.75,
        decay: Math.random() * 0.022 + 0.014,
        rotation: Math.random() * Math.PI,
        vRot: (Math.random() - 0.5) * 0.12,
        spikes: Math.random() > 0.45 ? 4 : 5, // mostly 4-pointed brilliant sparkle stars
        sparkleSpeed: Math.random() * 0.25 + 0.15,
        age: 0,
      });

      if (!isRunning) {
        isRunning = true;
        animationFrameId = requestAnimationFrame(loop);
      }
    };

    const handlePointerMove = (e: PointerEvent) => {
      const now = performance.now();
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      const dist = Math.hypot(dx, dy);

      // Throttling: emit only when moved at least 5px or every 24ms
      if (dist >= 5 || now - lastTime > 24) {
        lastX = e.clientX;
        lastY = e.clientY;
        lastTime = now;

        // Emit 1 to 2 stars per step for an elegant, non-cluttered royal trail
        addStar(e.clientX, e.clientY);
        if (dist > 18) {
          addStar(e.clientX - dx * 0.4, e.clientY - dy * 0.4);
        }
      }
    };

    window.addEventListener('pointermove', handlePointerMove, { passive: true });

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('resize', handleResize);
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 99998,
        display: 'block',
      }}
    />
  );
};
