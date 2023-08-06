from time import time


class Metricts:
    def __init__(self, tempo_inicial=None, tempo_final=None, tempo_total=None):
        self.tempo_inicial = tempo_final
        self.tempo_final = tempo_final
        self.tempo_total = tempo_total
    
    def initial_time(self):
        self.tempo_inicial = time() 
        return self.tempo_inicial
    
    def finall_time(self):
        self.tempo_final = time()
        return self.tempo_final
    
    def total_time(self):
        self.tempo_total = self.tempo_final - self.tempo_inicial
        return self.tempo_total


class ArmazenaMetricts(Metricts):
    def __init__(self):
        self.metricts = Metricts()
        
    def initial_time(self):
        self.metricts.initial_time()
    
    def finall_time(self):
        self.metricts.finall_time()
    
    def total_time(self):
        return self.metricts.total_time()
    
    def print_metricts(self):
        print(f"Tempo total: {self.metricts.total_time()}")
