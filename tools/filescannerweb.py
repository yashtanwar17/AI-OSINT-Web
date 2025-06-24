import requests
from urllib.parse import urljoin

def scan_directory_listing(domain):
    wordlist = [
        "robots.txt", ".env", ".env.local", ".env.bak", ".env.old", ".env.example", ".DS_Store",
        ".htaccess", ".htpasswd", "config.php", "config.bak", "config.old", "config.json",
        "config.ini", "config.yaml", "settings.py", "web.config", "local.settings.json", ".git/",
        ".git/config", ".git/HEAD", ".gitignore", ".gitattributes", ".gitkeep", ".svn/", ".hg/",
        ".bzr/", "database.sql", "db.sql", "dump.sql", "backup/", "backup.zip", "backup.tar.gz",
        "db_backup.sql", "test.sql", "old/", "old-site/", "site.old/", "index.bak", "index.old",
        "main.old", "main.bak", "admin/", "admin/login.php", "admin.php", "admin.html",
        "admin/index.php", "login/", "login.php", "signin/", "dashboard/", "wp-admin/",
        "wp-login.php", "cms/", "panel/", "controlpanel/", "cpanel/", "phpinfo.php", "test.php",
        "debug.php", "info.php", "setup.php", "install.php", "installer.php", "package.json",
        "package-lock.json", "yarn.lock", "node_modules/", "webpack.config.js", "vite.config.js",
        ".env.development", ".env.production", "manage.py", "requirements.txt", "Pipfile",
        "Pipfile.lock", "venv/", "instance/", "migrations/", "wsgi.py", "app.py", "settings.py",
        "artisan", "bootstrap/cache/", "storage/", "composer.json", "composer.lock", "sitemap.xml",
        "crossdomain.xml", "security.txt", "humans.txt", "server-status", "server-info", "logs/",
        "error.log", "access.log", ".gitlab-ci.yml", ".travis.yml", ".bash_history", ".bashrc",
        ".bash_profile", "README.md", "LICENSE", "docker-compose.yml", "Dockerfile", "nginx.conf",
        "apache.conf", "web.config", "wp-config.php", "wp-config-sample.php", "wp-content/",
        "wp-content/plugins/", "wp-content/uploads/", "xmlrpc.php", "license.txt", "id_rsa",
        "id_rsa.pub", "private.key", "public.key", "secrets.json", "key.pem", "cert.pem", "jwt.key",
        "apikey.txt", "apikeys.json", "admin/", "admin/login", "admin/login.php", "admin/login.html",
        "admin/index.php", "admin/index.html", "admin_area/", "administrator/", "admin1/",
        "admin2/", "cpanel/", "controlpanel/", "dashboard/", "dashboard.php", "dashboard.html",
        "login/", "login.php", "login.html", "signin/", "signin.php", "signin.html", "user/",
        "user/login", "users/login", "account/login", "system/login", "auth/", "auth/login",
        "portal/", "portal/login", "secure/", "secure/login", "security/", "security/login",
        "wp-admin/", "wp-login.php", "wp-login.html", "wp-admin/index.php", "wp-admin/admin.php",
        "administrator/index.php", "administrator/login.php", "user/login", "user/register",
        "user/password", "admin123/", "magento/", "magento_admin/", "backend/", "phpmyadmin/",
        "pma/", "mysql/", "sqladmin/", "webadmin/", "siteadmin/", "serveradmin/", "memberadmin/",
        "admin-console/", "admincontrol/", "webmail/", "email/", "mail/", "mailadmin/"
    ]

    if not domain.startswith("http"):
        domain = "http://" + domain

    print(f"[+] Scanning {domain} for common sensitive files & directories...")

    for path in wordlist:
        url = urljoin(domain, path)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code in [200, 401, 403]:
                print(f"[!] {url} -> {r.status_code}")
        except:
            pass
