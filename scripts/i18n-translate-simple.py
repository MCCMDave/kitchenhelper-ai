#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple i18n Translation Script
Extrahiert EN Keys aus translations.en und übersetzt sie direkt
"""
import json
import re
import sys
from pathlib import Path

# Fix Windows UTF-8 encoding (disabled - causes output buffering issues)
# if sys.platform == 'win32':
#     import codecs
#     sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
#     sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    import ollama
except ImportError:
    print("[ERROR] Ollama not installed: pip install ollama")
    sys.exit(1)

# Languages to translate (only missing ones)
LANGUAGES = {
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'nl': 'Dutch'
}


def extract_en_keys(i18n_path):
    """Extract English translation keys from en: section"""
    with open(i18n_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the en: { ... } section (more flexible pattern)
    en_pattern = r"en:\s*{(.*?)},\s*(?:fr|es|it|pt|sv|no|da|nl):"
    match = re.search(en_pattern, content, re.DOTALL)

    if not match:
        print("[ERROR] Could not find en: section")
        return {}

    en_section = match.group(1)

    # Extract key-value pairs
    translations = {}
    key_pattern = r"'([^']+)':\s*'([^']+)'"

    for m in re.finditer(key_pattern, en_section):
        key = m.group(1)
        value = m.group(2).replace("\\'", "'")  # Unescape single quotes
        translations[key] = value

    print(f"[OK] Extracted {len(translations)} EN keys", flush=True)
    return translations


def translate_with_ollama(text, target_lang):
    """Translate text using Ollama"""
    prompt = f"""Translate this UI text to {target_lang}.
Return ONLY the translation, no explanations:

{text}"""

    response = ollama.generate(model='llama3.2', prompt=prompt)
    return response['response'].strip().strip('"').strip("'")


def translate_keys(en_translations, lang_code, lang_name):
    """Translate all keys to target language"""
    print(f"\n{'='*70}", flush=True)
    print(f"Translating to {lang_name.upper()} ({lang_code.upper()})", flush=True)
    print(f"{'='*70}\n", flush=True)

    translated = {}
    total = len(en_translations)

    for idx, (key, value) in enumerate(en_translations.items(), 1):
        print(f"[{idx}/{total}] {key[:40]}...", end=" ", flush=True)

        try:
            translation = translate_with_ollama(value, lang_name)
            translated[key] = translation
            print("[OK]", flush=True)
        except Exception as e:
            print(f"[ERROR] {e}", flush=True)
            translated[key] = value  # Fallback to English

    return translated


def build_js_section(translations):
    """Build JavaScript object section"""
    lines = []
    current_category = None

    for key in sorted(translations.keys()):
        value = translations[key]

        # Add category comment
        category = key.split('.')[0]
        if category != current_category:
            if current_category is not None:
                lines.append('')
            lines.append(f"// {category.capitalize()}")
            current_category = category

        # Escape quotes
        value = value.replace("'", "\\'").replace("\n", "\\n")
        lines.append(f"        '{key}': '{value}',")

    return '\n'.join(lines)


def update_i18n_file(i18n_path, lang_code, translations):
    """Update i18n.js with new translations"""
    with open(i18n_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new section
    new_section = build_js_section(translations)

    # Find and replace language section
    pattern = f"({lang_code}:\\s*{{)(.*?)(\\s*}})"

    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"[ERROR] Could not find {lang_code} section")
        return False

    # Replace
    replacement = f'{match.group(1)}\n{new_section}\n{match.group(3)}'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=1)

    # Write back
    with open(i18n_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Saved {lang_code.upper()} to i18n.js", flush=True)
    return True


def main():
    print("\n" + "="*70, flush=True)
    print("KitchenHelper-AI: Simple i18n Translator", flush=True)
    print("="*70, flush=True)

    # Find i18n.js
    i18n_path = Path(__file__).parent.parent / 'frontend' / 'js' / 'i18n.js'

    if not i18n_path.exists():
        print(f"[ERROR] i18n.js not found: {i18n_path}")
        sys.exit(1)

    print(f"\ni18n.js: {i18n_path}\n", flush=True)

    # Check Ollama
    try:
        ollama.list()
        print("[OK] Ollama is running\n", flush=True)
    except Exception as e:
        print(f"[ERROR] Ollama not running: {e}", flush=True)
        sys.exit(1)

    # Extract EN keys
    en_translations = extract_en_keys(i18n_path)

    if not en_translations:
        print("[ERROR] No English translations found")
        sys.exit(1)

    # Translate each language
    for lang_code, lang_name in LANGUAGES.items():
        translated = translate_keys(en_translations, lang_code, lang_name)
        update_i18n_file(i18n_path, lang_code, translated)

    print("\n" + "="*70, flush=True)
    print("[OK] DONE! All languages translated!", flush=True)
    print("="*70 + "\n", flush=True)


if __name__ == '__main__':
    main()
