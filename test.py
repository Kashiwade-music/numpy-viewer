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

ndarray_3d = np.empty((3, S.shape[0], S.shape[1]))
ndarray_3d[0] = S
ndarray_3d[1] = Sdb
ndarray_3d[2] = Spower
np.save('./test_npy/stay_alive_test_3d_concat', ndarray_3d)

ndarray_4d = np.empty((3, 3, S.shape[0], S.shape[1]))
ndarray_4d[0] = ndarray_3d
ndarray_4d[1] = ndarray_3d
ndarray_4d[2] = ndarray_3d
np.save('./test_npy/stay_alive_test_4d_concat', ndarray_4d)
