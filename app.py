import json
import os
import re
import base64
from urllib.parse import urlparse

import streamlit as st

DATA_FILE = "links.json"

PALETTE = {
    "accent": "#ed9e1f",  # dourado
    "bg": "#0b0706",      # preto
    "brown": "#873a1c",   # marrom
    "cream": "#f6e7cb",   # creme
}


def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {
            "site": {
                "title": "Muniz Distribuidora | Links",
                "subtitle": "Acesse nossos canais oficiais",
                "columns": 2
            },
            "tabs": [
                {
                    "name": "Principais",
                    "items": [
                        {"label": "WhatsApp", "url": "https://wa.me/5591999999999", "icon": "💬"},
                        {"label": "Instagram", "url": "https://instagram.com/suaempresa", "icon": "📷"},
                        {"label": "iFood", "url": "https://www.ifood.com.br/delivery/sua-loja", "icon": "🍔"},
                        {"label": "Zé Delivery", "url": "https://www.ze.delivery/", "icon": "🍺"},
                    ],
                }
            ],
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    with open
