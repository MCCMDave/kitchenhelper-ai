#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KitchenHelper-AI: Automatic i18n Translation System
Verwendet lokales Ollama (llama3.2) für kostenlose Übersetzungen
"""
import json
import re
import sys
import time
from pathlib import Path

# Fix Windows UTF-8 encoding für Emojis
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Ollama Import
try:
    import ollama
except ImportError:
    print("❌ Ollama Python-Paket nicht installiert!")
    print("   Install: pip install ollama")
    sys.exit(1)


# Sprach-Mapping: Code → Name
LANGUAGES = {
    'fr': 'French',
    'es': 'Spanish',
    'it': 'Italian',
    'pt': 'Portuguese',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'nl': 'Dutch'
}


def extract_translations_from_js(file_path):
    """Extrahiert alle Übersetzungen aus i18n.js - KORRIGIERTE VERSION"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    translations = {}

    # Verwende eine robustere Methode: Finde alle Sprachblöcke
    # Pattern für kompletten i18n-Block
    full_pattern = r'i18n\s*=\s*{([^}]+(?:\{[^{}]*\}[^{}]*)*)}'

    full_match = re.search(full_pattern, content, re.DOTALL)
    if not full_match:
        print("❌ i18n-Block nicht gefunden!")
        return translations

    i18n_content = full_match.group(1)

    # Extrahiere jede Sprachsektion mit verbessertem Pattern
    lang_pattern = r"(\w+):\s*{((?:[^{}]*(?:\{[^{}]*\})?[^{}]*)*)}"

    for match in re.finditer(lang_pattern, i18n_content, re.DOTALL):
        lang_code = match.group(1)
        lang_section = match.group(2)
        translations[lang_code] = parse_lang_section(lang_section)

    return translations


def parse_lang_section(section):
    """Parse eine Sprach-Sektion und extrahiert Key-Value Paare - KORRIGIERT"""
    translations = {}

    # Verbessertes Pattern, das auch mehrzeilige Werte und Escapes besser handhabt
    pattern = r"'([^']+)':\s*'((?:[^'\\]|\\.)*)'"

    # Zusätzlich: Pattern für doppelte Anführungszeichen
    pattern_double = r'"([^"]+)":\s*"((?:[^"\\]|\\.)*)"'

    # Verarbeite einfache Anführungszeichen
    for match in re.finditer(pattern, section):
        key = match.group(1)
        value = match.group(2)
        # Decode escaped characters
        value = value.replace("\\'", "'").replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
        translations[key] = value

    # Verarbeite doppelte Anführungszeichen
    for match in re.finditer(pattern_double, section):
        key = match.group(1)
        value = match.group(2)
        # Decode escaped characters
        value = value.replace("\\'", "'").replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
        translations[key] = value

    return translations


def translate_with_ollama(text, target_lang, context_key=""):
    """Übersetzt Text mit Ollama"""

    # Context-aware Prompt
    context_hint = ""
    if "auth." in context_key:
        context_hint = "This is for a login/authentication form. "
    elif "nav." in context_key:
        context_hint = "This is a navigation menu item. "
    elif "recipes." in context_key:
        context_hint = "This is for a recipe generation feature. "
    elif "ingredients." in context_key:
        context_hint = "This is for ingredient management. "
    elif "error." in context_key:
        context_hint = "This is an error message. "
    elif "common." in context_key:
        context_hint = "This is a common UI element. "

    prompt = f"""You are a professional translator for a cooking/recipe web application.
{context_hint}Translate the following English text to {LANGUAGES[target_lang]}.

IMPORTANT:
- Keep the same tone and formality
- Preserve any placeholders like {{count}}, {{name}} EXACTLY as they are
- Keep emojis unchanged
- For UI elements, use common terminology
- Return ONLY the translation, no explanations

English text: "{text}"

{LANGUAGES[target_lang]} translation:"""

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )

        translation = response['message']['content'].strip()

        # Entferne Anführungszeichen am Anfang/Ende falls vorhanden
        translation = translation.strip('"').strip("'")

        return translation

    except Exception as e:
        print(f"   ⚠️  Fehler bei Übersetzung: {e}")
        return text  # Fallback: Original-Text


def complete_translations(i18n_path, lang_code, dry_run=False):
    """Vervollständigt Übersetzungen für eine Sprache"""

    print(f"\n{'='*70}")
    print(f"{LANGUAGES[lang_code].upper()} ({lang_code.upper()})")
    print(f"{'='*70}\n")

    # Lade bestehende Übersetzungen
    all_translations = extract_translations_from_js(i18n_path)

    en_translations = all_translations.get('en', {})
    lang_translations = all_translations.get(lang_code, {})

    print(f"Status:")
    print(f"   EN Keys: {len(en_translations)}")
    print(f"   {lang_code.upper()} Keys: {len(lang_translations)}")

    # Finde fehlende Keys
    missing_keys = [key for key in en_translations.keys() if key not in lang_translations]

    if not missing_keys:
        print(f"   ✅ OK: Keine fehlenden Keys!\n")
        return lang_translations

    print(f"   FEHLEN: {len(missing_keys)} Keys\n")

    if dry_run:
        print("DRY RUN - Zeige erste 10 fehlende Keys:\n")
        for key in missing_keys[:10]:
            print(f"   - {key}: {en_translations[key][:50]}...")
        return lang_translations

    # Übersetze fehlende Keys
    print(f"Starte Ollama-Uebersetzung ({len(missing_keys)} Keys)...\n")

    completed_translations = lang_translations.copy()

    for i, key in enumerate(missing_keys, 1):
        en_text = en_translations[key]

        print(f"   [{i:3d}/{len(missing_keys)}] {key[:40]:40s} ", end='', flush=True)

        translation = translate_with_ollama(en_text, lang_code, key)
        completed_translations[key] = translation

        print(f"OK")

        # Kleine Pause um Ollama nicht zu überlasten
        if i % 10 == 0:
            time.sleep(0.5)

    print(f"\n✅ OK: {lang_code.upper()} vollständig: {len(completed_translations)}/{len(en_translations)} Keys\n")

    return completed_translations


def build_js_lang_section(translations, indent=8):
    """Erstellt eine JS-Sprach-Sektion aus Übersetzungen"""
    lines = []
    current_category = None

    for key in sorted(translations.keys()):
        value = translations[key]

        # Kategorie-Kommentar hinzufügen
        category = key.split('.')[0]
        if category != current_category:
            if current_category is not None:
                lines.append('')
            lines.append(f"// {category.capitalize()}")
            current_category = category

        # Escape single quotes in value
        value = value.replace("'", "\\'").replace("\n", "\\n")

        lines.append(f"'{key}': '{value}',")

    # Indent
    indent_str = ' ' * indent
    return '\n'.join(indent_str + line for line in lines)


def update_i18n_file(i18n_path, lang_code, new_translations):
    """Updated die i18n.js Datei mit neuen Übersetzungen - KORRIGIERT"""

    with open(i18n_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Erstelle neue Sprach-Sektion
    new_section = build_js_lang_section(new_translations)

    # Verbesserte Pattern-Erkennung
    # Finde die genaue Position der Sprach-Sektion
    lang_pattern = f"({lang_code}:\\s*{{)(.*?)(\\s*}}(?:,|\\s*\\}};))"

    match = re.search(lang_pattern, content, re.DOTALL)
    if not match:
        print(f"❌ Sprach-Sektion für {lang_code} nicht gefunden!")
        return

    # Ersetze den Inhalt der Sprach-Sektion
    replacement = f'{match.group(1)}\n{new_section}\n{match.group(3)}'
    new_content = re.sub(lang_pattern, replacement, content, flags=re.DOTALL)

    # Schreibe zurück
    with open(i18n_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ GESPEICHERT: {lang_code.upper()} in i18n.js aktualisiert!")


def main():
    """Hauptfunktion"""

    print("\n" + "="*70)
    print("KitchenHelper-AI: Automatic i18n Translation System")
    print("="*70)

    # Finde i18n.js
    i18n_path = Path(__file__).parent.parent / 'frontend' / 'js' / 'i18n.js'

    if not i18n_path.exists():
        print(f"❌ FEHLER: i18n.js nicht gefunden: {i18n_path}")
        sys.exit(1)

    print(f"\ni18n.js: {i18n_path}")

    # Test: Ollama verfügbar?
    print(f"\nPrüfe Ollama...")
    try:
        models = ollama.list()
        print(f"   ✅ OK: Ollama läuft!")

        # Prüfe ob llama3.2 verfügbar
        has_llama = any('llama3.2' in str(m) for m in models.get('models', []))
        if not has_llama:
            print(f"   ⚠️ WARNUNG: llama3.2 nicht gefunden!")
            print(f"   Install: ollama pull llama3.2")
            sys.exit(1)
        print(f"   ✅ OK: llama3.2 verfügbar!")

    except Exception as e:
        print(f"   ❌ FEHLER: Ollama nicht erreichbar: {e}")
        print(f"   Starte Ollama: ollama serve")
        sys.exit(1)

    # Verarbeite alle Sprachen
    print(f"\nStarte Übersetzung für {len(LANGUAGES)} Sprachen...")

    for lang_code in LANGUAGES.keys():
        # Vervollständige Übersetzungen
        completed = complete_translations(i18n_path, lang_code, dry_run=False)

        # Update i18n.js
        update_i18n_file(i18n_path, lang_code, completed)

    print("\n" + "="*70)
    print("✅ FERTIG! Alle Sprachen vervollständigt!")
    print("="*70)
    print("\nNächste Schritte:")
    print("   1. Teste die App in verschiedenen Sprachen")
    print("   2. Bei Bedarf: Manuelle Feinabstimmung einzelner Übersetzungen")
    print("   3. Git commit & push\n")


if __name__ == '__main__':
    main()
