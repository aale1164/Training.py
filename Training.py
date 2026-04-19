import streamlit as st
import streamlit.components.v1 as components
import base64
import pytz
from datetime import datetime, date
import requests
from hijri_converter import Gregorian
import json

# --- إعداد الصفحة ---
st.set_page_config(page_title="مختبر التدريب - ساعة الأرض", page_icon="🧭", layout="wide")

# --- دالة تحويل الفيديو (عشان يشتغل كخلفية) ---
@st.cache_data
def get_video_base64(video_path):
    try:
        with open(video_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# جلب الفيديو (تأكد أن الملف tYdjwgYk-Wu19ONR.mp4 موجود في GitHub بجانب هذا الملف)
v_base64 = get_video_base64("tYdjwgYk-Wu19ONR.mp4")

# --- البيانات الأساسية (الطقس، التاريخ، المواقيت) ---
sa_tz = pytz.timezone('Asia/Riyadh')
now = datetime.now(sa_tz)
today = now.date()

# التاريخ الهجري والميلادي
try:
    h = Gregorian.fromdate(today).to_hijri()
    hij_str = f"{h.day}/{h.month}/{h.year} هـ"
except:
    hij_str = "--/--/---- هـ"
mil_str = f"{today.day}/{today.month}/{today.year} م"

# --- HTML + CSS + JavaScript ---
# ملاحظة: دمجت كود الساعة مع فيديو الشيخ في خلفية واحدة
html_code = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body, html {{ width: 100%; height: 100%; overflow: hidden; font-family: sans-serif; }}
        
        /* فيديو الخلفية */
        #bgVideo {{
            position: fixed;
            right: 0; bottom: 0;
            min-width: 100%; min-height: 100%;
            z-index: -1;
            filter: brightness(0.4); /* تعتيم الفيديو لبروز الساعة */
            object-fit: cover;
        }}

        .container {{
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: white;
            text-align: center;
            text-shadow: 2px 2px 15px rgba(0,0,0,0.9);
        }}

        .time {{ font-size: 5rem; font-weight: 900; margin-bottom: 10px; }}
        .ampm {{ font-size: 2.5rem; color: #FFD966; }}
        .date-info {{ font-size: 1.5rem; margin-top: 20px; }}
        .social {{ margin-top: 30px; font-size: 1.2rem; }}
        .social a {{ color: white; text-decoration: none; margin: 0 10px; font-weight: bold; }}
    </style>
</head>
<body>
    <video autoplay loop muted playsinline id="bgVideo">
        <source src="data:video/mp4;base64,{v_base64}" type="video/mp4">
    </video>

    <div class="container">
        <div>
            <span id="clock" class="time">--:--:--</span>
            <span id="ampm" class="ampm"></span>
        </div>
        
        <div class="date-info">
            <div style="font-size: 2.5rem; font-weight: bold;">{hij_str}</div>
            <div>{mil_str}</div>
        </div>

        <div class="social">
            <a href="https://twitter.com/aale1164">𝕏 @aale1164</a>
            <a href="https://snapchat.com/add/aale112">👻 aale112</a>
        </div>
    </div>

    <script>
        function update() {{
            const now = new Date();
            const options = {{ timeZone: 'Asia/Riyadh', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }};
            const parts = new Intl.DateTimeFormat('en-US', options).formatToParts(now);
            let t = "";
            let ap = "";
            parts.forEach(p => {{
                if (p.type === 'dayPeriod') ap = p.value;
                else if (p.type !== 'literal') t += p.value + (p.type === 'second' ? '' : ':');
            }});
            // تنظيف النقطتين الزايدتين في الأخير
            if (t.endsWith(':')) t = t.slice(0, -1);
            
            document.getElementById('clock').textContent = t;
            document.getElementById('ampm').textContent = ap;
        }}
        setInterval(update, 1000);
        update();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
