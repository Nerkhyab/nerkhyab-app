import requests
import re
import json
import os

CHANNEL = "https://t.me/s/NerkhYab_Khorasan"

def clean_html(raw):
    return re.sub(r'<.*?>', '', raw)

def get_messages():
    res = requests.get(CHANNEL)
    html = res.text
    messages = re.findall(r'<div class="tgme_widget_message_text.*?>(.*?)</div>', html, re.S)
    return [clean_html(m) for m in messages][-30:]

def extract_price(text):
    m = re.search(r'(\d[\d,]*)', text)
    return int(m.group(1).replace(",", "")) if m else None

def get_rates():
    msgs = get_messages()
    found = {
        "دلار هرات": None,
        "یورو هرات": None,
        "تومان بانکی": None
    }

    for msg in msgs:
        if found["دلار هرات"] is None and "دلار" in msg:
            found["دلار هرات"] = extract_price(msg)
        if found["یورو هرات"] is None and "یورو" in msg:
            found["یورو هرات"] = extract_price(msg)
        if found["تومان بانکی"] is None and "تومان" in msg:
            found["تومان بانکی"] = extract_price(msg)

    return found

def main():
    data = get_rates()
    with open("rates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
