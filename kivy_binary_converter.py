"""Binary Converter"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class BinaryConverterScreen(Screen):
    title_text = StringProperty('Binary Converter')
    
    def convert(self, value, from_base, to_base):
        try:
            value = str(value).strip()
            if from_base == 'binary':
                decimal = int(value, 2)
            elif from_base == 'octal':
                decimal = int(value, 8)
            elif from_base == 'decimal':
                decimal = int(value, 10)
            elif from_base == 'hex':
                decimal = int(value, 16)
            else:
                return 'Invalid base'
            
            if to_base == 'binary':
                return bin(decimal)[2:]
            elif to_base == 'octal':
                return oct(decimal)[2:]
            elif to_base == 'decimal':
                return str(decimal)
            elif to_base == 'hex':
                return hex(decimal)[2:].upper()
            else:
                return 'Invalid base'
        except ValueError:
            return 'Invalid input'
        except Exception as e:
            return f'Error: {e}'