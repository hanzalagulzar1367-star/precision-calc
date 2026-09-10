"""Scientific Calculator Screen"""
import math
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class ScientificCalculatorScreen(Screen):
    title_text = StringProperty('Scientific Calculator')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = '0'
        self.previous = None
        self.operator = None
        self.new_number = True
    
    def _update_display(self):
        self.ids.display.text = self.current
    
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
        self._update_display()
    
    def set_operator(self, op):
        if self.operator and not self.new_number:
            self.calculate()
        self.previous = float(self.current)
        self.operator = op
        self.new_number = True
    
    def calculate(self):
        if self.operator is None or self.previous is None:
            return
        current = float(self.current)
        try:
            if self.operator == '+':
                result = self.previous + current
            elif self.operator == '-':
                result = self.previous - current
            elif self.operator == '*':
                result = self.previous * current
            elif self.operator == '/':
                result = self.previous / current if current != 0 else 0
            elif self.operator == '^':
                result = self.previous ** current
            else:
                return
            
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 10))
        except Exception:
            self.current = 'Error'
        
        self.previous = None
        self.operator = None
        self.new_number = True
        self._update_display()
    
    def clear(self):
        self.current = '0'
        self.previous = None
        self.operator = None
        self.new_number = True
        self._update_display()
    
    def apply_function(self, func):
        try:
            value = float(self.current)
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'sqrt':
                result = math.sqrt(value)
            elif func == 'square':
                result = value ** 2
            elif func == 'fact':
                result = math.factorial(int(value))
            elif func == 'inv':
                result = 1 / value
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
        self._update_display()
    
    def toggle_sign(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        elif self.current != '0':
            self.current = '-' + self.current
        self._update_display()