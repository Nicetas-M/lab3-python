from googletrans import Translator
from googletrans.constants import LANGUAGES
from tabulate import tabulate

translator = Translator()

def TransLate(text: str, scr: str, dest: str) -> str:
    """Перекладає текст на задану мову або повертає повідомлення про помилку."""
    try:
        translation = translator.translate(text, src=scr, dest=dest)
        return translation.text
    except Exception as e:
        return f"Помилка: {str(e)}"


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


def LangDetect(text: str, set: str = 'all') -> str:
    """
    Визначає мову тексту та повертає інформацію залежно від значення параметра 'set'.

    Параметри:
    text -- текст для визначення мови
    set -- 'lang' для повернення тільки коду мови,
           'confidence' для повернення тільки коефіцієнта довіри,
           'all' (за замовчуванням) для повернення і коду мови, і коефіцієнта довіри

    Повертає:
    str -- код мови, коефіцієнт довіри або обидва значення.
    """
    translator = Translator()

    try:
        detection = translator.detect(text)
        language = detection.lang
        confidence = detection.confidence

        if set == 'lang':
            return language
        elif set == 'confidence':
            return str(confidence)
        elif set == 'all':
            return f"Мова: {language}, Коефіцієнт довіри: {confidence}"
        else:
            return "Помилка: Невірне значення параметра 'set'."

    except Exception as e:
        return f"Помилка визначення мови: {e}"