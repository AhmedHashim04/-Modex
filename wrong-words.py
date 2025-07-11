def convert_arabic_to_english_keyboard(text):
    mapping = {
        'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't', 'غ': 'y', 'ع': 'u', 'ه': 'i', 'خ': 'o', 'ح': 'p',
        'ش': 'a', 'س': 's', 'ي': 'd', 'ب': 'f', 'ل': 'g', 'ا': 'h', 'ت': 'j', 'ن': 'k', 'م': 'l',
        'ئ': 'z', 'ء': 'x', 'ؤ': 'c', 'ر': 'v', 'لا': 'b', 'ى': 'n', 'ة': 'm', 'و': ',', 'ز': '.', 'ظ': '/',
    }
    return ''.join(mapping.get(char, char) for char in text)

wrong_text = "ةشنث هف ةخقث ةخيثقى شىي شححقخحثقهشفث فخ فاث حخفاثق سثؤفهخىس"
print(convert_arabic_to_english_keyboard(wrong_text))
