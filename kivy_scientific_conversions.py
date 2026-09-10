"""Scientific Conversions"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class ScientificConversionsScreen(Screen):
    title_text = StringProperty('Scientific Conversions')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def convert_pressure(self, value, from_unit, to_unit):
        # Base unit: Pascal
        factors = {
            'Pascal': 1,
            'Kilopascal': 1000,
            'Bar': 100000,
            'PSI': 6894.76,
            'Atmosphere': 101325,
            'Torr': 133.322,
        }
        try:
            value = float(value)
            result = value * factors[from_unit] / factors[to_unit]
            return round(result, 6)
        except:
            return 'Error'
    
    def convert_energy(self, value, from_unit, to_unit):
        # Base unit: Joule
        factors = {
            'Joule': 1,
            'Kilojoule': 1000,
            'Calorie': 4.184,
            'Kilocalorie': 4184,
            'Watt-hour': 3600,
            'Electronvolt': 1.602176634e-19,
        }
        try:
            value = float(value)
            result = value * factors[from_unit] / factors[to_unit]
            return round(result, 10)
        except:
            return 'Error'
    
    def convert_power(self, value, from_unit, to_unit):
        # Base: Watt
        factors = {
            'Watt': 1,
            'Kilowatt': 1000,
            'Megawatt': 1e6,
            'Horsepower': 745.7,
        }
        try:
            value = float(value)
            result = value * factors[from_unit] / factors[to_unit]
            return round(result, 6)
        except:
            return 'Error'