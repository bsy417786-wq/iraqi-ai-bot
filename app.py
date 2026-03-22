import streamlit as st
import requests
import json
import re

# 1. الإعدادات
BRAND_NAME = "عباس حيدر للذكاء الاصطناعي"
EXPERT_NAME = "عباس"              
STORE_NAME = "متجر النور للتقنية" 
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzboWW6szwgFDiHOc9-nETt--8F33WZHimWRvJmT-ZHE-Y7TTjUFx4dC_OeIAwp7gcVVQ/exec"

st.set_page_config(page_title=BRAND_NAME, page_icon="🤖", layout="centered")

# --- التصميم وصعود الصندوق ---
design = """
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"], 
    [data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }
    .stApp { background: #0b141a; color: #e9edef; font-family: 'Segoe UI', sans-serif; }
    .chat-row { display: flex; margin: 15px 0; width: 100%; animation: fadeIn 0.4s ease-out; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 
    .bubble {
        padding: 12px 18px; border-radius: 18px; max-width: 78%;
        font-size: 16px; line-height: 1.5; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }
    
    div[data-testid="stChatInput"] {
        position: fixed !important; bottom: 40px !important; 
        left: 10% !important; right: 10% !important;
        width: 80% !important; z-index: 1000 !important;
        background: #202c33 !important; border: 1.5px solid #38bdf8 !important; border-radius: 20px !important;
    }
    .stChatContainer { padding-bottom: 180px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

def send_to_excel(name, phone, order):
    payload = {"name": name, "phone": phone, "order": order}
    try: requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=5)
    except: pass

# 2. الهوية
st.markdown(f"<h3 style='text-align:center; color:#38bdf8;'>🛡️ {BRAND_NAME}</h3>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 الزبون" if msg["role"] == "user" else f"🎮 {EXPERT_NAME}"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال والرد
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 الزبون:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # --- التعديل هنا ليكون عباس "ابن ولاية" ومثقف ---
    sys_instruction = (
        f"أنت المساعد الذكي '{EXPERT_NAME}' من شركة '{BRAND_NAME}'. "
        f"أسلوبك: بغدادي مؤدب جداً ومرحب. "
        "1. إذا سلم عليك الزبون، رد السلام بأفضل منه (مثلاً: هلا عيوني، مية هلا بيك، تفضل كلي شلون أساعدك؟). "
        "2. إذا سألك عن أي تفاصيل أو مواصفات، جاوبه بدقة وبروح طيبة. "
        "3. فقط عندما يقرر الزبون شراء شيء أو يطلب حجز منتج، قل له بأسلوب لبق: "
        "(صار عيوني من رخصتك بس الاسم والرقم حتى أثبت الحجز بالنظام ويوصلك الطلب بأسرع وقت). "
        "4. لا ترسل البيانات للإكسل إلا إذا كتب الزبون رقمه. "
        "5. عند استلام الرقم والاسم، قل حصراً: [تم تسجيل طلبك يا بطل]."
    )

    try:
        # استخراج البيانات
        extract_res = requests.post(url, headers=headers, json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": "Extract ONLY JSON: {name, phone, order}"}, {"role": "user", "content": prompt}]
        }, timeout=7)
        
        # الرد الطبيعي
        response = requests.post(url, headers=headers, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": sys_instruction}] + st.session_state.messages,
            "temperature": 0.8 # زدنا الـ Temperature شوية حتى يكون الكلام مو رسمي وجاف
        }, timeout=12)
        
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
            
            # الإرسال للإكسل فقط عند وجود رقم
            if re.search(r'07\d{8,9}', prompt):
                try:
                    raw_data = extract_res.json()['choices'][0]['message']['content']
                    clean_json = json.loads(re.search(r'\{.*\}', raw_data, re.DOTALL).group())
                    send_to_excel(clean_json.get('name', 'زبون جديد'), clean_json.get('phone', '07xxxxxxx'), clean_json.get('order', prompt))
                except:
                    send_to_excel("زبون جديد", "07xxxxxxx", prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 {EXPERT_NAME}:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول.")
