import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# إعداد الصفحة
st.set_page_config(page_title="مختبر التدريب", layout="wide")

# دالة لقراءة الفيديو وتحويله لكود (هذه الطريقة تكسر حماية المتصفح وتجبره يشغل الفيديو)
def get_video_html(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f"""
            <style>
                #bgVideo {{
                    position: fixed;
                    right: 0; bottom: 0;
                    min-width: 100%; min-height: 100%;
                    z-index: -1;
                    filter: brightness(0.4);
                    object-fit: cover;
                }}
                .content {{
                    position: relative; z-index: 1; color: white;
                    text-align: center; font-family: 'Tajawal', sans-serif;
                    display: flex; flex-direction: column;
                    align-items: center; justify-content: center;
                    height: 100vh; text-shadow: 2px 2px 20px black;
                }}
                .time {{ font-size: clamp(3rem, 10vw, 6rem); font-weight: bold; }}
            </style>
            <video autoplay loop muted playsinline id="bgVideo">
                <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            </video>
            <div class="content">
                <div class="time" id="clock">00:00:00</div>
                <h2 style="margin-top: 20px;">ساعة الأرض - نسخة التدريب 🧭</h2>
                <p style="opacity: 0.8;">تم سحب الفيديو من ملفات السيرفر بنجاح</p>
            </div>
            <script>
                function update() {{
                    const now = new Date();
                    document.getElementById('clock').textContent = now.toLocaleTimeString('en-GB');
                }}
                setInterval(update, 1000);
                update();
            </script>
        """
    else:
        return "<h1>⚠️ لم يتم العثور على ملف الفيديو في المستودع</h1>"

# اسم ملف الفيديو اللي أنت رفعته بالضبط
video_file_name = "tYdjwgYk-Wu19ONR.mp4"

html_content = get_video_html(video_file_name)
components.html(html_content, height=1000, scrolling=False)
