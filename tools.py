from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import ast
import operator
import math
import random
import string
import hashlib
import hmac
import base64
import uuid
import json
import os
import platform
import re
import io
import csv
import shutil
import socket
import urllib.parse
import difflib
import colorsys
import zipfile
import unicodedata
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
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
    """Returns the current weather for a given city."""
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        return f"Could not retrieve weather for {city} (Status: {response.status_code})"
    except Exception as e:
        return f"Error fetching weather: {e}"




# ============================================================================
# OPENAI TOOLS DEFINITIONS (130 TOOLS)
# ============================================================================

TOOLS = [
    # --- 1. TIME, DATE, CALENDAR & TIMEZONES ---
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns current date and time. Optionally accepts a timezone name (e.g. 'UTC', 'Asia/Kolkata', 'America/New_York').",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone_name": {"type": "string", "description": "Timezone name (e.g. 'UTC', 'Asia/Kolkata')."}
                },
            },
        },
    },
    

    # --- 2. WEATHER ---
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
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    # 1. Time, Date, Calendar & Timezones (10 tools)
    "get_current_time": get_current_time,

    # 2. Weather (1 tool)
    "get_city_weather": get_city_weather,
}
