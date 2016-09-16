from scipy.io import wavfile
import numpy as np

def load_audio_file(filename, channels=256, format="16bit_pcm"):
	sampling_rate, signal = wavfile.read(filename)
	# discard R channel to convert to mono
	signal = signal[:, 0].astype(float)
	# normalize to -1 ~ 1
	if format == "16bit_pcm":
		max = 1<<15
	elif format == "32bit_pcm":
		max = 1<<31
	elif format == "8bit_pcm":
		max = 1<<8 - 1
	signal /= max
	# mu-law companding transformation (ITU-T, 1988)
	mu = channels - 1
	signal = np.sign(signal) * np.log(1 + mu * np.absolute(signal)) / np.log(1 + mu)
	# quantize
	quantized_signal = (np.clip(signal * 0.5 + 0.5, 0, 1) * mu).astype(int)
	return quantized_signal, sampling_rate

def onehot_pixel(quantized_signal_batch, channels=256):
	print quantized_signal_batch
	zeros = np.zeros(())