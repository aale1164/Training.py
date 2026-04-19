import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="مختبر التدريب", layout="wide")

# رابط الفيديو المباشر من مستودعك (تأكد من اسم المستخدم الخاص بك بدلاً من USERNAME)
video_url = "https://raw.githubusercontent.com/aale1164/flat-earth-clock./main/tYdjwgYk-Wu19ONR.mp4"

# كود الخلفية
st.markdown(
    f"""
    <style>
    .stApp {{
        background: none;
    }}
    #bgVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1;
        filter: brightness(0.5);
        object-fit: cover;
    }}
    </style>
    <video autoplay loop muted playsinline id="bgVideo">
        <source src="{video_url}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

st.title("تم تشغيل خلفية الفيديو بنجاح! ✅")
st.write("الآن نستطيع دمج الساعة فوق هذا المنظر.")
