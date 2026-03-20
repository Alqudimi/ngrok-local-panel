# Ngrok Local Control Panel (Backend)

نظام متطور لإدارة وتحكم ngrok محلياً باستخدام FastAPI و Python.

## المميزات الرئيسية

- **إدارة العمليات**: تشغيل، إيقاف، وإعادة تشغيل ngrok كخدمة خلفية.
- **إدارة الأنفاق**: إنشاء وإدارة أنفاق متعددة (HTTP, TCP, TLS) ديناميكياً.
- **المراقبة**: متابعة حالة النظام، استهلاك الموارد، والأنفاق النشطة.
- **الأمان**: دعم JWT و API Keys (قابل للتفعيل).
- **التنبيهات**: تكامل مع Discord و Telegram عبر Webhooks.
- **التوثيق**: واجهة Swagger API كاملة.

## هيكل المشروع

```text
ngrok_control_panel/
├── app/
│   ├── api/            # API Endpoints
│   ├── core/           # الإعدادات والأمان
│   ├── models/         # نماذج البيانات
│   ├── schemas/        # Pydantic Schemas
│   ├── services/       # منطق العمل (Process, Tunnel, Webhook)
│   └── utils/          # أدوات مساعدة (Logging)
├── config/             # ملفات الإعدادات
├── data/               # بيانات ngrok (YAML)
├── logs/               # السجلات
└── main.py             # نقطة انطلاق التطبيق
```

## التشغيل

1. تثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```

2. تشغيل السيرفر:
   ```bash
   python main.py
   ```

3. الوصول للتوثيق:
   افتح المتصفح على `http://localhost:8000/docs`

## واجهة API (أمثلة)

- `GET /api/v1/status`: الحصول على حالة النظام.
- `POST /api/v1/start`: تشغيل ngrok.
- `POST /api/v1/tunnels`: إضافة نفق جديد.
- `GET /api/v1/active-tunnels`: عرض الأنفاق النشطة حالياً.

## المتطلبات التقنية
- Python 3.10+
- ngrok installed in system path

## حقوق النشر ©

Copyright © 2026 Abdulaziz Alqudimi. All rights reserved.
