"""
Kivy version of statistical_calculator.py
"""

import statistics

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex


def build_statistical_calculator(parent):
    title = Label(
        text="Statistical Calculator",
        font_size=22,
        bold=True,
        color=get_color_from_hex("#f5a623"),
        size_hint_y=None,
        height=40,
    )
    parent.add_widget(title)

    instructions = Label(
        text="Enter numbers separated by commas, e.g. 10, 20, 30, 40, 50",
        font_size=13,
        color=get_color_from_hex("#aaaaaa"),
        size_hint_y=None,
        height=25,
    )
    parent.add_widget(instructions)

    input_box = TextInput(
        size_hint_y=None,
        height=80,
        background_color=get_color_from_hex("#1a1a2e"),
        foreground_color=get_color_from_hex("#ffffff"),
        font_size=15,
        multiline=True,
    )
    parent.add_widget(input_box)

    results_label = Label(
        text="",
        font_size=14,
        color=get_color_from_hex("#00ff9d"),
        size_hint_y=None,
        halign="left",
        valign="top",
    )
    results_label.bind(width=lambda *a: results_label.setter("text_size")(results_label, (results_label.width, None)))
    results_label.bind(texture_size=lambda *a: setattr(results_label, "height", results_label.texture_size[1]))

    scroll = ScrollView(size_hint=(1, 1))
    scroll.add_widget(results_label)
    parent.add_widget(scroll)

    def show_result_text(text):
        results_label.text = text

    def calculate_stats(*_):
        raw_text = input_box.text.strip()

        if not raw_text:
            show_result_text("Please enter some numbers first.")
            return

        parts = raw_text.split(",")
        numbers = []
        for part in parts:
            part = part.strip()
            if part == "":
                continue
            try:
                numbers.append(float(part))
            except ValueError:
                show_result_text(f"Invalid number found: '{part}'\nPlease only enter numbers separated by commas.")
                return

        if len(numbers) == 0:
            show_result_text("No valid numbers found. Please enter numbers like: 10, 20, 30")
            return

        try:
            mean_val = statistics.mean(numbers)
        except Exception:
            mean_val = "N/A"

        try:
            median_val = statistics.median(numbers)
        except Exception:
            median_val = "N/A"

        try:
            mode_val = statistics.mode(numbers)
        except statistics.StatisticsError:
            mode_val = "No unique mode"

        minimum = min(numbers)
        maximum = max(numbers)
        range_val = maximum - minimum
        total_sum = sum(numbers)
        count = len(numbers)

        try:
            variance_val = statistics.variance(numbers) if count > 1 else "N/A (need 2+ numbers)"
        except Exception:
            variance_val = "N/A"

        try:
            stdev_val = statistics.stdev(numbers) if count > 1 else "N/A (need 2+ numbers)"
        except Exception:
            stdev_val = "N/A"

        try:
            quartiles = statistics.quantiles(numbers, n=4) if count >= 2 else None
            if quartiles:
                q1, q2, q3 = quartiles[0], quartiles[1], quartiles[2]
                iqr = q3 - q1
            else:
                q1 = q2 = q3 = iqr = "N/A"
        except Exception:
            q1 = q2 = q3 = iqr = "N/A"

        result_text = (
            f"Count:              {count}\n"
            f"Sum:                {total_sum}\n"
            f"Mean:               {mean_val}\n"
            f"Median:             {median_val}\n"
            f"Mode:               {mode_val}\n"
            f"Minimum:            {minimum}\n"
            f"Maximum:            {maximum}\n"
            f"Range:              {range_val}\n"
            f"Variance:           {variance_val}\n"
            f"Std Deviation:      {stdev_val}\n"
            f"Q1 (25th pct):      {q1}\n"
            f"Q2 / Median:        {q2}\n"
            f"Q3 (75th pct):      {q3}\n"
            f"IQR (Q3 - Q1):      {iqr}\n"
        )
        show_result_text(result_text)

    def clear_all(*_):
        input_box.text = ""
        show_result_text("")

    button_row = BoxLayout(size_hint_y=None, height=50, spacing=10)

    calc_btn = Button(
        text="Calculate",
        background_normal="",
        background_color=get_color_from_hex("#f5a623"),
        color=get_color_from_hex("#1a1a2e"),
        bold=True,
    )
    calc_btn.bind(on_release=calculate_stats)
    button_row.add_widget(calc_btn)

    clear_btn = Button(
        text="Clear",
        background_normal="",
        background_color=get_color_from_hex("#16213e"),
        color=get_color_from_hex("#ffffff"),
        bold=True,
    )
    clear_btn.bind(on_release=clear_all)
    button_row.add_widget(clear_btn)

    parent.add_widget(button_row)