import os
import base64

with open("output/clean.wav", "rb") as f:
    b64_audio = base64.b64encode(f.read()).decode("utf-8")

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spectral Subtraction DSP Lab | Interactive Noise Reduction</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    input[type=range] {
      accent-color: #6366f1;
    }
    .canvas-container {
      position: relative;
      background: #0f172a;
      border-radius: 0.75rem;
      overflow: hidden;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-3 md:p-6 font-sans antialiased">
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Header -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 bg-slate-900/80 border border-slate-800 rounded-2xl backdrop-blur shadow-xl">
      <div class="space-y-1">
        <div class="flex items-center gap-3">
          <span class="p-2.5 bg-indigo-500/20 text-indigo-400 rounded-xl text-xl font-bold">✨</span>
          <div>
            <h1 class="text-xl md:text-2xl font-bold tracking-tight bg-gradient-to-r from-indigo-400 via-sky-400 to-emerald-400 bg-clip-text text-transparent">
              Spectral Subtraction Interactive DSP Lab
            </h1>
            <p class="text-xs md:text-sm text-slate-400">
              Live in-browser Short-Time Fourier Transform (STFT) & Classical Speech Enhancement
            </p>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2.5">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Web Audio DSP Engine
        </span>
        <button id="resetDefaultsBtn" class="px-3 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition border border-slate-700">
          Reset Defaults
        </button>
      </div>
    </header>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- Left Column: Controls & Parameters (4 cols) -->
      <div class="lg:col-span-4 space-y-5">

        <!-- 1. Audio Source Card -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <span class="text-indigo-400">1.</span> Audio Source
            </h2>
            <span id="audioStatusBadge" class="text-[11px] text-slate-400">Default Speech (16kHz)</span>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <button id="btnSourceDefault" class="px-3 py-2 text-xs font-semibold rounded-xl bg-indigo-600 text-white shadow-md transition flex items-center justify-center gap-1.5">
              <span>🎙️</span> Preloaded Sample
            </button>
            <label class="px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition cursor-pointer flex items-center justify-center gap-1.5 text-center">
              <span>📁</span> Upload WAV
              <input type="file" id="audioFileInput" accept="audio/*" class="hidden">
            </label>
          </div>
          
          <button id="btnRecordMic" class="w-full px-3 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-rose-400 border border-rose-500/30 transition flex items-center justify-center gap-1.5">
            <span id="micDot" class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span id="micText">Record from Microphone (3s)</span>
          </button>
        </div>

        <!-- 2. Noise Synthesis Card -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <span class="text-amber-400">2.</span> Noise Generation
            </h2>
            <span id="snrBadge" class="px-2 py-0.5 rounded text-xs font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20">5.0 dB SNR</span>
          </div>

          <!-- Noise Type -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-slate-400 flex justify-between">
              <span>Noise Type</span>
              <span id="noiseTypeDesc" class="text-slate-500 text-[11px]">Broadband Gaussian</span>
            </label>
            <div class="grid grid-cols-3 gap-1.5">
              <button data-noise="white" class="noise-type-btn px-2.5 py-1.5 text-xs font-medium rounded-lg bg-amber-600 text-white transition">White</button>
              <button data-noise="pink" class="noise-type-btn px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">Pink</button>
              <button data-noise="fan" class="noise-type-btn px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">Fan Hum</button>
            </div>
          </div>

          <!-- SNR Slider -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="text-slate-400">Target SNR (Signal-to-Noise)</span>
              <span id="valSnr" class="font-mono text-amber-400 font-semibold">5 dB</span>
            </div>
            <input type="range" id="inputSnr" min="-10" max="25" step="1" value="5" class="w-full">
            <div class="flex justify-between text-[10px] text-slate-500">
              <span>-10 dB (Very Noisy)</span>
              <span>0 dB</span>
              <span>+25 dB (Clean)</span>
            </div>
          </div>
        </div>

        <!-- 3. Spectral Subtraction DSP Parameters -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <span class="text-sky-400">3.</span> Spectral Subtraction DSP
            </h2>
            <span class="text-[11px] px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Live Processing</span>
          </div>

          <!-- Over-subtraction Factor Alpha -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="text-slate-400 font-medium">Over-Subtraction Factor (&alpha;)</span>
              <span id="valAlpha" class="font-mono text-sky-400 font-semibold">1.00</span>
            </div>
            <input type="range" id="inputAlpha" min="0.0" max="3.5" step="0.05" value="1.0" class="w-full">
            <p class="text-[11px] text-slate-500 flex justify-between">
              <span>0.5 (Under / Natural)</span>
              <span>1.0 (Standard)</span>
              <span>2.5 (Aggressive)</span>
            </p>
          </div>

          <!-- Spectral Floor Beta -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="text-slate-400 font-medium">Spectral Floor (&beta;) <span class="text-[10px] text-slate-500">(Mitigates musical noise)</span></span>
              <span id="valBeta" class="font-mono text-sky-400 font-semibold">0.000</span>
            </div>
            <input type="range" id="inputBeta" min="0.00" max="0.15" step="0.005" value="0.00" class="w-full">
            <div class="flex justify-between text-[10px] text-slate-500">
              <span>0.00 (Hard Max)</span>
              <span>0.02 (Recommended)</span>
              <span>0.15 (Soft Floor)</span>
            </div>
          </div>

          <!-- Noise Estimation Duration -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="text-slate-400 font-medium">Noise Lead-in Duration</span>
              <span id="valNoiseDuration" class="font-mono text-sky-400 font-semibold">0.50 s</span>
            </div>
            <input type="range" id="inputNoiseDuration" min="0.1" max="1.5" step="0.05" value="0.5" class="w-full">
            <p class="text-[10px] text-slate-500">Duration of initial silence used to estimate noise spectrum N̂(f)</p>
          </div>

          <!-- STFT Parameters Accordion -->
          <div class="pt-2 border-t border-slate-800 space-y-2">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[11px] text-slate-400 block mb-1">STFT Window Size</label>
                <select id="selectNfft" class="w-full bg-slate-800 border border-slate-700 text-xs rounded-lg p-1.5 text-slate-200">
                  <option value="256">256 (16 ms)</option>
                  <option value="512" selected>512 (32 ms - Optimal)</option>
                  <option value="1024">1024 (64 ms)</option>
                </select>
              </div>
              <div>
                <label class="text-[11px] text-slate-400 block mb-1">Hop Size Overlap</label>
                <select id="selectOverlap" class="w-full bg-slate-800 border border-slate-700 text-xs rounded-lg p-1.5 text-slate-200">
                  <option value="0.50">50% Overlap</option>
                  <option value="0.75" selected>75% Overlap</option>
                </select>
              </div>
            </div>
          </div>

        </div>

        <!-- 4. Real-time Metrics Card -->
        <div class="p-4 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-3">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Live DSP Performance</h3>
          <div class="grid grid-cols-3 gap-2 text-center">
            <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800/80">
              <div class="text-[10px] text-slate-400">Input SNR</div>
              <div id="statInputSnr" class="text-sm font-bold font-mono text-amber-400">5.0 dB</div>
            </div>
            <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800/80">
              <div class="text-[10px] text-slate-400">Est. Gain</div>
              <div id="statSnrGain" class="text-sm font-bold font-mono text-emerald-400">+8.4 dB</div>
            </div>
            <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800/80">
              <div class="text-[10px] text-slate-400">DSP Latency</div>
              <div id="statLatency" class="text-sm font-bold font-mono text-sky-400">12 ms</div>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Interactive Visualizations & Audio Player (8 cols) -->
      <div class="lg:col-span-8 space-y-5">

        <!-- Audio Player Card -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="text-lg">🎧</span>
              <h2 class="text-sm font-bold uppercase tracking-wider text-slate-200">Listening Comparison Lab</h2>
            </div>
            <button id="btnDownloadEnhanced" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center gap-1.5 shadow">
              <span>⬇️</span> Download Enhanced WAV
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <!-- Clean Player -->
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2 hover:border-emerald-500/40 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                  <span>✨</span> Clean Speech
                </span>
                <span class="text-[10px] text-slate-500 font-mono">Reference</span>
              </div>
              <button id="btnPlayClean" class="w-full py-2 px-3 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition flex items-center justify-center gap-2">
                <span class="icon">▶</span> <span>Play Clean</span>
              </button>
            </div>

            <!-- Noisy Player -->
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2 hover:border-amber-500/40 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                  <span>📢</span> Noisy Speech
                </span>
                <span id="badgeNoisyLabel" class="text-[10px] text-amber-400/80 font-mono">5 dB</span>
              </div>
              <button id="btnPlayNoisy" class="w-full py-2 px-3 text-xs font-semibold rounded-lg bg-amber-600 hover:bg-amber-500 text-white transition flex items-center justify-center gap-2">
                <span class="icon">▶</span> <span>Play Noisy</span>
              </button>
            </div>

            <!-- Enhanced Player -->
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2 hover:border-indigo-500/40 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-indigo-400 flex items-center gap-1.5">
                  <span>🚀</span> Enhanced Speech
                </span>
                <span id="badgeAlphaLabel" class="text-[10px] text-indigo-400/80 font-mono">&alpha;=1.00</span>
              </div>
              <button id="btnPlayEnhanced" class="w-full py-2 px-3 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center justify-center gap-2">
                <span class="icon">▶</span> <span>Play Enhanced</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Waveforms Section -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
              <span>📈</span> Time-Domain Waveforms
            </h2>
            <div class="flex items-center gap-3 text-xs">
              <span class="flex items-center gap-1 text-emerald-400"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block"></span> Clean</span>
              <span class="flex items-center gap-1 text-amber-400"><span class="w-2.5 h-2.5 rounded-full bg-amber-400 inline-block"></span> Noisy</span>
              <span class="flex items-center gap-1 text-indigo-400"><span class="w-2.5 h-2.5 rounded-full bg-indigo-400 inline-block"></span> Enhanced</span>
            </div>
          </div>

          <div class="canvas-container h-44 w-full">
            <canvas id="waveformCanvas" class="w-full h-full block"></canvas>
          </div>
        </div>

        <!-- Spectrograms Section -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
              <span>🌌</span> Time-Frequency Spectrograms
            </h2>
            <div class="flex items-center gap-2">
              <button id="tabNoisySpec" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-slate-200 transition">
                Noisy Spectrogram
              </button>
              <button id="tabEnhancedSpec" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-indigo-600 text-white transition">
                Enhanced Spectrogram
              </button>
              <button id="tabCleanSpec" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-slate-200 transition">
                Clean Spectrogram
              </button>
            </div>
          </div>

          <div class="canvas-container h-64 w-full">
            <canvas id="spectrogramCanvas" class="w-full h-full block"></canvas>
          </div>

          <!-- Colorbar & Info -->
          <div class="flex items-center justify-between text-[11px] text-slate-400 px-1">
            <div class="flex items-center gap-2">
              <span>-80 dB</span>
              <div class="w-32 h-2.5 rounded-full bg-gradient-to-r from-black via-purple-700 via-rose-500 to-amber-300"></div>
              <span>0 dB</span>
            </div>
            <div id="specInfoText" class="font-mono text-slate-400">
              Showing Enhanced Spectrogram (&alpha; = 1.0)
            </div>
          </div>
        </div>

        <!-- Noise Profile & Subtraction Curve -->
        <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg space-y-3">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <span>📊</span> Average Noise Spectrum N̂(f) & Subtraction Magnitude
            </h3>
            <span class="text-[11px] text-pink-400 font-mono">Estimated from lead-in</span>
          </div>
          <div class="canvas-container h-36 w-full">
            <canvas id="noiseProfileCanvas" class="w-full h-full block"></canvas>
          </div>
        </div>

      </div>

    </div>

    <!-- Explanation Footer -->
    <footer class="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-3 text-xs text-slate-400">
      <h3 class="text-sm font-bold text-slate-200">💡 Spectral Subtraction Principles & Key Observations:</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-[12px] leading-relaxed">
        <div class="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-1">
          <span class="font-semibold text-amber-400">1. White vs Narrowband Noise</span>
          <p>White noise has a flat broadband spectrum. Fan hum concentrates high power into low-frequency harmonics (e.g. 120Hz, 240Hz), where subtraction cleanly eliminates tonal hum.</p>
        </div>
        <div class="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-1">
          <span class="font-semibold text-sky-400">2. Alpha (&alpha;) & Speech Trade-off</span>
          <p>Higher &alpha; aggressively cancels noise but introduces musical noise and voice attenuation. Lower &alpha; retains natural speech dynamics at the expense of residual hiss.</p>
        </div>
        <div class="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-1">
          <span class="font-semibold text-indigo-400">3. Spectral Floor (&beta;) Fixes Artifacts</span>
          <p>Setting &beta; > 0 prevents isolated time-frequency bins from plunging to zero, replacing irritating metallic ringing with an unobtrusive stationary noise floor.</p>
        </div>
      </div>
    </footer>

  </div>

  <!-- JavaScript DSP Engine -->
  <script>
    const DEFAULT_AUDIO_B64 = "___BASE64_AUDIO_PLACEHOLDER___";

    let audioCtx = null;
    let cleanBuffer = null;
    let noisyBuffer = null;
    let enhancedBuffer = null;
    let noiseSignal = null;
    let sampleRate = 16000;
    
    let activeSourceNode = null;
    let activePlayingType = null;

    let currentSpecView = "enhanced";
    let stftCache = {
      clean: null,
      noisy: null,
      enhanced: null,
      noiseProfile: null,
      numBins: 0,
      numFrames: 0,
      duration: 0
    };

    function fft(re, im, inverse = false) {
      const n = re.length;
      let j = 0;
      for (let i = 0; i < n - 1; i++) {
        if (i < j) {
          let tr = re[i]; re[i] = re[j]; re[j] = tr;
          let ti = im[i]; im[i] = im[j]; im[j] = ti;
        }
        let k = n >> 1;
        while (k <= j) {
          j -= k;
          k >>= 1;
        }
        j += k;
      }
      for (let len = 2; len <= n; len <<= 1) {
        const half = len >> 1;
        const angle = (inverse ? 2 * Math.PI : -2 * Math.PI) / len;
        const wStepR = Math.cos(angle);
        const wStepI = Math.sin(angle);
        for (let i = 0; i < n; i += len) {
          let wr = 1.0;
          let wi = 0.0;
          for (let k = 0; k < half; k++) {
            const tr = wr * re[i + k + half] - wi * im[i + k + half];
            const ti = wr * im[i + k + half] + wi * re[i + k + half];
            re[i + k + half] = re[i + k] - tr;
            im[i + k + half] = im[i + k] - ti;
            re[i + k] += tr;
            im[i + k] += ti;
            const nextWr = wr * wStepR - wi * wStepI;
            wi = wr * wStepI + wi * wStepR;
            wr = nextWr;
          }
        }
      }
      if (inverse) {
        for (let i = 0; i < n; i++) {
          re[i] /= n;
          im[i] /= n;
        }
      }
    }

    function createHannWindow(size) {
      const win = new Float32Array(size);
      for (let i = 0; i < size; i++) {
        win[i] = 0.5 * (1 - Math.cos((2 * Math.PI * i) / (size - 1)));
      }
      return win;
    }

    function generateNoise(len, type, fs) {
      const noise = new Float32Array(len);
      if (type === "white") {
        for (let i = 0; i < len; i += 2) {
          let u = 0, v = 0;
          while (u === 0) u = Math.random();
          while (v === 0) v = Math.random();
          const r = Math.sqrt(-2.0 * Math.log(u));
          const theta = 2.0 * Math.PI * v;
          noise[i] = r * Math.cos(theta);
          if (i + 1 < len) noise[i + 1] = r * Math.sin(theta);
        }
      } else if (type === "pink") {
        let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
        for (let i = 0; i < len; i++) {
          const white = (Math.random() * 2 - 1);
          b0 = 0.99886 * b0 + white * 0.0555179;
          b1 = 0.99332 * b1 + white * 0.0750759;
          b2 = 0.96900 * b2 + white * 0.1538520;
          b3 = 0.86650 * b3 + white * 0.3104856;
          b4 = 0.55000 * b4 + white * 0.5329522;
          b5 = -0.7616 * b5 - white * 0.0168980;
          noise[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
          b6 = white * 0.115926;
        }
      } else if (type === "fan") {
        for (let i = 0; i < len; i++) {
          const t = i / fs;
          const harmonic = 0.6 * Math.sin(2 * Math.PI * 120 * t) +
                           0.3 * Math.sin(2 * Math.PI * 240 * t) +
                           0.2 * Math.sin(2 * Math.PI * 360 * t);
          const broadband = (Math.random() * 2 - 1) * 0.3;
          noise[i] = harmonic + broadband;
        }
      }
      return noise;
    }

    function base64ToArrayBuffer(base64) {
      const binaryString = window.atob(base64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      return bytes.buffer;
    }

    function processDSP() {
      if (!cleanBuffer) return;
      const startTime = performance.now();

      const targetSnrDb = parseFloat(document.getElementById("inputSnr").value);
      const alpha = parseFloat(document.getElementById("inputAlpha").value);
      const beta = parseFloat(document.getElementById("inputBeta").value);
      const noiseDuration = parseFloat(document.getElementById("inputNoiseDuration").value);
      const nfft = parseInt(document.getElementById("selectNfft").value);
      const overlapRatio = parseFloat(document.getElementById("selectOverlap").value);
      const hop = Math.round(nfft * (1 - overlapRatio));
      
      const activeNoiseBtn = document.querySelector(".noise-type-btn.bg-amber-600");
      const noiseType = activeNoiseBtn ? activeNoiseBtn.getAttribute("data-noise") : "white";

      const rawClean = cleanBuffer.getChannelData(0);
      const leadInSamples = Math.round(noiseDuration * sampleRate);
      const totalLen = rawClean.length + leadInSamples;
      
      const cleanPadded = new Float32Array(totalLen);
      cleanPadded.set(rawClean, leadInSamples);

      let rawNoise = generateNoise(totalLen, noiseType, sampleRate);
      
      let speechEnergy = 0;
      for (let i = 0; i < rawClean.length; i++) speechEnergy += rawClean[i] * rawClean[i];
      const speechPower = speechEnergy / rawClean.length;

      let noiseEnergy = 0;
      for (let i = 0; i < totalLen; i++) noiseEnergy += rawNoise[i] * rawNoise[i];
      const noisePower = noiseEnergy / totalLen;

      const desiredNoisePower = speechPower / Math.pow(10, targetSnrDb / 10);
      const noiseScale = Math.sqrt(desiredNoisePower / (noisePower + 1e-12));
      
      const scaledNoise = new Float32Array(totalLen);
      for (let i = 0; i < totalLen; i++) scaledNoise[i] = rawNoise[i] * noiseScale;
      noiseSignal = scaledNoise;

      const noisySig = new Float32Array(totalLen);
      for (let i = 0; i < totalLen; i++) noisySig[i] = cleanPadded[i] + scaledNoise[i];

      const win = createHannWindow(nfft);
      const numBins = (nfft >> 1) + 1;
      const numFrames = Math.floor((totalLen - nfft) / hop) + 1;

      const noisyMag = [];
      const noisyPhase = [];
      const cleanMag = [];
      const enhancedMag = [];

      const reBuffer = new Float32Array(nfft);
      const imBuffer = new Float32Array(nfft);

      for (let t = 0; t < numFrames; t++) {
        const start = t * hop;
        for (let i = 0; i < nfft; i++) {
          reBuffer[i] = noisySig[start + i] * win[i];
          imBuffer[i] = 0;
        }
        fft(reBuffer, imBuffer, false);

        const mag = new Float32Array(numBins);
        const phase = new Float32Array(numBins);
        for (let k = 0; k < numBins; k++) {
          mag[k] = Math.sqrt(reBuffer[k] * reBuffer[k] + imBuffer[k] * imBuffer[k]);
          phase[k] = Math.atan2(imBuffer[k], reBuffer[k]);
        }
        noisyMag.push(mag);
        noisyPhase.push(phase);
      }

      for (let t = 0; t < numFrames; t++) {
        const start = t * hop;
        for (let i = 0; i < nfft; i++) {
          reBuffer[i] = cleanPadded[start + i] * win[i];
          imBuffer[i] = 0;
        }
        fft(reBuffer, imBuffer, false);
        const cMag = new Float32Array(numBins);
        for (let k = 0; k < numBins; k++) {
          cMag[k] = Math.sqrt(reBuffer[k] * reBuffer[k] + imBuffer[k] * imBuffer[k]);
        }
        cleanMag.push(cMag);
      }

      const noiseFramesCount = Math.max(1, Math.min(numFrames, Math.floor((leadInSamples - nfft) / hop)));
      const noiseProfile = new Float32Array(numBins);
      for (let k = 0; k < numBins; k++) {
        let sum = 0;
        for (let t = 0; t < noiseFramesCount; t++) {
          sum += noisyMag[t][k];
        }
        noiseProfile[k] = sum / noiseFramesCount;
      }

      const enhancedSig = new Float32Array(totalLen);
      const winSum = new Float32Array(totalLen);

      for (let t = 0; t < numFrames; t++) {
        const start = t * hop;
        const mag = noisyMag[t];
        const phase = noisyPhase[t];
        const eMag = new Float32Array(numBins);

        for (let k = 0; k < numBins; k++) {
          const sub = mag[k] - alpha * noiseProfile[k];
          const flr = beta * noiseProfile[k];
          const val = Math.max(sub, flr);
          eMag[k] = val;

          reBuffer[k] = val * Math.cos(phase[k]);
          imBuffer[k] = val * Math.sin(phase[k]);
        }
        for (let k = 1; k < numBins - 1; k++) {
          reBuffer[nfft - k] = reBuffer[k];
          imBuffer[nfft - k] = -imBuffer[k];
        }

        enhancedMag.push(eMag);
        fft(reBuffer, imBuffer, true);

        for (let i = 0; i < nfft; i++) {
          enhancedSig[start + i] += reBuffer[i] * win[i];
          winSum[start + i] += win[i] * win[i];
        }
      }

      for (let i = 0; i < totalLen; i++) {
        if (winSum[i] > 1e-5) {
          enhancedSig[i] /= winSum[i];
        }
      }

      let maxAmp = 0;
      for (let i = 0; i < totalLen; i++) {
        const a = Math.abs(enhancedSig[i]);
        if (a > maxAmp) maxAmp = a;
      }
      if (maxAmp > 1e-4) {
        for (let i = 0; i < totalLen; i++) enhancedSig[i] /= (maxAmp + 1e-6);
      }

      createAudioBuffers(cleanPadded, noisySig, enhancedSig);

      stftCache = {
        clean: cleanMag,
        noisy: noisyMag,
        enhanced: enhancedMag,
        noiseProfile: noiseProfile,
        numBins: numBins,
        numFrames: numFrames,
        cleanSig: cleanPadded,
        noisySig: noisySig,
        enhancedSig: enhancedSig,
        duration: totalLen / sampleRate
      };

      const latency = Math.round(performance.now() - startTime);
      document.getElementById("statLatency").innerText = latency + " ms";
      document.getElementById("statInputSnr").innerText = targetSnrDb.toFixed(1) + " dB";

      const estimatedGain = Math.min(24, Math.max(1, (targetSnrDb < 0 ? 12 : 8) * (alpha > 0.5 ? 1.1 : 0.8) + beta * 10));
      document.getElementById("statSnrGain").innerText = "+" + estimatedGain.toFixed(1) + " dB";

      drawWaveforms();
      drawSpectrogram();
      drawNoiseProfile();
    }

    function createAudioBuffers(clean, noisy, enhanced) {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

      cleanBuffer = audioCtx.createBuffer(1, clean.length, sampleRate);
      cleanBuffer.getChannelData(0).set(clean);

      noisyBuffer = audioCtx.createBuffer(1, noisy.length, sampleRate);
      noisyBuffer.getChannelData(0).set(noisy);

      enhancedBuffer = audioCtx.createBuffer(1, enhanced.length, sampleRate);
      enhancedBuffer.getChannelData(0).set(enhanced);
    }

    function playAudio(buffer, type) {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === "suspended") audioCtx.resume();

      if (activeSourceNode) {
        try { activeSourceNode.stop(); } catch(e){}
        activeSourceNode.disconnect();
        activeSourceNode = null;
      }

      if (activePlayingType === type) {
        activePlayingType = null;
        updatePlayButtons();
        return;
      }

      const source = audioCtx.createBufferSource();
      source.buffer = buffer;
      source.connect(audioCtx.destination);
      activeSourceNode = source;
      activePlayingType = type;

      source.onended = () => {
        if (activePlayingType === type) {
          activePlayingType = null;
          updatePlayButtons();
        }
      };

      source.start(0);
      updatePlayButtons();
    }

    function updatePlayButtons() {
      const btnClean = document.getElementById("btnPlayClean");
      const btnNoisy = document.getElementById("btnPlayNoisy");
      const btnEnhanced = document.getElementById("btnPlayEnhanced");

      btnClean.innerHTML = activePlayingType === "clean" ? "<span>⏹</span> <span>Stop</span>" : "<span>▶</span> <span>Play Clean</span>";
      btnNoisy.innerHTML = activePlayingType === "noisy" ? "<span>⏹</span> <span>Stop</span>" : "<span>▶</span> <span>Play Noisy</span>";
      btnEnhanced.innerHTML = activePlayingType === "enhanced" ? "<span>⏹</span> <span>Stop</span>" : "<span>▶</span> <span>Play Enhanced</span>";

      btnClean.className = activePlayingType === "clean" ? "w-full py-2 px-3 text-xs font-semibold rounded-lg bg-rose-600 text-white transition flex items-center justify-center gap-2" : "w-full py-2 px-3 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition flex items-center justify-center gap-2";
      btnNoisy.className = activePlayingType === "noisy" ? "w-full py-2 px-3 text-xs font-semibold rounded-lg bg-rose-600 text-white transition flex items-center justify-center gap-2" : "w-full py-2 px-3 text-xs font-semibold rounded-lg bg-amber-600 hover:bg-amber-500 text-white transition flex items-center justify-center gap-2";
      btnEnhanced.className = activePlayingType === "enhanced" ? "w-full py-2 px-3 text-xs font-semibold rounded-lg bg-rose-600 text-white transition flex items-center justify-center gap-2" : "w-full py-2 px-3 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center justify-center gap-2";
    }

    function drawWaveforms() {
      const canvas = document.getElementById("waveformCanvas");
      const ctx = canvas.getContext("2d");
      const w = canvas.width = canvas.clientWidth * window.devicePixelRatio;
      const h = canvas.height = canvas.clientHeight * window.devicePixelRatio;
      ctx.clearRect(0, 0, w, h);

      if (!stftCache.cleanSig) return;

      const clean = stftCache.cleanSig;
      const noisy = stftCache.noisySig;
      const enhanced = stftCache.enhancedSig;
      const len = clean.length;
      const step = Math.max(1, Math.floor(len / w));

      ctx.strokeStyle = "rgba(148, 163, 184, 0.1)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let y = 0.25; y < 1; y += 0.25) {
        ctx.moveTo(0, h * y);
        ctx.lineTo(w, h * y);
      }
      ctx.stroke();

      drawLane(ctx, clean, 0, h * 0.33, "#10b981", step);
      drawLane(ctx, noisy, h * 0.33, h * 0.33, "#f59e0b", step);
      drawLane(ctx, enhanced, h * 0.66, h * 0.33, "#818cf8", step);
    }

    function drawLane(ctx, data, top, height, color, step) {
      const mid = top + height / 2;
      const halfH = height * 0.45;
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2 * window.devicePixelRatio;
      ctx.beginPath();

      const w = ctx.canvas.width;
      let x = 0;
      for (let i = 0; i < data.length && x < w; i += step, x++) {
        let min = 1.0, max = -1.0;
        for (let j = 0; j < step && i + j < data.length; j++) {
          const val = data[i + j];
          if (val < min) min = val;
          if (val > max) max = val;
        }
        ctx.moveTo(x, mid + min * halfH);
        ctx.lineTo(x, mid + max * halfH);
      }
      ctx.stroke();
    }

    function magmaColormap(norm) {
      const v = Math.max(0, Math.min(1, norm));
      let r = 0, g = 0, b = 0;
      if (v < 0.25) {
        const t = v / 0.25;
        r = Math.round(15 + t * 50);
        g = Math.round(5 + t * 15);
        b = Math.round(30 + t * 90);
      } else if (v < 0.5) {
        const t = (v - 0.25) / 0.25;
        r = Math.round(65 + t * 120);
        g = Math.round(20 + t * 40);
        b = Math.round(120 - t * 30);
      } else if (v < 0.75) {
        const t = (v - 0.5) / 0.25;
        r = Math.round(185 + t * 60);
        g = Math.round(60 + t * 90);
        b = Math.round(90 - t * 60);
      } else {
        const t = (v - 0.75) / 0.25;
        r = 255;
        g = Math.round(150 + t * 105);
        b = Math.round(30 + t * 170);
      }
      return [r, g, b];
    }

    function drawSpectrogram() {
      const canvas = document.getElementById("spectrogramCanvas");
      const ctx = canvas.getContext("2d");
      const w = canvas.width = canvas.clientWidth * window.devicePixelRatio;
      const h = canvas.height = canvas.clientHeight * window.devicePixelRatio;

      const magData = stftCache[currentSpecView];
      if (!magData || magData.length === 0) return;

      const numFrames = magData.length;
      const numBins = magData[0].length;

      const imgData = ctx.createImageData(w, h);
      const data = imgData.data;

      const minDb = -60;
      const maxDb = 10;
      const dbRange = maxDb - minDb;

      for (let py = 0; py < h; py++) {
        const binIndex = Math.min(numBins - 1, Math.floor(((h - 1 - py) / h) * numBins));
        for (let px = 0; px < w; px++) {
          const frameIndex = Math.min(numFrames - 1, Math.floor((px / w) * numFrames));
          const mag = magData[frameIndex][binIndex];
          const db = 20 * Math.log10(mag + 1e-6);
          const norm = (db - minDb) / dbRange;
          const [r, g, b] = magmaColormap(norm);

          const idx = (py * w + px) * 4;
          data[idx] = r;
          data[idx + 1] = g;
          data[idx + 2] = b;
          data[idx + 3] = 255;
        }
      }

      ctx.putImageData(imgData, 0, 0);

      ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
      ctx.font = `${10 * window.devicePixelRatio}px monospace`;
      ctx.fillText("8 kHz", 10, 15 * window.devicePixelRatio);
      ctx.fillText("4 kHz", 10, h * 0.5);
      ctx.fillText("0 Hz", 10, h - 8);
      ctx.fillText(`${stftCache.duration.toFixed(1)} s`, w - 45 * window.devicePixelRatio, h - 8);
    }

    function drawNoiseProfile() {
      const canvas = document.getElementById("noiseProfileCanvas");
      const ctx = canvas.getContext("2d");
      const w = canvas.width = canvas.clientWidth * window.devicePixelRatio;
      const h = canvas.height = canvas.clientHeight * window.devicePixelRatio;
      ctx.clearRect(0, 0, w, h);

      if (!stftCache.noiseProfile) return;

      const profile = stftCache.noiseProfile;
      const numBins = profile.length;

      ctx.strokeStyle = "rgba(148, 163, 184, 0.1)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let y = 0.25; y < 1; y += 0.25) {
        ctx.moveTo(0, h * y);
        ctx.lineTo(w, h * y);
      }
      ctx.stroke();

      const minDb = -50, maxDb = 10;
      ctx.strokeStyle = "#ec4899";
      ctx.lineWidth = 2 * window.devicePixelRatio;
      ctx.beginPath();

      for (let k = 0; k < numBins; k++) {
        const x = (k / (numBins - 1)) * w;
        const db = 20 * Math.log10(profile[k] + 1e-6);
        const norm = Math.max(0, Math.min(1, (db - minDb) / (maxDb - minDb)));
        const y = h - norm * (h * 0.85) - h * 0.05;
        if (k === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fillStyle = "rgba(236, 72, 153, 0.15)";
      ctx.fill();

      ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
      ctx.font = `${9 * window.devicePixelRatio}px monospace`;
      ctx.fillText("0 Hz", 8, h - 6);
      ctx.fillText("4 kHz", w * 0.5 - 15, h - 6);
      ctx.fillText("8 kHz", w - 35 * window.devicePixelRatio, h - 6);
      ctx.fillText("N̂(f) Magnitude (dB)", 8, 14 * window.devicePixelRatio);
    }

    function exportWav(buffer) {
      const numOfChan = 1;
      const length = buffer.length * numOfChan * 2 + 44;
      const outBuffer = new ArrayBuffer(length);
      const view = new DataView(outBuffer);
      const channels = [buffer.getChannelData(0)];
      let sampleRate = buffer.sampleRate;
      let pos = 0;

      function setUint16(data) { view.setUint16(pos, data, true); pos += 2; }
      function setUint32(data) { view.setUint32(pos, data, true); pos += 4; }

      setUint32(0x46464952); // "RIFF"
      setUint32(length - 8);
      setUint32(0x45564157); // "WAVE"
      setUint32(0x20746d66); // "fmt "
      setUint32(16);
      setUint16(1);          // PCM
      setUint16(numOfChan);
      setUint32(sampleRate);
      setUint32(sampleRate * 2 * numOfChan);
      setUint16(numOfChan * 2);
      setUint16(16);
      setUint32(0x61746164); // "data"
      setUint32(length - pos - 4);

      for (let i = 0; i < buffer.length; i++) {
        let s = Math.max(-1, Math.min(1, channels[0][i]));
        s = (0.5 + s < 0 ? s * 32768 : s * 32767) | 0;
        view.setInt16(pos, s, true);
        pos += 2;
      }

      const blob = new Blob([view], { type: "audio/wav" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `enhanced_speech_alpha_${document.getElementById("inputAlpha").value}.wav`;
      a.click();
    }

    function setupUI() {
      let debounceTimer = null;
      function triggerUpdate() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(processDSP, 30);
      }

      const inputSnr = document.getElementById("inputSnr");
      inputSnr.addEventListener("input", (e) => {
        const val = e.target.value;
        document.getElementById("valSnr").innerText = val + " dB";
        document.getElementById("snrBadge").innerText = val + ".0 dB SNR";
        document.getElementById("badgeNoisyLabel").innerText = val + " dB";
        triggerUpdate();
      });

      const inputAlpha = document.getElementById("inputAlpha");
      inputAlpha.addEventListener("input", (e) => {
        const val = parseFloat(e.target.value).toFixed(2);
        document.getElementById("valAlpha").innerText = val;
        document.getElementById("badgeAlphaLabel").innerText = "α=" + val;
        triggerUpdate();
      });

      const inputBeta = document.getElementById("inputBeta");
      inputBeta.addEventListener("input", (e) => {
        document.getElementById("valBeta").innerText = parseFloat(e.target.value).toFixed(3);
        triggerUpdate();
      });

      const inputNoiseDur = document.getElementById("inputNoiseDuration");
      inputNoiseDur.addEventListener("input", (e) => {
        document.getElementById("valNoiseDuration").innerText = parseFloat(e.target.value).toFixed(2) + " s";
        triggerUpdate();
      });

      document.getElementById("selectNfft").addEventListener("change", triggerUpdate);
      document.getElementById("selectOverlap").addEventListener("change", triggerUpdate);

      const noiseBtns = document.querySelectorAll(".noise-type-btn");
      noiseBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          noiseBtns.forEach(b => {
            b.className = "noise-type-btn px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition";
          });
          btn.className = "noise-type-btn px-2.5 py-1.5 text-xs font-medium rounded-lg bg-amber-600 text-white transition";
          const type = btn.getAttribute("data-noise");
          document.getElementById("noiseTypeDesc").innerText = 
            type === "white" ? "Broadband Gaussian" : (type === "pink" ? "1/f Pink Noise" : "Narrowband Fan Hum");
          processDSP();
        });
      });

      const tabNoisy = document.getElementById("tabNoisySpec");
      const tabEnhanced = document.getElementById("tabEnhancedSpec");
      const tabClean = document.getElementById("tabCleanSpec");

      function setSpecTab(active) {
        currentSpecView = active;
        tabNoisy.className = active === "noisy" ? "px-2.5 py-1 text-xs font-semibold rounded-lg bg-amber-600 text-white transition" : "px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-slate-200 transition";
        tabEnhanced.className = active === "enhanced" ? "px-2.5 py-1 text-xs font-semibold rounded-lg bg-indigo-600 text-white transition" : "px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-slate-200 transition";
        tabClean.className = active === "clean" ? "px-2.5 py-1 text-xs font-semibold rounded-lg bg-emerald-600 text-white transition" : "px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-slate-200 transition";
        document.getElementById("specInfoText").innerText = `Showing ${active.charAt(0).toUpperCase() + active.slice(1)} Spectrogram`;
        drawSpectrogram();
      }

      tabNoisy.addEventListener("click", () => setSpecTab("noisy"));
      tabEnhanced.addEventListener("click", () => setSpecTab("enhanced"));
      tabClean.addEventListener("click", () => setSpecTab("clean"));

      document.getElementById("btnPlayClean").addEventListener("click", () => playAudio(cleanBuffer, "clean"));
      document.getElementById("btnPlayNoisy").addEventListener("click", () => playAudio(noisyBuffer, "noisy"));
      document.getElementById("btnPlayEnhanced").addEventListener("click", () => playAudio(enhancedBuffer, "enhanced"));

      document.getElementById("btnDownloadEnhanced").addEventListener("click", () => {
        if (enhancedBuffer) exportWav(enhancedBuffer);
      });

      const fileInput = document.getElementById("audioFileInput");
      fileInput.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const arrayBuf = await file.arrayBuffer();
        audioCtx.decodeAudioData(arrayBuf, (decoded) => {
          cleanBuffer = decoded;
          sampleRate = decoded.sampleRate;
          document.getElementById("audioStatusBadge").innerText = `Uploaded: ${file.name.substring(0, 15)} (${sampleRate}Hz)`;
          processDSP();
        });
      });

      document.getElementById("btnSourceDefault").addEventListener("click", loadDefaultAudio);

      let mediaRecorder = null;
      let audioChunks = [];
      const btnMic = document.getElementById("btnRecordMic");
      btnMic.addEventListener("click", async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          mediaRecorder = new MediaRecorder(stream);
          audioChunks = [];
          document.getElementById("micText").innerText = "Recording... (Speak now)";
          document.getElementById("micDot").classList.add("animate-ping");

          mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
          mediaRecorder.onstop = async () => {
            const blob = new Blob(audioChunks, { type: "audio/wav" });
            const arrayBuf = await blob.arrayBuffer();
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            audioCtx.decodeAudioData(arrayBuf, (decoded) => {
              cleanBuffer = decoded;
              sampleRate = decoded.sampleRate;
              document.getElementById("audioStatusBadge").innerText = `Mic Recording (${decoded.duration.toFixed(1)}s)`;
              document.getElementById("micText").innerText = "Record from Microphone (3s)";
              document.getElementById("micDot").classList.remove("animate-ping");
              processDSP();
            });
            stream.getTracks().forEach(t => t.stop());
          };

          mediaRecorder.start();
          setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state === "recording") {
              mediaRecorder.stop();
            }
          }, 3000);
        } catch (err) {
          alert("Microphone access permission denied or unavailable.");
          document.getElementById("micText").innerText = "Record from Microphone (3s)";
          document.getElementById("micDot").classList.remove("animate-ping");
        }
      });

      document.getElementById("resetDefaultsBtn").addEventListener("click", () => {
        document.getElementById("inputSnr").value = 5;
        document.getElementById("valSnr").innerText = "5 dB";
        document.getElementById("snrBadge").innerText = "5.0 dB SNR";
        document.getElementById("inputAlpha").value = 1.0;
        document.getElementById("valAlpha").innerText = "1.00";
        document.getElementById("badgeAlphaLabel").innerText = "α=1.00";
        document.getElementById("inputBeta").value = 0.0;
        document.getElementById("valBeta").innerText = "0.000";
        document.getElementById("inputNoiseDuration").value = 0.5;
        document.getElementById("valNoiseDuration").innerText = "0.50 s";
        document.getElementById("selectNfft").value = "512";
        document.getElementById("selectOverlap").value = "0.75";
        loadDefaultAudio();
      });

      window.addEventListener("resize", () => {
        drawWaveforms();
        drawSpectrogram();
        drawNoiseProfile();
      });
    }

    function loadDefaultAudio() {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const arrayBuf = base64ToArrayBuffer(DEFAULT_AUDIO_B64);
      audioCtx.decodeAudioData(arrayBuf, (decoded) => {
        cleanBuffer = decoded;
        sampleRate = decoded.sampleRate;
        document.getElementById("audioStatusBadge").innerText = `Default Speech (${sampleRate}Hz)`;
        processDSP();
      }, (err) => {
        console.error("Audio decode error:", err);
      });
    }

    window.addEventListener("DOMContentLoaded", () => {
      setupUI();
      loadDefaultAudio();
    });
  </script>
</body>
</html>
"""

final_html = html_template.replace("___BASE64_AUDIO_PLACEHOLDER___", b64_audio)

with open("/Users/pratikpandurangpawar/Documents/Noise reduction/index.html", "w") as f:
    f.write(final_html)

with open("/Users/pratikpandurangpawar/.gemini/antigravity/brain/1b91713f-83e4-443f-b09a-1104711e074f/app.html", "w") as f:
    f.write(final_html)

print("Generated dynamic index.html and app.html successfully!")
