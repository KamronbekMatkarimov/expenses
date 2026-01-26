# Kichik Bizneslar Uchun Xarajatlar va Hisobotlar REST API

## 1 Loyihaning Maqsadi
Ushbu loyiha kichik biznes egalariga o‘z xarajatlarini boshqarish, toifalarga ajratish, oylik byudjet belgilash va avtomatik hisobotlar olish imkoniyatini beradigan to‘liq REST API hisoblanadi. Frontend qismi mavjud emas, faqat backend va API ishlaydi.

## 2 Loyihaning Imkoniyatlari
Foydalanuvchilar ro‘yxatdan o‘tishi va tizimga kirishi mumkin.
Foydalanuvchi faqat o‘z ma’lumotlarini ko‘ra oladi.
Xarajat qo‘shish, tahrirlash, o‘chirish.
Xarajatlarni toifalarga ajratish (Masalan: Ovqat, Transport, Ijara, Reklama va boshqalar).
Xarajatga rasm (receipt) biriktirish imkoniyati.
Oylik byudjet belgilash va tahrirlash.
Hisobotlar: tanlangan oy uchun xarajatlar, byudjet bilan solishtirish.
Hisobotlarni CSV formatida eksport qilish.
Hisobotlarni email orqali jo‘natish (optional).
Xarajatlarni sanaga, toifaga yoki summaga ko‘ra filtrlash.
REST API endpointlari to‘liq hujjatlangan (Swagger).

## 3 Texnik Talablar
Python 3.11+
Django 4.x
Django REST Framework
drf-spectacular (Swagger hujjatlari uchun)
django-filter
Simple JWT (token asosidagi autentifikatsiya)
SQLite (default) yoki boshqa ma’lumotlar bazasi
Email yuborish uchun SMTP (Gmail yoki boshqa)

## 4 Loyihani Ishga Tushirish Bosqichlari:

1) Loyihani klonlash

```bash
git clone <repo_link>
cd expenses_api

```
2) Virtual muhit yaratish va faollashtirish:
python -m venv venv 

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate  

3) Talab qilinadigan kutubxonalarni o‘rnatish
pip install -r requirements.txt
    
4) .env faylini yaratish

# Loyihani ishga tushirishdan oldin .env fayl yarating va quyidagi o‘zgaruvchilarni belgilang: 

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_HOST_USER=matkarimovkamron10@gmail.com
EMAIL_HOST_PASSWORD=kamron10

5) Migratsiyalarni bajarish

python manage.py makemigrations
python manage.py migrate

6) Serverni ishga tushirish
python manage.py runserver

Swagger hujjatlari: http://127.0.0.1:8000/api/docs/
 Foydalanuvchi ro‘yxatdan o‘tishi: POST /api/users/register/
 Token olish: POST /api/users/login/



## 5 API Endpoints
    Foydalanuvchi ro‘yxatdan o‘tishi:
POST /api/users/register/
    Token olish:
POST /api/users/login/
    Oylik hisobot olish:
GET /api/reports/?month=YYYY-MM
    CSV formatida eksport:
GET /api/reports/?month=YYYY-MM&export=csv
    Email orqali hisobot yuborish:
POST /api/reports/email/

``` Misol request: ```
{
    "month": "2026-01",
    "to_email": "client@example.com"
}

``` Misol response: ```
{
    "message": "Hisobot email orqali yuborildi",
    "to": "client@example.com",
    "month": "2026-01"
}

# 6 Email orqali hisobot jo‘natish

Agar email sozlamalari .env faylida to‘g‘ri berilgan bo‘lsa, siz hisobotni foydalanuvchi emailiga yuborishingiz mumkin.

``` Misol request: ```

POST /api/reports/email/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
    "month": "2026-01",
    "to_email": "client@example.com"
}

``` Misol response: ```
{
    "message": "Hisobot email orqali yuborildi",
    "to": "client@example.com",
    "month": "2026-01"
}

Backend tomonidan EmailMessage va StringIO yordamida CSV tayyorlanadi va emailga biriktiriladi.

#  7 Xavfsizlik va himoya
 Parollar xavfsiz saqlanadi va validatsiya qilinadi.
 Foydalanuvchi o‘z ma’lumotlariga cheklangan.
 CSRF, SQL injection, XSS kabi xujumlarga qarshi himoya.
 Rate limiting: foydalanuvchi – 1000/day, anonim – 100/day.

# 8 Yakuniy Tekshiruv va Checklist
 Loyihani serverda ishga tushirish
 Swagger orqali barcha endpointlarni tekshirish
 Foydalanuvchi ro‘yxatdan o‘tganda token olishi
 Xarajat qo‘shish, tahrirlash va o‘chirish
 Byudjet qo‘shish va hisobotlarni ko‘rish
 CSV eksport ishlashi
 Email orqali hisobot yuborish (agar sozlangan bo‘lsa)
 Foydalanuvchi o‘z ma’lumotlariga kirishi mumkinligini tekshirish
 Xavfsizlik va rate limiting ishlashini tekshirish
 Swagger/OpenAPI dokumentatsiyasi to‘liq  