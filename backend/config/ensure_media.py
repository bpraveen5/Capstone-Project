import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Create media directory if it doesn't exist
MEDIA_ROOT = BASE_DIR / 'media'
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
