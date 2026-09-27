import React, { useState, useEffect, useCallback, useRef } from 'react';
import { SlideItem } from '../data/slidesData';

// ─── Types ──────────────────────────────────────────────────────────

export interface ElementInfo {
  element: HTMLElement;
  componentName: string | null;
  filePath: string | null;
  elementType: string;
  elementTypeAr: string;
  label: string;
  selector: string;
  domPath: string;
  attributes: string[];
  rect: DOMRect;
  computedStyles: {
    color: string;
    backgroundColor: string;
    fontSize: string;
    fontWeight: string;
    padding: string;
    margin: string;
    lineHeight: string;
  };
  slideInfo?: {
    slideId: number;
    slideBadge: string;
    slideTitle: string;
  };
}

interface VisualEditorProps {
  slides?: SlideItem[];
  onUpdateSlideText?: (slideId: number, field: string, value: string) => void;
}

// ─── Constants & Dictionaries ───────────────────────────────────────

const ELEMENT_TYPE_AR: Record<string, string> = {
  button: 'زر تفاعلي',
  link: 'رابط تشعبي',
  input: 'حقل إدخال',
  textarea: 'منطقة نص',
  select: 'قائمة منسدلة',
  checkbox: 'مربع اختيار',
  radio: 'زر راديو',
  switch: 'مفتاح تبديل',
  image: 'صورة',
  icon: 'أيقونة / رمز',
  card: 'بطاقة محتوى',
  text: 'نص',
  heading: 'عنوان',
  list: 'قائمة نقاط',
  listItem: 'عنصر قائمة',
  nav: 'شريط تنقل',
  sidebar: 'شريط جانبي',
  header: 'شريط علوي',
  footer: 'شريط سفلي',
  section: 'قسم شريحة',
  form: 'نموذج',
  table: 'جدول',
  dialog: 'نافذة حوار',
  badge: 'شارة / وسم',
  container: 'حاوية',
  slide: 'شريحة كتاب',
  bookCover: 'غلاف كتاب أندلسي',
  unknown: 'عنصر واجهة',
};

const SEMANTIC_CONTAINERS = new Set([
  'nav', 'aside', 'main', 'section', 'article', 'form',
  'header', 'footer', 'ul', 'ol', 'table', 'dialog',
]);

// ─── Component & File Path Auto-Detection ───────────────────────────

function getReactFiber(node: HTMLElement): any {
  const key = Object.keys(node).find(
    k => k.startsWith('__reactFiber$') || k.startsWith('__reactInternalInstance$')
  );
  return key ? (node as any)[key] : null;
}

function detectComponentAndFile(element: HTMLElement): { name: string; filePath: string } {
  // 1. Check explicit data-component attribute
  let el: HTMLElement | null = element;
  while (el && el !== document.body) {
    const compAttr = el.getAttribute('data-component');
    if (compAttr) {
      if (compAttr === 'BookFrontCover') return { name: 'BookFrontCover', filePath: 'src/components/BookFrontCover.tsx' };
      if (compAttr === 'BookBackCover') return { name: 'BookBackCover', filePath: 'src/components/BookBackCover.tsx' };
      if (compAttr === 'SlideView') return { name: 'SlideView', filePath: 'src/components/SlideView.tsx' };
      if (compAttr === 'App') return { name: 'App', filePath: 'src/App.tsx' };
      return { name: compAttr, filePath: `src/components/${compAttr}.tsx` };
    }

    // Heuristics by class names
    const cls = typeof el.className === 'string' ? el.className : '';
    if (cls.includes('book-leather-cover') && cls.includes('back-cover')) {
      return { name: 'BookBackCover', filePath: 'src/components/BookBackCover.tsx' };
    }
    if (cls.includes('book-leather-cover') || cls.includes('book-cover-wrapper')) {
      return { name: 'BookFrontCover', filePath: 'src/components/BookFrontCover.tsx' };
    }
    if (cls.includes('book-page-leaf') || cls.includes('slide-grid') || cls.includes('slide-content-col') || cls.includes('point-card')) {
      return { name: 'SlideView', filePath: 'src/components/SlideView.tsx' };
    }
    if (cls.includes('top-bar') || cls.includes('bottom-bar') || cls.includes('presentation-container')) {
      return { name: 'App', filePath: 'src/App.tsx' };
    }

    el = el.parentElement;
  }

  // 2. Walk React fiber tree
  let fiber = getReactFiber(element);
  let domEl: HTMLElement | null = element;
  while (!fiber && domEl?.parentElement) {
    domEl = domEl.parentElement;
    fiber = getReactFiber(domEl);
  }

  let fiberName: string | null = null;
  let fiberFile: string | null = null;

  while (fiber) {
    const name = fiber.type?.displayName || fiber.type?.name;
    if (name && typeof name === 'string' && /^[A-Z]/.test(name) && !['Fragment', 'MotionComponent'].includes(name)) {
      if (!fiberName) fiberName = name;
      if (fiber._debugSource?.fileName) {
        fiberFile = fiber._debugSource.fileName;
        break;
      }
    }
    fiber = fiber.return;
  }

  if (fiberName) {
    const normalizedFile = fiberFile ? fiberFile.replace(/\\/g, '/').replace(/^.*src\//, 'src/') : `src/components/${fiberName}.tsx`;
    return { name: fiberName, filePath: normalizedFile };
  }

  return { name: 'PresentationUI', filePath: 'src/App.tsx' };
}

// ─── Classification & Analysis ──────────────────────────────────────

function classifyElement(el: HTMLElement): { type: string; typeAr: string } {
  const tag = el.tagName.toLowerCase();
  const role = el.getAttribute('role');
  const cls = typeof el.className === 'string' ? el.className : '';

  if (cls.includes('book-leather-cover')) return { type: 'bookCover', typeAr: ELEMENT_TYPE_AR.bookCover };
  if (cls.includes('book-page-leaf')) return { type: 'slide', typeAr: ELEMENT_TYPE_AR.slide };
  if (cls.includes('point-card') || cls.includes('card')) return { type: 'card', typeAr: ELEMENT_TYPE_AR.card };
  if (cls.includes('section-tag') || cls.includes('badge') || cls.includes('stamp-badge')) return { type: 'badge', typeAr: ELEMENT_TYPE_AR.badge };
  if (tag === 'button' || role === 'button' || cls.includes('btn-')) return { type: 'button', typeAr: ELEMENT_TYPE_AR.button };
  if (tag === 'a' || role === 'link') return { type: 'link', typeAr: ELEMENT_TYPE_AR.link };
  if (tag === 'img' || tag === 'svg' && cls.includes('image-')) return { type: 'image', typeAr: ELEMENT_TYPE_AR.image };
  if (tag === 'svg' || cls.includes('lucide') || cls.includes('icon')) return { type: 'icon', typeAr: ELEMENT_TYPE_AR.icon };
  if (/^h[1-6]$/.test(tag) || cls.includes('title')) return { type: 'heading', typeAr: ELEMENT_TYPE_AR.heading };
  if (tag === 'p' || tag === 'span' || cls.includes('text') || cls.includes('point-text')) return { type: 'text', typeAr: ELEMENT_TYPE_AR.text };
  if (tag === 'header' || cls.includes('top-bar')) return { type: 'header', typeAr: ELEMENT_TYPE_AR.header };
  if (tag === 'footer' || cls.includes('bottom-bar')) return { type: 'footer', typeAr: ELEMENT_TYPE_AR.footer };
  if (tag === 'ul' || tag === 'ol' || cls.includes('points-list')) return { type: 'list', typeAr: ELEMENT_TYPE_AR.list };
  if (tag === 'li') return { type: 'listItem', typeAr: ELEMENT_TYPE_AR.listItem };
  if (tag === 'input') return { type: 'input', typeAr: ELEMENT_TYPE_AR.input };
  if (tag === 'textarea') return { type: 'textarea', typeAr: ELEMENT_TYPE_AR.textarea };

  return { type: 'container', typeAr: ELEMENT_TYPE_AR.container };
}

function getElementLabel(el: HTMLElement): string {
  const ariaLabel = el.getAttribute('aria-label') || el.getAttribute('title');
  if (ariaLabel) return ariaLabel;
  const alt = el.getAttribute('alt');
  if (alt) return alt;
  const text = el.textContent?.trim();
  if (text && text.length <= 45) return text;
  if (text && text.length > 45) return text.substring(0, 42) + '...';
  return '';
}

function getElementSelector(el: HTMLElement): string {
  const tag = el.tagName.toLowerCase();
  const id = el.id ? `#${el.id}` : '';
  const classes = typeof el.className === 'string'
    ? el.className.split(/\s+/).filter(c => c && c.length < 35 && !c.includes(':')).slice(0, 3).map(c => `.${c}`).join('')
    : '';
  return `${tag}${id}${classes}`;
}

function getDomPath(el: HTMLElement): string {
  const parts: string[] = [];
  let current: HTMLElement | null = el;
  while (current && current !== document.body && parts.length < 5) {
    const tag = current.tagName.toLowerCase();
    if (current.id) {
      parts.unshift(`${tag}#${current.id}`);
      break;
    }
    const cls = typeof current.className === 'string' ? current.className.split(' ')[0] : '';
    parts.unshift(cls ? `${tag}.${cls}` : tag);
    current = current.parentElement;
  }
  return parts.join(' > ');
}

function getSafeAttributes(el: HTMLElement): string[] {
  const names = ['id', 'class', 'role', 'title', 'data-slide-id', 'data-component', 'href', 'src'];
  return names.flatMap(name => {
    const value = el.getAttribute(name);
    return value ? [`${name}="${value.substring(0, 80)}"`] : [];
  });
}

function analyzeElement(el: HTMLElement): ElementInfo {
  const { type, typeAr } = classifyElement(el);
  const { name: componentName, filePath } = detectComponentAndFile(el);
  const cs = window.getComputedStyle(el);

  // Detect slide info if inside a slide
  let slideInfo: ElementInfo['slideInfo'] | undefined;
  const leaf = el.closest('.book-page-leaf');
  if (leaf) {
    const titleEl = leaf.querySelector('.slide-title-thuluth');
    const badgeEl = leaf.querySelector('.section-tag');
    slideInfo = {
      slideId: 1,
      slideBadge: badgeEl?.textContent?.trim() || '',
      slideTitle: titleEl?.textContent?.trim() || '',
    };
  }

  return {
    element: el,
    componentName,
    filePath,
    elementType: type,
    elementTypeAr: typeAr,
    label: getElementLabel(el),
    selector: getElementSelector(el),
    domPath: getDomPath(el),
    attributes: getSafeAttributes(el),
    rect: el.getBoundingClientRect(),
    computedStyles: {
      color: cs.color,
      backgroundColor: cs.backgroundColor,
      fontSize: cs.fontSize,
      fontWeight: cs.fontWeight,
      padding: cs.padding,
      margin: cs.margin,
      lineHeight: cs.lineHeight,
    },
    slideInfo,
  };
}

function findSemanticContainer(el: HTMLElement): HTMLElement | null {
  let current: HTMLElement | null = el.parentElement;
  while (current && current !== document.body) {
    const tag = current.tagName.toLowerCase();
    const cls = typeof current.className === 'string' ? current.className : '';
    if (SEMANTIC_CONTAINERS.has(tag)) return current;
    if (cls.includes('card') || cls.includes('slide-grid') || cls.includes('points-list') || cls.includes('book-leather-cover')) {
      return current;
    }
    current = current.parentElement;
  }
  return null;
}

function isInspectorUI(el: HTMLElement | null): boolean {
  while (el) {
    if (el.getAttribute('data-visual-editor') === 'true') return true;
    el = el.parentElement;
  }
  return false;
}

function generatePromptText(info: ElementInfo, isGroup: boolean): string {
  const lines = [
    `الصفحة: قانون الأعمال - عرض إنهاء عقد العمل (Business Law Presentation)`,
    info.filePath ? `الملف: ${info.filePath}` : null,
    info.componentName ? `المكوّن: ${info.componentName}` : null,
    `العنصر: ${info.elementTypeAr}${info.label ? ` — "${info.label}"` : ''}`,
    `المحدد: ${info.selector}`,
    `مسار DOM: ${info.domPath}`,
    `الأبعاد: ${Math.round(info.rect.width)} × ${Math.round(info.rect.height)} px`,
    `الخط واللون: font-size=${info.computedStyles.fontSize} | color=${info.computedStyles.color}`,
    info.attributes.length ? `السمات: ${info.attributes.join(' ، ')}` : null,
    info.slideInfo?.slideTitle ? `الشريحة الحالية: "${info.slideInfo.slideTitle}"` : null,
    isGroup ? `العناصر الفرعية: ${info.element.querySelectorAll('*').length} عنصر` : null,
  ];
  return lines.filter(Boolean).join('\n');
}

// ─── Main VisualEditor Component ────────────────────────────────────

export const VisualEditor: React.FC<VisualEditorProps> = () => {
  const [enabled, setEnabled] = useState<boolean>(() => {
    try {
      return localStorage.getItem('visual-editor-enabled') === 'on';
    } catch {
      return false;
    }
  });

  const [hoveredInfo, setHoveredInfo] = useState<ElementInfo | null>(null);
  const [selectedInfo, setSelectedInfo] = useState<ElementInfo | null>(null);
  const [multiSelected, setMultiSelected] = useState<ElementInfo[]>([]);
  const [isGroupSelection, setIsGroupSelection] = useState(false);
  const [copied, setCopied] = useState(false);
  const [copyError, setCopyError] = useState<string | null>(null);
  const [depthOffset, setDepthOffset] = useState(0);

  // Live in-place editing state
  const [editText, setEditText] = useState('');
  const [editFontSize, setEditFontSize] = useState('');
  const [editColor, setEditColor] = useState('');
  const [editBgColor, setEditBgColor] = useState('');
  const [isEditingInline, setIsEditingInline] = useState(false);

  // Drag selection
  const [dragRect, setDragRect] = useState<{ x: number; y: number; w: number; h: number } | null>(null);
  const dragRectRef = useRef<{ x: number; y: number; w: number; h: number } | null>(null);
  const dragSelectRef = useRef<{ startX: number; startY: number; active: boolean } | null>(null);
  dragRectRef.current = dragRect;

  const baseHoveredRef = useRef<HTMLElement | null>(null);
  const lastTargetRef = useRef<HTMLElement | null>(null);

  // ── Sync enabled with localStorage & trigger custom events ──
  useEffect(() => {
    try {
      localStorage.setItem('visual-editor-enabled', enabled ? 'on' : 'off');
    } catch { /* noop */ }
    window.dispatchEvent(new CustomEvent('visualEditorStateChange', { detail: { enabled } }));
  }, [enabled]);

  // ── Listen for custom toggle events from TopBar button ──
  useEffect(() => {
    const handleCustomToggle = (e: Event) => {
      const detail = (e as CustomEvent).detail;
      setEnabled(detail?.enabled ?? ((prev: boolean) => !prev));
    };
    window.addEventListener('visualEditorToggle', handleCustomToggle);
    return () => window.removeEventListener('visualEditorToggle', handleCustomToggle);
  }, []);

  // ── Keyboard Shortcuts: Ctrl+Shift+D or Ctrl+Shift+E ──
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && (e.key === 'D' || e.key === 'E' || e.key === 'd' || e.key === 'e')) {
        e.preventDefault();
        setEnabled(prev => !prev);
        setSelectedInfo(null);
        setHoveredInfo(null);
      }
      if (e.key === 'Escape' && (selectedInfo || multiSelected.length > 0)) {
        e.preventDefault();
        setSelectedInfo(null);
        setMultiSelected([]);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [selectedInfo, multiSelected]);

  // ── Clear states when disabled ──
  useEffect(() => {
    if (!enabled) {
      setSelectedInfo(null);
      setHoveredInfo(null);
      setMultiSelected([]);
      setDragRect(null);
      setDepthOffset(0);
      setIsEditingInline(false);
      baseHoveredRef.current = null;
      lastTargetRef.current = null;
      dragSelectRef.current = null;
    }
  }, [enabled]);

  // ── Crosshair cursor style when active ──
  useEffect(() => {
    if (!enabled) return;
    const style = document.createElement('style');
    style.setAttribute('data-visual-editor-style', 'true');
    style.textContent = `
      .visual-editor-active, .visual-editor-active * { cursor: crosshair !important; }
      [data-visual-editor="true"], [data-visual-editor="true"] * { cursor: default !important; }
      [data-visual-editor="true"] button, [data-visual-editor="true"] input { cursor: pointer !important; }
    `;
    document.head.appendChild(style);
    document.body.classList.add('visual-editor-active');
    return () => {
      document.body.classList.remove('visual-editor-active');
      style.remove();
    };
  }, [enabled]);

  // ── Mouse Move: Hover Highlight & Drag Marquee ──
  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!enabled) return;

    // Drag marquee
    const ds = dragSelectRef.current;
    if (ds && e.buttons === 1) {
      const dx = e.clientX - ds.startX;
      const dy = e.clientY - ds.startY;
      if (!ds.active && (Math.abs(dx) > 6 || Math.abs(dy) > 6)) {
        ds.active = true;
      }
      if (ds.active) {
        setDragRect({
          x: Math.min(e.clientX, ds.startX),
          y: Math.min(e.clientY, ds.startY),
          w: Math.abs(dx),
          h: Math.abs(dy),
        });
        return;
      }
    }

    const target = e.target as HTMLElement;
    if (isInspectorUI(target)) {
      setHoveredInfo(null);
      baseHoveredRef.current = null;
      lastTargetRef.current = null;
      return;
    }

    if (target !== lastTargetRef.current) {
      lastTargetRef.current = target;
      baseHoveredRef.current = target;
      setDepthOffset(0);
      setHoveredInfo(analyzeElement(target));
    }
  }, [enabled]);

  const handleMouseDown = useCallback((e: MouseEvent) => {
    if (!enabled || e.button !== 0) return;
    if (isInspectorUI(e.target as HTMLElement)) return;
    dragSelectRef.current = { startX: e.clientX, startY: e.clientY, active: false };
  }, [enabled]);

  const handleMouseUp = useCallback((e: MouseEvent) => {
    if (!enabled || e.button !== 0) return;
    const ds = dragSelectRef.current;
    dragSelectRef.current = null;
    const rect = dragRectRef.current;

    if (ds?.active && rect) {
      const allEls = document.querySelectorAll('*');
      const found: ElementInfo[] = [];
      const seen = new Set<HTMLElement>();
      allEls.forEach(node => {
        const el = node as HTMLElement;
        if (isInspectorUI(el) || seen.has(el)) return;
        const r = el.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) return;
        if (
          r.left < rect.x + rect.w &&
          r.right > rect.x &&
          r.top < rect.y + rect.h &&
          r.bottom > rect.y
        ) {
          const tag = el.tagName.toLowerCase();
          const isLeaf = ['button', 'a', 'h1', 'h2', 'h3', 'p', 'span', 'strong', 'img', 'svg'].includes(tag)
            || typeof el.className === 'string' && el.className.includes('card');
          if (isLeaf) {
            seen.add(el);
            found.push(analyzeElement(el));
          }
        }
      });

      if (found.length > 0) {
        setMultiSelected(found);
        setSelectedInfo(null);
        setIsGroupSelection(false);
      }
      setDragRect(null);
      return;
    }

    setDragRect(null);
  }, [enabled]);

  // ── Context Menu (Right Click) or Normal Click selection ──
  const selectElement = useCallback((target: HTMLElement, isGroup: boolean) => {
    let elToSelect = target;
    if (isGroup) {
      const container = findSemanticContainer(target);
      if (container) elToSelect = container;
      setIsGroupSelection(true);
    } else {
      setIsGroupSelection(false);
    }

    const analyzed = analyzeElement(elToSelect);
    setSelectedInfo(analyzed);
    setMultiSelected([]);
    setEditText(elToSelect.innerText || elToSelect.textContent || '');
    setEditFontSize(analyzed.computedStyles.fontSize);
    setEditColor(rgbToHex(analyzed.computedStyles.color));
    setEditBgColor(rgbToHex(analyzed.computedStyles.backgroundColor));
    setCopied(false);
  }, []);

  const handleClick = useCallback((e: MouseEvent) => {
    if (!enabled) return;
    const target = e.target as HTMLElement;
    if (isInspectorUI(target)) return;

    e.preventDefault();
    e.stopPropagation();
    selectElement(target, e.shiftKey);
  }, [enabled, selectElement]);

  const handleContextMenu = useCallback((e: MouseEvent) => {
    if (!enabled) return;
    const target = e.target as HTMLElement;
    if (isInspectorUI(target)) return;

    e.preventDefault();
    e.stopPropagation();
    selectElement(target, e.shiftKey);
  }, [enabled, selectElement]);

  // ── Alt+Scroll Depth navigation ──
  const handleWheel = useCallback((e: WheelEvent) => {
    if (!enabled || !baseHoveredRef.current) return;
    if (!e.altKey) return;
    if (isInspectorUI(e.target as HTMLElement)) return;

    e.preventDefault();
    setDepthOffset(prev => {
      const nextOffset = Math.max(0, prev + (e.deltaY < 0 ? 1 : -1));
      let el: HTMLElement | null = baseHoveredRef.current;
      for (let i = 0; i < nextOffset; i++) {
        if (el?.parentElement) el = el.parentElement;
      }
      if (el) setHoveredInfo(analyzeElement(el));
      return nextOffset;
    });
  }, [enabled]);

  // ── Register Listeners ──
  useEffect(() => {
    if (!enabled) return;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mousedown', handleMouseDown, true);
    document.addEventListener('mouseup', handleMouseUp, true);
    document.addEventListener('click', handleClick, true);
    document.addEventListener('contextmenu', handleContextMenu, true);
    document.addEventListener('wheel', handleWheel, { passive: false, capture: true });

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mousedown', handleMouseDown, true);
      document.removeEventListener('mouseup', handleMouseUp, true);
      document.removeEventListener('click', handleClick, true);
      document.removeEventListener('contextmenu', handleContextMenu, true);
      document.removeEventListener('wheel', handleWheel, true);
    };
  }, [enabled, handleMouseMove, handleMouseDown, handleMouseUp, handleClick, handleContextMenu, handleWheel]);

  // ── Copy Prompt for AI ──
  const handleCopy = useCallback(async () => {
    let text = '';
    if (multiSelected.length > 0) {
      text = `[المحرر المرئي - تحديد متعدد (${multiSelected.length} عناصر)]:\n\n` +
        multiSelected.map((info, idx) => `### العنصر ${idx + 1}:\n${generatePromptText(info, false)}`).join('\n\n');
    } else if (selectedInfo) {
      text = `[المحرر المرئي - فحص وتعديل العنصر]:\n\n` + generatePromptText(selectedInfo, isGroupSelection);
      if (isEditingInline) {
        text += `\n\nالنص المطلوب بعد التعديل:\n"${editText}"`;
      }
    } else return;

    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }
      setCopied(true);
      setCopyError(null);
      setTimeout(() => setCopied(false), 2200);
    } catch {
      setCopyError('تعذر النسخ إلى الحافظة');
      setTimeout(() => setCopyError(null), 2000);
    }
  }, [selectedInfo, multiSelected, isGroupSelection, isEditingInline, editText]);

  // ── Apply Live Changes directly to the DOM element ──
  const applyLiveText = () => {
    if (selectedInfo?.element) {
      selectedInfo.element.textContent = editText;
      setSelectedInfo(analyzeElement(selectedInfo.element));
    }
  };

  const applyLiveStyle = (property: string, value: string) => {
    if (selectedInfo?.element) {
      (selectedInfo.element.style as any)[property] = value;
      setSelectedInfo(analyzeElement(selectedInfo.element));
    }
  };

  // Convert RGB/RGBA to Hex for color inputs
  function rgbToHex(rgb: string): string {
    if (!rgb || rgb === 'transparent') return '#ffffff';
    const match = rgb.match(/\d+/g);
    if (!match || match.length < 3) return '#d4af37';
    const r = parseInt(match[0], 10).toString(16).padStart(2, '0');
    const g = parseInt(match[1], 10).toString(16).padStart(2, '0');
    const b = parseInt(match[2], 10).toString(16).padStart(2, '0');
    return `#${r}${g}${b}`;
  }

  const hoverRect = hoveredInfo?.rect;
  const selectRect = selectedInfo ? selectedInfo.element.getBoundingClientRect() : null;

  return (
    <>
      {/* ── Persistent Corner Toggle Button ── */}
      <div
        data-visual-editor="true"
        style={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          zIndex: 99999,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          background: enabled ? 'rgba(15, 23, 42, 0.95)' : 'rgba(15, 23, 42, 0.82)',
          border: `1.5px solid ${enabled ? '#10b981' : 'rgba(212, 175, 55, 0.5)'}`,
          backdropFilter: 'blur(12px)',
          borderRadius: 30,
          padding: '6px 14px',
          boxShadow: enabled
            ? '0 0 25px rgba(16, 185, 129, 0.4), 0 8px 30px rgba(0,0,0,0.6)'
            : '0 8px 24px rgba(0,0,0,0.5)',
          cursor: 'pointer',
          userSelect: 'none',
          transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        }}
        onClick={() => setEnabled(prev => !prev)}
        title="تبديل وضع المحرر المرئي وفاحص العناصر (Ctrl+Shift+D)"
      >
        <span
          style={{
            width: 10,
            height: 10,
            borderRadius: '50%',
            background: enabled ? '#10b981' : '#eab308',
            boxShadow: enabled ? '0 0 10px #10b981' : 'none',
            display: 'inline-block',
          }}
        />
        <span
          style={{
            color: enabled ? '#34d399' : '#e2e8f0',
            fontSize: 12,
            fontWeight: 700,
            fontFamily: 'system-ui, sans-serif',
          }}
        >
          {enabled ? 'المحرر المرئي نشط' : 'المحرر المرئي'}
        </span>
        <span
          style={{
            background: 'rgba(255, 255, 255, 0.12)',
            color: '#94a3b8',
            fontSize: 10,
            fontWeight: 600,
            padding: '2px 6px',
            borderRadius: 6,
            fontFamily: 'monospace',
          }}
        >
          Ctrl+Shift+D
        </span>
      </div>

      {/* ── Hover Bounding Box ── */}
      {enabled && hoverRect && !selectedInfo && (
        <div
          data-visual-editor="true"
          style={{
            position: 'fixed',
            top: hoverRect.top - 2,
            left: hoverRect.left - 2,
            width: hoverRect.width + 4,
            height: hoverRect.height + 4,
            border: '2px solid #3b82f6',
            borderRadius: 4,
            background: 'rgba(59, 130, 246, 0.08)',
            pointerEvents: 'none',
            zIndex: 99990,
            transition: 'all 0.05s ease-out',
            boxShadow: '0 0 12px rgba(59, 130, 246, 0.35)',
          }}
        >
          {/* Top Floating Badge */}
          <span
            style={{
              position: 'absolute',
              top: -26,
              left: 0,
              background: '#3b82f6',
              color: '#ffffff',
              fontSize: 11,
              fontWeight: 700,
              padding: '2px 8px',
              borderRadius: '4px 4px 0 0',
              whiteSpace: 'nowrap',
              fontFamily: 'system-ui, sans-serif',
              maxWidth: 320,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              direction: 'ltr',
              display: 'flex',
              alignItems: 'center',
              gap: 4,
            }}
          >
            <span>{hoveredInfo?.componentName || 'UI'}</span>
            <span style={{ opacity: 0.8 }}>›</span>
            <span>{hoveredInfo?.elementTypeAr}</span>
            {depthOffset > 0 && <span style={{ color: '#fef08a' }}>↑{depthOffset}</span>}
          </span>

          {/* Bottom Size Indicator */}
          <span
            style={{
              position: 'absolute',
              bottom: -18,
              right: 0,
              background: 'rgba(15, 23, 42, 0.88)',
              color: '#93c5fd',
              fontSize: 9,
              padding: '1px 5px',
              borderRadius: '0 0 3px 3px',
              fontFamily: 'monospace',
              direction: 'ltr',
            }}
          >
            {Math.round(hoverRect.width)}×{Math.round(hoverRect.height)}px
          </span>
        </div>
      )}

      {/* ── Selected Highlight Box ── */}
      {selectedInfo && selectRect && (
        <div
          data-visual-editor="true"
          style={{
            position: 'fixed',
            top: selectRect.top - 3,
            left: selectRect.left - 3,
            width: selectRect.width + 6,
            height: selectRect.height + 6,
            border: `3px solid ${isGroupSelection ? '#f59e0b' : '#10b981'}`,
            borderRadius: 6,
            background: isGroupSelection ? 'rgba(245, 158, 11, 0.1)' : 'rgba(16, 185, 129, 0.1)',
            pointerEvents: 'none',
            zIndex: 99990,
            boxShadow: isGroupSelection
              ? '0 0 20px rgba(245, 158, 11, 0.4)'
              : '0 0 20px rgba(16, 185, 129, 0.45)',
          }}
        >
          <span
            style={{
              position: 'absolute',
              top: -24,
              left: -3,
              background: isGroupSelection ? '#f59e0b' : '#10b981',
              color: '#000000',
              fontSize: 10,
              fontWeight: 800,
              padding: '2px 7px',
              borderRadius: '3px 3px 0 0',
              fontFamily: 'monospace',
              whiteSpace: 'nowrap',
            }}
          >
            ✓ {selectedInfo.componentName} · {selectedInfo.elementTypeAr}
          </span>
        </div>
      )}

      {/* ── Detailed Floating Inspector & Live Editor Panel ── */}
      {selectedInfo && (
        <div
          data-visual-editor="true"
          style={{
            position: 'fixed',
            bottom: 20,
            left: 20,
            zIndex: 99999,
            width: 395,
            maxHeight: '85vh',
            background: '#0f172a',
            border: `1.5px solid ${isGroupSelection ? '#f59e0b' : '#10b981'}`,
            borderRadius: 14,
            boxShadow: '0 16px 48px rgba(0,0,0,0.85), 0 0 0 1px rgba(255,255,255,0.06)',
            overflow: 'hidden',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            direction: 'rtl',
            display: 'flex',
            flexDirection: 'column',
            color: '#f8fafc',
            animation: 'fadeInUp 0.18s ease-out',
          }}
        >
          {/* Panel Header */}
          <div
            style={{
              padding: '10px 14px',
              background: '#090d16',
              borderBottom: '1px solid #1e293b',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 16 }}>🔍</span>
              <span style={{ color: '#38bdf8', fontSize: 13, fontWeight: 700 }}>
                {isGroupSelection ? 'فاحص الحاوية (Group Inspector)' : 'المحرر المرئي وفاحص العناصر'}
              </span>
            </div>
            <button
              data-visual-editor="true"
              onClick={() => setSelectedInfo(null)}
              style={{
                background: 'rgba(255,255,255,0.06)',
                border: 'none',
                color: '#94a3b8',
                borderRadius: 6,
                padding: '3px 8px',
                cursor: 'pointer',
                fontSize: 14,
                lineHeight: 1,
              }}
              title="إغلاق (Esc)"
            >
              ✕
            </button>
          </div>

          {/* Details Scroll Body */}
          <div style={{ padding: '12px 14px', overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
            
            {/* Component & File Cards */}
            <div style={{ background: '#1e293b', borderRadius: 8, padding: '8px 10px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ color: '#94a3b8', fontSize: 11 }}>المكوّن البرمجي:</span>
                <span style={{ color: '#a78bfa', fontWeight: 700, fontSize: 12, fontFamily: 'monospace' }}>
                  {selectedInfo.componentName}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#94a3b8', fontSize: 11 }}>مسار الملف:</span>
                <span style={{ color: '#38bdf8', fontSize: 11, fontFamily: 'monospace', direction: 'ltr' }}>
                  {selectedInfo.filePath}
                </span>
              </div>
            </div>

            {/* Element Identity Row */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
              <div style={{ background: '#1e293b', borderRadius: 8, padding: '6px 8px' }}>
                <span style={{ color: '#64748b', fontSize: 10, display: 'block' }}>نوع العنصر</span>
                <span style={{ color: '#10b981', fontWeight: 600, fontSize: 12 }}>{selectedInfo.elementTypeAr}</span>
              </div>
              <div style={{ background: '#1e293b', borderRadius: 8, padding: '6px 8px' }}>
                <span style={{ color: '#64748b', fontSize: 10, display: 'block' }}>الأبعاد الدقيقة</span>
                <span style={{ color: '#fbbf24', fontSize: 11, fontFamily: 'monospace' }}>
                  {Math.round(selectedInfo.rect.width)} × {Math.round(selectedInfo.rect.height)} px
                </span>
              </div>
            </div>

            {/* Selector & DOM Path */}
            <div style={{ background: '#111827', borderRadius: 6, padding: '6px 8px', fontSize: 11, fontFamily: 'monospace', color: '#cbd5e1', direction: 'ltr' }}>
              <div style={{ color: '#d4af37', marginBottom: 2 }}>{selectedInfo.selector}</div>
              <div style={{ color: '#64748b', fontSize: 10, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {selectedInfo.domPath}
              </div>
            </div>

            {/* ── Live In-Place Text Editor ── */}
            <div style={{ background: 'rgba(212, 175, 55, 0.07)', border: '1px solid rgba(212, 175, 55, 0.25)', borderRadius: 8, padding: 10 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                <span style={{ color: '#d4af37', fontSize: 12, fontWeight: 700 }}>
                  ✍️ تعديل النص فورياً (Live Text)
                </span>
                <button
                  data-visual-editor="true"
                  onClick={() => setIsEditingInline(prev => !prev)}
                  style={{
                    background: 'none',
                    border: '1px solid rgba(212, 175, 55, 0.4)',
                    color: '#d4af37',
                    borderRadius: 4,
                    padding: '2px 6px',
                    fontSize: 10,
                    cursor: 'pointer',
                  }}
                >
                  {isEditingInline ? 'إخفاء' : 'تعديل'}
                </button>
              </div>

              {isEditingInline ? (
                <div>
                  <textarea
                    data-visual-editor="true"
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                    style={{
                      width: '100%',
                      minHeight: 60,
                      background: '#090d16',
                      border: '1px solid #334155',
                      borderRadius: 6,
                      color: '#fff',
                      padding: 6,
                      fontSize: 12,
                      fontFamily: 'inherit',
                      resize: 'vertical',
                      boxSizing: 'border-box',
                    }}
                  />
                  <div style={{ display: 'flex', gap: 6, marginTop: 6 }}>
                    <button
                      data-visual-editor="true"
                      onClick={applyLiveText}
                      style={{
                        flex: 1,
                        background: '#10b981',
                        border: 'none',
                        borderRadius: 6,
                        color: '#000',
                        fontWeight: 700,
                        fontSize: 11,
                        padding: '6px 10px',
                        cursor: 'pointer',
                      }}
                    >
                      تطبيق التعديل على الصفحة
                    </button>
                  </div>
                </div>
              ) : (
                <div style={{ color: '#94a3b8', fontSize: 11, fontStyle: 'italic', maxHeight: 38, overflow: 'hidden' }}>
                  {selectedInfo.label ? `"${selectedInfo.label}"` : 'انقر على "تعديل" لتغيير نص هذا العنصر.'}
                </div>
              )}
            </div>

            {/* ── Quick Live Style Adjusters ── */}
            <div style={{ background: '#1e293b', borderRadius: 8, padding: 10, border: '1px solid #334155' }}>
              <span style={{ color: '#94a3b8', fontSize: 11, fontWeight: 700, display: 'block', marginBottom: 6 }}>
                🎨 تخصيص المظهر السريع (Live Styles)
              </span>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
                <div>
                  <label style={{ color: '#64748b', fontSize: 10, display: 'block' }}>حجم الخط</label>
                  <input
                    data-visual-editor="true"
                    type="text"
                    value={editFontSize}
                    onChange={(e) => {
                      setEditFontSize(e.target.value);
                      applyLiveStyle('fontSize', e.target.value);
                    }}
                    style={{
                      width: '100%',
                      background: '#0f172a',
                      border: '1px solid #475569',
                      borderRadius: 4,
                      color: '#fff',
                      padding: '3px 6px',
                      fontSize: 11,
                      fontFamily: 'monospace',
                      boxSizing: 'border-box',
                    }}
                  />
                </div>
                <div>
                  <label style={{ color: '#64748b', fontSize: 10, display: 'block' }}>لون النص</label>
                  <div style={{ display: 'flex', gap: 4 }}>
                    <input
                      data-visual-editor="true"
                      type="color"
                      value={editColor}
                      onChange={(e) => {
                        setEditColor(e.target.value);
                        applyLiveStyle('color', e.target.value);
                      }}
                      style={{ width: 28, height: 24, border: 'none', borderRadius: 4, cursor: 'pointer', background: 'transparent' }}
                    />
                    <input
                      data-visual-editor="true"
                      type="text"
                      value={editColor}
                      onChange={(e) => {
                        setEditColor(e.target.value);
                        applyLiveStyle('color', e.target.value);
                      }}
                      style={{
                        flex: 1,
                        background: '#0f172a',
                        border: '1px solid #475569',
                        borderRadius: 4,
                        color: '#fff',
                        padding: '3px 6px',
                        fontSize: 11,
                        fontFamily: 'monospace',
                        boxSizing: 'border-box',
                      }}
                    />
                  </div>
                </div>

                <div style={{ gridColumn: 'span 2', marginTop: 4 }}>
                  <label style={{ color: '#64748b', fontSize: 10, display: 'block' }}>لون الخلفية</label>
                  <div style={{ display: 'flex', gap: 4 }}>
                    <input
                      data-visual-editor="true"
                      type="color"
                      value={editBgColor}
                      onChange={(e) => {
                        setEditBgColor(e.target.value);
                        applyLiveStyle('backgroundColor', e.target.value);
                      }}
                      style={{ width: 28, height: 24, border: 'none', borderRadius: 4, cursor: 'pointer', background: 'transparent' }}
                    />
                    <input
                      data-visual-editor="true"
                      type="text"
                      value={editBgColor}
                      onChange={(e) => {
                        setEditBgColor(e.target.value);
                        applyLiveStyle('backgroundColor', e.target.value);
                      }}
                      style={{
                        flex: 1,
                        background: '#0f172a',
                        border: '1px solid #475569',
                        borderRadius: 4,
                        color: '#fff',
                        padding: '3px 6px',
                        fontSize: 11,
                        fontFamily: 'monospace',
                        boxSizing: 'border-box',
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>

          </div>

          {/* Copy for AI Button (Matches clincsa prompt export) */}
          <div style={{ padding: '10px 14px', background: '#090d16', borderTop: '1px solid #1e293b' }}>
            <button
              data-visual-editor="true"
              onClick={handleCopy}
              style={{
                width: '100%',
                padding: '9px 14px',
                background: copied ? '#10b981' : 'linear-gradient(135deg, #2563eb, #1d4ed8)',
                border: 'none',
                borderRadius: 8,
                color: '#ffffff',
                fontSize: 13,
                fontWeight: 700,
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 6,
                boxShadow: copied ? '0 0 16px rgba(16, 185, 129, 0.4)' : 'none',
              }}
            >
              <span>{copied ? '✅' : '📋'}</span>
              <span>{copied ? 'تم النسخ بنجاح للـ AI!' : 'نسخ وصف العنصر للـ AI (Prompt Ready)'}</span>
            </button>
            {copyError && (
              <div style={{ color: '#ef4444', fontSize: 11, textAlign: 'center', marginTop: 4 }}>
                {copyError}
              </div>
            )}
          </div>

          {/* Hints bar */}
          <div style={{ padding: '6px 14px', background: '#030712', borderTop: '1px solid #111827', fontSize: 10, color: '#64748b', textAlign: 'center' }}>
            انقر للفحص · Shift+Click للحاوية · سحب للتحديد المتعدد · Alt+Scroll للعمق · Esc للإغلاق
          </div>
        </div>
      )}

      {/* ── Drag Marquee Selection Box ── */}
      {enabled && dragRect && dragRect.w > 4 && dragRect.h > 4 && (
        <div
          data-visual-editor="true"
          style={{
            position: 'fixed',
            top: dragRect.y,
            left: dragRect.x,
            width: dragRect.w,
            height: dragRect.h,
            border: '2px dashed #a78bfa',
            background: 'rgba(167, 139, 250, 0.08)',
            borderRadius: 4,
            pointerEvents: 'none',
            zIndex: 99995,
          }}
        >
          <span
            style={{
              position: 'absolute',
              top: -18,
              left: 0,
              background: '#7c3aed',
              color: '#ffffff',
              fontSize: 9,
              fontWeight: 700,
              padding: '1px 6px',
              borderRadius: '3px 3px 0 0',
              fontFamily: 'monospace',
            }}
          >
            {Math.round(dragRect.w)}×{Math.round(dragRect.h)}
          </span>
        </div>
      )}

      {/* ── Multi-Select Info Panel ── */}
      {multiSelected.length > 0 && (
        <div
          data-visual-editor="true"
          style={{
            position: 'fixed',
            bottom: 20,
            left: 20,
            zIndex: 99999,
            width: 390,
            maxHeight: '65vh',
            background: '#0f172a',
            border: '1.5px solid #7c3aed',
            borderRadius: 14,
            boxShadow: '0 16px 48px rgba(0,0,0,0.85)',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            direction: 'rtl',
            color: '#f8fafc',
          }}
        >
          <div
            style={{
              padding: '10px 14px',
              background: '#090d16',
              borderBottom: '1px solid #1e293b',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <span style={{ color: '#a78bfa', fontSize: 13, fontWeight: 700 }}>
              🎯 تحديد متعدد ({multiSelected.length} عنصر)
            </span>
            <button
              data-visual-editor="true"
              onClick={() => setMultiSelected([])}
              style={{
                background: 'none',
                border: 'none',
                color: '#94a3b8',
                fontSize: 16,
                cursor: 'pointer',
              }}
            >
              ✕
            </button>
          </div>

          <div style={{ padding: '8px 14px', overflowY: 'auto', flex: 1 }}>
            {multiSelected.map((info, idx) => (
              <div
                key={idx}
                style={{
                  padding: '6px 0',
                  borderBottom: idx < multiSelected.length - 1 ? '1px solid #1e293b' : 'none',
                  display: 'flex',
                  gap: 8,
                  alignItems: 'center',
                }}
              >
                <span
                  style={{
                    background: '#7c3aed',
                    color: '#fff',
                    fontSize: 10,
                    fontWeight: 800,
                    padding: '2px 6px',
                    borderRadius: 4,
                  }}
                >
                  {idx + 1}
                </span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ color: '#e2e8f0', fontSize: 12, fontWeight: 600 }}>
                    {info.componentName} · {info.elementTypeAr}
                  </div>
                  {info.label && (
                    <div style={{ color: '#94a3b8', fontSize: 10, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      "{info.label}"
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div style={{ padding: '10px 14px', background: '#090d16', borderTop: '1px solid #1e293b' }}>
            <button
              data-visual-editor="true"
              onClick={handleCopy}
              style={{
                width: '100%',
                padding: '9px 12px',
                background: copied ? '#10b981' : '#7c3aed',
                border: 'none',
                borderRadius: 8,
                color: '#fff',
                fontSize: 12,
                fontWeight: 700,
                cursor: 'pointer',
              }}
            >
              {copied ? '✅ تم نسخ العناصر المحددة!' : `📋 نسخ ${multiSelected.length} عناصر للـ AI`}
            </button>
          </div>
        </div>
      )}
    </>
  );
};
