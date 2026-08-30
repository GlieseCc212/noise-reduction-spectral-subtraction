import os
import base64

with open("output/clean.wav", "rb") as f:
    b64_audio = base64.b64encode(f.read()).decode("utf-8")

html_template = """<!DOCTYPE html>
<html lang="en" class="h-full bg-white">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Intuitive DSP | Spectral Subtraction Acoustic Lab</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #ffffff;
      color: #202124;
    }
    .font-mono {
      font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    input[type=range] {
      -webkit-appearance: none;
      width: 100%;
      background: #e5e7eb;
      height: 6px;
      border-radius: 9999px;
      outline: none;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #1c23ba;
      cursor: pointer;
      box-shadow: 0 1px 3px rgba(0,0,0,0.25);
      border: 2px solid #ffffff;
      transition: transform 0.1s ease;
    }
    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.15);
      background: #0052cc;
    }
    .canvas-container {
      position: relative;
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 0.75rem;
      overflow: hidden;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
    }
  </style>
</head>
<body class="bg-white text-[#202124] min-h-full flex flex-col antialiased">

  <!-- Utility Header -->
  <div class="bg-[#f2f3f5] border-b border-[#e5e7eb] px-4 sm:px-8 py-1.5 text-xs text-[#55575c] flex justify-between items-center">
    <div class="flex items-center gap-4">
      <span class="font-medium tracking-tight">INTUITIVE AUDIO SURGICAL SYSTEMS</span>
      <span class="text-slate-300">|</span>
      <span>Acoustic Signal Processing Division</span>
    </div>
    <div class="flex items-center gap-4 text-[11px]">
      <span class="inline-flex items-center gap-1.5 text-emerald-700 font-medium">
        <span class="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span> DSP Engine Active (16 kHz)
      </span>
    </div>
  </div>

  <!-- Primary Navigation Bar -->
  <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-[#e5e7eb]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-[#1c23ba] text-white flex items-center justify-center font-bold text-lg shadow-sm">
          ◈
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-2">
            <span class="text-base font-bold tracking-tight text-[#202124]">INTUITIVE</span>
            <span class="text-sm font-light text-slate-400">/</span>
            <span class="text-sm font-semibold text-[#1c23ba]">Spectral Subtraction Lab</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-3">
        <button id="resetDefaultsBtn" class="px-4 py-1.5 text-xs font-semibold text-[#202124] bg-[#f2f3f5] hover:bg-[#e5e7eb] rounded-lg border border-[#d1d5db] transition shadow-2xs">
          Reset Defaults
        </button>
      </div>

    </div>
  </header>

  <!-- Hero Section -->
  <section class="border-b border-[#e5e7eb] bg-gradient-to-b from-[#fafbfc] to-white py-8 sm:py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-3">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-[#1c23ba] text-xs font-semibold border border-blue-200">
        Clinical Grade Digital Signal Processing
      </div>
      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#202124]">
        Spectral Subtraction Audio Enhancement
      </h1>
      <p class="text-sm sm:text-base text-[#55575c] max-w-3xl leading-relaxed">
        Real-time Short-Time Fourier Transform (STFT) speech enhancement and noise elimination platform. Adjust acoustic parameters, analyze time-frequency spectrograms, and isolate vocal formants with zero latency.
      </p>
    </div>
  </section>

  <!-- Main Interactive Lab Workspace -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 flex-1 w-full bg-white">

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <!-- Left Column: Precision Control Panel (4 cols) -->
      <div class="lg:col-span-4 space-y-6">

        <!-- 1. Audio Source Selection -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-5 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-[#f2f3f5] pb-3">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-[#1c23ba] text-white text-[11px] font-bold flex items-center justify-center">1</span>
              <h2 class="text-xs font-bold uppercase tracking-wider text-[#202124]">Acoustic Signal Source</h2>
            </div>
            <span id="audioStatusBadge" class="text-[11px] font-mono text-[#55575c] bg-[#f2f3f5] px-2 py-0.5 rounded border border-[#e5e7eb]">
              Default (16kHz)
            </span>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <button id="btnSourceDefault" class="px-3 py-2.5 text-xs font-semibold rounded-lg bg-[#1c23ba] hover:bg-[#0052cc] text-white transition shadow-xs flex items-center justify-center gap-1.5">
              <span>🎙️</span> Standard Voice
            </button>
            <label class="px-3 py-2.5 text-xs font-semibold rounded-lg bg-white hover:bg-[#f8f9fa] text-[#202124] border border-[#d1d5db] transition cursor-pointer flex items-center justify-center gap-1.5 text-center shadow-xs">
              <span>📁</span> Upload WAV
              <input type="file" id="audioFileInput" accept="audio/*" class="hidden">
            </label>
          </div>

          <button id="btnRecordMic" class="w-full px-3 py-2.5 text-xs font-semibold rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-800 border border-rose-200 transition flex items-center justify-center gap-2">
            <span id="micDot" class="w-2 h-2 rounded-full bg-rose-600"></span>
            <span id="micText">Capture Microphone Audio (3s)</span>
          </button>
        </div>

        <!-- 2. Additive Noise Model -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-5 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-[#f2f3f5] pb-3">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-[#1c23ba] text-white text-[11px] font-bold flex items-center justify-center">2</span>
              <h2 class="text-xs font-bold uppercase tracking-wider text-[#202124]">Additive Noise Model</h2>
            </div>
            <span id="snrBadge" class="text-xs font-mono font-semibold text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
              5.0 dB SNR
            </span>
          </div>

          <!-- Noise Profile Selector -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-[#55575c] flex justify-between">
              <span>Noise Profile</span>
              <span id="noiseTypeDesc" class="text-slate-400 text-[11px]">Gaussian Broadband</span>
            </label>
            <div class="grid grid-cols-3 gap-1.5">
              <button id="btnNoiseWhite" data-noise="white" class="noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#202124] text-white transition shadow-xs">White</button>
              <button id="btnNoisePink" data-noise="pink" class="noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#f2f3f5] hover:bg-[#e5e7eb] text-[#202124] border border-[#e5e7eb] transition">Pink (1/f)</button>
              <button id="btnNoiseFan" data-noise="fan" class="noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#f2f3f5] hover:bg-[#e5e7eb] text-[#202124] border border-[#e5e7eb] transition">Fan Hum</button>
            </div>
          </div>

          <!-- SNR Slider -->
          <div class="space-y-2 pt-1">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[#202124]">Signal-to-Noise Ratio (SNR)</span>
              <span id="valSnr" class="font-mono font-semibold text-[#202124] bg-[#f2f3f5] px-2 py-0.5 rounded border border-[#e5e7eb]">5 dB</span>
            </div>
            <input type="range" id="inputSnr" min="-10" max="25" step="1" value="5" class="w-full">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>-10 dB (Heavy Noise)</span>
              <span>0 dB</span>
              <span>+25 dB (Mild)</span>
            </div>
          </div>
        </div>

        <!-- 3. Spectral Subtraction Parameters -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-5 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-[#f2f3f5] pb-3">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-[#1c23ba] text-white text-[11px] font-bold flex items-center justify-center">3</span>
              <h2 class="text-xs font-bold uppercase tracking-wider text-[#202124]">DSP Subtraction Filter</h2>
            </div>
            <span class="text-[11px] font-mono text-[#1c23ba] bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              Live ISTFT
            </span>
          </div>

          <!-- Over-subtraction Alpha Slider -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[#202124]">Over-Subtraction Factor (&alpha;)</span>
              <span id="valAlpha" class="font-mono font-semibold text-[#1c23ba] bg-blue-50 px-2 py-0.5 rounded border border-blue-200">1.00</span>
            </div>
            <input type="range" id="inputAlpha" min="0.0" max="3.5" step="0.05" value="1.0" class="w-full">
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
                <span class="font-medium text-[#202124]">Spectral Floor (&beta;)</span>
                <span class="text-[10px] text-slate-400 block">Suppresses metallic musical noise</span>
              </div>
              <span id="valBeta" class="font-mono font-semibold text-[#202124] bg-[#f2f3f5] px-2 py-0.5 rounded border border-[#e5e7eb]">0.000</span>
            </div>
            <input type="range" id="inputBeta" min="0.00" max="0.15" step="0.005" value="0.00" class="w-full">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>0.00 (Hard Max)</span>
              <span>0.02 (Recommended)</span>
              <span>0.15 (Soft Floor)</span>
            </div>
          </div>

          <!-- Noise Lead-in Duration -->
          <div class="space-y-1.5 pt-1">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[#202124]">Noise Estimation Lead-in</span>
              <span id="valNoiseDuration" class="font-mono font-semibold text-[#202124] bg-[#f2f3f5] px-2 py-0.5 rounded border border-[#e5e7eb]">0.50 s</span>
            </div>
            <input type="range" id="inputNoiseDuration" min="0.1" max="1.5" step="0.05" value="0.5" class="w-full">
            <span class="text-[10px] text-slate-400 block">Initial quiet window used to compute N̂(f)</span>
          </div>

          <!-- STFT Parameters -->
          <div class="pt-3 border-t border-[#f2f3f5] grid grid-cols-2 gap-3">
            <div>
              <label class="text-[11px] font-semibold text-[#55575c] block mb-1">STFT Window</label>
              <select id="selectNfft" class="w-full bg-[#f8f9fa] border border-[#d1d5db] text-xs rounded-lg p-2 text-[#202124] font-medium focus:ring-1 focus:ring-[#1c23ba]">
                <option value="256">256 (16 ms)</option>
                <option value="512" selected>512 (32 ms - Optimal)</option>
                <option value="1024">1024 (64 ms)</option>
              </select>
            </div>
            <div>
              <label class="text-[11px] font-semibold text-[#55575c] block mb-1">Frame Overlap</label>
              <select id="selectOverlap" class="w-full bg-[#f8f9fa] border border-[#d1d5db] text-xs rounded-lg p-2 text-[#202124] font-medium focus:ring-1 focus:ring-[#1c23ba]">
                <option value="0.50">50% Overlap</option>
                <option value="0.75" selected>75% Overlap</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 4. Diagnostic Metrics -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-5 shadow-xs space-y-3">
          <h3 class="text-xs font-bold uppercase tracking-wider text-[#55575c]">DSP Real-Time Telemetry</h3>
          <div class="grid grid-cols-3 gap-3 text-center">
            <div class="p-3 rounded-lg bg-[#fafbfc] border border-[#e5e7eb]">
              <div class="text-[10px] font-medium text-[#55575c] uppercase">Input SNR</div>
              <div id="statInputSnr" class="text-sm font-bold font-mono text-amber-700 mt-0.5">5.0 dB</div>
            </div>
            <div class="p-3 rounded-lg bg-[#fafbfc] border border-[#e5e7eb]">
              <div class="text-[10px] font-medium text-[#55575c] uppercase">Est. Gain</div>
              <div id="statSnrGain" class="text-sm font-bold font-mono text-emerald-700 mt-0.5">+8.4 dB</div>
            </div>
            <div class="p-3 rounded-lg bg-[#fafbfc] border border-[#e5e7eb]">
              <div class="text-[10px] font-medium text-[#55575c] uppercase">Latency</div>
              <div id="statLatency" class="text-sm font-bold font-mono text-[#1c23ba] mt-0.5">12 ms</div>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Visualizations & Audio Evaluation (8 cols) -->
      <div class="lg:col-span-8 space-y-6">

        <!-- Listening Evaluation Section -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-6 shadow-xs space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#f2f3f5] pb-4">
            <div>
              <h2 class="text-sm font-bold uppercase tracking-wider text-[#202124] flex items-center gap-2">
                <span>🎧</span> Acoustic Evaluation Station
              </h2>
              <p class="text-xs text-[#55575c]">Compare Clean Reference, Noisy Mixture, and Enhanced Speech</p>
            </div>
            <button id="btnDownloadEnhanced" class="px-4 py-2 text-xs font-semibold rounded-lg bg-[#202124] hover:bg-black text-white transition shadow-xs flex items-center gap-2 self-start sm:self-auto">
              <span>⬇️</span> Download Enhanced WAV
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <!-- Clean Audio Player -->
            <div class="p-4 rounded-xl bg-[#fafbfc] border border-[#e5e7eb] space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-emerald-800 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-600"></span> Clean Reference
                </span>
                <span class="text-[10px] font-mono text-slate-400">Target</span>
              </div>
              <button id="btnPlayClean" class="w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 transition flex items-center justify-center gap-2">
                <span>▶</span> <span>Play Clean</span>
              </button>
            </div>

            <!-- Noisy Audio Player -->
            <div class="p-4 rounded-xl bg-[#fafbfc] border border-[#e5e7eb] space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-900 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-amber-600"></span> Noisy Speech
                </span>
                <span id="badgeNoisyLabel" class="text-[10px] font-mono text-amber-800 font-semibold bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">5 dB</span>
              </div>
              <button id="btnPlayNoisy" class="w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-950 border border-amber-300 transition flex items-center justify-center gap-2">
                <span>▶</span> <span>Play Noisy</span>
              </button>
            </div>

            <!-- Enhanced Audio Player -->
            <div class="p-4 rounded-xl bg-blue-50/60 border border-blue-200 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-[#1c23ba] flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-[#1c23ba]"></span> Enhanced Output
                </span>
                <span id="badgeAlphaLabel" class="text-[10px] font-mono text-[#1c23ba] font-semibold bg-white px-1.5 py-0.5 rounded border border-blue-200">&alpha;=1.00</span>
              </div>
              <button id="btnPlayEnhanced" class="w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-[#1c23ba] hover:bg-[#0052cc] text-white shadow-xs transition flex items-center justify-center gap-2">
                <span>▶</span> <span>Play Enhanced</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Waveforms Section -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-[#f2f3f5] pb-3">
            <h2 class="text-xs font-bold uppercase tracking-wider text-[#202124] flex items-center gap-2">
              <span>📈</span> Time-Domain Waveform Analysis
            </h2>
            <div class="flex items-center gap-4 text-xs font-medium">
              <span class="flex items-center gap-1.5 text-emerald-800"><span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span> Clean</span>
              <span class="flex items-center gap-1.5 text-amber-800"><span class="w-2.5 h-2.5 rounded-full bg-amber-600"></span> Noisy</span>
              <span class="flex items-center gap-1.5 text-[#1c23ba]"><span class="w-2.5 h-2.5 rounded-full bg-[#1c23ba]"></span> Enhanced</span>
            </div>
          </div>

          <div class="canvas-container h-48 w-full" style="height: 190px;">
            <canvas id="waveformCanvas"></canvas>
          </div>
        </div>

        <!-- Spectrograms Section -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-6 shadow-xs space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#f2f3f5] pb-3">
            <div>
              <h2 class="text-xs font-bold uppercase tracking-wider text-[#202124] flex items-center gap-2">
                <span>🌌</span> Time-Frequency Spectrogram Heatmaps
              </h2>
              <span class="text-[11px] text-slate-400">STFT Spectral Energy Distribution (0 Hz – 8 kHz)</span>
            </div>
            <div class="flex items-center gap-1 bg-[#f2f3f5] p-1 rounded-lg border border-[#e5e7eb]">
              <button id="tabNoisySpec" class="spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md text-[#55575c] hover:text-[#202124] transition">
                Noisy
              </button>
              <button id="tabEnhancedSpec" class="spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md bg-white text-[#1c23ba] shadow-2xs transition">
                Enhanced
              </button>
              <button id="tabCleanSpec" class="spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md text-[#55575c] hover:text-[#202124] transition">
                Clean
              </button>
            </div>
          </div>

          <div class="canvas-container h-64 w-full" style="height: 256px;">
            <canvas id="spectrogramCanvas"></canvas>
          </div>

          <!-- Colorbar & Information -->
          <div class="flex items-center justify-between text-[11px] text-[#55575c] px-1">
            <div class="flex items-center gap-2">
              <span class="font-mono">-60 dB</span>
              <div class="w-28 h-2 rounded-full bg-gradient-to-r from-[#101827] via-[#7c3aed] via-[#f43f5e] to-[#fef08a]"></div>
              <span class="font-mono">0 dB</span>
            </div>
            <div id="specInfoText" class="font-mono font-semibold text-[#1c23ba]">
              Enhanced Spectrogram (&alpha; = 1.0)
            </div>
          </div>
        </div>

        <!-- Estimated Noise Profile Section -->
        <div class="bg-white rounded-xl border border-[#e5e7eb] p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-[#f2f3f5] pb-3">
            <div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-[#202124] flex items-center gap-2">
                <span>📊</span> Estimated Noise Spectrum N̂(f)
              </h3>
              <p class="text-[11px] text-slate-400">Magnitude profile extracted from initial silence lead-in</p>
            </div>
            <span class="text-[11px] text-[#1c23ba] bg-blue-50 font-mono font-medium px-2 py-0.5 rounded border border-blue-200">
              Averaged Spectrum
            </span>
          </div>
          <div class="canvas-container h-36 w-full" style="height: 144px;">
            <canvas id="noiseProfileCanvas"></canvas>
          </div>
        </div>

      </div>

    </div>

    <!-- Engineering Principles Footer -->
    <footer class="bg-[#fafbfc] rounded-xl border border-[#e5e7eb] p-6 space-y-4 text-xs text-[#55575c]">
      <div class="flex items-center gap-2 text-[#202124] font-bold text-sm">
        <span>💡</span> Engineering Insights & Signal Principles
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-[12px] leading-relaxed">
        <div class="space-y-1.5 p-4 rounded-lg bg-white border border-[#e5e7eb]">
          <span class="font-bold text-[#202124]">1. Broadband vs Narrowband Attenuation</span>
          <p class="text-[#55575c]">White noise presents a uniform broadband floor. Periodic drone noise concentrates energy in low harmonics (120Hz, 240Hz), where subtraction eliminates hum with surgical precision.</p>
        </div>
        <div class="space-y-1.5 p-4 rounded-lg bg-white border border-[#e5e7eb]">
          <span class="font-bold text-[#202124]">2. Over-Subtraction Factor (&alpha;) Trade-off</span>
          <p class="text-[#55575c]">Higher &alpha; completely cancels residual noise in speech pauses, but causes isolated spectral valleys. A balanced factor &alpha; &approx; 1.0 preserves natural speech formants.</p>
        </div>
        <div class="space-y-1.5 p-4 rounded-lg bg-white border border-[#e5e7eb]">
          <span class="font-bold text-[#202124]">3. Spectral Floor (&beta;) Artifact Control</span>
          <p class="text-[#55575c]">Setting a small spectral floor (&beta; &approx; 0.02) prevents random STFT bins from dropping to zero, converting irritating musical ringing chirps into a soft, unobtrusive background floor.</p>
        </div>
      </div>
    </footer>

  </main>

  <!-- JavaScript DSP Engine -->
  <script>
    const DEFAULT_AUDIO_B64 = "___BASE64_AUDIO_PLACEHOLDER___";

    let audioCtx = null;
    let rawCleanAudio = null; // Float32Array
    let cleanBuffer = null;
    let noisyBuffer = null;
    let enhancedBuffer = null;
    let sampleRate = 16000;
    
    let activeSourceNode = null;
    let activePlayingType = null;

    let currentNoiseType = "white";
    let currentSpecView = "enhanced";

    let stftCache = {
      clean: null,
      noisy: null,
      enhanced: null,
      noiseProfile: null,
      numBins: 0,
      numFrames: 0,
      duration: 0,
      cleanSig: null,
      noisySig: null,
      enhancedSig: null
    };

    function parseWav(arrayBuffer) {
      const view = new DataView(arrayBuffer);
      let pos = 12;
      let fs = 16000;
      let channels = 1;
      while (pos < view.byteLength - 8) {
        const id = String.fromCharCode(view.getUint8(pos), view.getUint8(pos+1), view.getUint8(pos+2), view.getUint8(pos+3));
        const size = view.getUint32(pos + 4, true);
        if (id === "fmt ") {
          channels = view.getUint16(pos + 10, true);
          fs = view.getUint32(pos + 12, true);
        } else if (id === "data") {
          const numSamples = Math.floor(size / (2 * channels));
          const samples = new Float32Array(numSamples);
          const dataOffset = pos + 8;
          for (let i = 0; i < numSamples; i++) {
            let sum = 0;
            for (let ch = 0; ch < channels; ch++) {
              sum += view.getInt16(dataOffset + (i * channels + ch) * 2, true) / 32768.0;
            }
            samples[i] = sum / channels;
          }
          return { samples, sampleRate: fs };
        }
        pos += 8 + size;
      }
      return null;
    }

    function fft(re, im, inverse) {
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

    function getCanvasDimensions(canvas) {
      const dpr = window.devicePixelRatio || 1;
      const w = Math.max(300, Math.floor(canvas.offsetWidth * dpr));
      const h = Math.max(80, Math.floor(canvas.offsetHeight * dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
      return { w, h, dpr };
    }

    function processDSP() {
      if (!rawCleanAudio) return;
      const startTime = performance.now();

      const targetSnrDb = parseFloat(document.getElementById("inputSnr").value);
      const alpha = parseFloat(document.getElementById("inputAlpha").value);
      const beta = parseFloat(document.getElementById("inputBeta").value);
      const noiseDuration = parseFloat(document.getElementById("inputNoiseDuration").value);
      const nfft = parseInt(document.getElementById("selectNfft").value);
      const overlapRatio = parseFloat(document.getElementById("selectOverlap").value);
      const hop = Math.round(nfft * (1 - overlapRatio));
      
      const noiseType = currentNoiseType || "white";

      const leadInSamples = Math.round(noiseDuration * sampleRate);
      const totalLen = rawCleanAudio.length + leadInSamples;
      
      const cleanPadded = new Float32Array(totalLen);
      cleanPadded.set(rawCleanAudio, leadInSamples);

      let rawNoise = generateNoise(totalLen, noiseType, sampleRate);
      
      let speechEnergy = 0;
      for (let i = 0; i < rawCleanAudio.length; i++) speechEnergy += rawCleanAudio[i] * rawCleanAudio[i];
      const speechPower = speechEnergy / rawCleanAudio.length;

      let noiseEnergy = 0;
      for (let i = 0; i < totalLen; i++) noiseEnergy += rawNoise[i] * rawNoise[i];
      const noisePower = noiseEnergy / totalLen;

      const desiredNoisePower = speechPower / Math.pow(10, targetSnrDb / 10);
      const noiseScale = Math.sqrt(desiredNoisePower / (noisePower + 1e-12));
      
      const scaledNoise = new Float32Array(totalLen);
      for (let i = 0; i < totalLen; i++) scaledNoise[i] = rawNoise[i] * noiseScale;

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

    function createAudioBufferFromData(data) {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const buf = audioCtx.createBuffer(1, data.length, sampleRate);
      buf.getChannelData(0).set(data);
      return buf;
    }

    function playAudio(type) {
      if (!stftCache) return;
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

      let data = null;
      if (type === "clean") data = stftCache.cleanSig;
      else if (type === "noisy") data = stftCache.noisySig;
      else if (type === "enhanced") data = stftCache.enhancedSig;

      if (!data) return;

      const buffer = createAudioBufferFromData(data);
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

      btnClean.className = activePlayingType === "clean" ? "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-rose-600 text-white shadow-xs transition flex items-center justify-center gap-2" : "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 transition flex items-center justify-center gap-2";
      btnNoisy.className = activePlayingType === "noisy" ? "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-rose-600 text-white shadow-xs transition flex items-center justify-center gap-2" : "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-950 border border-amber-300 transition flex items-center justify-center gap-2";
      btnEnhanced.className = activePlayingType === "enhanced" ? "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-rose-600 text-white shadow-xs transition flex items-center justify-center gap-2" : "w-full py-2.5 px-3 text-xs font-semibold rounded-lg bg-[#1c23ba] hover:bg-[#0052cc] text-white shadow-xs transition flex items-center justify-center gap-2";
    }

    function drawWaveforms() {
      const canvas = document.getElementById("waveformCanvas");
      if (!canvas) return;
      const { w, h, dpr } = getCanvasDimensions(canvas);
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, w, h);

      ctx.fillStyle = "#fafbfc";
      ctx.fillRect(0, 0, w, h);

      ctx.strokeStyle = "#e5e7eb";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let y = 0.333; y < 1; y += 0.333) {
        ctx.moveTo(0, Math.floor(h * y));
        ctx.lineTo(w, Math.floor(h * y));
      }
      ctx.stroke();

      if (!stftCache || !stftCache.cleanSig) return;

      const clean = stftCache.cleanSig;
      const noisy = stftCache.noisySig;
      const enhanced = stftCache.enhancedSig;

      drawWaveLane(ctx, clean, 0, h * 0.333, "#059669", "Clean Speech", w, dpr);
      drawWaveLane(ctx, noisy, h * 0.333, h * 0.333, "#d97706", "Noisy Speech (5 dB)", w, dpr);
      drawWaveLane(ctx, enhanced, h * 0.666, h * 0.333, "#1c23ba", "Enhanced Output", w, dpr);
    }

    function drawWaveLane(ctx, data, top, height, color, label, w, dpr) {
      const mid = top + height / 2;
      const amp = height * 0.42;
      const len = data.length;
      if (len === 0) return;

      ctx.strokeStyle = "#e5e7eb";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, mid);
      ctx.lineTo(w, mid);
      ctx.stroke();

      ctx.strokeStyle = color;
      ctx.lineWidth = Math.max(1, 1.2 * dpr);
      ctx.beginPath();

      const step = Math.max(1, len / w);
      for (let x = 0; x < w; x++) {
        const startIdx = Math.floor(x * step);
        const endIdx = Math.min(len, Math.floor((x + 1) * step));
        let max = -1, min = 1;
        for (let i = startIdx; i < endIdx; i++) {
          const v = data[i];
          if (v > max) max = v;
          if (v < min) min = v;
        }
        if (min > max) { min = 0; max = 0; }
        const yTop = mid - Math.max(Math.abs(max) * amp, 1.5);
        const yBot = mid + Math.max(Math.abs(min) * amp, 1.5);
        ctx.moveTo(x, yTop);
        ctx.lineTo(x, yBot);
      }
      ctx.stroke();

      ctx.fillStyle = color;
      ctx.font = `bold ${Math.round(9 * dpr)}px 'JetBrains Mono', monospace`;
      ctx.fillText(label, 10 * dpr, top + 13 * dpr);
    }

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
      if (!canvas) return;
      const { w, h, dpr } = getCanvasDimensions(canvas);
      const ctx = canvas.getContext("2d");

      const magData = stftCache[currentSpecView];
      if (!magData || magData.length === 0) {
        ctx.fillStyle = "#fafbfc";
        ctx.fillRect(0, 0, w, h);
        return;
      }

      const numFrames = magData.length;
      const numBins = magData[0].length;

      const offscreen = document.createElement("canvas");
      offscreen.width = numFrames;
      offscreen.height = numBins;
      const offCtx = offscreen.getContext("2d");
      const imgData = offCtx.createImageData(numFrames, numBins);
      const data = imgData.data;

      const minDb = -60;
      const maxDb = 10;
      const dbRange = maxDb - minDb;

      for (let y = 0; y < numBins; y++) {
        const binIdx = numBins - 1 - y;
        for (let x = 0; x < numFrames; x++) {
          const mag = magData[x][binIdx];
          const db = 20 * Math.log10(mag + 1e-6);
          const norm = Math.max(0, Math.min(1, (db - minDb) / dbRange));
          const [r, g, b] = clinicalColormap(norm);
          const pixelIdx = (y * numFrames + x) * 4;
          data[pixelIdx] = r;
          data[pixelIdx + 1] = g;
          data[pixelIdx + 2] = b;
          data[pixelIdx + 3] = 255;
        }
      }

      offCtx.putImageData(imgData, 0, 0);

      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(offscreen, 0, 0, w, h);

      // HUD Overlay
      ctx.fillStyle = "rgba(255, 255, 255, 0.95)";
      ctx.font = `bold ${Math.round(10 * dpr)}px 'JetBrains Mono', monospace`;
      ctx.fillText("8.0 kHz", 12 * dpr, 16 * dpr);
      ctx.fillText("4.0 kHz", 12 * dpr, Math.floor(h * 0.5));
      ctx.fillText("0.0 Hz", 12 * dpr, h - 8 * dpr);
      ctx.fillText(`${(stftCache.duration || 0).toFixed(1)} s`, w - 48 * dpr, h - 8 * dpr);
    }

    function drawNoiseProfile() {
      const canvas = document.getElementById("noiseProfileCanvas");
      if (!canvas) return;
      const { w, h, dpr } = getCanvasDimensions(canvas);
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, w, h);

      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, w, h);

      ctx.strokeStyle = "#e5e7eb";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let y = 0.25; y < 1; y += 0.25) {
        ctx.moveTo(0, Math.floor(h * y));
        ctx.lineTo(w, Math.floor(h * y));
      }
      ctx.stroke();

      if (!stftCache || !stftCache.noiseProfile) return;

      const profile = stftCache.noiseProfile;
      const numBins = profile.length;
      const minDb = -50, maxDb = 10;

      ctx.strokeStyle = "#1c23ba";
      ctx.lineWidth = 2 * dpr;
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

      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fillStyle = "rgba(28, 35, 186, 0.08)";
      ctx.fill();

      ctx.fillStyle = "#55575c";
      ctx.font = `${Math.round(9 * dpr)}px 'JetBrains Mono', monospace`;
      ctx.fillText("0 Hz", 8 * dpr, h - 6 * dpr);
      ctx.fillText("4 kHz", Math.floor(w * 0.5 - 15 * dpr), h - 6 * dpr);
      ctx.fillText("8 kHz", w - 40 * dpr, h - 6 * dpr);
      ctx.fillText("N̂(f) Spectral Magnitude (dB)", 8 * dpr, 14 * dpr);
    }

    function exportWav(data) {
      const numOfChan = 1;
      const length = data.length * numOfChan * 2 + 44;
      const outBuffer = new ArrayBuffer(length);
      const view = new DataView(outBuffer);
      let pos = 0;

      function setUint16(val) { view.setUint16(pos, val, true); pos += 2; }
      function setUint32(val) { view.setUint32(pos, val, true); pos += 4; }

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

      for (let i = 0; i < data.length; i++) {
        let s = Math.max(-1, Math.min(1, data[i]));
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

    function updateNoiseButtonsUI() {
      const btnWhite = document.getElementById("btnNoiseWhite");
      const btnPink = document.getElementById("btnNoisePink");
      const btnFan = document.getElementById("btnNoiseFan");

      btnWhite.className = currentNoiseType === "white" ? "noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#202124] text-white transition shadow-xs" : "noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#f2f3f5] hover:bg-[#e5e7eb] text-[#202124] border border-[#e5e7eb] transition";
      btnPink.className = currentNoiseType === "pink" ? "noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#202124] text-white transition shadow-xs" : "noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#f2f3f5] hover:bg-[#e5e7eb] text-[#202124] border border-[#e5e7eb] transition";
      btnFan.className = currentNoiseType === "fan" ? "noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#202124] text-white transition shadow-xs" : "noise-btn px-2.5 py-2 text-xs font-semibold rounded-lg bg-[#f2f3f5] hover:bg-[#e5e7eb] text-[#202124] border border-[#e5e7eb] transition";

      document.getElementById("noiseTypeDesc").innerText = 
        currentNoiseType === "white" ? "Gaussian Broadband" : (currentNoiseType === "pink" ? "1/f Pink Noise" : "Narrowband Fan Hum");
    }

    function updateSpecTabsUI() {
      const tabNoisy = document.getElementById("tabNoisySpec");
      const tabEnhanced = document.getElementById("tabEnhancedSpec");
      const tabClean = document.getElementById("tabCleanSpec");

      tabNoisy.className = currentSpecView === "noisy" ? "spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md bg-white text-[#1c23ba] shadow-2xs transition" : "spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md text-[#55575c] hover:text-[#202124] transition";
      tabEnhanced.className = currentSpecView === "enhanced" ? "spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md bg-white text-[#1c23ba] shadow-2xs transition" : "spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md text-[#55575c] hover:text-[#202124] transition";
      tabClean.className = currentSpecView === "clean" ? "spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md bg-white text-[#1c23ba] shadow-2xs transition" : "spec-tab-btn px-3 py-1 text-xs font-semibold rounded-md text-[#55575c] hover:text-[#202124] transition";

      document.getElementById("specInfoText").innerText = `${currentSpecView.charAt(0).toUpperCase() + currentSpecView.slice(1)} Spectrogram`;
    }

    function setupUI() {
      let debounceTimer = null;
      function triggerUpdate() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(processDSP, 25);
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

      document.getElementById("btnNoiseWhite").addEventListener("click", () => { currentNoiseType = "white"; updateNoiseButtonsUI(); processDSP(); });
      document.getElementById("btnNoisePink").addEventListener("click", () => { currentNoiseType = "pink"; updateNoiseButtonsUI(); processDSP(); });
      document.getElementById("btnNoiseFan").addEventListener("click", () => { currentNoiseType = "fan"; updateNoiseButtonsUI(); processDSP(); });

      document.getElementById("tabNoisySpec").addEventListener("click", () => { currentSpecView = "noisy"; updateSpecTabsUI(); drawSpectrogram(); });
      document.getElementById("tabEnhancedSpec").addEventListener("click", () => { currentSpecView = "enhanced"; updateSpecTabsUI(); drawSpectrogram(); });
      document.getElementById("tabCleanSpec").addEventListener("click", () => { currentSpecView = "clean"; updateSpecTabsUI(); drawSpectrogram(); });

      document.getElementById("btnPlayClean").addEventListener("click", () => playAudio("clean"));
      document.getElementById("btnPlayNoisy").addEventListener("click", () => playAudio("noisy"));
      document.getElementById("btnPlayEnhanced").addEventListener("click", () => playAudio("enhanced"));

      document.getElementById("btnDownloadEnhanced").addEventListener("click", () => {
        if (stftCache && stftCache.enhancedSig) exportWav(stftCache.enhancedSig);
      });

      const fileInput = document.getElementById("audioFileInput");
      fileInput.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const arrayBuf = await file.arrayBuffer();
        const parsed = parseWav(arrayBuf);
        if (parsed) {
          rawCleanAudio = parsed.samples;
          sampleRate = parsed.sampleRate;
          document.getElementById("audioStatusBadge").innerText = `${file.name.substring(0, 12)}... (${sampleRate}Hz)`;
          processDSP();
        } else {
          if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          audioCtx.decodeAudioData(arrayBuf, (decoded) => {
            rawCleanAudio = decoded.getChannelData(0);
            sampleRate = decoded.sampleRate;
            document.getElementById("audioStatusBadge").innerText = `${file.name.substring(0, 12)}... (${sampleRate}Hz)`;
            processDSP();
          });
        }
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
              rawCleanAudio = decoded.getChannelData(0);
              sampleRate = decoded.sampleRate;
              document.getElementById("audioStatusBadge").innerText = `Mic (${decoded.duration.toFixed(1)}s)`;
              document.getElementById("micText").innerText = "Capture Microphone Audio (3s)";
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
          document.getElementById("micText").innerText = "Capture Microphone Audio (3s)";
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
        currentNoiseType = "white";
        currentSpecView = "enhanced";
        updateNoiseButtonsUI();
        updateSpecTabsUI();
        loadDefaultAudio();
      });

      window.addEventListener("resize", () => {
        drawWaveforms();
        drawSpectrogram();
        drawNoiseProfile();
      });
    }

    function loadDefaultAudio() {
      try {
        const arrayBuf = base64ToArrayBuffer(DEFAULT_AUDIO_B64);
        const parsed = parseWav(arrayBuf);
        if (parsed) {
          rawCleanAudio = parsed.samples;
          sampleRate = parsed.sampleRate;
          document.getElementById("audioStatusBadge").innerText = `Standard Voice (${sampleRate}Hz)`;
          processDSP();
        }
      } catch (err) {
        console.error("WAV decode error:", err);
      }
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

print("Rebuilt with synchronous zero-dependency WAV decoder and instant rendering!")
