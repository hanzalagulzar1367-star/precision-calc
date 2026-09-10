"""
Kivy version of simple_calculator.py
Mirrors the logic of the original CustomTkinter simple calculator.
"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex


def build_simple_calculator(parent):
    """
    Builds the Simple Calculator UI and adds it to 'parent'
    (parent is expected to be a Kivy BoxLayout / container widget).
    """

    state = {"display": "0"}

    display = Label(
        text=state["display"],
        font_size=34,
        bold=True,
        color=get_color_from_hex("#ffffff"),
        size_hint_y=None,
        height=80,
        halign="right",
        valign="middle",
    )
    display.bind(size=lambda *a: setattr(display, "text_size", display.size))
    parent.add_widget(display)

    def refresh():
        display.text = state["display"]

    def press_number(char):
        current = state["display"]
        if current in ("0", "Error"):
            state["display"] = char
        else:
            state["display"] = current + char
        refresh()

    def press_operator(op):
        current = state["display"]
        if current == "Error" or "Error" in current:
            state["display"] = op
        else:
            state["display"] = current + op
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

    def percentage(*_):
        try:
            current = float(state["display"])
            state["display"] = str(current / 100)
        except Exception:
            state["display"] = "Error"
        refresh()

    def power(*_):
        press_operator("**")

    def square(*_):
        try:
            current = float(state["display"])
            state["display"] = str(current ** 2)
        except Exception:
            state["display"] = "Error"
        refresh()

    def square_root(*_):
        try:
            current = float(state["display"])
            if current < 0:
                state["display"] = "Error"
            else:
                state["display"] = str(current ** 0.5)
        except Exception:
            state["display"] = "Error"
        refresh()

    grid = GridLayout(cols=4, spacing=6, padding=6)

    button_rows = [
        [("C", clear_all), ("<-", backspace), ("%", percentage), ("/", lambda *_: press_operator("/"))],
        [("7", lambda *_: press_number("7")), ("8", lambda *_: press_number("8")), ("9", lambda *_: press_number("9")), ("*", lambda *_: press_operator("*"))],
        [("4", lambda *_: press_number("4")), ("5", lambda *_: press_number("5")), ("6", lambda *_: press_number("6")), ("-", lambda *_: press_operator("-"))],
        [("1", lambda *_: press_number("1")), ("2", lambda *_: press_number("2")), ("3", lambda *_: press_number("3")), ("+", lambda *_: press_operator("+"))],
        [("x^2", square), ("sqrt", square_root), ("x^y", power), ("=", calculate)],
        [("0", lambda *_: press_number("0")), (".", lambda *_: press_number(".")), ("", None), ("", None)],
    ]

    for row in button_rows:
        for label, action in row:
            if label == "":
                grid.add_widget(Label(text=""))
                continue
            btn = Button(
                text=label,
                font_size=18,
                background_normal="",
                background_color=get_color_from_hex("#16213e"),
                color=get_color_from_hex("#ffffff"),
            )
            if action:
                btn.bind(on_release=action)
            grid.add_widget(btn)

    parent.add_widget(grid)