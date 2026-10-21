from datetime import datetime
from zoneinfo import ZoneInfo
import ast
import operator
import json
import requests

# ============================================================================
# 1. TIME, DATE, CALENDAR & TIMEZONES
# ============================================================================

def get_current_time(timezone_name: str = "") -> str:
    """Returns the current date and time. Optionally accepts a timezone name (e.g. 'UTC', 'Asia/Kolkata', 'America/New_York')."""
    try:
        if timezone_name:
            tz = ZoneInfo(timezone_name.strip())
            now = datetime.now(tz)
            return now.strftime("%Y-%m-%d %H:%M:%S (%Z %z)")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error resolving timezone '{timezone_name}': {e}. Current local time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# ============================================================================
# 2. WEATHER TOOL
# ============================================================================

def get_city_weather(city: str) -> str:
    """Returns live weather and temperature for a given city."""
    try:
        clean_city = city.strip()
        url = f"https://wttr.in/{clean_city}?format=3"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        return f"Could not retrieve weather for {clean_city} (Status: {response.status_code})"
    except Exception as e:
        return f"Error fetching weather for '{city}': {e}"


# ============================================================================
# 3. USER PROFILE & LOCATION (CHAIN TRIGGER)
# ============================================================================

def get_user_location() -> str:
    """Returns the simulated current location, country, and timezone of the user."""
    location_data = {
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
        "postal_code": "560001"
    }
    return json.dumps(location_data)


# ============================================================================
# 4. GEOGRAPHY & CAPITALS (CHAIN TRIGGER)
# ============================================================================

_CAPITALS = {
    "france": "Paris",
    "germany": "Berlin",
    "japan": "Tokyo",
    "united kingdom": "London",
    "uk": "London",
    "united states": "Washington, D.C.",
    "usa": "Washington, D.C.",
    "india": "New Delhi",
    "canada": "Ottawa",
    "australia": "Canberra",
    "italy": "Rome",
    "spain": "Madrid",
    "brazil": "Brasília",
    "russia": "Moscow",
    "china": "Beijing",
    "south korea": "Seoul",
    "switzerland": "Bern",
    "netherlands": "Amsterdam",
    "sweden": "Stockholm",
    "iceland": "Reykjavik"
}

def get_capital_city(country: str) -> str:
    """Returns the capital city of a given country."""
    c = country.strip().lower()
    capital = _CAPITALS.get(c)
    if capital:
        return json.dumps({"country": country, "capital": capital})
    return json.dumps({"error": f"Capital for '{country}' not found in database."})


_CITY_TIMEZONES = {
    "tokyo": "Asia/Tokyo",
    "paris": "Europe/Paris",
    "london": "Europe/London",
    "berlin": "Europe/Berlin",
    "new york": "America/New_York",
    "san francisco": "America/Los_Angeles",
    "los angeles": "America/Los_Angeles",
    "seattle": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "toronto": "America/Toronto",
    "sydney": "Australia/Sydney",
    "bengaluru": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata",
    "mumbai": "Asia/Kolkata",
    "new delhi": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "osaka": "Asia/Tokyo",
    "reykjavik": "Atlantic/Reykjavik",
    "zurich": "Europe/Zurich",
    "rome": "Europe/Rome"
}

def get_city_timezone(city: str) -> str:
    """Returns the standard IANA timezone name for a given city."""
    c = city.strip().lower()
    tz = _CITY_TIMEZONES.get(c)
    if tz:
        return json.dumps({"city": city, "timezone": tz})
    return json.dumps({"error": f"Timezone for '{city}' not found."})


# ============================================================================
# 5. CONTACT DIRECTORY (CHAIN TRIGGER)
# ============================================================================

_CONTACTS = {
    "alice": {
        "name": "Alice Smith",
        "role": "Lead Architect",
        "city": "London",
        "country": "United Kingdom",
        "timezone": "Europe/London",
        "email": "alice.smith@example.com"
    },
    "bob": {
        "name": "Bob Jones",
        "role": "Product Manager",
        "city": "Osaka",
        "country": "Japan",
        "timezone": "Asia/Tokyo",
        "email": "bob.jones@example.com"
    },
    "charlie": {
        "name": "Charlie Brown",
        "role": "Data Scientist",
        "city": "New York",
        "country": "United States",
        "timezone": "America/New_York",
        "email": "charlie.b@example.com"
    },
    "priya": {
        "name": "Priya Sharma",
        "role": "Engineering Director",
        "city": "Bengaluru",
        "country": "India",
        "timezone": "Asia/Kolkata",
        "email": "priya.sharma@example.com"
    }
}

def get_contact_info(name: str) -> str:
    """Looks up a person in your private contact directory to retrieve their city, country, email, and timezone."""
    query = name.strip().lower()
    for key, contact in _CONTACTS.items():
        if query in key or key in query or query in contact["name"].lower():
            return json.dumps(contact)
    return json.dumps({"error": f"No contact found matching '{name}'."})


# ============================================================================
# 6. PRODUCT CATALOG & PRICING
# ============================================================================

_CATALOG = {
    "ultra laptop": 1200.0,
    "laptop": 1000.0,
    "pro mouse": 50.0,
    "mouse": 25.0,
    "mechanical keyboard": 120.0,
    "keyboard": 60.0,
    "4k monitor": 400.0,
    "monitor": 250.0,
    "wireless headphones": 150.0,
    "headphones": 80.0,
    "smartwatch": 200.0,
    "desk lamp": 35.0
}

def get_product_price(product_name: str) -> str:
    """Returns the catalog unit price in USD for a given product or electronic item."""
    query = product_name.strip().lower()
    for item, price in _CATALOG.items():
        if query in item or item in query:
            return json.dumps({"product": item, "price_usd": price, "currency": "USD"})
    return json.dumps({"error": f"Product '{product_name}' not found in store catalog."})


# ============================================================================
# 7. SAFE CALCULATOR
# ============================================================================

_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}

def _eval_ast(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in _SAFE_OPERATORS:
            return _SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in _SAFE_OPERATORS:
            return _SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    else:
        raise ValueError(f"Unsupported expression syntax: {type(node)}")

def calculate(expression: str) -> str:
    """Safely evaluates a mathematical expression (e.g. '(2 * 1200 + 50) * 0.9')."""
    try:
        clean = expression.replace(",", "").strip()
        parsed = ast.parse(clean, mode="eval")
        result = _eval_ast(parsed.body)
        return json.dumps({"expression": expression, "result": round(float(result), 4)})
    except Exception as e:
        return json.dumps({"error": f"Failed to calculate '{expression}': {e}"})


# ============================================================================
# 8. CURRENCY CONVERSION
# ============================================================================

_RATES_FROM_USD = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.78,
    "INR": 83.2,
    "JPY": 155.0,
    "CAD": 1.36,
    "AUD": 1.52,
    "CHF": 0.90
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts a monetary amount between currencies (USD, EUR, GBP, INR, JPY, CAD, AUD, CHF)."""
    try:
        f = from_currency.strip().upper()
        t = to_currency.strip().upper()
        if f not in _RATES_FROM_USD:
            return json.dumps({"error": f"Unsupported source currency '{f}'"})
        if t not in _RATES_FROM_USD:
            return json.dumps({"error": f"Unsupported target currency '{t}'"})
        
        # Normalize to USD then convert to target
        usd_val = float(amount) / _RATES_FROM_USD[f]
        converted = usd_val * _RATES_FROM_USD[t]
        return json.dumps({
            "original_amount": amount,
            "from_currency": f,
            "converted_amount": round(converted, 2),
            "to_currency": t
        })
    except Exception as e:
        return json.dumps({"error": f"Error converting currency: {e}"})


# ============================================================================
# 9. NOTES STORE (CHAIN TRIGGER)
# ============================================================================

_NOTES_STORE = {
    "trip_itinerary": "Flight landing in Zurich, Switzerland on Friday. Hotel booked downtown.",
    "project_specs": "Client meeting scheduled with Alice in London regarding Q4 cloud roadmap.",
    "shopping_list": "Need to order 2 ultra laptops and 3 mechanical keyboards for the new hires."
}

def save_note(title: str, content: str) -> str:
    """Saves a note with a title and text content to the notes store."""
    key = title.strip().lower().replace(" ", "_")
    _NOTES_STORE[key] = content.strip()
    return json.dumps({"status": "saved", "title": title})

def get_note(title: str) -> str:
    """Retrieves the content of a saved note by its title or keyword."""
    query = title.strip().lower().replace(" ", "_")
    for key, content in _NOTES_STORE.items():
        if query in key or key in query:
            return json.dumps({"title": key, "content": content})
    return json.dumps({"error": f"Note '{title}' not found."})

def list_notes() -> str:
    """Lists the titles of all saved notes."""
    return json.dumps({"notes": list(_NOTES_STORE.keys())})


# ============================================================================
# OPENAI TOOLS DEFINITIONS
# ============================================================================

TOOLS = [
    # 1. Current Time
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns current date and time. Optionally accepts a timezone name (e.g. 'UTC', 'Asia/Kolkata', 'America/New_York').",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone_name": {"type": "string", "description": "Timezone name (e.g. 'UTC', 'Asia/Kolkata', 'Europe/London')."}
                },
            },
        },
    },

    # 2. Weather
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "Returns live weather and temperature for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name."}
                },
                "required": ["city"],
            },
        },
    },

    # 3. User Location
    {
        "type": "function",
        "function": {
            "name": "get_user_location",
            "description": "Returns the current user's location, city, country, and timezone.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },

    # 4. Capital City
    {
        "type": "function",
        "function": {
            "name": "get_capital_city",
            "description": "Returns the capital city of a given country.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {"type": "string", "description": "Country name, e.g. 'France', 'Japan', 'Germany'."}
                },
                "required": ["country"],
            },
        },
    },

    # 5. City Timezone
    {
        "type": "function",
        "function": {
            "name": "get_city_timezone",
            "description": "Returns the standard IANA timezone name for a given city (e.g. 'Asia/Tokyo', 'Europe/Paris', 'America/New_York').",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name."}
                },
                "required": ["city"],
            },
        },
    },

    # 6. Contact Directory
    {
        "type": "function",
        "function": {
            "name": "get_contact_info",
            "description": "Looks up a person in your private contact directory to retrieve their current city, country, email, and timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the person/contact to look up."}
                },
                "required": ["name"],
            },
        },
    },

    # 7. Product Catalog
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Returns the unit catalog price in USD for an item (e.g. 'ultra laptop', 'pro mouse', 'keyboard', 'monitor').",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "The name of the product."}
                },
                "required": ["product_name"],
            },
        },
    },

    # 8. Safe Calculator
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a mathematical expression like arithmetic, discounts, totals, etc. (e.g. '(2 * 1200 + 50) * 0.9').",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The mathematical formula to compute."}
                },
                "required": ["expression"],
            },
        },
    },

    # 9. Currency Conversion
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Converts an amount from one currency to another (supports USD, EUR, GBP, INR, JPY, CAD, AUD, CHF).",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Numeric amount of money to convert."},
                    "from_currency": {"type": "string", "description": "3-letter source currency code (e.g. 'USD', 'EUR')."},
                    "to_currency": {"type": "string", "description": "3-letter target currency code (e.g. 'INR', 'EUR', 'JPY')."}
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
        },
    },

    # 10. Notes Store
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Saves a text note with a title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the note."},
                    "content": {"type": "string", "description": "Content of the note."}
                },
                "required": ["title", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_note",
            "description": "Retrieves the content of a saved note by its title or keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title or keyword of the note."}
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "Lists the titles of all saved notes in memory.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_user_location": get_user_location,
    "get_capital_city": get_capital_city,
    "get_city_timezone": get_city_timezone,
    "get_contact_info": get_contact_info,
    "get_product_price": get_product_price,
    "calculate": calculate,
    "convert_currency": convert_currency,
    "save_note": save_note,
    "get_note": get_note,
    "list_notes": list_notes,
}
