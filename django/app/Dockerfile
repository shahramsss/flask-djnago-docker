FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تنظیم اطلاعات ادمین
ENV DJANGO_SUPERUSER_USERNAME=ss2
ENV DJANGO_SUPERUSER_EMAIL=ss2@gmail.com
ENV DJANGO_SUPERUSER_PASSWORD=111

# نصب ابزارهای لازم برای build پکیج‌ها
RUN apk update
RUN apk add --no-cache gcc musl-dev libffi-dev mariadb-dev

RUN mkdir /app
WORKDIR /app

# نصب پکیج‌های Python
RUN pip install --upgrade pip && pip install django gunicorn djangorestframework khayyam mysqlclient 


RUN apk del gcc musl-dev libffi-dev 
# اجرای migration و collectstatic و ساخت ادمین (در صورت نبود)
CMD python manage.py makemigrations --noinput && \
    while ! python manage.py migrate --noinput ; sleep 1 ; done  && \
    python manage.py collectstatic --noinput && \
    python manage.py createsuperuser --noinput || true && \
    gunicorn -b 0.0.0.0:8000 flash_card.wsgi
