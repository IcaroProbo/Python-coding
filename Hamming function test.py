import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. Dados do sinal
# ============================================================

fs = 1000.0          # frequência de amostragem [Hz]
duration = 2.0       # duração da medição [s]

t = np.arange(0, duration, 1 / fs)

# Exemplo: sinal com duas frequências
signal = (
    2.0 * np.sin(2 * np.pi * 50 * t)
    + 0.8 * np.sin(2 * np.pi * 120 * t)
)

# ============================================================
# 2. Remover componente DC
# ============================================================

signal = signal - np.mean(signal)

# ============================================================
# 3. Aplicar janela de Hann
# ============================================================

N = len(signal)

window = np.hanning(N)
windowed_signal = signal * window

# ============================================================
# 4. FFT de um lado
# ============================================================

fft_values = np.fft.rfft(windowed_signal)
frequencies = np.fft.rfftfreq(N, d=1 / fs)

# ============================================================
# 5. Corrigir amplitude
# ============================================================

# Ganho coerente da janela
coherent_gain = np.mean(window)

amplitude = np.abs(fft_values) / (N * coherent_gain)

# FFT unilateral: dobrar amplitudes, exceto DC e Nyquist
if N % 2 == 0:
    amplitude[1:-1] *= 2
else:
    amplitude[1:] *= 2

# ============================================================
# 6. Gráficos
# ============================================================

plt.figure(figsize=(10, 4))
plt.plot(t, signal)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Original signal")
plt.grid()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(t, windowed_signal)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Signal after Hann window")
plt.grid()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(frequencies, amplitude)
plt.xlim(0, 200)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.title("FFT spectrum with Hann window")
plt.grid()
plt.tight_layout()
plt.show()