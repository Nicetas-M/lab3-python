from deep_translator import GoogleTranslator
from langdetect import detect
from tabulate import tabulate

# Мапа мов та їх кодів для deep_translator
LANGUAGES = {
    'be': 'belarusian', 'bg': 'bulgarian', 'hr': 'croatian',
    'cs': 'czech', 'en': 'english', 'ru': 'russian',
}


def TransLate(text: str, scr: str, dest: str) -> str:
    """Перекладає текст на задану мову або повертає повідомлення про помилку."""
    try:
        translation = GoogleTranslator(source=scr, target=dest).translate(text)
        return translation
    except Exception as e:
        return f"Помилка: {str(e)}"


def CodeLang(lang: str) -> str:
    """Повертає код мови за її назвою або назву мови за її кодом."""
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
    elif lang in LANGUAGES.values():
        return next(code for code, name in LANGUAGES.items() if name == lang)
    return "Помилка: некоректна мова або код мови"


def LanguageList(out: str = "screen", text: str = "") -> str:
    """
    Виводить таблицю підтримуваних мов з перекладом тексту, якщо задано.
    out = "screen" (за замовчуванням) – вивід таблиці на екран
    out = "file" – зберегти таблицю у файл
    text – текст, який необхідно перекласти. Якщо не задано, відповідна колонка не заповнюється.
    """
    table_data = []
    for i, (lang_code, lang_name) in enumerate(LANGUAGES.items(), start=1):
        try:
            translated_text = TransLate(text, 'auto', lang_code) if text else ""
            table_data.append([i, lang_name.capitalize(), lang_code, translated_text])
        except Exception:
            table_data.append([i, lang_name.capitalize(), lang_code, "Помилка перекладу"])

    # Вивід таблиці на екран або у файл
    headers = ["N", "Language", "ISO-639 code", "Text"]
    table_output = tabulate(table_data, headers=headers, tablefmt="plain", stralign="left")

    if out == "screen":
        print(table_output)
    elif out == "file":
        with open("language_list.txt", "w", encoding="utf-8") as file:
            file.write(table_output)

    return "Ok"