import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# ========== إعدادات الصفحة ==========
st.set_page_config(
    page_title="مختبر التدريب - خلفية فيديو",
    page_icon="🧭",
    layout="wide"
)

# ========== دالة إنشاء HTML مع Base64 ==========
def get_video_html(file_path):
    """تقرأ الفيديو من static وتحوله إلى HTML مع Base64 ليعمل كخلفية كاملة"""
    # التحقق من وجود الملف
    if not os.path.exists(file_path):
        return f"""
        <div style="color:red; text-align:center; padding:50px; font-family:sans-serif;">
            <h1>⚠️ خطأ: ملف الفيديو غير موجود</h1>
            <p>المسار المطلوب: {file_path}</p>
            <p>تأكد من وجود مجلد <code>static</code> بداخله الفيديو بالاسم الصحيح.</p>
        </div>
        """

    # قراءة الملف وتحويله إلى Base64
    try:
        with open(file_path, "rb") as f:
            video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode()
    except Exception as e:
        return f"<h1 style='color:red; text-align:center;'>❌ خطأ في قراءة الفيديو: {e}</h1>"

    # قالب HTML مع CSS محسّن
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- خط Tajawal للعربية -->
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
                font-family: 'Tajawal', sans-serif;
            }}
            #bgVideo {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%;
                min-height: 100%;
                width: auto;
                height: auto;
                z-index: -1;
                filter: brightness(0.55);  /* زيادة السطوع قليلاً لجعل التفاصيل أوضح */
                object-fit: cover;
            }}
            .content {{
                position: relative;
                z-index: 1;
                color: white;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-shadow: 2px 2px 20px #000;
                padding: 20px;
                box-sizing: border-box;
            }}
            .time {{
                font-size: clamp(3rem, 15vw, 7rem);
                font-weight: bold;
                letter-spacing: 5px;
                background: rgba(0, 0, 0, 0.3);
                padding: 0.2em 0.8em;
                border-radius: 20px;
                backdrop-filter: blur(5px);
                margin-bottom: 30px;
            }}
            h2 {{
                font-size: clamp(1.8rem, 6vw, 3rem);
                margin: 10px 0;
            }}
            p {{
                opacity: 0.9;
                font-size: 1.2rem;
            }}
            .note {{
                position: absolute;
                bottom: 20px;
                right: 20px;
                color: rgba(255, 255, 255, 0.6);
                font-size: 0.8rem;
                z-index: 2;
            }}
        </style>
    </head>
    <body>
        <!-- فيديو الخلفية Base64 -->
        <video autoplay loop muted playsinline id="bgVideo">
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو.
        </video>

        <!-- المحتوى النصي فوق الفيديو -->
        <div class="content">
            <div class="time" id="clock">--:--:--</div>
            <h2>🧭 ساعة الأرض - نسخة التدريب</h2>
            <p>✅ تم سحب الفيديو من ملفات السيرفر بنجاح</p>
        </div>

        <!-- تذييل صغير -->
        <div class="note">🎥 خلفية متحركة | مختبر التدريب</div>

        <!-- ساعة رقمية تتحدث تلقائياً -->
        <script>
            (function() {{
                function updateClock() {{
                    const now = new Date();
                    const timeStr = now.toLocaleTimeString('en-GB');
                    const clockEl = document.getElementById('clock');
                    if (clockEl) clockEl.textContent = timeStr;
                }}
                updateClock();
                setInterval(updateClock, 1000);
            }})();
        </script>
    </body>
    </html>
    """

# ========== تشغيل التطبيق ==========
def main():
    # المسار القياسي: مجلد static بجانب app.py
    VIDEO_FILE = os.path.join("static", "tYdjwgYk-Wu19ONR.mp4")

    # عرض HTML داخل Streamlit
    html_content = get_video_html(VIDEO_FILE)
    components.html(html_content, height=850, scrolling=False)

    # رسالة إضافية في واجهة Streamlit في حالة عدم وجود الملف
    if not os.path.exists(VIDEO_FILE):
        st.error(f"🔴 الملف غير موجود: {VIDEO_FILE}")
        st.info("📁 تأكد من وجود مجلد `static` في نفس مسار التطبيق، وأن الفيديو بداخله بالاسم الصحيح.")

if __name__ == "__main__":
    main()
