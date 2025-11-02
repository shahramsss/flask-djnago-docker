# Dockerfile
FROM python

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های پروژه
COPY . /app

# نصب وابستگی‌ها
RUN pip install --upgrade pip && \
    pip install -r req.txt
    # pip install gunicorn django 

# باز کردن پورت
EXPOSE 8003

# اجرای Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8003", "flash_card.wsgi:application"]
# gunicorn --workers 3 --bind 0.0.0.0:8003 flash_card.wsgi:application