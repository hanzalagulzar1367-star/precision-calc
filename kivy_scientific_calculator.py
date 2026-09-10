"""
Kivy version of scientific_calculator.py
Mirrors the logic of the original CustomTkinter scientific calculator.
"""

import math

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex


def build_scientific_calculator(parent):
    state = {"display": "0", "angle_mode": "DEG"}

    display = Label(
        text=state["display"],
        font_size=30,
        bold=True,
        color=get_color_from_hex("#ffffff"),
        size_hint_y=None,
        height=70,
        halign="right",
        valign="middle",
    )
    display.bind(size=lambda *a: setattr(display, "text_size", display.size))
    parent.add_widget(display)

    mode_label = Label(
        text=state["angle_mode"],
        font_size=13,
        bold=True,
        color=get_color_from_hex("#e94560"),
        size_hint_y=None,
        height=25,
        halign="right",
    )
    mode_label.bind(size=lambda *a: setattr(mode_label, "text_size", mode_label.size))
    parent.add_widget(mode_label)

    def refresh():
        display.text = state["display"]
        mode_label.text = state["angle_mode"]

    def press_number(char):
        current = state["display"]
        if current in ("0", "Error"):
            state["display"] = char
        else:
            state["display"] = current + char
        refresh()

    def clear_all(*_):
        state["display"] = "0"
        refresh()

    def backspace(*_):
        current = state["display"]
        if len(current) <= 1 or current == "Error":
            state["display"] = "0"
        else:
            state["display"] = current[:-1]
        refresh()

    def press_operator(op):
        current = state["display"]
        if current == "Error" or "Error" in current:
            state["display"] = op
        else:
            state["display"] = current + op
        refresh()

    def calculate(*_):
        expression = state["display"]
        try:
            safe_expression = expression.replace("×", "*").replace("÷", "/")
            allowed_chars = "0123456789+-*/.() "
            if not all(c in allowed_chars for c in safe_expression):
                state["display"] = "Error"
                refresh()
                return
            result = eval(safe_expression)
            state["display"] = str(result)
        except ZeroDivisionError:
            state["display"] = "Error: Div by 0"
        except Exception:
            state["display"] = "Error"
        refresh()

    def get_current_number():
        try:
            return float(state["display"])
        except Exception:
            return None

    def to_radians_if_needed(value):
        if state["angle_mode"] == "DEG":
            return math.radians(value)
        return value

    def apply_sin(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
        else:
            state["display"] = str(math.sin(to_radians_if_needed(num)))
        refresh()

    def apply_cos(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
        else:
            state["display"] = str(math.cos(to_radians_if_needed(num)))
        refresh()

    def apply_tan(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
        else:
            state["display"] = str(math.tan(to_radians_if_needed(num)))
        refresh()

    def apply_asin(*_):
        num = get_current_number()
        if num is None or num < -1 or num > 1:
            state["display"] = "Error"
            refresh()
            return
        result = math.asin(num)
        if state["angle_mode"] == "DEG":
            result = math.degrees(result)
        state["display"] = str(result)
        refresh()

    def apply_acos(*_):
        num = get_current_number()
        if num is None or num < -1 or num > 1:
            state["display"] = "Error"
            refresh()
            return
        result = math.acos(num)
        if state["angle_mode"] == "DEG":
            result = math.degrees(result)
        state["display"] = str(result)
        refresh()

    def apply_atan(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
            refresh()
            return
        result = math.atan(num)
        if state["angle_mode"] == "DEG":
            result = math.degrees(result)
        state["display"] = str(result)
        refresh()

    def apply_log(*_):
        num = get_current_number()
        if num is None or num <= 0:
            state["display"] = "Error"
        else:
            state["display"] = str(math.log10(num))
        refresh()

    def apply_ln(*_):
        num = get_current_number()
        if num is None or num <= 0:
            state["display"] = "Error"
        else:
            state["display"] = str(math.log(num))
        refresh()

    def apply_sqrt(*_):
        num = get_current_number()
        if num is None or num < 0:
            state["display"] = "Error"
        else:
            state["display"] = str(math.sqrt(num))
        refresh()

    def apply_square(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
        else:
            state["display"] = str(num ** 2)
        refresh()

    def apply_power(*_):
        press_operator("**")

    def apply_pi(*_):
        state["display"] = str(math.pi)
        refresh()

    def apply_e(*_):
        state["display"] = str(math.e)
        refresh()

    def apply_factorial(*_):
        num = get_current_number()
        if num is None or num < 0 or num != int(num):
            state["display"] = "Error"
        else:
            state["display"] = str(math.factorial(int(num)))
        refresh()

    def apply_abs(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
        else:
            state["display"] = str(abs(num))
        refresh()

    def apply_exp(*_):
        num = get_current_number()
        if num is None:
            state["display"] = "Error"
        else:
            state["display"] = str(math.exp(num))
        refresh()

    def toggle_angle_mode(*_):
        state["angle_mode"] = "RAD" if state["angle_mode"] == "DEG" else "DEG"
        refresh()

    buttons_container = BoxLayout(orientation="vertical", spacing=4)

    button_rows = [
        [("sin", apply_sin), ("cos", apply_cos), ("tan", apply_tan), ("DEG/RAD", toggle_angle_mode)],
        [("asin", apply_asin), ("acos", apply_acos), ("atan", apply_atan), ("n!", apply_factorial)],
        [("log", apply_log), ("ln", apply_ln), ("pi", apply_pi), ("e", apply_e)],
        [("sqrt", apply_sqrt), ("x^2", apply_square), ("x^y", apply_power), ("exp", apply_exp)],
        [("C", clear_all), ("<-", backspace), ("|x|", apply_abs), ("/", lambda *_: press_operator("/"))],
        [("7", lambda *_: press_number("7")), ("8", lambda *_: press_number("8")), ("9", lambda *_: press_number("9")), ("*", lambda *_: press_operator("*"))],
        [("4", lambda *_: press_number("4")), ("5", lambda *_: press_number("5")), ("6", lambda *_: press_number("6")), ("-", lambda *_: press_operator("-"))],
        [("1", lambda *_: press_number("1")), ("2", lambda *_: press_number("2")), ("3", lambda *_: press_number("3")), ("+", lambda *_: press_operator("+"))],
        [("0", lambda *_: press_number("0")), (".", lambda *_: press_number(".")), ("=", calculate), ("", None)],
    ]

    for row in button_rows:
        row_layout = GridLayout(cols=4, spacing=3, size_hint_y=None, height=42)
        for label, action in row:
            if label == "":
                row_layout.add_widget(Label(text=""))
                continue
            btn = Button(
                text=label,
                font_size=13,
                background_normal="",
                background_color=get_color_from_hex("#16213e"),
                color=get_color_from_hex("#ffffff"),
            )
            if action:
                btn.bind(on_release=action)
            row_layout.add_widget(btn)
        buttons_container.add_widget(row_layout)

    parent.add_widget(buttons_container)