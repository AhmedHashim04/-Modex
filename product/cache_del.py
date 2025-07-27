
import os
import shutil

def delete_cache_dirs(root_dir="."):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname in ["__pycache__", ".pytest_cache"]:
                full_path = os.path.join(dirpath, dirname)
                print(f"Deleting: {full_path}")
                shutil.rmtree(full_path, ignore_errors=True)

if __name__ == "__main__":
    delete_cache_dirs()
