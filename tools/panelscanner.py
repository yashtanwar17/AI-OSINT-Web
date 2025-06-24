import requests

admin_paths = [
    "admin/", "admin/login", "admin.php", "adminarea/", "adminpanel/", "admin-console/",
    "administrator/", "administrator/index.php", "backend/", "backend/login",
    "cpanel/", "cpanel/login", "dashboard/", "dashboard/login",
    "wp-admin/", "wp-login.php",
    "user/login", "login.php", "login.html", "signin", "account/login",
    "admin/login.php", "admin/index.php", "admin/home",
    "cms/admin", "cms/login",
    "systemadmin/", "sysadmin/", "manage/", "management/",
    "console/", "controlpanel/", "memberadmin/",
    "portal/admin", "portal/login",
    "backend/index.php", "backend/admin",
    "webadmin/", "webadmin/login.php",
    "webmail/", "webmail/login.php",
    "emailadmin/", "mailadmin/", "roundcube/",
    "shop/admin", "magento/admin", "store/admin",
    "joomla/administrator", "drupal/admin", "drupal/login",
    "phpmyadmin/", "mysql-admin/",
    "strapi/admin", "ghost/ghost", "ghost/admin", "directadmin/",
    "laravel/public/admin", "api/admin", "admin/api", "admin/dashboard",
    "panel/", "panel/login", "superadmin/",
    "flask-admin/", "django-admin/"
]

def scan_admin_panels(base_url):
    base_url = "http://" + base_url
    print(f"\n🔍 Scanning {base_url} for exposed admin panels...\n")
    for path in admin_paths:
        url = base_url.rstrip("/") + "/" + path
        try:
            r = requests.get(url, timeout=5)
            if r.status_code in [200, 301, 302]:
                print(f"[FOUND] {url} (Status: {r.status_code})")
        except requests.RequestException:
            continue

