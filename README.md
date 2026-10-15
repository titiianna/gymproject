<p align="center">
  <a href="https://quera.org/bootcamp/python-alpha-qbc13">
    <img src="assets/banner.png"
         alt="Gym Management System Banner"
         width="100%">
  </a>
</p>

---

## ۱. نمای کلی برنامه

```mermaid
flowchart TD
    A([شروع: python main.py]) --> B["database_init()<br/>خواندن اطلاعات از فایل‌ها"]
    B --> C{"users.json<br/>وجود دارد؟"}
    C -- "نه (اولین اجرا)" --> D["seed_data()<br/>ساخت داده‌ی نمونه"]
    D --> E["save_all()<br/>ذخیره در فایل‌ها"]
    E --> F
    C -- "بله" --> G["خواندن همه‌ی فایل‌های JSON و TXT"]
    G --> F["منوی اصلی"]

    F --> F1["1. Admin login"]
    F --> F2["2. Coach login"]
    F --> F3["3. Member login"]
    F --> F4["4. Exit"]

    F1 --> L["login_flow(role)"]
    F2 --> L
    F3 --> L

    L --> M{"ورود موفق؟"}
    M -- "نه" --> N{"Try again<br/>یا Back؟"}
    N -- "Try again" --> L
    N -- "Back" --> F
    M -- "بله" --> P{"نقش کاربر"}
    P -- "admin" --> AP["admin_panel"]
    P -- "coach" --> CP["coach_panel"]
    P -- "member" --> MP["member_panel"]
    AP --> F
    CP --> F
    MP --> F

    F4 --> S["save_all()<br/>ذخیره‌ی نهایی"]
    S --> Z([پایان: Goodbye!])
```

---

## ۲. ورود به سیستم (Login)

```mermaid
flowchart TD
    A(["login_flow(role, db)"]) --> B["پرسیدن Username و Password"]
    B --> C{"کاربر خالی گذاشت<br/>یا لغو کرد؟"}
    C -- "بله" --> Z([برگشت به منوی اصلی])
    C -- "نه" --> D["AuthService.login()"]
    D --> E{"کاربر وجود دارد؟"}
    E -- "نه" --> X["پیام: Incorrect username or password"]
    E -- "بله" --> F{"نقش درست است؟"}
    F -- "نه" --> X
    F -- "بله" --> G{"رمز درست است؟"}
    G -- "نه" --> X
    G -- "بله" --> H{"حساب فعال است؟"}
    H -- "نه" --> Y["پیام: This account is inactive"]
    H -- "بله" --> OK["پیام: Login successful"]
    OK --> PANEL([رفتن به پنل مربوط به نقش])
    X --> R{"Try again یا Back؟"}
    Y --> R
    R -- "Try again" --> B
    R -- "Back" --> Z
```

---

## ۳. پنل ادمین (Admin)

```mermaid
flowchart TD
    A(["Admin panel"]) --> M{"منوی ادمین"}
    M --> U["1. Manage users"]
    M --> H["2. Manage halls"]
    M --> C["3. Manage classes"]
    M --> P["4. Manage plans and payments"]
    M --> R["5. View reports"]
    M --> E["6. Exit"]

    U --> U1["Add user<br/>Edit user<br/>Activate/deactivate<br/>View users<br/>+ خروجی txt کاربران"]
    H --> H1["Add hall<br/>Edit hall<br/>Activate/deactivate<br/>View halls"]
    C --> C1["Create class<br/>Edit class<br/>Activate/deactivate<br/>View classes"]
    P --> P1["Define a new plan<br/>View plans<br/>Assign a plan to a member<br/>View payments<br/>Members' subscription status"]
    R --> R1["اعضای فعال، مربی‌های فعال<br/>کلاس‌های فعال، کل درآمد<br/>محبوب‌ترین کلاس"]

    U1 --> M
    H1 --> M
    C1 --> M
    P1 --> M
    R1 --> M
    E --> S["save_all()"] --> Z([خروج از پنل])
```

---

## ۴. پنل مربی (Coach)

```mermaid
flowchart TD
    A(["Coach panel"]) --> M{"منوی مربی"}
    M --> V["1. View my classes"]
    M --> T["2. Manage members' training programs"]
    M --> E["3. Exit"]

    V --> V1["نمایش کلاس‌های مربی<br/>و اعضای ثبت‌نام‌شده"] --> M

    T --> T1["انتخاب کلاس"]
    T1 --> T2["انتخاب عضو"]
    T2 --> T3{"عضو برنامه‌ی تمرینی دارد؟"}
    T3 -- "نه" --> T4["Create program<br/>افزودن تمرین‌ها"]
    T4 --> T3
    T3 -- "بله" --> T5["View program<br/>Add exercise<br/>Edit exercise<br/>Back"]
    T5 --> M

    E --> S["save_all()"] --> Z([خروج از پنل])
```

---

## ۵. پنل عضو (Member)

```mermaid
flowchart TD
    A(["Member panel"]) --> M{"منوی عضو"}
    M --> P1["1. Profile and subscription status"]
    M --> P2["2. Wallet"]
    M --> P3["3. Classes"]
    M --> P4["4. Training program"]
    M --> E["5. Exit"]

    P1 --> P1a["نمایش نام، ایمیل، پلن،<br/>تاریخ شروع و پایان اشتراک"] --> M
    P2 --> W["View balance<br/>Top up wallet<br/>View transactions<br/>Pay for or renew a plan"] --> M
    P3 --> K["View classes available for enrollment<br/>Enroll in a class<br/>Cancel class enrollment<br/>My classes"] --> M
    P4 --> T["نمایش برنامه‌ی تمرینی<br/>که مربی نوشته"] --> M

    E --> S["save_all()"] --> Z([خروج از پنل])
```

---

## ۶. ساختار فایل‌ها (چه کسی با چه کسی حرف می‌زند؟)

```mermaid
flowchart LR
    main["main.py<br/>شروع برنامه"] --> ui["ui/<br/>منوها<br/>admin_menu, coach_menu,<br/>member_menu, helpers"]
    main --> auth["services/auth_service.py<br/>ورود"]
    main --> db["database.py<br/>خواندن/ذخیره"]

    ui --> services["services/<br/>منطق کارها<br/>admin_service, coach_service,<br/>member_service"]
    services --> models["models/<br/>شکل داده‌ها<br/>user, wallet, subscription,<br/>class_session, hall,<br/>training_program, enrollment"]
    db --> models
    db --> fh["utils/file_handler.py<br/>خواندن و نوشتن فایل"]
    services --> utils["utils/<br/>validators, constants,<br/>generators, id_generator,<br/>decorators, Bank"]
    fh --> files[("فایل‌های داده<br/>*.json و transactions.txt")]
```

---

## ۷. مسیر ذخیره‌ی اطلاعات

```mermaid
flowchart LR
    A["شروع برنامه"] --> B["database_init()"]
    B --> C[("فایل‌ها")]
    C --> D["db = دیکشنری در حافظه"]
    D --> E["کاربر کار می‌کند<br/>(ثبت‌نام، پرداخت، ...)"]
    E --> D
    E --> F["خروج از پنل یا برنامه"]
    F --> G["save_all(db)"]
    G --> C
```