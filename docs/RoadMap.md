# 🛣️ RaceTech.isr – RoadMap

## ✅ הושלם

### Client
- [x] main.py כולל התחברות ל-iRacing ו־Google
- [x] שליחה לשרת דרך WebSocket עם Fallback
- [x] מערכת config גמישה (send_interval, server_url וכו')
- [x] ניהול טוקן Google ו־RaceTech מקומי

### Web
- [x] מבנה React עם דפי בית, נהג, Checkout
- [x] תכנון עיצוב OnlyFans-style
- [x] רכיבי UI בסיסיים (components/pages)

### BackEnd
- [x] FastAPI – קובץ main.py ראשון
- [x] מסלול `/auth/google` לקבלת טוקן מהקליינט
- [x] אימות בסיסי של טוקן + החזרת טוקן פיקטיבי
- [x] הגדרת CORS והרצה עם uvicorn

---

## 🔜 בעבודה

### אבטחה
- [ ] בדיקת טוקן Google אמיתי (google.oauth2)
- [ ] יצירת JWT מאובטח עם exp + user_id
- [ ] Middleware לאימות כל בקשה עם Bearer Token

### WebSocket
- [ ] `/ws/lap` – קבלת הקפות מהלקוח
- [ ] אימות לפי הטוקן המצורף
- [ ] שמירת הקפה למסד נתונים + חישוב סקטורים

### Database
- [ ] חיבור PostgreSQL (RDS/AWS או Railway)
- [ ] יצירת ORM (SQLAlchemy/SQLModel)
- [ ] טבלת Users, Laps, Subscriptions
- [ ] CRUD בסיסי לנתוני משתמשים וטלמטריה

---

## ☁️ Deployment
- [ ] בניית תשתית AWS מלאה:
  - [ ] API Gateway
  - [ ] Lambda/EC2 להרצת FastAPI
  - [ ] RDS + S3
- [ ] CI/CD + הרצה אוטומטית

---

## 💳 רכישות
- [ ] Stripe או PayPal
- [ ] מנוי לפי הקפה / חודש / סשן
- [ ] ניהול רכישות, מעקב, והגבלות גישה

---

## 🧪 בדיקות
- [ ] סימולציית שליחה ללא iRacing
- [ ] בדיקות End-to-End
- [ ] בדיקות כשל ב־Client

---

## 📄 משפטי
- [ ] תנאי שימוש מלאים
- [ ] הסכמים עם נהגים / יוצרים
- [ ] פרטיות והסרת אחריות

---

📅 עודכן לאחרונה: 4 ביוני 2025
