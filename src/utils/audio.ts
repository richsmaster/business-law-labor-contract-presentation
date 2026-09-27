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
 * Synthesizes an authentic acoustic sound of turning or opening an antique parchment page.
 * @param isCover If true, produces a deeper, heavier sound of opening a leather book cover.
 */
export function playPageTurnSound(isCover: boolean = false): void {
  try {
    const ctx = getAudioContext();
    const now = ctx.currentTime;
    const duration = isCover ? 0.58 : 0.42;

    // 1. Noise buffer: generates organic paper friction texture
    const sampleRate = ctx.sampleRate;
    const bufferSize = Math.floor(sampleRate * duration);
    const noiseBuffer = ctx.createBuffer(1, bufferSize, sampleRate);
    const output = noiseBuffer.getChannelData(0);

    // Generate textured noise with gentle parchment grain and micro-flutter
    for (let i = 0; i < bufferSize; i++) {
      const progress = i / bufferSize;
      // Multi-frequency flutter envelope
      const flutter = 1 + 0.28 * Math.sin(progress * Math.PI * 18);
      const decay = Math.sin(progress * Math.PI); // Smooth rise and fall
      output[i] = (Math.random() * 2 - 1) * decay * flutter;
    }

    const whiteNoise = ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;

    // 2. Sweeping bandpass filter: captures the swoosh of paper moving through air
    const bandpass = ctx.createBiquadFilter();
    bandpass.type = 'bandpass';
    bandpass.Q.setValueAtTime(isCover ? 1.6 : 2.4, now);

    if (isCover) {
      // Deeper leather binding opening
      bandpass.frequency.setValueAtTime(380, now);
      bandpass.frequency.exponentialRampToValueAtTime(1250, now + duration * 0.38);
      bandpass.frequency.exponentialRampToValueAtTime(280, now + duration);
    } else {
      // Crisp parchment leaf turn
      bandpass.frequency.setValueAtTime(750, now);
      bandpass.frequency.exponentialRampToValueAtTime(3200, now + duration * 0.32);
      bandpass.frequency.exponentialRampToValueAtTime(600, now + duration);
    }

    // 3. Highpass filter: eliminates rumble while preserving crisp paper edges
    const highpass = ctx.createBiquadFilter();
    highpass.type = 'highpass';
    highpass.frequency.setValueAtTime(isCover ? 140 : 320, now);

    // 4. Amplitude gain envelope
    const noiseGain = ctx.createGain();
    const peakVolume = isCover ? 0.36 : 0.26;
    noiseGain.gain.setValueAtTime(0.0001, now);
    noiseGain.gain.linearRampToValueAtTime(peakVolume, now + 0.035);
    noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

    // Connect noise pipeline
    whiteNoise.connect(bandpass);
    bandpass.connect(highpass);
    highpass.connect(noiseGain);
    noiseGain.connect(ctx.destination);

    // 5. Low-frequency displacement whoosh (gives the physical 3D weight of the page)
    const whooshOsc = ctx.createOscillator();
    whooshOsc.type = 'sine';
    whooshOsc.frequency.setValueAtTime(isCover ? 110 : 160, now);
    whooshOsc.frequency.exponentialRampToValueAtTime(isCover ? 40 : 65, now + duration);

    const whooshGain = ctx.createGain();
    whooshGain.gain.setValueAtTime(0.0001, now);
    whooshGain.gain.linearRampToValueAtTime(isCover ? 0.12 : 0.06, now + 0.04);
    whooshGain.gain.exponentialRampToValueAtTime(0.0001, now + duration * 0.85);

    whooshOsc.connect(whooshGain);
    whooshGain.connect(ctx.destination);

    // Start audio sources
    whiteNoise.start(now);
    whooshOsc.start(now);
    whiteNoise.stop(now + duration);
    whooshOsc.stop(now + duration);
  } catch (err) {
    console.debug('Page turn audio unavailable:', err);
  }
}
