# Arabic to English mapping (based on keyboard layout)
mapping = {
    'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't', 'غ': 'y', 'ع': 'u', 'ه': 'i','ج': '[', 'خ': 'o','د': ']', 'ح': 'p',
    'ش': 'a', 'س': 's', 'ي': 'd', 'ب': 'f', 'ل': 'g', 'ا': 'h', 'ت': 'j', 'ن': 'k', 'م': 'l',
    'ئ': 'z', 'ء': 'x', 'ؤ': 'c', 'ر': 'v', 'لا': 'b', 'ى': 'n', 'ة': 'm', 'و': ',', 'ز': '.', 'ظ': '/',
}

reverse_mapping = {v: k for k, v in mapping.items() if len(k) == 1}

def swap_ar_en(text):
    result = []
    for char in text:
        if char in mapping:
            result.append(mapping[char])
        elif char in reverse_mapping:
            result.append(reverse_mapping[char])
        else:
            result.append(char)
    return ''.join(result)

# تجربة
mixed_text = "سفغمث ,hsjolg hg قخخف ؤخمخقس g, phff"
print("Swapped:", swap_ar_en(mixed_text))



