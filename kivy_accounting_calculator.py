"""
Kivy version of accounting_calculator.py
Includes: Profit & Loss, Interest, Break-Even, Depreciation, Markup/Margin
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.utils import get_color_from_hex

BG_MAIN = "#0f0f1a"
CARD_BG = "#131c26"
ACCENT = "#00d9ff"
TEXT_MAIN = "#e0e6f0"
TEXT_SUB = "#c8d6e5"
ENTRY_BG = "#1a1a2e"
GREEN = "#3ddc97"
RED = "#ff5c5c"


def _make_card(parent):
    """Create a card-style container"""
    card = BoxLayout(
        orientation="vertical",
        padding=15,
        spacing=10,
        size_hint_y=None,
    )
    card.bind(minimum_height=card.setter("height"))
    parent.add_widget(card)
    return card


def _add_label(card, text, font_size=18, bold=True, color=ACCENT):
    """Add a label to a card"""
    lbl = Label(
        text=text,
        font_size=font_size,
        bold=bold,
        color=get_color_from_hex(color),
        size_hint_y=None,
        height=40,
        halign="left",
    )
    lbl.bind(width=lambda *a: lbl.setter("text_size")(lbl, (lbl.width, None)))
    card.add_widget(lbl)
    return lbl


def _field(card, label_text, default=""):
    """Create a labeled input field"""
    row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
    row.add_widget(Label(
        text=label_text,
        font_size=13,
        color=get_color_from_hex(TEXT_SUB),
        size_hint_x=0.4,
        halign="left",
    ))
    entry = TextInput(
        multiline=False,
        background_color=get_color_from_hex(ENTRY_BG),
        foreground_color=get_color_from_hex(TEXT_MAIN),
        size_hint_x=0.6,
        font_size=14,
    )
    if default:
        entry.text = default
    row.add_widget(entry)
    card.add_widget(row)
    return entry


def _result_label(card):
    """Create a result label"""
    lbl = Label(
        text="",
        font_size=16,
        bold=True,
        color=get_color_from_hex(ACCENT),
        size_hint_y=None,
        height=60,
        halign="left",
        valign="middle",
    )
    lbl.bind(width=lambda *a: lbl.setter("text_size")(lbl, (lbl.width, None)))
    card.add_widget(lbl)
    return lbl


def _safe_float(entry, default=0.0):
    """Safely convert entry text to float"""
    try:
        return float(entry.text.strip())
    except (ValueError, TypeError):
        return default


def _button(card, text, command):
    """Create a button"""
    btn = Button(
        text=text,
        font_size=14,
        bold=True,
        size_hint_y=None,
        height=42,
        background_normal="",
        background_color=get_color_from_hex(ACCENT),
        color=get_color_from_hex("#0a0a12"),
    )
    btn.bind(on_release=command)
    card.add_widget(btn)
    return btn


# ─────────────────────────────────────────────────────────────
# 1. PROFIT & LOSS
# ─────────────────────────────────────────────────────────────
def _build_profit_loss(parent):
    card = _make_card(parent)
    _add_label(card, "📈 Profit & Loss Calculator")

    cp = _field(card, "Cost Price (CP)")
    sp = _field(card, "Selling Price (SP)")
    result = _result_label(card)

    def calculate(*_):
        c, s = _safe_float(cp), _safe_float(sp)
        diff = s - c
        if c == 0:
            result.text = "Enter a valid non-zero Cost Price."
            result.color = get_color_from_hex(RED)
            return
        pct = (diff / c) * 100
        if diff > 0:
            result.text = f"✅ Profit: {diff:,.2f}   ({pct:,.2f}%)"
            result.color = get_color_from_hex(GREEN)
        elif diff < 0:
            result.text = f"🔻 Loss: {abs(diff):,.2f}   ({abs(pct):,.2f}%)"
            result.color = get_color_from_hex(RED)
        else:
            result.text = "⚖️ No Profit, No Loss"
            result.color = get_color_from_hex(TEXT_SUB)

    _button(card, "Calculate", calculate)


# ─────────────────────────────────────────────────────────────
# 2. INTEREST CALCULATOR (Simple + Compound)
# ─────────────────────────────────────────────────────────────
def _build_interest(parent):
    card = _make_card(parent)
    _add_label(card, "💰 Interest Calculator")

    principal = _field(card, "Principal Amount")
    rate = _field(card, "Annual Rate (%)")
    time_ = _field(card, "Time (years)")

    # Interest type dropdown
    row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
    row.add_widget(Label(
        text="Interest Type",
        font_size=13,
        color=get_color_from_hex(TEXT_SUB),
        size_hint_x=0.4,
        halign="left",
    ))
    interest_type = Spinner(
        text="Simple Interest",
        values=["Simple Interest", "Compound Interest"],
        background_color=get_color_from_hex(ENTRY_BG),
        color=get_color_from_hex(TEXT_MAIN),
        size_hint_x=0.6,
    )
    row.add_widget(interest_type)
    card.add_widget(row)

    # Compounds per year
    row2 = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
    row2.add_widget(Label(
        text="Compounds / Year",
        font_size=13,
        color=get_color_from_hex(TEXT_SUB),
        size_hint_x=0.4,
        halign="left",
    ))
    n_compound = TextInput(
        multiline=False,
        text="1",
        background_color=get_color_from_hex(ENTRY_BG),
        foreground_color=get_color_from_hex(TEXT_MAIN),
        size_hint_x=0.6,
        font_size=14,
    )
    row2.add_widget(n_compound)
    card.add_widget(row2)

    result = _result_label(card)

    def calculate(*_):
        p, r, t = _safe_float(principal), _safe_float(rate), _safe_float(time_)
        n = _safe_float(n_compound, 1) or 1
        if interest_type.text == "Simple Interest":
            interest = (p * r * t) / 100
        else:
            interest = p * ((1 + (r / 100) / n) ** (n * t)) - p
        total = p + interest
        result.text = f"Interest Earned: {interest:,.2f}\nTotal Amount: {total:,.2f}"
        result.color = get_color_from_hex(GREEN)

    _button(card, "Calculate", calculate)


# ─────────────────────────────────────────────────────────────
# 3. BREAK-EVEN POINT
# ─────────────────────────────────────────────────────────────
def _build_breakeven(parent):
    card = _make_card(parent)
    _add_label(card, "⚖️ Break-Even Point")

    fixed = _field(card, "Fixed Costs")
    price = _field(card, "Selling Price / Unit")
    var_cost = _field(card, "Variable Cost / Unit")
    result = _result_label(card)

    def calculate(*_):
        f, p, v = _safe_float(fixed), _safe_float(price), _safe_float(var_cost)
        contribution = p - v
        if contribution <= 0:
            result.text = "Selling price must be greater than variable cost."
            result.color = get_color_from_hex(RED)
            return
        units = f / contribution
        revenue = units * p
        result.text = f"Break-Even Units: {units:,.2f}\nBreak-Even Revenue: {revenue:,.2f}"
        result.color = get_color_from_hex(GREEN)

    _button(card, "Calculate", calculate)


# ─────────────────────────────────────────────────────────────
# 4. DEPRECIATION (Straight Line)
# ─────────────────────────────────────────────────────────────
def _build_depreciation(parent):
    card = _make_card(parent)
    _add_label(card, "📉 Straight-Line Depreciation")

    cost = _field(card, "Asset Cost")
    salvage = _field(card, "Salvage Value")
    life = _field(card, "Useful Life (years)")
    result = _result_label(card)

    def calculate(*_):
        c, s, life_years = _safe_float(cost), _safe_float(salvage), _safe_float(life)
        if life_years <= 0:
            result.text = "Useful life must be greater than 0."
            result.color = get_color_from_hex(RED)
            return
        annual_dep = (c - s) / life_years
        rate = (annual_dep / c) * 100 if c else 0
        result.text = f"Annual Depreciation: {annual_dep:,.2f}\nDepreciation Rate: {rate:,.2f}% / year"
        result.color = get_color_from_hex(GREEN)

    _button(card, "Calculate", calculate)


# ─────────────────────────────────────────────────────────────
# 5. MARKUP / MARGIN
# ─────────────────────────────────────────────────────────────
def _build_markup_margin(parent):
    card = _make_card(parent)
    _add_label(card, "🏷️ Markup / Margin Calculator")

    cost = _field(card, "Cost Price")

    # Mode dropdown
    row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
    row.add_widget(Label(
        text="Calculate By",
        font_size=13,
        color=get_color_from_hex(TEXT_SUB),
        size_hint_x=0.4,
        halign="left",
    ))
    mode = Spinner(
        text="Markup %",
        values=["Markup %", "Margin %"],
        background_color=get_color_from_hex(ENTRY_BG),
        color=get_color_from_hex(TEXT_MAIN),
        size_hint_x=0.6,
    )
    row.add_widget(mode)
    card.add_widget(row)

    pct_entry = _field(card, "Percentage (%)")
    result = _result_label(card)

    def calculate(*_):
        c, pct = _safe_float(cost), _safe_float(pct_entry)
        if mode.text == "Markup %":
            sp = c * (1 + pct / 100)
            margin_pct = ((sp - c) / sp) * 100 if sp else 0
            result.text = f"Selling Price: {sp:,.2f}\nEquivalent Margin: {margin_pct:,.2f}%"
            result.color = get_color_from_hex(GREEN)
        else:  # Margin %
            if pct >= 100:
                result.text = "Margin % must be less than 100."
                result.color = get_color_from_hex(RED)
                return
            sp = c / (1 - pct / 100)
            markup_pct = ((sp - c) / c) * 100 if c else 0
            result.text = f"Selling Price: {sp:,.2f}\nEquivalent Markup: {markup_pct:,.2f}%"
            result.color = get_color_from_hex(GREEN)

    _button(card, "Calculate", calculate)


# ─────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────
def build_accounting_calculator(parent):
    """
    Build the Accounting Calculator with tabs for each feature.
    """
    # Title
    title = Label(
        text="🧾 Accounting Calculator",
        font_size=26,
        bold=True,
        color=get_color_from_hex(ACCENT),
        size_hint_y=None,
        height=50,
        halign="center",
    )
    title.bind(width=lambda *a: title.setter("text_size")(title, (title.width, None)))
    parent.add_widget(title)

    # Tab Panel
    tab_panel = TabbedPanel(
        size_hint=(1, 1),
        do_default_tab=False,
        background_color=get_color_from_hex(BG_MAIN),
        tab_width=120,
        tab_height=40,
    )
    tab_panel.bind(width=lambda *a: setattr(tab_panel, "size", tab_panel.size))

    # Create tabs
    tabs = [
        ("Profit & Loss", _build_profit_loss),
        ("Interest", _build_interest),
        ("Break-Even", _build_breakeven),
        ("Depreciation", _build_depreciation),
        ("Markup/Margin", _build_markup_margin),
    ]

    for tab_name, builder in tabs:
        tab = TabbedPanelItem(text=tab_name)
        tab.content = BoxLayout(orientation="vertical", padding=5, spacing=5)
        scroll = ScrollView(size_hint=(1, 1))
        content_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=5)
        content_box.bind(minimum_height=content_box.setter("height"))
        builder(content_box)
        scroll.add_widget(content_box)
        tab.content.add_widget(scroll)
        tab_panel.add_widget(tab)

    parent.add_widget(tab_panel)


# ─────────────────────────────────────────────────────────────
# TESTING (if run directly)
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout

    class TestApp(App):
        def build(self):
            root = BoxLayout(orientation="vertical")
            build_accounting_calculator(root)
            return root

    TestApp().run()