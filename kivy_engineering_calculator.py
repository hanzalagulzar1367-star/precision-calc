"""Engineering Calculator"""
import math
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class EngineeringCalculatorScreen(Screen):
    title_text = StringProperty('Engineering Calculator')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = '0'
        self.new_number = True
    
    def add_digit(self, digit):
        if self.new_number:
            self.current = digit
            self.new_number = False
        else:
            if digit == '.' and '.' in self.current:
                return
            if self.current == '0' and digit != '.':
                self.current = digit
            else:
                self.current += digit
        self.ids.display.text = self.current
    
    def apply_function(self, func):
        try:
            value = float(self.current)
            if func == 'sqrt':
                result = math.sqrt(value)
            elif func == 'cbrt':
                result = value ** (1/3)
            elif func == 'square':
                result = value ** 2
            elif func == 'cube':
                result = value ** 3
            elif func == 'inv':
                result = 1 / value
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'exp':
                result = math.exp(value)
            elif func == 'abs':
                result = abs(value)
            elif func == 'sin':
                result = math.sin(value)
            elif func == 'cos':
                result = math.cos(value)
            elif func == 'tan':
                result = math.tan(value)
            elif func == 'asin':
                result = math.asin(value)
            elif func == 'acos':
                result = math.acos(value)
            elif func == 'atan':
                result = math.atan(value)
            elif func == 'pi':
                result = math.pi
            elif func == 'e':
                result = math.e
            else:
                return
            
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 10))
        except Exception:
            self.current = 'Error'
        self.new_number = True
        self.ids.display.text = self.current
    
    def clear(self):
        self.current = '0'
        self.new_number = True
        self.ids.display.text = self.current