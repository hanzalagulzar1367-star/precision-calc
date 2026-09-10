"""
Kivy entry point for PrecisionCalc — a NEW file, separate from your original
main.py (CustomTkinter). This does not modify or replace main.py in any way.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

from kivy_simple_calculator import build_simple_calculator
from kivy_scientific_calculator import build_scientific_calculator
from kivy_statistical_calculator import build_statistical_calculator
from kivy_simple_conversions import build_simple_conversions
from kivy_scientific_conversions import build_scientific_conversions
from kivy_currency_converter import build_currency_converter
from kivy_engineering_calculator import build_engineering_calculator
from kivy_binary_converter import build_binary_converter
from kivy_accounting_calculator import build_accounting_calculator  # ADDED

Window.clearcolor = get_color_from_hex("#0f0f1a")

MODES = [
    "Simple Calculator",
    "Scientific Calculator",
    "Statistical Calculator",
    "Simple Conversions",
    "Scientific Conversions",
    "Currency Converter",
    "Engineering Calculator",
    "Binary Converter",
    "Accounting Calculator",  # ADDED
]

BUILDERS = {
    "Simple Calculator": build_simple_calculator,
    "Scientific Calculator": build_scientific_calculator,
    "Statistical Calculator": build_statistical_calculator,
    "Simple Conversions": build_simple_conversions,
    "Scientific Conversions": build_scientific_conversions,
    "Currency Converter": build_currency_converter,
    "Engineering Calculator": build_engineering_calculator,
    "Binary Converter": build_binary_converter,
    "Accounting Calculator": build_accounting_calculator,  # ADDED
}


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)

        # ---- SIDEBAR ----
        self.sidebar = BoxLayout(
            orientation="vertical", size_hint_x=None, width=200,
            padding=10, spacing=6,
        )
        with self.sidebar.canvas.before:
            Color(*get_color_from_hex("#1a1a2e"))
            self._sidebar_rect = Rectangle(pos=self.sidebar.pos, size=self.sidebar.size)
        self.sidebar.bind(pos=self._sync_sidebar_rect, size=self._sync_sidebar_rect)

        title_label = Label(
            text="PrecisionCalc", font_size=20, bold=True,
            color=get_color_from_hex("#00d9ff"),
            size_hint_y=None, height=50,
        )
        self.sidebar.add_widget(title_label)

        nav_scroll = ScrollView(size_hint=(1, 1))
        nav_box = BoxLayout(orientation="vertical", spacing=6, size_hint_y=None)
        nav_box.bind(minimum_height=nav_box.setter("height"))

        for mode in MODES:
            btn = Button(
                text=mode, size_hint_y=None, height=44,
                background_normal="", background_color=get_color_from_hex("#16213e"),
                color=get_color_from_hex("#ffffff"), font_size=13,
            )
            btn.bind(on_release=lambda inst, m=mode: self.show_mode(m))
            nav_box.add_widget(btn)

        nav_scroll.add_widget(nav_box)
        self.sidebar.add_widget(nav_scroll)
        self.add_widget(self.sidebar)

        # ---- MAIN CONTENT AREA ----
        outer_scroll = ScrollView(size_hint=(1, 1))
        self.main_area = BoxLayout(
            orientation="vertical", padding=15, spacing=10,
            size_hint_y=None,
        )
        self.main_area.bind(minimum_height=self.main_area.setter("height"))
        with self.main_area.canvas.before:
            Color(*get_color_from_hex("#0f0f1a"))
            self._main_rect = Rectangle(pos=self.main_area.pos, size=self.main_area.size)
        self.main_area.bind(pos=self._sync_main_rect, size=self._sync_main_rect)

        outer_scroll.add_widget(self.main_area)
        self.add_widget(outer_scroll)

        self.show_mode(MODES[0])

    def _sync_sidebar_rect(self, *_):
        self._sidebar_rect.pos = self.sidebar.pos
        self._sidebar_rect.size = self.sidebar.size

    def _sync_main_rect(self, *_):
        self._main_rect.pos = self.main_area.pos
        self._main_rect.size = self.main_area.size

    def show_mode(self, mode_name):
        self.main_area.clear_widgets()
        builder = BUILDERS.get(mode_name)
        if builder:
            builder(self.main_area)
        else:
            self.main_area.add_widget(
                Label(text=f"{mode_name}\n(coming soon)", font_size=22, size_hint_y=None, height=100)
            )


class PrecisionCalcApp(App):
    def build(self):
        self.title = "PrecisionCalc"
        return RootLayout()


if __name__ == "__main__":
    PrecisionCalcApp().run()