import numpy as np
import librosa

audio_path = "./test_npy/stay_alive_test.wav"
y, sr = librosa.load(audio_path, sr=44100)
print(y, sr)
D = librosa.stft(y)  # STFT
S, _ = librosa.magphase(D)  # 複素数を強度と位相へ変換
np.save('./test_npy/stay_alive_test_amplitude', S)
Sdb = librosa.amplitude_to_db(S, ref=np.max)
np.save('./test_npy/stay_alive_test_db', Sdb)
Spower = librosa.db_to_power(Sdb)
np.save('./test_npy/stay_alive_test_power', Spower)
