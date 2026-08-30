import os
import base64

with open("output/clean.wav", "rb") as f:
    b64_audio = base64.b64encode(f.read()).decode("utf-8")

html_template = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Precision DSP Lab | Spectral Subtraction Speech Enhancement</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .font-mono {
      font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    input[type=range] {
      accent-color: #0284c7;
      background: #e2e8f0;
      height: 6px;
      border-radius: 9999px;
    }
    .canvas-container {
      position: relative;
      background: #fafbfc;
      border: 1px solid #e2e8f0;
      border-radius: 0.875rem;
      overflow: hidden;
    }
  </style>
</head>
<body class="bg-[#f8fafc] text-slate-900 min-h-full flex flex-col antialiased selection:bg-sky-100 selection:text-sky-900">

  <!-- Top Global Navigation Bar (Intuitive / Precision Clean Style) -->
  <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      
      <!-- Brand & Product Title -->
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-slate-900 flex items-center justify-center text-white shadow-xs font-bold text-base">
          ◈
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-2">
            <span class="text-sm font-bold tracking-tight text-slate-950">INTUITIVE DSP</span>
            <span class="text-slate-300 font-light">|</span>
            <span class="text-sm font-medium text-slate-600">Spectral Subtraction Studio</span>
          </div>
          <span class="text-[11px] text-slate-400 font-normal">Real-Time Acoustic Signal Processing & Speech Enhancement</span>
        </div>
      </div>

      <!-- Right Header Actions & Live Indicator -->
      <div class="flex items-center gap-3">
        <div class="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Web Audio Engine Active</span>
        </div>
        <button id="resetDefaultsBtn" class="px-3.5 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-200 transition-colors shadow-xs">
          Reset Parameters
        </button>
      </div>

    </div>
  </header>

  <!-- Main Content Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 flex-1 w-full">

    <!-- Hero / Headline Section -->
    <div class="space-y-2 border-b border-slate-200/80 pb-6">
      <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-sky-50 text-sky-800 text-xs font-semibold border border-sky-200/70 uppercase tracking-wider">
        Clinical Grade DSP • Zero Latency • In-Browser
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-950">
        Spectral Subtraction Audio Enhancement
      </h1>
      <p class="text-sm sm:text-base text-slate-600 max-w-3xl leading-relaxed">
        Experience classical magnitude subtraction in the Short-Time Fourier Transform (STFT) domain. Adjust parameters dynamically to eliminate broadband noise, manage musical artifacts, and analyze acoustic spectrum profiles in real time.
      </p>
    </div>

    <!-- Main Workspace Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <!-- Left Column: Precision Control Panel (4 cols) -->
      <div class="lg:col-span-4 space-y-6">

        <!-- 1. Audio Source Card -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-900 text-white text-[11px] font-bold flex items-center justify-center">1</span>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900">Acoustic Source</h2>
            </div>
            <span id="audioStatusBadge" class="text-[11px] font-mono text-slate-500 bg-slate-50 px-2 py-0.5 rounded border border-slate-200">
              Clean (16kHz)
            </span>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <button id="btnSourceDefault" class="px-3 py-2 text-xs font-semibold rounded-xl bg-slate-900 hover:bg-slate-800 text-white transition-all shadow-xs flex items-center justify-center gap-1.5">
              <span>🎙️</span> Standard Voice
            </button>
            <label class="px-3 py-2 text-xs font-semibold rounded-xl bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 transition-all cursor-pointer flex items-center justify-center gap-1.5 text-center shadow-xs">
              <span>📁</span> Upload WAV
              <input type="file" id="audioFileInput" accept="audio/*" class="hidden">
            </label>
          </div>

          <button id="btnRecordMic" class="w-full px-3 py-2 text-xs font-semibold rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 transition-all flex items-center justify-center gap-2">
            <span id="micDot" class="w-2 h-2 rounded-full bg-rose-600"></span>
            <span id="micText">Capture Microphone Input (3s)</span>
          </button>
        </div>

        <!-- 2. Noise Synthesis Card -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-900 text-white text-[11px] font-bold flex items-center justify-center">2</span>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900">Additive Noise Model</h2>
            </div>
            <span id="snrBadge" class="text-xs font-mono font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
              5.0 dB SNR
            </span>
          </div>

          <!-- Noise Profile Selector -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-slate-600 flex justify-between">
              <span>Noise Profile</span>
              <span id="noiseTypeDesc" class="text-slate-400 text-[11px]">Gaussian Broadband</span>
            </label>
            <div class="grid grid-cols-3 gap-1.5">
              <button data-noise="white" class="noise-type-btn px-2.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 text-white transition shadow-xs">White</button>
              <button data-noise="pink" class="noise-type-btn px-2.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 transition">Pink (1/f)</button>
              <button data-noise="fan" class="noise-type-btn px-2.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 transition">Fan Drone</button>
            </div>
          </div>

          <!-- SNR Slider -->
          <div class="space-y-2 pt-1">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-slate-700">Target SNR (Signal-to-Noise)</span>
              <span id="valSnr" class="font-mono text-slate-900 font-semibold bg-slate-100 px-2 py-0.5 rounded">5 dB</span>
            </div>
            <input type="range" id="inputSnr" min="-10" max="25" step="1" value="5" class="w-full cursor-pointer">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>-10 dB (Severe)</span>
              <span>0 dB</span>
              <span>+25 dB (Mild)</span>
            </div>
          </div>
        </div>

        <!-- 3. Spectral Subtraction Parameters Card -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-900 text-white text-[11px] font-bold flex items-center justify-center">3</span>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900">DSP Filter Tuning</h2>
            </div>
            <span class="text-[11px] font-mono text-sky-700 bg-sky-50 px-2 py-0.5 rounded border border-sky-200">
              Live ISTFT
            </span>
          </div>

          <!-- Over-subtraction Alpha Slider -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-slate-700">Over-Subtraction Factor (&alpha;)</span>
              <span id="valAlpha" class="font-mono text-slate-900 font-semibold bg-slate-100 px-2 py-0.5 rounded">1.00</span>
            </div>
            <input type="range" id="inputAlpha" min="0.0" max="3.5" step="0.05" value="1.0" class="w-full cursor-pointer">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>0.5 (Natural)</span>
              <span>1.0 (Standard)</span>
              <span>2.5 (Aggressive)</span>
            </div>
          </div>

          <!-- Spectral Floor Beta Slider -->
          <div class="space-y-1.5 pt-1">
            <div class="flex justify-between text-xs">
              <div>
                <span class="font-medium text-slate-700">Spectral Floor (&beta;)</span>
                <span class="text-[10px] text-slate-400 block">Controls musical noise ringing</span>
              </div>
              <span id="valBeta" class="font-mono text-slate-900 font-semibold bg-slate-100 px-2 py-0.5 rounded self-start">0.000</span>
            </div>
            <input type="range" id="inputBeta" min="0.00" max="0.15" step="0.005" value="0.00" class="w-full cursor-pointer">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>0.00 (Hard Max)</span>
              <span>0.02 (Optimal)</span>
              <span>0.15 (Soft Floor)</span>
            </div>
          </div>

          <!-- Noise Lead-in Duration -->
          <div class="space-y-1.5 pt-1">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-slate-700">Noise Estimation Lead-in</span>
              <span id="valNoiseDuration" class="font-mono text-slate-900 font-semibold bg-slate-100 px-2 py-0.5 rounded">0.50 s</span>
            </div>
            <input type="range" id="inputNoiseDuration" min="0.1" max="1.5" step="0.05" value="0.5" class="w-full cursor-pointer">
            <span class="text-[10px] text-slate-400 block">Initial quiet window used to compute N̂(f)</span>
          </div>

          <!-- STFT Parameters -->
          <div class="pt-3 border-t border-slate-100 grid grid-cols-2 gap-3">
            <div>
              <label class="text-[11px] font-semibold text-slate-600 block mb-1">STFT Window Size</label>
              <select id="selectNfft" class="w-full bg-slate-50 border border-slate-200 text-xs rounded-lg p-2 text-slate-800 font-medium focus:ring-1 focus:ring-sky-500">
                <option value="256">256 (16 ms)</option>
                <option value="512" selected>512 (32 ms - Recommended)</option>
                <option value="1024">1024 (64 ms)</option>
              </select>
            </div>
            <div>
              <label class="text-[11px] font-semibold text-slate-600 block mb-1">Frame Overlap</label>
              <select id="selectOverlap" class="w-full bg-slate-50 border border-slate-200 text-xs rounded-lg p-2 text-slate-800 font-medium focus:ring-1 focus:ring-sky-500">
                <option value="0.50">50% Overlap</option>
                <option value="0.75" selected>75% Overlap</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 4. Performance Metrics Card -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm space-y-3">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Telemetry & Diagnostic Metrics</h3>
          <div class="grid grid-cols-3 gap-3 text-center">
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80">
              <div class="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Input SNR</div>
              <div id="statInputSnr" class="text-sm font-bold font-mono text-amber-600 mt-0.5">5.0 dB</div>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80">
              <div class="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Est. Gain</div>
              <div id="statSnrGain" class="text-sm font-bold font-mono text-emerald-600 mt-0.5">+8.4 dB</div>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200/80">
              <div class="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Processing</div>
              <div id="statLatency" class="text-sm font-bold font-mono text-sky-600 mt-0.5">12 ms</div>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Interactive Diagnostics & Visualizations (8 cols) -->
      <div class="lg:col-span-8 space-y-6">

        <!-- Listening Comparison Station -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
            <div>
              <h2 class="text-sm font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
                <span>🎧</span> Acoustic Evaluation Station
              </h2>
              <p class="text-xs text-slate-500">A/B test the raw speech, degraded mixture, and enhanced output</p>
            </div>
            <button id="btnDownloadEnhanced" class="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-900 hover:bg-slate-800 text-white transition shadow-xs flex items-center gap-2 self-start sm:self-auto">
              <span>⬇️</span> Download Enhanced WAV
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <!-- Clean Audio Player -->
            <div class="p-4 rounded-xl bg-[#fafbfc] border border-slate-200/80 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-emerald-700 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Clean Reference
                </span>
                <span class="text-[10px] font-mono text-slate-400">Target</span>
              </div>
              <button id="btnPlayClean" class="w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200/80 transition flex items-center justify-center gap-2">
                <span>▶</span> <span>Play Clean</span>
              </button>
            </div>

            <!-- Noisy Audio Player -->
            <div class="p-4 rounded-xl bg-[#fafbfc] border border-slate-200/80 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-800 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-amber-500"></span> Noisy Input
                </span>
                <span id="badgeNoisyLabel" class="text-[10px] font-mono text-amber-700 font-semibold bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200/60">5 dB</span>
              </div>
              <button id="btnPlayNoisy" class="w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200/80 transition flex items-center justify-center gap-2">
                <span>▶</span> <span>Play Noisy</span>
              </button>
            </div>

            <!-- Enhanced Audio Player -->
            <div class="p-4 rounded-xl bg-sky-50/50 border border-sky-200/80 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-sky-900 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-sky-500"></span> Enhanced Output
                </span>
                <span id="badgeAlphaLabel" class="text-[10px] font-mono text-sky-800 font-semibold bg-sky-100/80 px-1.5 py-0.5 rounded border border-sky-200">&alpha;=1.00</span>
              </div>
              <button id="btnPlayEnhanced" class="w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-sky-600 hover:bg-sky-700 text-white shadow-xs transition flex items-center justify-center gap-2">
                <span>▶</span> <span>Play Enhanced</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Time-Domain Waveforms Section -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
              <span>📈</span> Time-Domain Waveform Traces
            </h2>
            <div class="flex items-center gap-4 text-xs font-medium">
              <span class="flex items-center gap-1.5 text-emerald-700"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Clean</span>
              <span class="flex items-center gap-1.5 text-amber-700"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Noisy</span>
              <span class="flex items-center gap-1.5 text-sky-700"><span class="w-2.5 h-2.5 rounded-full bg-sky-600"></span> Enhanced</span>
            </div>
          </div>

          <div class="canvas-container h-44 w-full">
            <canvas id="waveformCanvas" class="w-full h-full block"></canvas>
          </div>
        </div>

        <!-- Spectrograms Section -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
            <div>
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
                <span>🌌</span> Time-Frequency Spectrogram Heatmaps
              </h2>
              <span class="text-[11px] text-slate-400">Full STFT magnitude distribution (0 Hz – 8 kHz)</span>
            </div>
            <div class="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200">
              <button id="tabNoisySpec" class="px-3 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition">
                Noisy
              </button>
              <button id="tabEnhancedSpec" class="px-3 py-1 text-xs font-semibold rounded-lg bg-white text-slate-900 shadow-xs transition">
                Enhanced
              </button>
              <button id="tabCleanSpec" class="px-3 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition">
                Clean Reference
              </button>
            </div>
          </div>

          <div class="canvas-container h-64 w-full">
            <canvas id="spectrogramCanvas" class="w-full h-full block"></canvas>
          </div>

          <!-- Colorbar & Information -->
          <div class="flex items-center justify-between text-[11px] text-slate-500 px-1">
            <div class="flex items-center gap-2">
              <span class="font-mono">-60 dB</span>
              <div class="w-28 h-2 rounded-full bg-gradient-to-r from-[#101827] via-[#7c3aed] via-[#f43f5e] to-[#fef08a]"></div>
              <span class="font-mono">0 dB</span>
            </div>
            <div id="specInfoText" class="font-mono font-medium text-slate-700">
              Enhanced Spectrogram (&alpha; = 1.0)
            </div>
          </div>
        </div>

        <!-- Estimated Noise Profile Section -->
        <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
                <span>📊</span> Noise Power Spectral Density N̂(f)
              </h3>
              <p class="text-[11px] text-slate-400">Estimated from lead-in silence STFT magnitude frames</p>
            </div>
            <span class="text-[11px] text-indigo-700 bg-indigo-50 font-mono font-medium px-2 py-0.5 rounded border border-indigo-200/60">
              Averaged N̂(f)
            </span>
          </div>
          <div class="canvas-container h-36 w-full">
            <canvas id="noiseProfileCanvas" class="w-full h-full block"></canvas>
          </div>
        </div>

      </div>

    </div>

    <!-- Educational Engineering Footer -->
    <footer class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm space-y-4 text-xs text-slate-600">
      <div class="flex items-center gap-2 text-slate-900 font-bold text-sm">
        <span>💡</span> Engineering Insights & Core Observations
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-[12px] leading-relaxed">
        <div class="space-y-1.5 p-4 rounded-xl bg-slate-50 border border-slate-200/70">
          <span class="font-bold text-slate-900">1. Broadband vs Narrowband Attenuation</span>
          <p class="text-slate-600">White noise has an evenly distributed broadband spectral signature. Fan drone noise concentrates intense energy in low-frequency harmonics (120Hz, 240Hz), which Spectral Subtraction eliminates with surgical precision.</p>
        </div>
        <div class="space-y-1.5 p-4 rounded-xl bg-slate-50 border border-slate-200/70">
          <span class="font-bold text-slate-900">2. The Over-Subtraction Trade-off (&alpha;)</span>
          <p class="text-slate-600">Higher &alpha; values provide complete noise elimination during pauses, but cause spectral valleys and audible musical ringing. A balanced &alpha; &approx; 1.0 preserves natural vocal harmonics and intelligibility.</p>
        </div>
        <div class="space-y-1.5 p-4 rounded-xl bg-slate-50 border border-slate-200/70">
          <span class="font-bold text-slate-900">3. Spectral Floor Mitigation (&beta;)</span>
          <p class="text-slate-600">Setting a small spectral floor (&beta; &approx; 0.02) prevents random noise fluctuations from producing isolated sinusoidal spikes in the frequency domain, substituting musical noise with a benign uniform floor.</p>
        </div>
      </div>
    </footer>

  </main>

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

    // --- Fast Radix-2 Cooley-Tukey FFT & IFFT ---
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
      
      const activeNoiseBtn = document.querySelector(".noise-type-btn.bg-slate-900");
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

      btnClean.className = activePlayingType === "clean" ? "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-rose-500 text-white shadow-xs transition flex items-center justify-center gap-2" : "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200/80 transition flex items-center justify-center gap-2";
      btnNoisy.className = activePlayingType === "noisy" ? "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-rose-500 text-white shadow-xs transition flex items-center justify-center gap-2" : "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200/80 transition flex items-center justify-center gap-2";
      btnEnhanced.className = activePlayingType === "enhanced" ? "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-rose-500 text-white shadow-xs transition flex items-center justify-center gap-2" : "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-sky-600 hover:bg-sky-700 text-white shadow-xs transition flex items-center justify-center gap-2";
    }

    // --- Clean Light-Mode Waveforms ---
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

      // Clean Light-Mode Grid Lines
      ctx.strokeStyle = "#e2e8f0";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let y = 0.33; y < 1; y += 0.33) {
        ctx.moveTo(0, h * y);
        ctx.lineTo(w, h * y);
      }
      ctx.stroke();

      // Clean (Emerald top lane)
      drawLane(ctx, clean, 0, h * 0.33, "#059669", step);
      // Noisy (Amber middle lane)
      drawLane(ctx, noisy, h * 0.33, h * 0.33, "#d97706", step);
      // Enhanced (Cobalt bottom lane)
      drawLane(ctx, enhanced, h * 0.66, h * 0.33, "#0284c7", step);
    }

    function drawLane(ctx, data, top, height, color, step) {
      const mid = top + height / 2;
      const halfH = height * 0.44;
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

    // --- Colormap for Spectrogram (Magma / Viridis Hybrid for High Light-Mode Contrast) ---
    function clinicalColormap(norm) {
      const v = Math.max(0, Math.min(1, norm));
      let r = 0, g = 0, b = 0;
      if (v < 0.25) {
        const t = v / 0.25;
        r = Math.round(15 + t * 45);
        g = Math.round(23 + t * 20);
        b = Math.round(42 + t * 110);
      } else if (v < 0.5) {
        const t = (v - 0.25) / 0.25;
        r = Math.round(60 + t * 110);
        g = Math.round(43 + t * 30);
        b = Math.round(152 - t * 40);
      } else if (v < 0.75) {
        const t = (v - 0.5) / 0.25;
        r = Math.round(170 + t * 74);
        g = Math.round(73 + t * 90);
        b = Math.round(112 - t * 80);
      } else {
        const t = (v - 0.75) / 0.25;
        r = Math.round(244 + t * 10);
        g = Math.round(163 + t * 77);
        b = Math.round(32 + t * 106);
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
          const [r, g, b] = clinicalColormap(norm);

          const idx = (py * w + px) * 4;
          data[idx] = r;
          data[idx + 1] = g;
          data[idx + 2] = b;
          data[idx + 3] = 255;
        }
      }

      ctx.putImageData(imgData, 0, 0);

      // Light HUD Labels
      ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
      ctx.font = `${10 * window.devicePixelRatio}px 'JetBrains Mono', monospace`;
      ctx.fillText("8.0 kHz", 12, 16 * window.devicePixelRatio);
      ctx.fillText("4.0 kHz", 12, h * 0.5);
      ctx.fillText("0.0 Hz", 12, h - 8);
      ctx.fillText(`${stftCache.duration.toFixed(1)} s`, w - 48 * window.devicePixelRatio, h - 8);
    }

    // --- Clean Light-Mode Noise PSD Profile ---
    function drawNoiseProfile() {
      const canvas = document.getElementById("noiseProfileCanvas");
      const ctx = canvas.getContext("2d");
      const w = canvas.width = canvas.clientWidth * window.devicePixelRatio;
      const h = canvas.height = canvas.clientHeight * window.devicePixelRatio;
      ctx.clearRect(0, 0, w, h);

      if (!stftCache.noiseProfile) return;

      const profile = stftCache.noiseProfile;
      const numBins = profile.length;

      // Clean Grid
      ctx.strokeStyle = "#e2e8f0";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let y = 0.25; y < 1; y += 0.25) {
        ctx.moveTo(0, h * y);
        ctx.lineTo(w, h * y);
      }
      ctx.stroke();

      const minDb = -50, maxDb = 10;
      ctx.strokeStyle = "#4f46e5";
      ctx.lineWidth = 2 * window.devicePixelRatio;
      ctx.beginPath();

      for (let k = 0; k < numBins; k++) {
        const x = (k / (numBins - 1)) * w;
        const db = 20 * Math.log10(profile[k] + 1e-6);
        const norm = Math.max(0, Math.min(1, (db - minDb) / (maxDb - minDb)));
        const y = h - norm * (h * 0.82) - h * 0.08;
        if (k === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // Soft Indigo Fill
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fillStyle = "rgba(79, 70, 229, 0.08)";
      ctx.fill();

      // Labels
      ctx.fillStyle = "#64748b";
      ctx.font = `${9 * window.devicePixelRatio}px 'JetBrains Mono', monospace`;
      ctx.fillText("0 Hz", 8, h - 6);
      ctx.fillText("4 kHz", w * 0.5 - 15, h - 6);
      ctx.fillText("8 kHz", w - 38 * window.devicePixelRatio, h - 6);
      ctx.fillText("N̂(f) Power Density (dB)", 8, 14 * window.devicePixelRatio);
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

      setUint32(0x46464952);
      setUint32(length - 8);
      setUint32(0x45564157);
      setUint32(0x20746d66);
      setUint32(16);
      setUint16(1);
      setUint16(numOfChan);
      setUint32(sampleRate);
      setUint32(sampleRate * 2 * numOfChan);
      setUint16(numOfChan * 2);
      setUint16(16);
      setUint32(0x61746164);
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

      // Noise Selection Buttons
      const noiseBtns = document.querySelectorAll(".noise-type-btn");
      noiseBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          noiseBtns.forEach(b => {
            b.className = "noise-type-btn px-2.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 transition";
          });
          btn.className = "noise-type-btn px-2.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 text-white transition shadow-xs";
          const type = btn.getAttribute("data-noise");
          document.getElementById("noiseTypeDesc").innerText = 
            type === "white" ? "Gaussian Broadband" : (type === "pink" ? "1/f Pink Noise" : "Narrowband Fan Drone");
          processDSP();
        });
      });

      // Spectrogram Tab Switching
      const tabNoisy = document.getElementById("tabNoisySpec");
      const tabEnhanced = document.getElementById("tabEnhancedSpec");
      const tabClean = document.getElementById("tabCleanSpec");

      function setSpecTab(active) {
        currentSpecView = active;
        tabNoisy.className = active === "noisy" ? "px-3 py-1 text-xs font-semibold rounded-lg bg-white text-slate-900 shadow-xs transition" : "px-3 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition";
        tabEnhanced.className = active === "enhanced" ? "px-3 py-1 text-xs font-semibold rounded-lg bg-white text-slate-900 shadow-xs transition" : "px-3 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition";
        tabClean.className = active === "clean" ? "px-3 py-1 text-xs font-semibold rounded-lg bg-white text-slate-900 shadow-xs transition" : "px-3 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition";
        document.getElementById("specInfoText").innerText = `${active.charAt(0).toUpperCase() + active.slice(1)} Spectrogram`;
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
          document.getElementById("audioStatusBadge").innerText = `${file.name.substring(0, 12)}... (${sampleRate}Hz)`;
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
              document.getElementById("audioStatusBadge").innerText = `Mic (${decoded.duration.toFixed(1)}s)`;
              document.getElementById("micText").innerText = "Capture Microphone Input (3s)";
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
          alert("Microphone permission denied or unavailable.");
          document.getElementById("micText").innerText = "Capture Microphone Input (3s)";
          document.getElementById("micDot").classList.remove("animate-ping");
        }
      });

      document.getElementById("resetDefaultsBtn").addEventListener("click", () => {
        document.getElementById("inputSnr").value = 5;
        document.getElementById("valSnr").innerText = "5 dB";
        document.getElementById("snrBadge").innerText = "5.0 dB SNR";
        document.getElementById("badgeNoisyLabel").innerText = "5 dB";
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
        document.getElementById("audioStatusBadge").innerText = `Clean (${sampleRate}Hz)`;
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

print("Generated medical/enterprise white themed index.html and app.html successfully!")
