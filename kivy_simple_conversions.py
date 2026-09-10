"""
Kivy version of simple_conversions.py
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex

CATEGORIES = {
    "Length": {
        "base": "Meter",
        "units": {
            "Millimeter": 0.001, "Centimeter": 0.01, "Meter": 1.0, "Kilometer": 1000.0,
            "Inch": 0.0254, "Foot": 0.3048, "Yard": 0.9144, "Mile": 1609.344,
        }
    },
    "Weight/Mass": {
        "base": "Gram",
        "units": {
            "Milligram": 0.001, "Gram": 1.0, "Kilogram": 1000.0,
            "Ounce": 28.3495, "Pound": 453.592,
        }
    },
    "Temperature": {
        "base": "Celsius",
        "units": {"Celsius": None, "Fahrenheit": None, "Kelvin": None}
    },
    "Time": {
        "base": "Second",
        "units": {"Seconds": 1.0, "Minutes": 60.0, "Hours": 3600.0, "Days": 86400.0}
    },
    "Area": {
        "base": "Square meter",
        "units": {
            "Square meter": 1.0, "Square kilometer": 1_000_000.0,
            "Square foot": 0.092903, "Acre": 4046.86,
        }
    },
}


def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    else:  # Kelvin
        celsius = value - 273.15

    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    else:  # Kelvin
        return celsius + 273.15


def build_simple_conversions(parent):
    category_names = list(CATEGORIES.keys())
    state = {"category": category_names[0]}

    title = Label(
        text="Simple Conversions", font_size=22, bold=True,
        color=get_color_from_hex("#2ecc71"), size_hint_y=None, height=40,
    )
    parent.add_widget(title)

    category_spinner = Spinner(
        text=category_names[0], values=category_names,
        size_hint_y=None, height=44,
        background_color=get_color_from_hex("#16213e"),
        color=get_color_from_hex("#ffffff"),
    )
    parent.add_widget(category_spinner)

    grid = GridLayout(cols=2, size_hint_y=None, height=170, spacing=8, padding=(0, 10))

    first_units = list(CATEGORIES[category_names[0]]["units"].keys())

    grid.add_widget(Label(text="From:"))
    from_spinner = Spinner(text=first_units[0], values=first_units, background_color=get_color_from_hex("#16213e"))
    grid.add_widget(from_spinner)

    grid.add_widget(Label(text="To:"))
    to_spinner = Spinner(text=first_units[1] if len(first_units) > 1 else first_units[0], values=first_units, background_color=get_color_from_hex("#16213e"))
    grid.add_widget(to_spinner)

    grid.add_widget(Label(text="Value:"))
    value_input = TextInput(multiline=False, input_filter="float", background_color=get_color_from_hex("#1a1a2e"))
    grid.add_widget(value_input)

    parent.add_widget(grid)

    result_label = Label(
        text="", font_size=18, bold=True,
        color=get_color_from_hex("#00ff9d"), size_hint_y=None, height=60,
    )
    parent.add_widget(result_label)

    def on_category_change(spinner, text):
        state["category"] = text
        units = list(CATEGORIES[text]["units"].keys())
        from_spinner.values = units
        to_spinner.values = units
        from_spinner.text = units[0]
        to_spinner.text = units[1] if len(units) > 1 else units[0]
        result_label.text = ""

    category_spinner.bind(text=on_category_change)

    def do_conversion(*_):
        raw_value = value_input.text.strip()
        if raw_value == "":
            result_label.text = "Please enter a value."
            return
        try:
            value = float(raw_value)
        except ValueError:
            result_label.text = "Invalid number. Please enter digits only."
            return

        category = state["category"]
        from_unit = from_spinner.text
        to_unit = to_spinner.text

        if category == "Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            unit_data = CATEGORIES[category]["units"]
            from_factor = unit_data[from_unit]
            to_factor = unit_data[to_unit]
            base_value = value * from_factor
            result = base_value / to_factor

        result_label.text = f"{value} {from_unit} = {result} {to_unit}"

    convert_btn = Button(
        text="Convert", size_hint_y=None, height=48,
        background_normal="", background_color=get_color_from_hex("#2ecc71"),
        color=get_color_from_hex("#1a1a2e"), bold=True,
    )
    convert_btn.bind(on_release=do_conversion)
    parent.add_widget(convert_btn)