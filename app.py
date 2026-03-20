import streamlit as st
import requests
import json
import re

# 1. إعدادات المتجر (هنا القوة: تغيرها حسب الزبون اللي يشتري منك)
STORE_NAME = "متجر النور للتقنية"  # اسم محل الزبون
EXPERT_NAME = "عباس"              # اسم البوت
PRODUCT_TYPE = "أجهزة الموبايل والحاسبات" # نوع البضاعة
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzboWW6szwgFDiHOc9-nETt--8F33WZHimWRvJmT-ZHE-Y7TTjUFx4dC_OeIAwp7gcVVQ/exec"

st.set_page_config(page_title=f"نظام مبيعات {STORE_NAME}", page_icon="🤖", layout="centered")

# --- التصميم الاحترافي ---
design = f"""
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] {{ visibility: hidden; display: none !important; }}
    .stApp {{ background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }}
    .chat-row {{ display: flex; margin: 15px 0; width: 100%; }}
    .user-row {{ justify-content: flex-start; }} 
    .abbas-row {{ justify-content: flex-end; }} 
    .bubble {{ padding: 15px; border-radius: 20px; max-width: 80%; font-size: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
    .user-bubble {{ background: #1e293b; color: white; border-bottom-left-radius: 2px; border: 1px solid #334155; }}
    .abbas-bubble {{ background: linear-gradient(135deg, #0284c7, #0369a1); color: white; border-bottom-right-radius: 2px; }}
    div[data-testid="stChatInput"] {{
        position: fixed !important; bottom: 20px !important; 
        background: #1e293b !important; border: 1px solid #0ea5e9 !important; border-radius: 15px !important;
    }}
    .stChatContainer {{ padding-bottom: 120px !important; }}
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# دالة الإرسال للإكسل
def send_to_excel(name, phone, order):
    payload = {"name": name, "phone": phone, "order": order}
    try: requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=5)
    except: pass

# 2. الواجهة
st.markdown(f"<h2 style='text-align:center; color:#38bdf8;'>🛡️ مساعد {STORE_NAME} الذكي</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#94a3b8;'>نظام {EXPERT_NAME} لإدارة المبيعات الآلية</p>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state: st.session_state.messages = []

# 4. عرض المحادثة
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 الزبون" if msg["role"] == "user" else f"🤖 {EXPERT_NAME}"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال والرد
if prompt := st.chat_input("تفضل، كيف أقدر أساعدك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 الزبون:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    # استخراج البيانات بالذكاء الاصطناعي (فلترة صافية)
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # تعليمات عباس المتغيرة حسب المحل
    context = f"""
    أنت المساعد الذكي '{EXPERT_NAME}' لمتجر '{STORE_NAME}' المتخصص في {PRODUCT_TYPE}.
    أسلوبك: عربي فصيح محبب مع كلمات عراقية (تدلل، عيوني، من رخصتك).
    هدفك: إقناع الزبون وطلب (اسمه ورقم هاتفه) لإتمام الطلب.
    عند استلام الرقم، قل له: [تم تسجيل طلبك بنجاح].
    """

    try:
        # 1. تحليل البيانات (بالخلفية)
        extract_prompt = f"Extract (name, phone, specific_order) from this text as JSON: {prompt}. If not found, use 'Unknown'."
        extract_res = requests.post(url, headers=headers, json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": "You are a data extractor."}, {"role": "user", "content": extract_prompt}]
        }, timeout=5)
        data_json = json.loads(extract_res.json()['choices'][0]['message']['content'])

        # 2. الرد على الزبون
        response = requests.post(url, headers=headers, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": context}] + st.session_state.messages,
            "temperature": 0.7
        }, timeout=10)
        ans = response.json()['choices'][0]['message']['content']

        # 3. إرسال للإكسل إذا وجدنا رقم هاتف
        if re.search(r'07\d{8,9}', prompt):
            send_to_excel(data_json.get('name', 'زبون جديد'), data_json.get('phone', 'بدون رقم'), data_json.get('specific_order', prompt))

        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🤖 {EXPERT_NAME}:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول، حاول مرة ثانية!")
