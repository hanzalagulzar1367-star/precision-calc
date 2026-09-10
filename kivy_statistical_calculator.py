"""Statistical Calculator Screen"""
import statistics
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class StatisticalCalculatorScreen(Screen):
    title_text = StringProperty('Statistical Calculator')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numbers = []
    
    def _update_display(self):
        if self.numbers:
            self.ids.display.text = ', '.join(str(n) for n in self.numbers)
        else:
            self.ids.display.text = 'Enter numbers, tap Add'
    
    def add_digit(self, digit):
        current = self.ids.display.text if self.ids.display.text != 'Enter numbers, tap Add' else ''
        if digit == '.' and '.' in current:
            return
        self.ids.display.text = current + digit
    
    def add_number(self):
        try:
            text = self.ids.display.text
            if text and text != 'Enter numbers, tap Add':
                # Support comma-separated input
                for part in text.replace(',', ' ').split():
                    self.numbers.append(float(part))
                self._update_display()
        except ValueError:
            self.ids.display.text = 'Invalid input'
    
    def clear(self):
        self.numbers = []
        self.ids.display.text = 'Enter numbers, tap Add'
        self.ids.result.text = ''
    
    def calculate_stat(self, stat_type):
        if len(self.numbers) < 1:
            self.ids.result.text = 'No data'
            return
        try:
            if stat_type == 'mean':
                result = statistics.mean(self.numbers)
            elif stat_type == 'median':
                result = statistics.median(self.numbers)
            elif stat_type == 'mode':
                result = statistics.mode(self.numbers)
            elif stat_type == 'stdev':
                result = statistics.stdev(self.numbers) if len(self.numbers) > 1 else 0
            elif stat_type == 'variance':
                result = statistics.variance(self.numbers) if len(self.numbers) > 1 else 0
            elif stat_type == 'sum':
                result = sum(self.numbers)
            elif stat_type == 'count':
                result = len(self.numbers)
            elif stat_type == 'min':
                result = min(self.numbers)
            elif stat_type == 'max':
                result = max(self.numbers)
            else:
                return
            
            self.ids.result.text = f'{stat_type.title()}: {round(result, 6)}'
        except Exception as e:
            self.ids.result.text = f'Error: {e}'