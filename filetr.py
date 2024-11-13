import os
from translation_tool.google_module import TransLate, LangDetect

def read_config(file_path):
    """Зчитує конфігурацію з файлу і повертає як словник."""
    config = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip()
    return config

def read_text(file_path, max_chars, max_words, max_sentences):
    """Зчитує текст із файлу до вказаних обмежень."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Рахуємо символи, слова, речення
    sentences = text.split('.')
    words = text.split()
    if len(text) > max_chars:
        text = text[:max_chars]
    if len(words) > max_words:
        text = ' '.join(words[:max_words])
    if len(sentences) > max_sentences:
        text = '.'.join(sentences[:max_sentences]) + '.'

    return text

def translate_text_from_file(config_path):
    """Основна функція для перекладу тексту з файлу."""
    # Зчитування конфігурації
    config = read_config(config_path)

    # Отримуємо параметри з конфігурації
    text_file = config.get('text_file')
    target_language = config.get('target_language', 'en')
    output = config.get('output', 'screen')
    max_chars = int(config.get('max_chars', 600))
    max_words = int(config.get('max_words', 100))
    max_sentences = int(config.get('max_sentences', 5))

    # Перевірка існування текстового файлу
    if not os.path.exists(text_file):
        print(f"Помилка: Файл {text_file} не знайдено.")
        return

    # Зчитуємо та обмежуємо текст
    text = read_text(text_file, max_chars, max_words, max_sentences)

    # Визначення мови тексту
    detected_lang = LangDetect(text, 'lang')
    print(f"Мова тексту: {detected_lang}")

    # Завжди виконувати переклад, навіть якщо мова збігається
    translated_text = TransLate(text, detected_lang, target_language)

    # Перевірка, чи відбувся переклад
    if translated_text == text:
        print("Переклад не змінив текст. Це може бути через те, що функція TransLate не працює належним чином.")
    else:
        print(f"Переклад на {target_language}: {translated_text}")

    # Вивід або збереження результату
    if output == "screen":
        print(f"Переклад ({target_language}):\n{translated_text}")
    elif output == "file":
        output_file = f"{os.path.splitext(text_file)[0]}_{target_language}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)
        print("Ok")
    else:
        print("Помилка: Неправильний параметр 'output' у конфігурації.")

# Запуск функції перекладу
translate_text_from_file('config.txt')
