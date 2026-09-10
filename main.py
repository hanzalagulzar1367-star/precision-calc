"""
PrecisionCalc - Main Entry Point
Mobile-first Kivy Calculator App
"""
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.app import App

# Import all calculator screens
from kivy_simple_calculator import SimpleCalculatorScreen
from kivy_scientific_calculator import ScientificCalculatorScreen
from kivy_statistical_calculator import StatisticalCalculatorScreen
from kivy_simple_conversions import SimpleConversionsScreen
from kivy_scientific_conversions import ScientificConversionsScreen
from kivy_currency_converter import CurrencyConverterScreen
from kivy_engineering_calculator import EngineeringCalculatorScreen
from kivy_binary_converter import BinaryConverterScreen
from kivy_accounting_calculator import AccountingCalculatorScreen


# ✅ Home screen class (was missing before)
class HomeScreen(Screen):
    pass


class PrecisionCalcApp(App):
    def build(self):
        self.title = "PrecisionCalc"
        Window.size = (360, 640)

        # Load KV safely (no double load warnings)
        with open('precisioncalc.kv', 'r', encoding='utf-8') as f:
            root_widget = Builder.load_string(f.read())

        # ✅ Force the app to start on Home menu
        root_widget.ids.sm.current = 'home'

        return root_widget

    def go_to(self, screen_name):
        self.root.ids.sm.transition = SlideTransition(direction='left')
        self.root.ids.sm.current = screen_name

    def go_back(self):
        self.root.ids.sm.transition = SlideTransition(direction='right')
        self.root.ids.sm.current = 'home'


if __name__ == '__main__':
    PrecisionCalcApp().run()