"""
ASGI config for template project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# template_for_analyze directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "template_for_analyze"))

# DJANGO_SETTINGS_MODULE 환경변수가 주입될 경우 해당 환경변수에 설정된 세팅 파일 활용
# 환경변수가 주입되지 않을 경우 기본적으로 config.settings.local 세팅 활용
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django_application = get_asgi_application()
