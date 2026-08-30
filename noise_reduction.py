import os
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import stft, istft

def add_noise_at_snr(signal, snr_db):
    """
    Add zero-mean Gaussian white noise to a signal to achieve a target SNR in dB.
    """
    signal_power = np.mean(signal ** 2)
    noise = np.random.randn(len(signal))
    noise_power = np.mean(noise ** 2)
    desired_noise_power = signal_power / (10 ** (snr_db / 10))
    noise = noise * np.sqrt(desired_noise_power / noise_power)
    noisy = signal + noise
    return noisy, noise

def spectral_subtraction(noisy_signal, fs, noise_duration_sec=0.5, alpha=1.0, beta=0.0):
    """
    Apply Spectral Subtraction noise reduction.
    
    Parameters:
    - noisy_signal: 1D numpy array of noisy audio
    - fs: sample rate (Hz)
    - noise_duration_sec: duration of initial silence/noise-only section (seconds)
    - alpha: over-subtraction factor
    - beta: spectral floor factor
    """
    # STFT parameters: 25 ms window, 10 ms hop (60% overlap)
    nperseg = int(0.025 * fs)
    hop = int(0.010 * fs)
    noverlap = nperseg - hop

    # 1. Compute STFT of the entire noisy signal
    f, t, Zxx = stft(
        noisy_signal,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap
    )
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    # 2. Estimate noise spectrum from initial noise-only frames
    noise_only_samples = int(noise_duration_sec * fs)
    noise_only = noisy_signal[:noise_only_samples]
    _, _, Z_noise = stft(
        noise_only,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap
    )
    noise_mag = np.mean(np.abs(Z_noise), axis=1, keepdims=True)

    # 3. Spectral Subtraction with spectral floor
    clean_mag = magnitude - alpha * noise_mag
    # Apply spectral floor (beta * noise_mag) to mitigate musical noise
    floor = beta * noise_mag
    clean_mag = np.maximum(clean_mag, floor)

    # 4. Reconstruct complex spectrum using original noisy phase
    Z_clean = clean_mag * np.exp(1j * phase)

    # 5. Inverse STFT to get enhanced time-domain signal
    _, enhanced = istft(
        Z_clean,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap
    )
    
    # Match length with input signal
    if len(enhanced) > len(noisy_signal):
        enhanced = enhanced[:len(noisy_signal)]
    elif len(enhanced) < len(noisy_signal):
        enhanced = np.pad(enhanced, (0, len(noisy_signal) - len(enhanced)))

    return enhanced, f, t, Zxx, magnitude, phase, noise_mag, Z_clean

def run_experiment():
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    print("==================================================")
    print("Lesson 14: Spectral Subtraction in Python")
    print("==================================================")

    # Step 3: Load audio
    print("\n--- Step 3: Load the Audio ---")
    audio, fs = sf.read("clean.wav")
    print("Sample rate (fs):", fs)
    print("Raw audio shape:", audio.shape)
    print("Total samples:", len(audio))
    print(f"Duration: {len(audio) / fs:.2f} seconds")

    # Step 4: Mono vs Stereo
    print("\n--- Step 4: Mono Conversion ---")
    if audio.ndim > 1:
        print("Stereo detected! Converting to Mono by averaging channels...")
        audio = np.mean(audio, axis=1)
    else:
        print("Audio is already mono.")
    print("Mono audio shape:", audio.shape)

    # Step 5: Normalize carefully
    print("\n--- Step 5: Normalization ---")
    audio = audio / (np.max(np.abs(audio)) + 1e-8)
    print(f"Signal amplitude range: [{np.min(audio):.4f}, {np.max(audio):.4f}]")

    # Save normalized clean audio
    sf.write("output/clean.wav", audio, fs)
    print("Saved output/clean.wav")

    # Add 0.5s of silence at the beginning to have a clean noise estimation period
    silence_prefix = np.zeros(int(0.5 * fs))
    audio_with_silence = np.concatenate([silence_prefix, audio])
    
    # Step 6 & 7: Add Artificial Noise (5 dB SNR)
    print("\n--- Step 6 & 7: Add White Noise at 5 dB SNR ---")
    snr_target = 5.0  # dB
    noisy, noise = add_noise_at_snr(audio_with_silence, snr_target)
    
    # Calculate measured SNR
    sig_p = np.mean(audio_with_silence ** 2)
    noise_p = np.mean(noise ** 2)
    measured_snr = 10 * np.log10(sig_p / noise_p)
    print(f"Target SNR: {snr_target} dB, Measured SNR: {measured_snr:.2f} dB")

    # Save noisy signal
    sf.write("output/noisy.wav", noisy, fs)
    print("Saved output/noisy.wav")

    # Step 8: Visualize Clean vs Noisy Waveforms
    print("\n--- Step 8: Visualize Clean vs Noisy Waveforms ---")
    time_axis = np.arange(len(audio_with_silence)) / fs
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, audio_with_silence, color='#2b5c8f', lw=0.8)
    plt.title("Clean Speech (with 0.5s initial lead-in)", fontsize=12, fontweight='bold')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)

    plt.subplot(2, 1, 2)
    plt.plot(time_axis, noisy, color='#d95f02', lw=0.8)
    plt.title(f"Noisy Speech (5 dB SNR White Noise)", fontsize=12, fontweight='bold')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig("output/step8_clean_vs_noisy_waveform.png", dpi=150)
    plt.close()
    print("Saved output/step8_clean_vs_noisy_waveform.png")

    # Step 9 & 10: Calculate STFT
    print("\n--- Step 9 & 10: STFT Analysis ---")
    nperseg = int(0.025 * fs)  # 25 ms = 400 samples at 16kHz
    hop = int(0.010 * fs)      # 10 ms = 160 samples at 16kHz
    noverlap = nperseg - hop   # 240 samples (60% overlap)
    print(f"Window length (nperseg): {nperseg} samples ({nperseg/fs*1000:.1f} ms)")
    print(f"Hop size: {hop} samples ({hop/fs*1000:.1f} ms)")
    print(f"Overlap (noverlap): {noverlap} samples ({noverlap/nperseg*100:.0f}% overlap)")

    f, t, Zxx = stft(
        noisy,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap
    )

    # Step 11: Extract Magnitude and Phase
    print("\n--- Step 11: Extract Magnitude and Phase ---")
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)
    print(f"STFT shape: {Zxx.shape} (Frequencies: {len(f)}, Time frames: {len(t)})")
    print(f"Frequency range: {f[0]:.1f} Hz to {f[-1]:.1f} Hz")

    # Step 12: Plot Noisy Spectrogram
    print("\n--- Step 12: Plot Noisy Spectrogram ---")
    plt.figure(figsize=(12, 5))
    plt.pcolormesh(
        t,
        f,
        20 * np.log10(magnitude + 1e-10),
        shading="gouraud",
        cmap="magma"
    )
    plt.colorbar(label="Magnitude (dB)")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.title("Noisy Speech Spectrogram (White Noise 5 dB SNR)", fontsize=12, fontweight='bold')
    plt.ylim(0, fs / 2)
    plt.tight_layout()
    plt.savefig("output/step12_noisy_spectrogram.png", dpi=150)
    plt.close()
    print("Saved output/step12_noisy_spectrogram.png")

    # Step 13 & 14: Estimate Noise and Plot Noise Profile
    print("\n--- Step 13 & 14: Noise Spectrum Estimation ---")
    noise_only = noisy[:int(0.5 * fs)]
    _, _, Z_noise = stft(
        noise_only,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap
    )
    noise_mag = np.mean(np.abs(Z_noise), axis=1, keepdims=True)
    print(f"Estimated noise spectrum computed from first 0.5s ({Z_noise.shape[1]} STFT frames)")

    plt.figure(figsize=(10, 4))
    plt.plot(f, 20 * np.log10(noise_mag[:, 0] + 1e-10), color='#e7298a', lw=1.5)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("Estimated Noise Spectrum (Averaged across initial silent frames)", fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, fs / 2)
    plt.tight_layout()
    plt.savefig("output/step14_noise_spectrum.png", dpi=150)
    plt.close()
    print("Saved output/step14_noise_spectrum.png")

    # Step 15-18: Spectral Subtraction with Different Alpha Values
    print("\n--- Step 15 to 18: Spectral Subtraction & Audio Generation ---")
    alphas = [0.5, 1.0, 2.0]
    enhanced_dict = {}

    for alpha in alphas:
        enhanced, _, _, _, _, _, _, Z_clean = spectral_subtraction(
            noisy, fs, noise_duration_sec=0.5, alpha=alpha, beta=0.0
        )
        enhanced_dict[alpha] = enhanced
        
        # Save audio file
        out_filename = f"output/enhanced_alpha_{alpha}.wav"
        sf.write(out_filename, enhanced, fs)
        print(f"Generated & Saved: {out_filename} (alpha = {alpha})")

    # Main default enhanced audio (alpha = 1.0)
    sf.write("output/enhanced.wav", enhanced_dict[1.0], fs)
    print("Saved default output/enhanced.wav (alpha = 1.0)")

    # Step 19: Plot Comparison of Waveforms (Clean vs Noisy vs Enhanced)
    print("\n--- Step 19: Plot Clean vs Noisy vs Enhanced Waveforms ---")
    time_enhanced = np.arange(len(enhanced_dict[1.0])) / fs
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(time_axis, audio_with_silence, color='#1b9e77', lw=0.8)
    plt.title("1. Clean Speech", fontsize=11, fontweight='bold')
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.2, 1.2)

    plt.subplot(3, 1, 2)
    plt.plot(time_axis, noisy, color='#d95f02', lw=0.8)
    plt.title("2. Noisy Speech (5 dB SNR)", fontsize=11, fontweight='bold')
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.5, 1.5)

    plt.subplot(3, 1, 3)
    plt.plot(time_enhanced, enhanced_dict[1.0], color='#7570b3', lw=0.8)
    plt.title("3. Enhanced Speech (Spectral Subtraction, alpha=1.0)", fontsize=11, fontweight='bold')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.2, 1.2)

    plt.tight_layout()
    plt.savefig("output/step19_waveform_comparison.png", dpi=150)
    plt.close()
    print("Saved output/step19_waveform_comparison.png")

    # Step 20: Plot Enhanced Spectrogram vs Noisy vs Clean
    print("\n--- Step 20: Plot Spectrogram Comparison ---")
    # STFT of clean
    f_c, t_c, Z_c = stft(audio_with_silence, fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap)
    # STFT of enhanced alpha=1.0
    f_e, t_e, Z_e = stft(enhanced_dict[1.0], fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap)

    fig, axes = plt.subplots(3, 1, figsize=(13, 10), sharex=True, sharey=True)

    vmin, vmax = -60, 20
    im0 = axes[0].pcolormesh(t_c, f_c, 20 * np.log10(np.abs(Z_c) + 1e-10), shading="gouraud", cmap="magma", vmin=vmin, vmax=vmax)
    axes[0].set_title("Clean Speech Spectrogram", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("Frequency (Hz)")

    im1 = axes[1].pcolormesh(t, f, 20 * np.log10(magnitude + 1e-10), shading="gouraud", cmap="magma", vmin=vmin, vmax=vmax)
    axes[1].set_title("Noisy Speech Spectrogram (5 dB SNR)", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("Frequency (Hz)")

    im2 = axes[2].pcolormesh(t_e, f_e, 20 * np.log10(np.abs(Z_e) + 1e-10), shading="gouraud", cmap="magma", vmin=vmin, vmax=vmax)
    axes[2].set_title("Enhanced Speech Spectrogram (alpha=1.0)", fontsize=11, fontweight='bold')
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Frequency (Hz)")

    plt.ylim(0, fs / 2)
    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    fig.colorbar(im2, cax=cbar_ax, label="Magnitude (dB)")

    plt.savefig("output/step20_spectrogram_comparison.png", dpi=150)
    plt.close()
    print("Saved output/step20_spectrogram_comparison.png")

    # Alpha Parameter Exploration Comparison Plot
    print("\n--- Alpha Exploration Plot (alpha = 0.5, 1.0, 2.0) ---")
    fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True, sharey=True)
    for i, a in enumerate(alphas):
        f_a, t_a, Z_a = stft(enhanced_dict[a], fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap)
        axes[i].pcolormesh(t_a, f_a, 20 * np.log10(np.abs(Z_a) + 1e-10), shading="gouraud", cmap="magma", vmin=vmin, vmax=vmax)
        axes[i].set_title(f"Enhanced Spectrogram with Subtraction Factor alpha = {a}", fontsize=11, fontweight='bold')
        axes[i].set_ylabel("Frequency (Hz)")
        if i == len(alphas) - 1:
            axes[i].set_xlabel("Time (s)")

    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    fig.colorbar(im2, cax=cbar_ax, label="Magnitude (dB)")
    plt.savefig("output/alpha_comparison_spectrograms.png", dpi=150)
    plt.close()
    print("Saved output/alpha_comparison_spectrograms.png")

    print("\n==================================================")
    print("All steps completed successfully!")
    print("Generated Audio Files in ./output/:")
    print("  - clean.wav")
    print("  - noisy.wav")
    print("  - enhanced.wav (alpha=1.0)")
    print("  - enhanced_alpha_0.5.wav")
    print("  - enhanced_alpha_1.0.wav")
    print("  - enhanced_alpha_2.0.wav")
    print("\nGenerated Visualizations in ./output/:")
    print("  - step8_clean_vs_noisy_waveform.png")
    print("  - step12_noisy_spectrogram.png")
    print("  - step14_noise_spectrum.png")
    print("  - step19_waveform_comparison.png")
    print("  - step20_spectrogram_comparison.png")
    print("  - alpha_comparison_spectrograms.png")
    print("==================================================")

if __name__ == "__main__":
    run_experiment()
