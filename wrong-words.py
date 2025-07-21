# Arabic to English mapping (based on keyboard layout)
mapping = {
    'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't', 'غ': 'y', 'ع': 'u', 'ه': 'i', 'خ': 'o', 'ح': 'p',
    'ش': 'a', 'س': 's', 'ي': 'd', 'ب': 'f', 'ل': 'g', 'ا': 'h', 'ت': 'j', 'ن': 'k', 'م': 'l',
    'ئ': 'z', 'ء': 'x', 'ؤ': 'c', 'ر': 'v', 'لا': 'b', 'ى': 'n', 'ة': 'm', 'و': ',', 'ز': '.', 'ظ': '/',
}

# عكس الماب (بنتجاهل 'لا' لأنها حرفين)
reverse_mapping = {v: k for k, v in mapping.items() if len(k) == 1}

def convert_arabic_to_english(text):
    return ''.join(mapping.get(char, char) for char in text)

def convert_english_to_arabic(text):
    return ''.join(reverse_mapping.get(char, char) for char in text)

# تجربة
wrong_text = "dktu hfpe uk hg;glm ]d td ;g hglgthj uk]d thglav,u"
print("To English:", convert_arabic_to_english(wrong_text))
print("To Arabic:", convert_english_to_arabic(wrong_text))
