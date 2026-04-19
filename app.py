import streamlit as st
import streamlit.components.v1 as components
import pytz
from datetime import datetime, date, timedelta
import requests
from hijri_converter import Gregorian
import json
import base64

st.set_page_config(page_title="ط³ط§ط¹ط© ط§ظ„ط£ط±ط¶ - aale1164", layout="wide")

try:
    from streamlit_js_eval import get_geolocation
    GEO_LIB_AVAILABLE = True
except ImportError:
    GEO_LIB_AVAILABLE = False

sa_tz = pytz.timezone('Asia/Riyadh')

# --- ط¯ظˆط§ظ„ ط¬ظ„ط¨ ط§ظ„ط¨ظٹط§ظ†ط§طھ (ظ…ط¹ طھط®ط²ظٹظ† ظ…ط¤ظ‚طھ) ---
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
        params = {'latitude': lat, 'longitude': lon, 'method': 4, 'school': 0}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data['code'] == 200:
            timings = data['data']['timings']
            return {
                'Fajr': timings['Fajr'],
                'Sunrise': timings['Sunrise'],
                'Dhuhr': timings['Dhuhr'],
                'Asr': timings['Asr'],
                'Maghrib': timings['Maghrib'],
                'Isha': timings['Isha'],
            }
    except:
        pass
    return None

def get_tawalee_data():
    today = date.today()
    y = today.year
    tawalee = [
        ("ط§ظ„ظ…ط±ط¨ط¹ط§ظ†ظٹط©", date(y, 12, 7), "â‌„ï¸ڈ"),
        ("ط§ظ„ط´ط¨ط·", date(y + (1 if today > date(y, 1, 15) else 0), 1, 15), "ًںŒ¬ï¸ڈ"),
        ("ط§ظ„ط¹ظ‚ط§ط±ط¨", date(y + (1 if today > date(y, 2, 10) else 0), 2, 10), "ًں¦‚"),
        ("ط§ظ„ط­ظ…ظٹظ…ظٹظ†", date(y + (1 if today > date(y, 3, 21) else 0), 3, 21), "â›ˆï¸ڈ"),
        ("ط§ظ„ط°ط±ط¹ط§ظ†", date(y + (1 if today > date(y, 4, 16) else 0), 4, 16), "ًںŒ،ï¸ڈ"),
        ("ط§ظ„ظƒظ†ط©", date(y + (1 if today > date(y, 4, 29) else 0), 4, 29), "ًں”¥"),
        ("ط§ظ„ط«ط±ظٹط§", date(y + (1 if today > date(y, 6, 7) else 0), 6, 7), "âœ¨"),
        ("ط³ظ‡ظٹظ„", date(y + (1 if today > date(y, 8, 24) else 0), 8, 24), "ًںŒں"),
        ("ط§ظ„ظˆط³ظ…", date(y + (1 if today > date(y, 10, 16) else 0), 10, 16), "ًںŒ§ï¸ڈ")
    ]
    results = []
    for name, start_date, icon in tawalee:
        diff = (start_date - today).days
        if diff < 0:
            start_date = start_date.replace(year=start_date.year + 1)
            diff = (start_date - today).days
        results.append({"name": name, "days": diff, "icon": icon})
    results.sort(key=lambda x: x['days'])
    return results[:3]

def get_zodiac_data():
    today = date.today()
    zodiacs = [
        ("â™ˆ ط§ظ„ط­ظ…ظ„", (3, 21), (4, 19)),
        ("â™‰ ط§ظ„ط«ظˆط±", (4, 20), (5, 20)),
        ("â™ٹ ط§ظ„ط¬ظˆط²ط§ط،", (5, 21), (6, 20)),
        ("â™‹ ط§ظ„ط³ط±ط·ط§ظ†", (6, 21), (7, 22)),
        ("â™Œ ط§ظ„ط£ط³ط¯", (7, 23), (8, 22)),
        ("â™چ ط§ظ„ط¹ط°ط±ط§ط،", (8, 23), (9, 22)),
        ("â™ژ ط§ظ„ظ…ظٹط²ط§ظ†", (9, 23), (10, 22)),
        ("â™ڈ ط§ظ„ط¹ظ‚ط±ط¨", (10, 23), (11, 21)),
        ("â™گ ط§ظ„ظ‚ظˆط³", (11, 22), (12, 21)),
        ("â™‘ ط§ظ„ط¬ط¯ظٹ", (12, 22), (1, 19)),
        ("â™’ ط§ظ„ط¯ظ„ظˆ", (1, 20), (2, 18)),
        ("â™“ ط§ظ„ط­ظˆطھ", (2, 19), (3, 20))
    ]
    y = today.year
    for name, start, end in zodiacs:
        start_date = date(y, start[0], start[1])
        end_date = date(y, end[0], end[1])
        if start_date <= today <= end_date:
            return name
        if name == "â™‘ ط§ظ„ط¬ط¯ظٹ" and (today >= date(y, 12, 22) or today <= date(y, 1, 19)):
            return name
    return "â™ˆ ط§ظ„ط­ظ…ظ„"

@st.cache_data(ttl=86400)
def get_city_name_cached(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=ar"
        headers = {'User-Agent': 'FlatEarthClock/1.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            address = data.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village') or address.get('state')
            if city:
                return city
    except:
        pass
    try:
        url = f"https://geocode.xyz/{lat},{lon}?json=1"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            city = data.get('city') or data.get('region')
            if city:
                return city
    except:
        pass
    return "ط¬ط§ط±ظٹ طھط­ط¯ظٹط¯ ط§ظ„ظ…ظˆظ‚ط¹..."

@st.cache_data
def get_video_base64(video_path):
    try:
        with open(video_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

@st.cache_data
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# --- ط¥ط¯ط§ط±ط© ط­ط§ظ„ط© ط§ظ„ظ…ظˆظ‚ط¹ ط§ظ„ط¬ط؛ط±ط§ظپظٹ ---
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = 26.32, 43.97
    st.session_state.location_checked = False

if not st.session_state.location_checked and GEO_LIB_AVAILABLE:
    st.markdown("""
    <style>
        .stApp { background: url("https://raw.githubusercontent.com/aale1164/flat-earth-clock./main/background.png") center/cover fixed; }
        .permission-box {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; color: white; text-shadow: 2px 2px 5px black; text-align: center;
            background: rgba(0,0,0,0.3); backdrop-filter: blur(5px); padding: 20px;
        }
        .permission-box button {
            padding: 15px 30px; font-size: 20px; background: #FFA500; color: black;
            border: none; border-radius: 50px; cursor: pointer; font-weight: bold;
            margin-top: 20px; transition: 0.3s;
        }
        .permission-box button:hover { background: #FFD700; transform: scale(1.05); }
    </style>
    <div class="permission-box">
        <h1>ًںŒچ ط£ظ‡ظ„ط§ظ‹ ط¨ظƒ</h1>
        <p style="font-size: 18px;">ظ‡ط°ط§ ط§ظ„طھط·ط¨ظٹظ‚ ظ†ط³ط®ط© طھط¬ط±ظٹط¨ظٹط©طŒ ط´ط§ط±ظƒظˆظ†ط§ ط¢ط±ط§ط¦ظƒظ… ظˆط§ظ‚طھط±ط§ط­ط§طھظƒظ…</p>
        <p style="font-size: 18px;">ظ„ظƒظٹ ظ†ط¬ط¹ظ„ظ‡ ظٹطھظ†ط§ط³ط¨ ظ…ط¹ ط§ط­طھظٹط§ط¬ط§طھظƒظ…</p>
        <p style="font-size: 16px; margin-top: 15px;">ظ…ظ† ط®ظ„ط§ظ„ ط§ظ„ط¶ط؛ط· ط¹ظ„ظ‰ ظˆط³ط§ط¦ظ„ ط§ظ„طھظˆط§طµظ„ ظپظٹ ط§ظ„طµظپط­ط© ط§ظ„طھط§ظ„ظٹط© ظپظٹ ط¬ظ‡ط© ط§ظ„ظٹظ…ظٹظ†</p>
        <p style="font-size: 18px; margin-top: 25px;">ط¯ظ…طھظ… ط¨ط®ظٹط±طŒ ط£ط®ظˆظƒظ… / ط¹ط¯ظ†ط§ظ†ظٹ</p>
        <p style="font-size: 16px; margin-top: 30px;">ظ„ظ„ط­طµظˆظ„ ط¹ظ„ظ‰ ظ…ظˆط§ظ‚ظٹطھ ط§ظ„طµظ„ط§ط© ظˆط§ظ„ط·ظ‚ط³ ط¨ط¯ظ‚ط©طŒ ظ†ط±ط¬ظˆ ط§ظ„ظ…ظˆط§ظپظ‚ط© ط¹ظ„ظ‰ ظ…ط´ط§ط±ظƒط© ظ…ظˆظ‚ط¹ظƒ.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("ًں“چ ظ…ط´ط§ط±ظƒط© ط§ظ„ظ…ظˆظ‚ط¹", type="primary", use_container_width=True):
            try:
                loc = get_geolocation()
                if loc and 'coords' in loc:
                    st.session_state.lat = loc['coords']['latitude']
                    st.session_state.lon = loc['coords']['longitude']
                else:
                    st.warning("طھط¹ط°ط± ط§ظ„ط­طµظˆظ„ ط¹ظ„ظ‰ ط§ظ„ظ…ظˆظ‚ط¹. ط³ظٹطھظ… ط§ط³طھط®ط¯ط§ظ… ط§ظ„ظ…ظˆظ‚ط¹ ط§ظ„ط§ظپطھط±ط§ط¶ظٹ.")
                st.session_state.location_checked = True
                st.rerun()
            except Exception as e:
                st.error(f"ط­ط¯ط« ط®ط·ط£: {e}")
                st.session_state.location_checked = True
                st.rerun()
    st.stop()

if not st.session_state.location_checked:
    st.session_state.location_checked = True

# --- ط§ظ„ط¨ظٹط§ظ†ط§طھ ط§ظ„ط£ط³ط§ط³ظٹط© ---
now = datetime.now(sa_tz)
today = now.date()

weekdays_ar = ["ط§ظ„ط§ط«ظ†ظٹظ†", "ط§ظ„ط«ظ„ط§ط«ط§ط،", "ط§ظ„ط£ط±ط¨ط¹ط§ط،", "ط§ظ„ط®ظ…ظٹط³", "ط§ظ„ط¬ظ…ط¹ط©", "ط§ظ„ط³ط¨طھ", "ط§ظ„ط£ط­ط¯"]
weekdays_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_ar = weekdays_ar[today.weekday()]
day_en = weekdays_en[today.weekday()]

try:
    h = Gregorian.fromdate(today).to_hijri()
    hij_str = f"{h.day}/{h.month}/{h.year} ظ‡ظ€"
except:
    hij_str = "--/--/---- ظ‡ظ€"
mil_str = f"{today.day}/{today.month}/{today.year} ظ…"

temp = fetch_weather_cached(st.session_state.lat, st.session_state.lon)
weather_str = f"{temp}آ°C" if temp is not None else "--آ°C"

prayer_times_data = fetch_prayer_times_cached(st.session_state.lat, st.session_state.lon, today.strftime("%d-%m-%Y"))
sunrise = sunset = "--:--"
prayer_dict = {}
if prayer_times_data:
    sunrise = prayer_times_data.get('Sunrise', '--:--')
    sunset = prayer_times_data.get('Maghrib', '--:--')
    prayer_dict = {
        'ط§ظ„ظپط¬ط±': prayer_times_data.get('Fajr', '--:--'),
        'ط§ظ„ط¸ظ‡ط±': prayer_times_data.get('Dhuhr', '--:--'),
        'ط§ظ„ط¹طµط±': prayer_times_data.get('Asr', '--:--'),
        'ط§ظ„ظ…ط؛ط±ط¨': prayer_times_data.get('Maghrib', '--:--'),
        'ط§ظ„ط¹ط´ط§ط،': prayer_times_data.get('Isha', '--:--')
    }

def get_next_prayer(prayer_dict, current_time):
    prayers = [
        ('ط§ظ„ظپط¬ط±', prayer_dict.get('ط§ظ„ظپط¬ط±')),
        ('ط§ظ„ط¸ظ‡ط±', prayer_dict.get('ط§ظ„ط¸ظ‡ط±')),
        ('ط§ظ„ط¹طµط±', prayer_dict.get('ط§ظ„ط¹طµط±')),
        ('ط§ظ„ظ…ط؛ط±ط¨', prayer_dict.get('ط§ظ„ظ…ط؛ط±ط¨')),
        ('ط§ظ„ط¹ط´ط§ط،', prayer_dict.get('ط§ظ„ط¹ط´ط§ط،'))
    ]
    current_time_str = current_time.strftime('%H:%M')
    for name, time_str in prayers:
        if time_str and time_str > current_time_str:
            return name, time_str
    return 'ط§ظ„ظپط¬ط±', prayer_dict.get('ط§ظ„ظپط¬ط±', '--:--')

next_prayer_name, next_prayer_time = get_next_prayer(prayer_dict, now) if prayer_dict else ('ط§ظ„ظپط¬ط±', '--:--')

prayer_json = json.dumps(prayer_dict, ensure_ascii=False)

tawalee_list = get_tawalee_data()
tawalee_json = json.dumps(tawalee_list, ensure_ascii=False)

zodiac_current = get_zodiac_data()

city_name = get_city_name_cached(st.session_state.lat, st.session_state.lon)

video_path = "ARRR1.mp4"
video_base64 = get_video_base64(video_path)

image_path = "TTTT1.jpg"
image_base64 = get_image_base64(image_path)

html_code = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: 'Tajawal', sans-serif;
        }}

        .background-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}

        .bg-image {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/jpeg;base64,{image_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.75;
            z-index: -2;
        }}

        .video-card {{
            position: absolute;
            top: 2%;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 500px;
            z-index: 1;
            background: rgba(0,0,0,0.05);
            backdrop-filter: blur(8px);
            border-radius: 40px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        #bgVideo {{
            width: 100%;
            height: auto;
            display: block;
            opacity: 0.2;
            mix-blend-mode: lighten;
            filter: brightness(1.2);
        }}

        .main-container {{
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 600px;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: 24vh 16px 0 16px;
            margin: 0 auto;
            color: white;
            pointer-events: none;
        }}
        .main-container * {{
            pointer-events: auto;
        }}

        .card {{
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(5px);
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 10px 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}

        .time-card {{
            margin-bottom: 8px;
            margin-top: 0;
        }}
        .time-display {{
            font-size: clamp(2.5rem, 12vw, 4.5rem);
            font-weight: 900;
            line-height: 1;
            display: inline-block;
        }}
        .ampm-display {{
            font-size: clamp(2rem, 8vw, 3.5rem);
            margin-right: 8px;
            color: white;
            font-weight: 700;
            display: inline-block;
        }}

        .cards-grid {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: stretch;
            gap: 6px;
            width: 100%;
            margin-top: 5px;
        }}

        .date-card {{
            flex: 1.1;
            min-width: 110px;
            text-align: right;
        }}
        .day-ar {{ font-size: 1.4rem; font-weight: 900; }}
        .day-en {{ font-size: 0.9rem; opacity: 0.9; }}
        .hijri-date {{ font-size: 1.1rem; font-weight: 700; margin-top: 5px; }}
        .miladi-date {{ font-size: 0.9rem; opacity: 0.9; }}

        .prayer-card {{
            flex: 1.2;
            min-width: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .prayer-icon {{ font-size: 1.6rem; }}
        .prayer-name {{ font-size: 1.2rem; font-weight: 700; margin: 4px 0; }}
        .prayer-time {{ font-size: 1.4rem; font-weight: 900; }}

        .weather-card {{
            flex: 1.1;
            min-width: 110px;
            text-align: left;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .weather-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2px;
        }}
        .weather-label {{
            opacity: 0.8;
            font-size: 0.8rem;
        }}
        .weather-value {{
            font-weight: bold;
            font-size: 1.1rem;
        }}

        .tawalee-container {{
            display: flex;
            justify-content: center;
            align-items: stretch;
            gap: 6px;
            margin-top: 8px;
            flex-wrap: wrap;
        }}
        .tawalee-item, .zodiac-item {{
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(5px);
            padding: 6px 10px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
            min-width: 75px;
            flex: 1 0 70px;
        }}
        .tawalee-icon, .zodiac-icon {{ font-size: 1.4rem; display: block; }}
        .tawalee-name, .zodiac-name {{ font-weight: bold; font-size: 0.9rem; }}
        .tawalee-days {{ font-size: 0.8rem; opacity: 0.9; }}

        .city-card {{
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(5px);
            padding: 6px 12px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
            min-width: 100px;
            margin-top: 5px;
        }}
        .city-icon {{ font-size: 1.2rem; }}
        .city-name {{ font-weight: bold; font-size: 0.9rem; }}

        .social-footer {{
            margin-top: 10px;
            padding-bottom: 15px;
            display: flex;
            gap: 12px;
            justify-content: center;
        }}
        .social-footer a {{
            color: white;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: bold;
            padding: 6px 16px;
            background: rgba(0,0,0,0.4);
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(5px);
            transition: 0.2s;
        }}
        .social-footer a:hover {{
            background: rgba(255,165,0,0.6);
        }}

        @media (max-width: 480px) {{
            .main-container {{ padding: 24vh 10px 0 10px; }}
            .time-display {{ font-size: 2.2rem; }}
            .ampm-display {{ font-size: 1.8rem; }}
            .cards-grid {{ gap: 4px; }}
            .date-card, .weather-card {{ min-width: 100px; }}
            .day-ar {{ font-size: 1.2rem; }}
            .prayer-name {{ font-size: 1rem; }}
            .prayer-time {{ font-size: 1.2rem; }}
            .weather-value {{ font-size: 1rem; }}
            .tawalee-item, .zodiac-item {{ min-width: 65px; padding: 5px 4px; }}
            .city-card {{ min-width: 80px; }}
        }}
    </style>
</head>
<body>
    <div class="background-container">
        <div class="bg-image"></div>
        <div class="video-card">
            {f'<video autoplay loop muted playsinline id="bgVideo"><source src="data:video/mp4;base64,{video_base64}" type="video/mp4"></video>' if video_base64 else ''}
        </div>
    </div>

    <div class="main-container">
        <div class="card time-card">
            <span id="live-time" class="time-display">--:--:--</span>
            <span id="live-ampm" class="ampm-display"></span>
        </div>

        <div class="cards-grid">
            <div class="card date-card">
                <div class="day-ar">{day_ar}</div>
                <div class="day-en">{day_en}</div>
                <div class="hijri-date">{hij_str}</div>
                <div class="miladi-date">{mil_str}</div>
            </div>

            <div class="card prayer-card">
                <div class="prayer-icon">ًں•Œ</div>
                <div class="prayer-name">{next_prayer_name}</div>
                <div class="prayer-time">{next_prayer_time}</div>
            </div>

            <div class="card weather-card">
                <div class="weather-row">
                    <span class="weather-label">ًںŒ،ï¸ڈ ط§ظ„ط­ط±ط§ط±ط©</span>
                    <span class="weather-value">{weather_str}</span>
                </div>
                <div class="weather-row">
                    <span class="weather-label">âک€ï¸ڈ ط§ظ„ط´ط±ظˆظ‚</span>
                    <span class="weather-value">{sunrise}</span>
                </div>
                <div class="weather-row">
                    <span class="weather-label">ًںŒ… ط§ظ„ط؛ط±ظˆط¨</span>
                    <span class="weather-value">{sunset}</span>
                </div>
            </div>
        </div>

        <!-- طµظپ ظˆط§ط­ط¯ ظٹط¬ظ…ط¹ ط§ظ„ط·ظˆط§ظ„ظٹط¹ + ط§ظ„ط¨ط±ط¬ -->
        <div id="tawalee-container" class="tawalee-container"></div>

        <div class="city-card">
            <span class="city-icon">ًں“چ</span>
            <span class="city-name">{city_name}</span>
        </div>

        <div class="social-footer">
            <a href="https://twitter.com/aale1164" target="_blank">ً‌•ڈ @aale1164</a>
            <a href="https://www.snapchat.com/add/aale112" target="_blank">ًں‘» aale112</a>
        </div>
    </div>

    <script>
        const prayerTimes = {prayer_json};
        const TIMEZONE = 'Asia/Riyadh';
        const tawaleeData = {tawalee_json};
        const zodiacCurrent = "{zodiac_current}";

        function renderTawalee() {{
            const container = document.getElementById('tawalee-container');
            container.innerHTML = '';
            
            // ط¥ط¶ط§ظپط© ط¨ط·ط§ظ‚ط§طھ ط§ظ„ط·ظˆط§ظ„ظٹط¹ ط§ظ„ط«ظ„ط§ط«
            tawaleeData.forEach(item => {{
                const div = document.createElement('div');
                div.className = 'tawalee-item';
                div.innerHTML = `
                    <span class="tawalee-icon">${{item.icon}}</span>
                    <div class="tawalee-name">${{item.name}}</div>
                    <div class="tawalee-days">${{item.days}} ظٹظˆظ…</div>
                `;
                container.appendChild(div);
            }});
            
            // ط¥ط¶ط§ظپط© ط¨ط·ط§ظ‚ط© ط§ظ„ط¨ط±ط¬ ظƒط§ظ„ط¨ط·ط§ظ‚ط© ط§ظ„ط±ط§ط¨ط¹ط©
            const zodiacDiv = document.createElement('div');
            zodiacDiv.className = 'zodiac-item';
            zodiacDiv.innerHTML = `
                <span class="zodiac-icon">${{zodiacCurrent.split(' ')[0]}}</span>
                <div class="zodiac-name">${{zodiacCurrent}}</div>
            `;
            container.appendChild(zodiacDiv);
        }}

        function updateClock() {{
            const now = new Date();
            const formatter = new Intl.DateTimeFormat('en-US', {{
                timeZone: TIMEZONE,
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric',
                hour12: false
            }});
            const parts = formatter.formatToParts(now);
            const timeObj = {{}};
            parts.forEach(p => {{ timeObj[p.type] = p.value; }});

            let hour = parseInt(timeObj.hour);
            const minute = parseInt(timeObj.minute);
            const second = parseInt(timeObj.second);

            const hour12 = hour % 12 || 12;
            const ampmEn = hour >= 12 ? 'PM' : 'AM';

            document.getElementById('live-time').textContent = 
                `${{hour12}}:${{minute.toString().padStart(2, '0')}}:${{second.toString().padStart(2, '0')}}`;
            document.getElementById('live-ampm').textContent = ampmEn;
        }}

        function scheduleMidnightRefresh() {{
            const now = new Date();
            const nextMidnight = new Date(now);
            nextMidnight.setDate(now.getDate() + 1);
            nextMidnight.setHours(0, 0, 5, 0);
            const timeUntilMidnight = nextMidnight - now;
            setTimeout(() => {{ location.reload(); }}, timeUntilMidnight);
        }}

        renderTawalee();
        updateClock();
        setInterval(updateClock, 1000);
        scheduleMidnightRefresh();
    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
