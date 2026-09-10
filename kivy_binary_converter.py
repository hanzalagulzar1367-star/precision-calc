"""
Kivy version of binary_converter.py
"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex

SYSTEMS = ["Decimal", "Binary", "Octal", "Hexadecimal"]


def build_binary_converter(parent):
    title = Label(
        text="Binary / Number System Converter", font_size=20, bold=True,
        color=get_color_from_hex("#3498db"), size_hint_y=None, height=40,
    )
    parent.add_widget(title)

    instructions = Label(
        text="Choose the number system you're entering, type the value, then convert.",
        font_size=13, color=get_color_from_hex("#aaaaaa"),
        size_hint_y=None, height=25,
    )
    parent.add_widget(instructions)

    grid = GridLayout(cols=2, size_hint_y=None, height=100, spacing=8, padding=(0, 10))
    grid.add_widget(Label(text="Input type:"))
    system_spinner = Spinner(text=SYSTEMS[0], values=SYSTEMS, background_color=get_color_from_hex("#16213e"))
    grid.add_widget(system_spinner)

    grid.add_widget(Label(text="Value:"))
    value_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
    grid.add_widget(value_input)
    parent.add_widget(grid)

    results_label = Label(
        text="", font_size=16, bold=True,
        color=get_color_from_hex("#00ff9d"), size_hint_y=None, height=140,
        halign="left", valign="top",
    )
    results_label.bind(width=lambda *a: results_label.setter("text_size")(results_label, (results_label.width, None)))
    parent.add_widget(results_label)

    def show_result_text(text):
        results_label.text = text

    def convert_number(*_):
        raw_value = value_input.text.strip()
        system = system_spinner.text

        if raw_value == "":
            show_result_text("Please enter a value.")
            return

        try:
            if system == "Decimal":
                decimal_value = int(raw_value)
            elif system == "Binary":
                decimal_value = int(raw_value, 2)
            elif system == "Octal":
                decimal_value = int(raw_value, 8)
            else:  # Hexadecimal
                decimal_value = int(raw_value, 16)

            if decimal_value < 0:
                show_result_text("Please enter a positive whole number.")
                return

        except ValueError:
            show_result_text(
                f"Invalid {system} value: '{raw_value}'\n"
                f"Please check the digits match the {system} number system."
            )
            return

        binary_str = bin(decimal_value)[2:]
        octal_str = oct(decimal_value)[2:]
        hex_str = hex(decimal_value)[2:].upper()

        result_text = (
            f"Decimal:      {decimal_value}\n"
            f"Binary:       {binary_str}\n"
            f"Octal:        {octal_str}\n"
            f"Hexadecimal:  {hex_str}\n"
        )
        show_result_text(result_text)

    convert_btn = Button(
        text="Convert", size_hint_y=None, height=48,
        background_normal="", background_color=get_color_from_hex("#3498db"),
        color=get_color_from_hex("#ffffff"), bold=True,
    )
    convert_btn.bind(on_release=convert_number)
    parent.add_widget(convert_btn)