import streamlit as st
import streamlit.components.v1 as components
import pytz
from datetime import datetime, date, timedelta
import requests
from hijri_converter import Gregorian
import json
import base64

# --- إعداد الصفحة ---
st.set_page_config(page_title="الأرض المسطحة - نسخة التدريب", page_icon="🧭", layout="wide")

# دالة لتحويل الفيديو المحلي لبيانات (Base64) ليتم عرضه كخلفية
@st.cache_data
def get_video_base64(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# محاولة استيراد مكتبة الموقع الجغرافي
try:
    from streamlit_js_eval import get_geolocation
    GEO_LIB_AVAILABLE = True
except ImportError:
    GEO_LIB_AVAILABLE = False

sa_tz = pytz.timezone('Asia/Riyadh')

# --- دوال جلب البيانات (مع تخزين مؤقت) ---
@st.cache_data(ttl=600)
def fetch_weather_cached(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        resp = requests.get(url, timeout=5).json()
        return resp['current_weather']['temperature']
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_prayer_times_cached(lat, lon, date_str):
    try:
        url = f"https://api.aladhan.com/v1/timings/{date_str}"
        params = {'latitude': lat, 'longitude': lon, 'method': 4}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data['code'] == 200:
            timings = data['data']['timings']
            return {
                'Fajr': timings['Fajr'], 'Sunrise': timings['Sunrise'],
                'Dhuhr': timings['Dhuhr'], 'Asr': timings['Asr'],
                'Maghrib': timings['Maghrib'], 'Isha': timings['Isha'],
            }
    except:
        pass
    return None

def get_season_data():
    today = date.today()
    y = today.year
    seasons = [
        ('الربيع', 'Spring', date(y, 3, 21), '🌸'),
        ('الصيف', 'Summer', date(y, 6, 21), '☀️'),
        ('الخريف', 'Autumn', date(y, 9, 23), '🍂'),
        ('الشتاء', 'Winter', date(y, 12, 21), '❄️')
    ]
    for ar, en, s_date, icon in seasons:
        if s_date > today:
            return ar, en, (s_date - today).days, icon
    next_spring = date(y + 1, 3, 21)
    return 'الربيع', 'Spring', (next_spring - today).days, '🌸'

# --- إدارة حالة الموقع الجغرافي ---
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = 26.32, 43.97
    st.session_state.location_checked = False

# تحويل الفيديو (تأكد من وجود ملف الفيديو في نفس المجلد بجوار الكود)
try:
    video_base64 = get_video_base64("tYdjwgYk-Wu19ONR.mp4")
except:
    video_base64 = "" # في حال لم يجد الملف

# --- البيانات الأساسية ---
now = datetime.now(sa_tz)
today = now.date()
weekdays_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
weekdays_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_ar = weekdays_ar[today.weekday()]
day_en = weekdays_en[today.weekday()]

try:
    h = Gregorian.fromdate(today).to_hijri()
    hij_str = f"{h.day}/{h.month}/{h.year} هـ"
except:
    hij_str = "--/--/---- هـ"
mil_str = f"{today.day}/{today.month}/{today.year} م"

temp = fetch_weather_cached(st.session_state.lat, st.session_state.lon)
weather_str = f"{temp}°C" if temp is not None else "--°C"
prayer_times_data = fetch_prayer_times_cached(st.session_state.lat, st.session_state.lon, today.strftime("%d-%m-%Y"))
sunrise = prayer_times_data.get('Sunrise', '--:--') if prayer_times_data else "--:--"
sunset = prayer_times_data.get('Maghrib', '--:--') if prayer_times_data else "--:--"
season_ar, season_en, days_left, season_icon = get_season_data()

# --- الـ HTML مع دمج الفيديو كخلفية ---
html_code = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body, html {{ 
            width: 100%; height: 100%; overflow: hidden; 
            font-family: 'Tajawal', sans-serif; 
        }}
        
        /* فيديو الخلفية */
        #bgVideo {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%; 
            min-height: 100%;
            z-index: -1;
            filter: brightness(0.4); /* تعتيم الفيديو لبروز النصوص */
            object-fit: cover;
        }}

        .main-container {{
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 5vh;
            color: white;
            height: 100vh;
            text-align: center;
        }}

        .text-shadow {{ text-shadow: 2px 2px 15px rgba(0,0,0,1); }}
        .time-display {{ font-size: clamp(3rem, 12vw, 5.5rem); font-weight: 900; }}
        .ampm-display {{ font-size: clamp(1.5rem, 6vw, 3rem); color: #FFD966; font-weight: 700; }}
        .season-main {{ font-size: 1.5rem; color: #B5FFB5; margin-top: 10px; font-weight: bold; }}
        
        .info-row {{
            display: flex;
            width: 90%;
            max-width: 600px;
            justify-content: space-between;
            margin-top: 30px;
        }}
        .info-col {{ flex: 1; }}
        .right-col {{ text-align: right; }}
        .left-col {{ text-align: left; }}
        
        .social-links {{ margin-top: 15px; display: flex; flex-direction: column; gap: 5px; }}
        .social-links a {{ color: white; text-decoration: none; font-weight: bold; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <video autoplay loop muted playsinline id="bgVideo">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>

    <div class="main-container">
        <div class="text-shadow">
            <span id="live-time" class="time-display">--:--:--</span>
            <span id="live-ampm" class="ampm-display"></span>
        </div>

        <div class="text-shadow season-main">
            {season_icon} متبقي على {season_ar}: {days_left} يوم
        </div>

        <div class="info-row">
            <div class="info-col right-col text-shadow">
                <div style="font-size: 2rem; font-weight: 900;">{day_ar}</div>
                <div style="font-size: 1.2rem; opacity: 0.8;">{day_en}</div>
                <div style="margin-top:10px; font-weight:bold;">{hij_str}</div>
                <div style="opacity:0.8;">{mil_str}</div>
                <div class="social-links">
                    <a href="https://twitter.com/aale1164">𝕏 @aale1164</a>
                    <a href="https://snapchat.com/add/aale112">👻 aale112</a>
                </div>
            </div>

            <div class="info-col left-col text-shadow">
                <div style="font-size: 1.8rem; font-weight: bold;">🌡️ {weather_str}</div>
                <div style="margin-top:15px;">
                    <div>☀️ الشروق: {sunrise}</div>
                    <div>🌅 الغروب: {sunset}</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateClock() {{
            const now = new Date();
            const options = {{ timeZone: 'Asia/Riyadh', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }};
            const timeStr = now.toLocaleTimeString('en-US', options);
            const [time, ampm] = timeStr.split(' ');
            document.getElementById('live-time').textContent = time;
            document.getElementById('live-ampm').textContent = ampm;
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
