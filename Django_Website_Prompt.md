# برومبت احترافي كامل — موقع شركة هندسة معمارية/مقاولات باستخدام Django + Alpine.js

> تم تحليل ملفات التصميم (Home, About, Contact, Project Details, Projects, News) الخاصة بشركة "B-Group / Moonlight Architecture Studio" واستخلاص البنية والمكونات المشتركة لبناء برومبت تطوير احترافي.

---

## 1. ملخص تحليل التصميم

الموقع عبارة عن موقع تعريفي لشركة معمارية/مقاولات بألوان (كحلي داكن #14213D تقريبًا + رمادي فاتح مزرق للخلفية + أبيض)، خط Sans-serif نظيف، وتصميم Minimal مع خطوط فاصلة تحت العناوين.

### الصفحات المكتشفة:
| الصفحة | المكونات الرئيسية |
|---|---|
| **Home** | Hero (عنوان + وصف + زر) / قسم Specialization بتبويبات (Previous/Next) / قسم "We Turn Ideas Into Works of Art" / شبكة مشاريع (Our Projects) / شهادات عملاء (Testimonials Slider) / شعارات عملاء (Client Logos) / أحدث الأخبار (Latest News) / Footer |
| **About Us** | Hero نصي / "Who We Are" + قائمة "What We Do" / Testimonials / Client Logos / قسم الفريق (Our Team) مع بطاقة عضو مميزة |
| **Contact** | صورة Hero / معلومات التواصل (Address, Phone, Email, Social) / فورم تواصل (Name, Email, Message) / اقتباس جانبي |
| **Project Details** | Hero بعنوان المشروع وصورة كبيرة / صندوق معلومات جانبي (Info: Date, Client, Status, Location) / زر Description |
| **Projects (Listing)** | شبكة مشاريع متكررة بصورة + عنوان + وصف + زر "View Project" / Filter + Pagination (13/20) |
| **News (Blog Listing)** | قائمة مقالات (صورة + عنوان + مقتطف + زر View More) بالتناوب يمين/يسار / Pagination بالأرقام |

### المكونات المشتركة (Shared Components) عبر كل الصفحات:
1. **Header / Navbar**: شعار + قائمة روابط (Home, About Us, Project, Services, Contact Us) + قائمة موبايل.
2. **Footer**: 3 أعمدة (Call us / Write / Visit) + حقوق الملكية + أيقونات سوشيال ميديا.
3. **صندوق الاقتباس (Testimonial Quote Box)**: يظهر بجانب الفوتر في كل الصفحات الداخلية (لوجو + اقتباس + علامة تنصيص كبيرة).
4. **بطاقة الشهادة (Testimonial Card)**: اسم + منصب + نص شهادة + علامة تنصيص.
5. **بطاقة المشروع (Project Card)**: صورة + عنوان + وصف مختصر + رابط "View Project".
6. **بطاقة الخبر (News Card)**: صورة + عنوان + مقتطف + زر "View More".
7. **زر أساسي (Primary Button)**: بحدود/تعبئة كحلي، له حالة hover.
8. **Pagination**: أرقام صفحات + "...".
9. **شعارات العملاء (Client Logos Grid)**.
10. **فورم التواصل (Contact Form)**.

---

## 2. البرومبت الكامل (جاهز للاستخدام مع أداة برمجة/AI)

```
أنت مطوّر Django Full-Stack محترف. مطلوب منك بناء موقع شركة معمارية/مقاولات
باحتراف عالي باستخدام Django (Backend + Templates) و Alpine.js (للتفاعل في الواجهة).

==================================================
1) المتطلبات التقنية العامة
==================================================
- Django 5.x (آخر إصدار مستقر) + Python 3.12+
- Alpine.js (عبر CDN أو ملف محلي) للتفاعلات الأمامية فقط (Menu, Slider, Filter, Tabs, Form feedback)
- قاعدة بيانات: PostgreSQL (وSQLite للتطوير المحلي فقط)
- إدارة الملفات الثابتة عبر Django Static Files (whitenoise للإنتاج)
- HTMX اختياري إذا احتجنا تحديث جزئي (Pagination/Filter) بدون إعادة تحميل كامل — لكن التركيز الأساسي على Alpine.js
- استخدام Django Forms + CSRF لجميع النماذج
- التصميم Responsive بالكامل (Mobile First) بدون أي Framework CSS ضخم (لا Bootstrap) — بناء نظام تصميم مخصص (Design System) بسيط باستخدام CSS Variables

==================================================
2) قاعدة صارمة: ممنوع الكود المضمّن (Inline)
==================================================
- ممنوع نهائيًا استخدام style="..." داخل عناصر HTML.
- ممنوع نهائيًا استخدام <style> داخل أي template.
- ممنوع نهائيًا استخدام <script> يحتوي كود JS مباشر داخل الصفحات (Inline JS) أو onclick="" وما شابه.
- كل CSS يوضع في ملفات منفصلة داخل static/css/ مقسّمة حسب المكوّن:
    base.css        -> المتغيرات العامة، الـ Reset، الـ Typography
    layout.css       -> Header, Footer, Grid, Container
    components.css    -> Buttons, Cards, Testimonials, Pagination, Forms
    pages/home.css, pages/about.css, pages/contact.css, pages/project-detail.css,
    pages/projects.css, pages/news.css   -> تخصيصات كل صفحة فقط
- كل JS (منطق Alpine.js المخصص) يوضع في static/js/ مقسّم حسب الوظيفة:
    static/js/alpine-components.js  -> Alpine.data() لكل مكوّن (menu, tabsSpecialization, testimonialSlider, projectFilter, contactForm)
    static/js/main.js         -> تهيئة عامة فقط (تسجيل مكونات Alpine قبل تحميل alpine.js)
- الربط بين HTML و Alpine يتم فقط عبر x-data="componentName()" (استدعاء دالة معرفة في ملف JS خارجي)، وليس عبر x-data="{ ... }" مكتوب Inline داخل القالب لأي منطق معقد (يُسمح بـ x-data="{ open: false }" البسيط جدًا فقط عند الضرورة القصوى لعناصر صغيرة جدًا مثل toggle واحد، وما دون ذلك يُفضّل استخدام Alpine.data المسجل خارجيًا لضمان قابلية إعادة الاستخدام).

==================================================
3) هيكلة المشروع (Project Structure)
==================================================
bgroup_project/
├── manage.py
├── config/                     # إعدادات المشروع
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── apps/
│   ├── core/                   # الصفحات الثابتة (Home/About/Contact) + الموديلات المشتركة
│   │   ├── models.py           # SiteSettings, Testimonial, ClientLogo, TeamMember, ServiceItem
│   │   ├── views.py
│   │   ├── forms.py            # ContactForm
│   │   └── templatetags/
│   │       └── core_extras.py  # template tags مخصصة (مثل get_testimonials, get_client_logos)
│   ├── projects/                # تطبيق المشاريع
│   │   ├── models.py           # Project, ProjectImage, ProjectCategory
│   │   ├── views.py             # ListView + DetailView + Filter
│   │   └── urls.py
│   └── news/                    # تطبيق المدونة/الأخبار
│       ├── models.py            # Post, Category
│       ├── views.py             # ListView + Pagination
│       └── urls.py
├── templates/
│   ├── base.html                 # القالب الأساسي (Layout)
│   ├── includes/
│   │   ├── header.html            # Navbar (مكوّن مشترك)
│   │   ├── footer.html            # Footer (مكوّن مشترك)
│   │   ├── testimonial_box.html    # صندوق الاقتباس الجانبي
│   │   ├── testimonial_card.html    # كارت شهادة عميل
│   │   ├── client_logos.html       # شريط شعارات العملاء
│   │   ├── project_card.html       # كارت مشروع
│   │   ├── news_card.html          # كارت خبر
│   │   ├── pagination.html         # مكوّن الصفحات
│   │   └── button.html            # زر عام (يُستدعى بـ {% include %} مع متغيرات)
│   └── pages/
│       ├── home.html
│       ├── about.html
│       ├── contact.html
│       ├── project_detail.html
│       ├── project_list.html
│       └── news_list.html
├── static/
│   ├── css/  (كما وُصف أعلاه)
│   ├── js/   (كما وُصف أعلاه)
│   └── img/
└── media/                        # صور المشاريع/الأخبار المرفوعة من لوحة التحكم

==================================================
4) الموديلات (Models) المطلوبة
==================================================
- SiteSettings (Singleton): phone_sale, phone_support, email_support, email_sale, address, map_url, social_links (JSONField)
- Testimonial: client_name, position, company, quote, avatar (optional), is_featured
- ClientLogo: name, logo_image, order
- TeamMember: name, position, photo, quote, order
- ServiceItem: title, description, icon, order   (يُستخدم في "What We Do" و"Our Specialization")
- ProjectCategory: name, slug
- Project: title, slug, category(FK), cover_image, short_description, full_description,
           client_name, status(choices: ongoing/completed), location, date, is_featured, order
- ProjectImage: project(FK), image, caption   (لمعرض صور المشروع)
- NewsCategory: name, slug
- Post: title, slug, category(FK), cover_image, excerpt, content(RichText), published_at, is_published
- ContactMessage: name, email, message, created_at, is_read

==================================================
5) الصفحات ومنطقها
==================================================

### Home (/)
- Hero Section مع عنوان "MOONLIGHT ARCHITECTURE STUDIO" وزر "View More"
- قسم "Our Specialization" بتبويبات (Previous/Next) — مبني بـ Alpine.data('specializationTabs') لتبديل المحتوى بدون إعادة تحميل
- قسم "We Turn Ideas Into Works of Art" (نص ثابت من SiteSettings أو صفحة About)
- شبكة "Our Projects" — آخر 6 مشاريع مميزة (is_featured=True) عبر project_card.html
- Testimonials Slider — عرض 3 شهادات مع إمكانية التنقل (Alpine.data('testimonialSlider'))
- Client Logos — عرض شعارات العملاء (client_logos.html)
- Latest News — عرض آخر خبر (news_card.html)
- Footer + Testimonial Box

### About Us (/about/)
- Hero نصي "We Like To Build Things People Use"
- قسم "What We Do" (قائمة روابط من ServiceItem) + "Who We Are" (نص + صورة خلفية)
- Testimonials (نفس مكوّن الهوم)
- Client Logos (نفس المكوّن)
- "Our Team" — شبكة صور الفريق مع بطاقة عضو مُبرزة (TeamMember)

### Contact (/contact/)
- صورة Hero كبيرة (static/img)
- عمود معلومات التواصل: Address, Phone, Email, Social — تُسحب من SiteSettings
- ContactForm (Django Form: name, email, message) مع:
  - عرض/إخفاء رسائل النجاح/الخطأ عبر Alpine (x-show) بدون Inline JS — المنطق داخل alpine-components.js
  - Server-side validation عبر Django Forms + CSRF Token
  - عند النجاح: حفظ في ContactMessage + إرسال إيميل تنبيه (Django send_mail عبر Celery/queue اختياري)

### Project List (/projects/)
- شبكة مشاريع (Grid) عبر project_card.html
- فلترة حسب ProjectCategory:
  - الخيار المفضل: فلترة من السيرفر (Django View + GET params) لضمان SEO وعدم الاعتماد الكلي على JS
  - Alpine يُستخدم فقط لتحسين تجربة الفلترة بصريًا (active state على الأزرار) وليس لتنفيذ الفلترة نفسها
- Pagination عبر Django Paginator + مكوّن pagination.html القابل لإعادة الاستخدام

### Project Detail (/projects/<slug>/)
- Hero بصورة المشروع الرئيسية + عنوان + وصف
- صندوق Info جانبي (Date, Client, Status, Location) — بيانات من الموديل مباشرة
- زر "Description" (Accordion/Toggle بسيط عبر Alpine لعرض التفاصيل الكاملة)
- معرض صور إضافي إن وجد (ProjectImage)

### News List (/news/)
- قائمة مقالات بالتناوب (صورة يمين/يسار) عبر news_card.html مع متغير alternate
- Pagination عبر Django Paginator + pagination.html

==================================================
6) القالب الأساسي base.html
==================================================
- <head> يحتوي: meta tags أساسية (title ديناميكي عبر block title، description، og:tags)، ربط ملفات CSS (base.css, layout.css, components.css + ملف الصفحة الخاص عبر block extra_css)
- روابط CSS بعلامة <link rel="stylesheet"> فقط — ممنوع أي <style>
- {% include 'includes/header.html' %}
- {% block content %}{% endblock %}
- {% include 'includes/footer.html' %}
- {% include 'includes/testimonial_box.html' %} (فقط في الصفحات الداخلية، يُتحكم بها عبر متغير show_testimonial_box)
- تحميل Alpine.js من CDN مع defer، ثم main.js و alpine-components.js (يجب تسجيل المكونات عبر document.addEventListener('alpine:init', ...) قبل تحميل alpine.js نفسه، أو استخدام defer بالترتيب الصحيح)
- {% block extra_js %}{% endblock %} لأي ملف JS إضافي خاص بصفحة معينة (يبقى كملف خارجي منفصل أيضًا وليس Inline)

==================================================
7) مكونات Alpine.js المطلوب بناؤها (كلها في alpine-components.js)
==================================================
1. mobileMenu()        -> فتح/إغلاق قائمة الموبايل
2. specializationTabs() -> التنقل بين تبويبات "Our Specialization" في الهوم
3. testimonialSlider()  -> سلايدر شهادات العملاء (prev/next + dots)
4. projectFilter()      -> تحسين واجهة أزرار الفلترة (active class) مع submit فعلي للفورم نحو السيرفر
5. contactForm()        -> حالة الإرسال (loading/success/error) لفورم التواصل مع AJAX (fetch API) اختياري لتجربة أفضل بدون إعادة تحميل الصفحة، مع Fallback كامل للعمل بدون JS (Progressive Enhancement)
6. projectDescriptionToggle() -> إظهار/إخفاء الوصف الكامل في صفحة تفاصيل المشروع

كل دالة تُسجَّل هكذا داخل alpine-components.js:
document.addEventListener('alpine:init', () => {
    Alpine.data('mobileMenu', () => ({ ... }));
    Alpine.data('testimonialSlider', () => ({ ... }));
    ...
});

وفي القالب: <nav x-data="mobileMenu()"> ... </nav>

==================================================
8) معايير التصميم (Design System)
==================================================
- الألوان (تُعرَّف كـ CSS Variables في base.css):
  --color-primary: #14213D  (كحلي داكن)
  --color-bg-light: #E8ECF3 (رمادي مزرق فاتح للخلفيات)
  --color-white: #FFFFFF
  --color-text: #333333
  --color-text-muted: #6B7280
- الخطوط: خط Sans-serif نظيف (مثل Poppins أو Inter) لكل العناوين، وخط أساسي للنصوص
- استخدام خط فاصل صغير (underline accent) تحت العناوين الفرعية كما في التصميم الأصلي
- زوايا الأزرار حادة أو شبه حادة (Sharp/Minimal) بدون ظلال مبالغ فيها
- شبكة (Grid System) مبنية بـ CSS Grid/Flexbox فقط بدون أي مكتبة خارجية

==================================================
9) قابلية إعادة الاستخدام (Reusable Components)
==================================================
- كل مكوّن HTML متكرر (Button, Card, Pagination, Testimonial) يجب أن يكون Template مستقل في includes/
  يُستدعى بـ {% include 'includes/xxx.html' with param1=value1 param2=value2 %}
- إنشاء Template Tags مخصصة (core_extras.py) لجلب البيانات المشتركة (مثل {% get_client_logos %}, {% get_site_settings %}) بدلاً من تكرار الاستعلامات في كل View عبر Context Processor:
  - بناء context_processors.py يضيف site_settings تلقائيًا لكل الصفحات

==================================================
10) لوحة التحكم (Django Admin)
==================================================
- تسجيل كل الموديلات في admin.py مع list_display, search_fields, list_filter مناسبة
- استخدام django-ckeditor أو django-tinymce لحقل المحتوى في Post
- استخدام Inline Admin لـ ProjectImage داخل Project

==================================================
11) الأداء والجودة
==================================================
- ضغط الصور تلقائيًا عند الرفع (Pillow + django-imagekit اختياري)
- استخدام {% load static %} في كل مكان بدل مسارات ثابتة
- كتابة Tests أساسية (pytest-django) للـ Views الرئيسية والـ Models
- التأكد من كل الصفحات Responsive على الموبايل والتابلت
- استخدام Lazy Loading للصور (loading="lazy")
- عدم وجود console.log أو كود تجريبي في الإنتاج

==================================================
12) الناتج المطلوب
==================================================
سلّم لي:
1. هيكل المشروع الكامل بالملفات كما هو موضح أعلاه
2. كل ملفات CSS/JS منفصلة تمامًا عن الـ HTML (صفر Inline)
3. كل Templates تستخدم {% include %} للمكونات المشتركة
4. Alpine.js components جاهزة وموثقة بتعليقات قصيرة
5. Django Admin جاهز لإدارة كل المحتوى (بدون الحاجة لتعديل كود لإضافة مشروع/خبر/شهادة جديدة)
```

---

## 3. ملاحظات إضافية سريعة
- إذا رغبت لاحقًا في تفعيل **HTMX** بجانب Alpine.js لتحديث الفلترة/الـ Pagination دون إعادة تحميل الصفحة بالكامل، يمكن إضافته كطبقة تحسين دون كسر مبدأ "لا Inline JS" لأن كل الخصائص تكون عبر `hx-*` attributes في HTML وهو نمط مقبول (تصريحي وليس كود منفّذ inline).
- يُفضل إنشاء **Style Guide** بسيط (صفحة `/style-guide/` داخلية أثناء التطوير فقط) لعرض كل المكونات المشتركة (أزرار، كروت، فورم) في مكان واحد لتسهيل المراجعة.
- الألوان والقيم المذكورة في قسم Design System تقريبية بناءً على تحليل الصور، ويُفضّل تأكيدها مع فريق التصميم أو الحصول على ملف Figma/Brand Guide الرسمي إن وُجد.
