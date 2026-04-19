import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="مختبر التدريب", layout="wide")

# رابط الفيديو المباشر (Raw) من مستودعك
# تأكد أن اسم المستخدم في الرابط أدناه هو اسم حسابك في GitHub
video_url = "https://raw.githubusercontent.com/aale1164/flat-earth-clock./main/tYdjwgYk-Wu19ONR.mp4"

# كود الـ HTML الصافي مع الساعة والخلفية
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; width: 100%; }}
        
        #bgVideo {{
            position: fixed;
            right: 0; bottom: 0;
            min-width: 100%; min-height: 100%;
            z-index: -1;
            filter: brightness(0.4);
            object-fit: cover;
        }}

        .content {{
            position: relative;
            z-index: 1;
            color: white;
            text-align: center;
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-shadow: 2px 2px 20px black;
        }}

        .time {{ font-size: 80px; font-weight: bold; }}
    </style>
</head>
<body>
    <video autoplay loop muted playsinline id="bgVideo">
        <source src="{video_url}" type="video/mp4">
    </video>

    <div class="content">
        <div class="time" id="clock">00:00:00</div>
        <h2 style="margin-top: 20px;">نسخة التدريب - الساعة المباشرة</h2>
        <p>إذا ظهر هذا النص والخلفية سوداء، انتظر ثواني لتحميل الفيديو</p>
    </div>

    <script>
        function update() {{
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleTimeString('en-GB');
        }}
        setInterval(update, 1000);
        update();
    </script>
</body>
</html>
"""

components.html(html_code, height=800)
