# 📁✨ Fayl Yuklash va Parsing Tizimi - Django REST API

> 🚀 Fayl yuklash, parsing va boshqarish uchun zamonaviy RESTful API

---

## 🌍 Loyiha Tavsifi

🔹 **Tizim imkoniyatlari:**
- 📂 Turli formatdagi fayllarni (PDF, rasm, CSV, Excel) yuklash va ko‘rish
- 🏷️ Fayllarni kategoriyalarga ajratish
- 🔍 Fayl qidirish va filtrlash
- 🛠️ CSV va Excel parsing qilish va ma'lumotlarni saqlash
- 📥 Katta hajmdagi fayllarni chunked upload orqali yuklash

---

## 🛠️ Texnologiyalar

| Texnologiya         | Tavsif                             |
|---------------------|------------------------------------|
| Django REST Framework | API server |
| SimpleJWT             | Token autentifikatsiya |
| PostgreSQL           | Ma'lumotlar bazasi |
| Pandas, openpyxl      | CSV va Excel fayl parsing |
| drf-yasg             | Swagger dokumentatsiyasi |

---

## 🚦 API Endpointlari

### 🔑 Autentifikatsiya
| Endpoint                | Metod | Tavsif                        |
|--------------------------|-------|-------------------------------|
| `/api/auth/register/`    | POST  | Ro‘yxatdan o‘tish             |
| `/api/auth/login/`       | POST  | Kirish va token olish         |
| `/api/auth/logout/`      | POST  | Chiqish                       |
| `/api/auth/user/`        | GET   | Joriy foydalanuvchi ma’lumotlari |

---

### 🗂️ Kategoriyalar
| Endpoint                | Metod | Tavsif                     |
|--------------------------|-------|----------------------------|
| `/api/categories/`       | GET/POST | Kategoriyalar ro'yxati yoki yaratish |
| `/api/categories/{id}/`  | GET/PUT/PATCH/DELETE | Kategoriya tafsilotlari, tahrirlash yoki o'chirish |

---

### 📁 Fayllar
| Endpoint                | Metod | Tavsif                        |
|--------------------------|-------|-------------------------------|
| `/api/files/`            | GET/POST | Fayl ro'yxati yoki yuklash    |
| `/api/files/{id}/`       | GET/PUT/PATCH/DELETE | Fayl tafsilotlari yoki tahrirlash |
| `/api/files/{id}/download/` | GET | Faylni yuklab olish           |
| `/api/files/search/`     | GET   | Fayl qidirish                 |
| `/api/files/by-category/{category_id}/` | GET | Kategoriya bo'yicha fayllar |
| `/api/files/my-files/`   | GET   | Shaxsiy yuklangan fayllar     |

---

### 🧩 Katta Fayl Yuklash (Chunked Upload)
| Endpoint                      | Metod | Tavsif                  |
|--------------------------------|-------|--------------------------|
| `/api/chunked-uploads/`        | POST  | Yuklashni boshlash       |
| `/api/chunked-uploads/{id}/`   | PUT/GET | Fayl qismini yuklash yoki holat tekshirish |
| `/api/chunked-uploads/{id}/complete/` | POST | Yuklashni tugatish        |

---

### 🧪 CSV/Excel Parsing
| Endpoint                        | Metod | Tavsif                    |
|----------------------------------|-------|----------------------------|
| `/api/files/{id}/parse/`         | POST  | CSV/Excel parsing qilish   |
| `/api/imported-data/`            | GET   | Import qilingan ma'lumotlar |
| `/api/imported-data/{id}/`       | GET   | Ma'lumot tafsilotlari       |
| `/api/imported-data/{id}/export/` | GET  | CSV/Excel formatga eksport  |

---

### 🛡️ Fayl Ruxsatlari
| Endpoint                        | Metod | Tavsif                     |
|----------------------------------|-------|-----------------------------|
| `/api/files/{id}/permissions/`   | GET/POST | Fayl ruxsatlari ko'rish yoki qo'shish |
| `/api/permissions/{id}/`         | PUT/PATCH/DELETE | Ruxsat yangilash yoki o'chirish |

---
## 🔹🔒 Xavfsizlik

- Barcha fayllarga faqat autentifikatsiya qilingan foydalanuvchilar kirishi mumkin.
- Fayl egasi yoki ruxsat berilgan foydalanuvchi faylni ko‘rishi/tahrir qilishi mumkin.
- Fayl hajmi va turi cheklanadi.
- Fayl nomlari tozalab, xavfsiz qilinadi.

## 📂 O'rnatish va Ishga Tushirish

```bash
# Loyihani yuklab olish
git clone https://github.com/Bunyodjon-Mamadaliyev/Amaliy-loyiha.git
cd file-upload-parser-api

# Virtual muhit yaratish va faollashtirish
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Talablar faylini o'rnatish
pip install -r requirements.txt

# Migratsiyalarni qo'llash
python manage.py migrate

# Serverni ishga tushirish
python manage.py runserver
```