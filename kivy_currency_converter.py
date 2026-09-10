"""Currency Converter (offline with fixed rates)"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class CurrencyConverterScreen(Screen):
    title_text = StringProperty('Currency Converter')
    
    # Fixed rates (for offline use) - 1 unit = X USD
    RATES = {
        'USD': 1.0,
        'EUR': 1.08,
        'GBP': 1.27,
        'PKR': 0.0036,
        'INR': 0.012,
        'AED': 0.27,
        'SAR': 0.27,
        'JPY': 0.0067,
        'CNY': 0.14,
        'CAD': 0.74,
        'AUD': 0.66,
    }
    
    def convert(self, value, from_curr, to_curr):
        try:
            value = float(value)
            usd = value * self.RATES[from_curr]
            result = usd / self.RATES[to_curr]
            return round(result, 4)
        except Exception as e:
            return f'Error: {e}'
            