"""
Kivy version of engineering_calculator.py
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex

SECTIONS = ["Ohm's Law", "Electrical Power", "Series Resistance", "Parallel Resistance"]


def build_engineering_calculator(parent):
    title = Label(
        text="Engineering Calculator", font_size=22, bold=True,
        color=get_color_from_hex("#e67e22"), size_hint_y=None, height=40,
    )
    parent.add_widget(title)

    section_spinner = Spinner(
        text=SECTIONS[0], values=SECTIONS,
        size_hint_y=None, height=44,
        background_color=get_color_from_hex("#16213e"),
    )
    parent.add_widget(section_spinner)

    content_area = BoxLayout(orientation="vertical", spacing=8, padding=(0, 10))
    parent.add_widget(content_area)

    def clear_content():
        content_area.clear_widgets()

    def add_info(text):
        lbl = Label(
            text=text, font_size=13, color=get_color_from_hex("#aaaaaa"),
            size_hint_y=None, height=50, halign="left",
        )
        lbl.bind(width=lambda *a: lbl.setter("text_size")(lbl, (lbl.width, None)))
        content_area.add_widget(lbl)

    def add_result_label():
        result_label = Label(
            text="", font_size=17, bold=True,
            color=get_color_from_hex("#00ff9d"), size_hint_y=None, height=50,
        )
        content_area.add_widget(result_label)
        return result_label

    def add_calc_button(callback):
        btn = Button(
            text="Calculate", size_hint_y=None, height=46,
            background_normal="", background_color=get_color_from_hex("#e67e22"),
            color=get_color_from_hex("#ffffff"), bold=True,
        )
        btn.bind(on_release=callback)
        content_area.add_widget(btn)

    def build_ohms_law():
        clear_content()
        add_info("Ohm's Law: Voltage (V) = Current (I) x Resistance (R)\nFill in any 2 values, leave the one you want to find empty.")

        grid = GridLayout(cols=2, size_hint_y=None, height=150, spacing=6)
        grid.add_widget(Label(text="Voltage (V):"))
        v_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        grid.add_widget(v_input)
        grid.add_widget(Label(text="Current (I):"))
        i_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        grid.add_widget(i_input)
        grid.add_widget(Label(text="Resistance (R):"))
        r_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        grid.add_widget(r_input)
        content_area.add_widget(grid)

        result_label = add_result_label()

        def calculate_ohms(*_):
            v_text, i_text, r_text = v_input.text.strip(), i_input.text.strip(), r_input.text.strip()
            filled = [x for x in [v_text, i_text, r_text] if x != ""]
            if len(filled) != 2:
                result_label.text = "Please fill exactly 2 fields, leave 1 empty."
                return
            try:
                if v_text == "":
                    result_label.text = f"Voltage = {float(i_text) * float(r_text)} V"
                elif i_text == "":
                    r_val = float(r_text)
                    if r_val == 0:
                        result_label.text = "Error: Resistance can't be 0 (division by zero)"
                        return
                    result_label.text = f"Current = {float(v_text) / r_val} A"
                elif r_text == "":
                    i_val = float(i_text)
                    if i_val == 0:
                        result_label.text = "Error: Current can't be 0 (division by zero)"
                        return
                    result_label.text = f"Resistance = {float(v_text) / i_val} ohm"
            except ValueError:
                result_label.text = "Please enter valid numbers only."

        add_calc_button(calculate_ohms)

    def build_power():
        clear_content()
        add_info("Power: P = V x I\nFill in any 2 values, leave the one you want to find empty.")

        grid = GridLayout(cols=2, size_hint_y=None, height=150, spacing=6)
        grid.add_widget(Label(text="Power (P):"))
        p_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        grid.add_widget(p_input)
        grid.add_widget(Label(text="Voltage (V):"))
        v_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        grid.add_widget(v_input)
        grid.add_widget(Label(text="Current (I):"))
        i_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        grid.add_widget(i_input)
        content_area.add_widget(grid)

        result_label = add_result_label()

        def calculate_power(*_):
            p_text, v_text, i_text = p_input.text.strip(), v_input.text.strip(), i_input.text.strip()
            filled = [x for x in [p_text, v_text, i_text] if x != ""]
            if len(filled) != 2:
                result_label.text = "Please fill exactly 2 fields, leave 1 empty."
                return
            try:
                if p_text == "":
                    result_label.text = f"Power = {float(v_text) * float(i_text)} W"
                elif v_text == "":
                    i_val = float(i_text)
                    if i_val == 0:
                        result_label.text = "Error: Current can't be 0 (division by zero)"
                        return
                    result_label.text = f"Voltage = {float(p_text) / i_val} V"
                elif i_text == "":
                    v_val = float(v_text)
                    if v_val == 0:
                        result_label.text = "Error: Voltage can't be 0 (division by zero)"
                        return
                    result_label.text = f"Current = {float(p_text) / v_val} A"
            except ValueError:
                result_label.text = "Please enter valid numbers only."

        add_calc_button(calculate_power)

    def build_series_resistance():
        clear_content()
        add_info("Series Resistance: R_total = R1 + R2 + R3 + ...\nEnter resistor values separated by commas.")

        grid = GridLayout(cols=1, size_hint_y=None, height=80, spacing=6)
        grid.add_widget(Label(text="Resistors (Ω):"))
        r_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        r_input.text = "100, 220, 330"
        grid.add_widget(r_input)
        content_area.add_widget(grid)

        result_label = add_result_label()

        def calculate_series(*_):
            raw = r_input.text.strip()
            if not raw:
                result_label.text = "Please enter resistor values."
                return
            try:
                resistors = [float(x.strip()) for x in raw.split(",") if x.strip()]
                if not resistors:
                    result_label.text = "No valid resistor values found."
                    return
                total = sum(resistors)
                result_label.text = f"R_total = {total} Ω"
            except ValueError:
                result_label.text = "Please enter valid numbers separated by commas."

        add_calc_button(calculate_series)

    def build_parallel_resistance():
        clear_content()
        add_info("Parallel Resistance: 1/R_total = 1/R1 + 1/R2 + ...\nEnter resistor values separated by commas.")

        grid = GridLayout(cols=1, size_hint_y=None, height=80, spacing=6)
        grid.add_widget(Label(text="Resistors (Ω):"))
        r_input = TextInput(multiline=False, background_color=get_color_from_hex("#1a1a2e"))
        r_input.text = "100, 220, 330"
        grid.add_widget(r_input)
        content_area.add_widget(grid)

        result_label = add_result_label()

        def calculate_parallel(*_):
            raw = r_input.text.strip()
            if not raw:
                result_label.text = "Please enter resistor values."
                return
            try:
                resistors = [float(x.strip()) for x in raw.split(",") if x.strip()]
                if not resistors:
                    result_label.text = "No valid resistor values found."
                    return
                reciprocal_sum = sum(1.0 / r for r in resistors)
                total = 1.0 / reciprocal_sum
                result_label.text = f"R_total = {total} Ω"
            except ValueError:
                result_label.text = "Please enter valid numbers separated by commas."

        add_calc_button(calculate_parallel)

    # Build the default section
    build_ohms_law()

    # Section change handler
    def on_section_change(spinner, text):
        if text == "Ohm's Law":
            build_ohms_law()
        elif text == "Electrical Power":
            build_power()
        elif text == "Series Resistance":
            build_series_resistance()
        elif text == "Parallel Resistance":
            build_parallel_resistance()

    section_spinner.bind(text=on_section_change)