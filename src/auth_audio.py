import librosa 
import numpy as np

class AudioAuth():
    m0_arr = []
    user_m0 = None
    user_s0 = None

    def __init__(self) -> None:
        pass

    def calc_f0_from_file(self, filename, sr=44100, calc_mean=False):
        m0 = None
        y, sr = librosa.load(filename, sr=sr)

        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), # calc f0
                                                        fmax=librosa.note_to_hz('E3'))

        if calc_mean:
            if f0.any():
                m0 = np.nanmean(f0)

            return m0, f0
        else:
            return f0
    
    def fit(self, user_file_list, sr):
        
        for user_file in user_file_list:
            m0, _ = self.calc_f0_from_file(user_file, sr, True)
            self.m0_arr.append(m0) # salvando no array
        
        self.m0_arr = np.array(self.m0_arr) # transformando em numpy array

        self.user_m0 = np.round(self.m0_arr.mean(), 2) # calculando media de f0 para todos os usuário (estimando oa f0 do usuário)
        self.user_s0 = np.round(self.m0_arr.std(), 2) # calculando o desvio das amostras
        print("f0 stats:", self.user_m0, self.user_s0)
    
    def predict(self, file_name, sr):
        m, _ = self.calc_f0_from_file(file_name, sr, True)
        if not np.isnan(m):
            return m, ((self.user_m0 - self.user_s0) <= m) and (m <= (self.user_m0 + self.user_s0))
        else:
            return False

