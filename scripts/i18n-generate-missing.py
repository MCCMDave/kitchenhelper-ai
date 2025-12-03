#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KitchenHelper-AI: Generate ONLY missing languages (SV/NO/DA/NL)
"""
import json
import re
import sys
import time
from pathlib import Path

import ollama

# Only missing languages
LANGUAGES = {
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'nl': 'Dutch'
}

def extract_en_translations(file_path):
    """Extract English translations from i18n.js"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find 'en:' block
    en_match = re.search(r'en:\s*{([^}]+)}', content, re.DOTALL)
    if not en_match:
        print('[ERROR] Could not find en: block!')
        sys.exit(1)

    en_block = en_match.group(1)

    # Extract all key-value pairs
    translations = {}
    pattern = r'(\w+):\s*["\']([^"\']*)["\']'

    for match in re.finditer(pattern, en_block):
        key = match.group(1)
        value = match.group(2)
        # Unescape quotes
        value = value.replace("\\'", "'").replace('\\"', '"')
        translations[key] = value

    return translations

def translate_text(text, target_lang):
    """Translate using Ollama"""
    prompt = f"""Translate this UI text to {LANGUAGES[target_lang]}. Return ONLY the translation, no explanation:

{text}"""

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.3}
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f'[ERROR] Ollama error: {e}', flush=True)
        return None

def main():
    project_root = Path('/home/dave/kitchenhelper-ai')
    i18n_file = project_root / 'frontend' / 'js' / 'i18n.js'

    if not i18n_file.exists():
        print(f'[ERROR] File not found: {i18n_file}')
        sys.exit(1)

    print('[OK] Extracting English translations...', flush=True)
    en_translations = extract_en_translations(i18n_file)
    print(f'[OK] Found {len(en_translations)} keys', flush=True)

    for lang_code, lang_name in LANGUAGES.items():
        print(f'\n=== {lang_name} ({lang_code}) ===', flush=True)

        translations = {}
        total = len(en_translations)

        for idx, (key, en_text) in enumerate(en_translations.items(), 1):
            print(f'[{idx}/{total}] {key}...', end=' ', flush=True)

            translated = translate_text(en_text, lang_code)

            if translated:
                translations[key] = translated
                print('[OK]', flush=True)
            else:
                translations[key] = en_text  # Fallback
                print('[FALLBACK]', flush=True)

            time.sleep(0.1)  # Rate limiting

        # Save to file
        output_file = project_root / 'frontend' / 'js' / 'translations' / f'{lang_code}.json'
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)

        print(f'[OK] Saved: {output_file}', flush=True)

    print('\n[OK] All missing languages generated!', flush=True)

if __name__ == '__main__':
    main()
