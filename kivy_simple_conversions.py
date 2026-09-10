"""Simple Unit Conversions"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class SimpleConversionsScreen(Screen):
    title_text = StringProperty('Simple Conversions')
    
    # Conversion factors (to base units)
    CONVERSIONS = {
        'Length': {
            'base': 'Meter',
            'units': {
                'Meter': 1,
                'Kilometer': 1000,
                'Centimeter': 0.01,
                'Millimeter': 0.001,
                'Mile': 1609.344,
                'Yard': 0.9144,
                'Foot': 0.3048,
                'Inch': 0.0254,
            }
        },
        'Weight': {
            'base': 'Kilogram',
            'units': {
                'Kilogram': 1,
                'Gram': 0.001,
                'Milligram': 0.000001,
                'Pound': 0.45359237,
                'Ounce': 0.0283495,
                'Ton': 1000,
            }
        },
        'Temperature': {
            'base': 'Celsius',
            'units': {
                'Celsius': 1,
                'Fahrenheit': 1,
                'Kelvin': 1,
            }
        },
        'Time': {
            'base': 'Second',
            'units': {
                'Second': 1,
                'Minute': 60,
                'Hour': 3600,
                'Day': 86400,
                'Week': 604800,
            }
        },
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def convert(self, category, from_unit, to_unit, value):
        try:
            value = float(value)
            if category == 'Temperature':
                return self._convert_temp(from_unit, to_unit, value)
            
            units = self.CONVERSIONS[category]['units']
            base_value = value * units[from_unit]
            result = base_value / units[to_unit]
            return round(result, 6)
        except Exception as e:
            return f'Error: {e}'
    
    def _convert_temp(self, from_unit, to_unit, value):
        # Convert to Celsius first
        if from_unit == 'Celsius':
            celsius = value
        elif from_unit == 'Fahrenheit':
            celsius = (value - 32) * 5 / 9
        elif from_unit == 'Kelvin':
            celsius = value - 273.15
        else:
            return 'Invalid unit'
        
        # Convert to target
        if to_unit == 'Celsius':
            return round(celsius, 4)
        elif to_unit == 'Fahrenheit':
            return round(celsius * 9 / 5 + 32, 4)
        elif to_unit == 'Kelvin':
            return round(celsius + 273.15, 4)
        return 'Invalid unit'
        