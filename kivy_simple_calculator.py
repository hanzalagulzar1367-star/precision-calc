"""Simple Calculator Screen"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class SimpleCalculatorScreen(Screen):
    title_text = StringProperty('Simple Calculator')
    
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
        if self.operator == '+':
            result = self.previous + current
        elif self.operator == '-':
            result = self.previous - current
        elif self.operator == '*':
            result = self.previous * current
        elif self.operator == '/':
            result = self.previous / current if current != 0 else 0
        else:
            return
        
        if result == int(result):
            self.current = str(int(result))
        else:
            self.current = str(round(result, 8))
        
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
    
    def toggle_sign(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        elif self.current != '0':
            self.current = '-' + self.current
        self._update_display()
    
    def percent(self):
        try:
            self.current = str(float(self.current) / 100)
            self._update_display()
        except:
            pass