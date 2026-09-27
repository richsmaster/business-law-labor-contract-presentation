// Realistic Manuscript & Book Page Turn Sound Synthesizer using Web Audio API
// 100% self-contained, zero external files, zero latency, works offline and in all modern browsers.

let audioCtx: AudioContext | null = null;

function getAudioContext(): AudioContext {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    audioCtx = new AudioContextClass();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

/**
 * Synthesizes a slow, natural, gentle paper page-turn sound (صوت تصفح ورقة بطيء وناعم).
 * Completely eliminates any bass impact/thud/strike, focusing purely on organic paper friction and air whisper.
 * 
 * @param isCover If true, produces a slightly deeper, slower leather cover opening sound.
 */
export function playPageTurnSound(isCover: boolean = false): void {
  try {
    const ctx = getAudioContext();
    const now = ctx.currentTime;
    
    // Slow, soothing page turn duration (0.88s for slide page, 1.08s for book cover)
    const duration = isCover ? 1.08 : 0.88;
    const sampleRate = ctx.sampleRate;
    const bufferSize = Math.floor(sampleRate * duration);
    const noiseBuffer = ctx.createBuffer(1, bufferSize, sampleRate);
    const output = noiseBuffer.getChannelData(0);

    // Generate soft, textured paper fiber noise with gentle undulating friction
    let lastNoise = 0;
    for (let i = 0; i < bufferSize; i++) {
      const progress = i / bufferSize;
      
      // Soft organic envelope: smooth bell curve with gentle rise and long gradual tail
      const envelope = Math.pow(Math.sin(progress * Math.PI), 1.4);
      
      // Multi-layered paper flutter & micro-crinkle texture
      const flutter = 1 + 0.16 * Math.sin(progress * Math.PI * 10) + 0.08 * Math.sin(progress * Math.PI * 22);
      
      // Pink-filtered noise (smoother than raw white noise, eliminates harshness and strikes)
      const white = Math.random() * 2 - 1;
      const pinkish = (lastNoise * 0.74) + (white * 0.26);
      lastNoise = pinkish;

      output[i] = pinkish * envelope * flutter;
    }

    const noiseSource = ctx.createBufferSource();
    noiseSource.buffer = noiseBuffer;

    // 1. Highpass filter: completely cuts all low frequencies (blocks all bass thuds / strike sounds)
    const highpass = ctx.createBiquadFilter();
    highpass.type = 'highpass';
    highpass.frequency.setValueAtTime(isCover ? 280 : 380, now);
    highpass.Q.setValueAtTime(0.7, now);

    // 2. Sweeping bandpass filter: simulates the natural acoustic arc of paper gliding through air
    const bandpass = ctx.createBiquadFilter();
    bandpass.type = 'bandpass';
    bandpass.Q.setValueAtTime(isCover ? 1.8 : 2.2, now);

    if (isCover) {
      // Heavier leather/hardcover opening: deeper resonant glide
      bandpass.frequency.setValueAtTime(450, now);
      bandpass.frequency.exponentialRampToValueAtTime(1400, now + duration * 0.42);
      bandpass.frequency.exponentialRampToValueAtTime(480, now + duration);
    } else {
      // Gentle, slow paper parchment turn: silky air sweep
      bandpass.frequency.setValueAtTime(650, now);
      bandpass.frequency.exponentialRampToValueAtTime(2100, now + duration * 0.38);
      bandpass.frequency.exponentialRampToValueAtTime(700, now + duration);
    }

    // 3. Lowpass filter: softens any digital harshness for a velvety, tactile feel
    const lowpass = ctx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.setValueAtTime(isCover ? 3200 : 4200, now);

    // 4. Amplitude gain envelope: slow, gentle swell and natural whispering release (no sudden hit)
    const gainNode = ctx.createGain();
    const peakVolume = isCover ? 0.22 : 0.16; // Soft, comfortable listening volume
    const attackTime = duration * 0.24; // ~0.21s smooth gradual swell (no punch/strike)

    gainNode.gain.setValueAtTime(0.0001, now);
    gainNode.gain.linearRampToValueAtTime(peakVolume, now + attackTime);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, now + duration);

    // Connect audio processing chain
    noiseSource.connect(highpass);
    highpass.connect(bandpass);
    bandpass.connect(lowpass);
    lowpass.connect(gainNode);
    gainNode.connect(ctx.destination);

    // Trigger audio
    noiseSource.start(now);
    noiseSource.stop(now + duration);
  } catch (err) {
    console.debug('Page turn audio unavailable:', err);
  }
}
