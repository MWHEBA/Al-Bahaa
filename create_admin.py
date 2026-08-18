import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@albahaacontracting.com", "admin123456")
    print("[OK] Superuser 'admin' created with password 'admin123456'")
else:
    u = User.objects.get(username="admin")
    u.set_password("admin123456")
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("[OK] Superuser 'admin' updated with password 'admin123456'")
