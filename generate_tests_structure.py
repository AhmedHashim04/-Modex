import os

TEST_FILES = [
    '__init__.py',
    'test_models.py',
    'test_views.py',
    'test_urls.py',
    # 'test_api.py',
]

def is_django_app(path):
    """يتأكد إذا كان المجلد عبارة عن app في Django"""
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, 'apps.py'))

def create_test_files(app_path):
    tests_dir = os.path.join(app_path, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    for file_name in TEST_FILES:
        file_path = os.path.join(tests_dir, file_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('# ' + file_name + '\n')

def main():
    BASE_DIR = os.getcwd()
    for item in os.listdir(BASE_DIR):
        app_path = os.path.join(BASE_DIR, item)
        if is_django_app(app_path):
            print(f'✅ إنشاء ملفات الاختبار في: {item}')
            create_test_files(app_path)

if __name__ == '__main__':
    main()
