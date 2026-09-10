"""
Kivy version of currency_converter.py with 160+ world currencies
Network calls run in a background thread so the UI doesn't freeze.
"""

import json
import threading
import urllib.request
import urllib.error

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex

# Free API - no key required
API_URL = "https://open.er-api.com/v6/latest/{base}"

# 160+ World Currencies (ISO 4217)
CURRENCIES = {
    "AED": "UAE Dirham", "AFN": "Afghan Afghani", "ALL": "Albanian Lek",
    "AMD": "Armenian Dram", "ANG": "Neth. Antillean Guilder", "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso", "AUD": "Australian Dollar", "AWG": "Aruban Florin",
    "AZN": "Azerbaijani Manat", "BAM": "Bosnia-Herzegovina Mark", "BBD": "Barbadian Dollar",
    "BDT": "Bangladeshi Taka", "BGN": "Bulgarian Lev", "BHD": "Bahraini Dinar",
    "BIF": "Burundian Franc", "BMD": "Bermudan Dollar", "BND": "Brunei Dollar",
    "BOB": "Bolivian Boliviano", "BRL": "Brazilian Real", "BSD": "Bahamian Dollar",
    "BTN": "Bhutanese Ngultrum", "BWP": "Botswanan Pula", "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar", "CAD": "Canadian Dollar", "CDF": "Congolese Franc",
    "CHF": "Swiss Franc", "CLP": "Chilean Peso", "CNY": "Chinese Yuan",
    "COP": "Colombian Peso", "CRC": "Costa Rican Colón", "CUP": "Cuban Peso",
    "CVE": "Cape Verdean Escudo", "CZK": "Czech Koruna", "DJF": "Djiboutian Franc",
    "DKK": "Danish Krone", "DOP": "Dominican Peso", "DZD": "Algerian Dinar",
    "EGP": "Egyptian Pound", "ERN": "Eritrean Nakfa", "ETB": "Ethiopian Birr",
    "EUR": "Euro", "FJD": "Fijian Dollar", "FKP": "Falkland Islands Pound",
    "GBP": "British Pound", "GEL": "Georgian Lari", "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound", "GMD": "Gambian Dalasi", "GNF": "Guinean Franc",
    "GTQ": "Guatemalan Quetzal", "GYD": "Guyanaese Dollar", "HKD": "Hong Kong Dollar",
    "HNL": "Honduran Lempira", "HRK": "Croatian Kuna", "HTG": "Haitian Gourde",
    "HUF": "Hungarian Forint", "IDR": "Indonesian Rupiah", "ILS": "Israeli New Shekel",
    "INR": "Indian Rupee", "IQD": "Iraqi Dinar", "IRR": "Iranian Rial",
    "ISK": "Icelandic Króna", "JMD": "Jamaican Dollar", "JOD": "Jordanian Dinar",
    "JPY": "Japanese Yen", "KES": "Kenyan Shilling", "KGS": "Kyrgystani Som",
    "KHR": "Cambodian Riel", "KMF": "Comorian Franc", "KPW": "North Korean Won",
    "KRW": "South Korean Won", "KWD": "Kuwaiti Dinar", "KYD": "Cayman Islands Dollar",
    "KZT": "Kazakhstani Tenge", "LAK": "Laotian Kip", "LBP": "Lebanese Pound",
    "LKR": "Sri Lankan Rupee", "LRD": "Liberian Dollar", "LSL": "Lesotho Loti",
    "LYD": "Libyan Dinar", "MAD": "Moroccan Dirham", "MDL": "Moldovan Leu",
    "MGA": "Malagasy Ariary", "MKD": "Macedonian Denar", "MMK": "Myanma Kyat",
    "MNT": "Mongolian Tugrik", "MOP": "Macanese Pataca", "MRU": "Mauritanian Ouguiya",
    "MUR": "Mauritian Rupee", "MVR": "Maldivian Rufiyaa", "MWK": "Malawian Kwacha",
    "MXN": "Mexican Peso", "MYR": "Malaysian Ringgit", "MZN": "Mozambican Metical",
    "NAD": "Namibian Dollar", "NGN": "Nigerian Naira", "NIO": "Nicaraguan Córdoba",
    "NOK": "Norwegian Krone", "NPR": "Nepalese Rupee", "NZD": "New Zealand Dollar",
    "OMR": "Omani Rial", "PAB": "Panamanian Balboa", "PEN": "Peruvian Sol",
    "PGK": "Papua New Guinean Kina", "PHP": "Philippine Peso", "PKR": "Pakistani Rupee",
    "PLN": "Polish Zloty", "PYG": "Paraguayan Guarani", "QAR": "Qatari Rial",
    "RON": "Romanian Leu", "RSD": "Serbian Dinar", "RUB": "Russian Ruble",
    "RWF": "Rwandan Franc", "SAR": "Saudi Riyal", "SBD": "Solomon Islands Dollar",
    "SCR": "Seychellois Rupee", "SDG": "Sudanese Pound", "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar", "SHP": "Saint Helena Pound", "SLE": "Sierra Leonean Leone",
    "SOS": "Somali Shilling", "SRD": "Surinamese Dollar", "SSP": "South Sudanese Pound",
    "STN": "São Tomé Dobra", "SYP": "Syrian Pound", "SZL": "Eswatini Lilangeni",
    "THB": "Thai Baht", "TJS": "Tajikistani Somoni", "TMT": "Turkmenistani Manat",
    "TND": "Tunisian Dinar", "TOP": "Tongan Paʻanga", "TRY": "Turkish Lira",
    "TTD": "Trinidad & Tobago Dollar", "TWD": "New Taiwan Dollar", "TZS": "Tanzanian Shilling",
    "UAH": "Ukrainian Hryvnia", "UGX": "Ugandan Shilling", "USD": "US Dollar",
    "UYU": "Uruguayan Peso", "UZS": "Uzbekistan Som", "VES": "Venezuelan Bolívar",
    "VND": "Vietnamese Dong", "VUV": "Vanuatu Vatu", "WST": "Samoan Tala",
    "XAF": "Central African CFA Franc", "XCD": "East Caribbean Dollar",
    "XOF": "West African CFA Franc", "XPF": "CFP Franc",
    "YER": "Yemeni Rial", "ZAR": "South African Rand", "ZMW": "Zambian Kwacha",
    "ZWL": "Zimbabwean Dollar",
}

# Display strings: "USD - US Dollar"
CURRENCY_OPTIONS = [f"{code} - {name}" for code, name in sorted(CURRENCIES.items())]


def _code_from_option(option_str):
    return option_str.split(" - ")[0]


def build_currency_converter(parent):
    title = Label(
        text="Currency Converter", font_size=22, bold=True,
        color=get_color_from_hex("#1abc9c"), size_hint_y=None, height=40,
    )
    parent.add_widget(title)

    subtitle = Label(
        text="Live exchange rates for 160+ world currencies (requires internet)",
        font_size=12, color=get_color_from_hex("#aaaaaa"),
        size_hint_y=None, height=25,
    )
    parent.add_widget(subtitle)

    grid = GridLayout(cols=2, size_hint_y=None, height=170, spacing=8, padding=(0, 10))

    grid.add_widget(Label(text="From:"))
    from_spinner = Spinner(
        text=CURRENCY_OPTIONS[0],
        values=CURRENCY_OPTIONS,
        background_color=get_color_from_hex("#16213e")
    )
    grid.add_widget(from_spinner)

    grid.add_widget(Label(text="To:"))
    to_spinner = Spinner(
        text=CURRENCY_OPTIONS[CURRENCY_OPTIONS.index("PKR - Pakistani Rupee")] if "PKR - Pakistani Rupee" in CURRENCY_OPTIONS else CURRENCY_OPTIONS[1],
        values=CURRENCY_OPTIONS,
        background_color=get_color_from_hex("#16213e")
    )
    grid.add_widget(to_spinner)

    grid.add_widget(Label(text="Amount:"))
    value_input = TextInput(
        multiline=False,
        input_filter="float",
        background_color=get_color_from_hex("#1a1a2e")
    )
    value_input.text = "1"
    grid.add_widget(value_input)

    parent.add_widget(grid)

    result_label = Label(
        text="", font_size=17, bold=True,
        color=get_color_from_hex("#00ff9d"), size_hint_y=None, height=50,
    )
    parent.add_widget(result_label)

    status_label = Label(
        text="", font_size=12,
        color=get_color_from_hex("#e94560"), size_hint_y=None, height=30,
    )
    parent.add_widget(status_label)

    def set_status(text):
        status_label.text = text

    def set_result(text):
        result_label.text = text

    def fetch_rate(from_code, to_code, amount):
        """Runs in a background thread — must not touch widgets directly."""
        url = API_URL.format(base=from_code)
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())

            if data.get("result") != "success":
                Clock.schedule_once(lambda dt: (set_status("API error: Please try again"), set_result("")))
                return

            rates = data["rates"]
            rate = rates.get(to_code)
            if rate is None:
                Clock.schedule_once(lambda dt: (set_status(f"Rate not available for {to_code}"), set_result("")))
                return

            converted_amount = amount * rate

            def update_ui(dt):
                set_result(f"{amount} {from_code} = {converted_amount:.4f} {to_code}")
                set_status(f"Rate: 1 {from_code} = {rate:.6f} {to_code} | {data.get('time_last_update_utc', '')}")

            Clock.schedule_once(update_ui)

        except urllib.error.URLError:
            Clock.schedule_once(lambda dt: (set_status("No internet connection. Please check your network and try again."), set_result("")))
        except Exception as e:
            Clock.schedule_once(lambda dt: (set_status(f"Error: {str(e)[:50]}"), set_result("")))

    def do_conversion(*_):
        raw_value = value_input.text.strip()

        if raw_value == "":
            set_result("")
            set_status("Please enter an amount.")
            return

        try:
            amount = float(raw_value)
        except ValueError:
            set_result("")
            set_status("Invalid number. Please enter digits only.")
            return

        from_code = _code_from_option(from_spinner.text)
        to_code = _code_from_option(to_spinner.text)

        set_status("Fetching live rates...")
        threading.Thread(target=fetch_rate, args=(from_code, to_code, amount), daemon=True).start()

    convert_btn = Button(
        text="Convert", size_hint_y=None, height=48,
        background_normal="", background_color=get_color_from_hex("#1abc9c"),
        color=get_color_from_hex("#ffffff"), bold=True,
    )
    convert_btn.bind(on_release=do_conversion)
    parent.add_widget(convert_btn)