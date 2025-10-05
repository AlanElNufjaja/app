import numpy as np

class SimuladorImpacto:
  
    def __init__(self, diametro_meteoro_m, velocidad_meteoro_ms, densidad_meteoro_kg_m3=3000):
        self.diametro = diametro_meteoro_m
        self.velocidad = velocidad_meteoro_ms
        self.densidad = densidad_meteoro_kg_m3
        
        self.masa_kg = self._calcular_masa()
        self.energia_cinetica_joules = self._calcular_energia_cinetica()
        self.energia_megatones = self.energia_cinetica_joules / 4.184e15

    def _calcular_masa(self):
        radio = self.diametro / 2
        volumen = (4/3) * np.pi * (radio ** 3)
        return volumen * self.densidad

    def _calcular_energia_cinetica(self):
        return 0.5 * self.masa_kg * (self.velocidad ** 2)

    def calcular_diametro_crater(self, densidad_objetivo_kg_m3=2600, g=9.81):
        diametro = 1.8 * (densidad_objetivo_kg_m3 ** - (1/3)) * (g ** -0.25) * (self.energia_cinetica_joules ** 0.25)
        return diametro

    def calcular_radio_bola_fuego(self):
        energia_kilotones = self.energia_megatones * 1000
        radio = 30 * (energia_kilotones ** (1/3))
        return radio

    def calcular_terremoto(self, eficiencia_sismica=1e-4):
        if self.energia_cinetica_joules <= 0:
            return {"magnitud_mw": 0, "radio_danio_severo_km": 0}

        energia_sismica_joules = self.energia_cinetica_joules * eficiencia_sismica
        magnitud = (np.log10(energia_sismica_joules) - 4.8) / 1.5
        radio_danio_severo_km = np.exp((magnitud - 5.56) / 0.82)
        
        return {"magnitud_mw": magnitud, "radio_danio_severo_km": radio_danio_severo_km}

    def calcular_alcance_onda_sonora(self, db_objetivo=120):
        if self.energia_megatones <= 0:
            return 0.0
        
        energia_kilotones = self.energia_megatones * 1000
        exponente = (195 + 10 * np.log10(energia_kilotones) - db_objetivo) / 20
        distancia_km = 10 ** exponente
        return distancia_km
