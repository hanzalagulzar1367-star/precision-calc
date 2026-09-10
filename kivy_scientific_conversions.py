"""
Kivy version of scientific_conversions.py
"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex

CATEGORIES = {
    "Speed": {"base": "m/s", "units": {"m/s": 1.0, "km/s": 1000.0, "km/h": 0.277778, "mph": 0.44704}},
    "Acceleration": {"base": "m/s2", "units": {"m/s2": 1.0, "km/s2": 1000.0, "km/h2": 0.0000771605}},
    "Force": {"base": "Newton", "units": {"Newton": 1.0, "Kilonewton": 1000.0, "Pound-force": 4.44822}},
    "Pressure": {"base": "Pascal", "units": {
        "Pascal": 1.0, "Kilopascal": 1000.0, "Bar": 100000.0, "Atmosphere": 101325.0, "PSI": 6894.76,
    }},
    "Energy": {"base": "Joule", "units": {
        "Joule": 1.0, "Kilojoule": 1000.0, "Calorie": 4.184, "Kilowatt-hour": 3600000.0,
    }},
    "Power": {"base": "Watt", "units": {"Watt": 1.0, "Kilowatt": 1000.0, "Horsepower": 745.7}},
    "Frequency": {"base": "Hertz", "units": {
        "Hertz": 1.0, "Kilohertz": 1000.0, "Megahertz": 1000000.0, "Gigahertz": 1000000000.0,
    }},
}


def build_scientific_conversions(parent):
    category_names = list(CATEGORIES.keys())
    state = {"category": category_names[0]}

    title = Label(
        text="Scientific Conversions", font_size=22, bold=True,
        color=get_color_from_hex("#9b59b6"), size_hint_y=None, height=40,
    )
    parent.add_widget(title)

    category_spinner = Spinner(
        text=category_names[0], values=category_names,
        size_hint_y=None, height=44,
        background_color=get_color_from_hex("#16213e"),
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

        unit_data = CATEGORIES[category]["units"]
        from_factor = unit_data[from_unit]
        to_factor = unit_data[to_unit]
        base_value = value * from_factor
        result = base_value / to_factor

        result_label.text = f"{value} {from_unit} = {result} {to_unit}"

    convert_btn = Button(
        text="Convert", size_hint_y=None, height=48,
        background_normal="", background_color=get_color_from_hex("#9b59b6"),
        color=get_color_from_hex("#ffffff"), bold=True,
    )
    convert_btn.bind(on_release=do_conversion)
    parent.add_widget(convert_btn)
    