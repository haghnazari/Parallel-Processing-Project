# 1. استفاده از نسخه پایدار و سبک پایتون 3.12 لینوکس
FROM python:3.12-slim

# 2. جلوگیری از تولید فایل‌های کش pyc و لاگ‌گیری آنی فرآیندها
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. تعیین پوشه کاری پیش‌فرض درون کانتینر
WORKDIR /app

# 4. کپی کردن فایل نیازمندی‌ها به داخل کانتینر
COPY requirements.txt .

# 5. نصب کتابخانه‌های پروژه بدون ذخیره کش اضافی
RUN pip install --no-cache-dir -r requirements.txt

# 6. کپی کردن کل کدهای پروژه به داخل کانتینر
COPY . .

# 7. باز کردن پورت 8000 (پورت پیش‌فرض FastAPI) برای دسترسی خارج از کانتینر
EXPOSE 8000

# 8. دستور نهایی برای اجرای وب‌سرور Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]