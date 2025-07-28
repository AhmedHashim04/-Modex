# #!/bin/bash

# # python manage.py runserver --settings=project.settings.dev


# # تثبيت كل الحاجات المطلوبة
# sudo apt update
# sudo apt install python3-pip python3-venv nginx postgresql redis -y

# # إنشاء virtualenv
# python3 -m venv venv
# source venv/bin/activate

# # تثبيت الباكدجات
# pip install -r requirements.txt

# # Apply migrations
# python manage.py migrate --settings=yourproject.settings.production

# # Collect static
# python manage.py collectstatic --noinput --settings=yourproject.settings.production

# # Run gunicorn
# gunicorn yourproject.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=yourproject.settings.production


# sudo apt update && sudo apt install nginx
# sudo nano /etc/nginx/sites-available/mysite
# server {
#     listen 80;
#     server_name localhost;

#     location / {
#         proxy_pass http://127.0.0.1:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#     }

#     location /static/ {
#         alias /home/ahmed/yourproject/staticfiles/;
#     }
# }
# sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
# sudo nginx -t
# sudo systemctl restart nginx
