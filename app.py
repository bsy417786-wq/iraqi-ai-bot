import streamlit as st
import requests
import json
import re

# 1. إعدادات النظام
BRAND_NAME = "عباس حيدر للذكاء الاصطناعي"
EXPERT_NAME = "عباس"              
STORE_NAME = "متجر النور للتقنية" 
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzboWW6szwgFDiHOc9-nETt--8F33WZHimWRvJmT-ZHE-Y7TTjUFx4dC_OeIAwp7gcVVQ/exec"

st.set_page_config(page_title=BRAND_NAME, page_icon="🤖", layout="centered")

# --- التصميم الاحترافي (صندوق الكتابة صاعد وواضح) ---
design = """
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"], [data-testid="stStatusWidget"] { visibility: hidden; display: none !important; }
    .stApp { background: #0b141a; color: #e9edef; font-family: 'Segoe UI', sans-serif; }
    .chat-row { display: flex; margin: 15px 0; width: 100%; animation: fadeIn 0.3s; }
    .user-row { justify-content: flex-start; } .abbas-row { justify-content: flex-end; } 
    .bubble { padding: 12px 18px; border-radius: 18px; max-width: 78%; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }
    div[data-testid="stChatInput"] { position: fixed !important; bottom: 40px !important; left: 10% !important; right: 10% !important; width: 80% !important; z-index: 1000 !important; background: #202c33 !important; border: 1.5px solid #38bdf8 !important; border-radius: 20px !important; }
    .stChatContainer { padding-bottom: 180px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

def send_to_excel(name, phone, order):
    payload = {"name": name, "phone": phone, "order": order}
    try:
        requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=10)
    except:
        pass

# 2. الهوية
st.markdown(f"<h3 style='text-align:center; color:#38bdf8;'>🛡️ {BRAND_NAME}</h3>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 الزبون" if msg["role"] == "user" else f"🎮 {EXPERT_NAME}"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 4. المنطق (مفحوص ومباشر)
if prompt := st.chat_input("سولف ويا عباس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 الزبون:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # تعليمات عباس: رد السلام واطلب الاسم والرقم
    sys_instruction = f"أنت '{EXPERT_NAME}' بلهجة بغدادية مؤدبة. رد السلام وجاوب الزبون. إذا انطاك الاسم والرقم قل [تم تسجيل طلبك]."

    # تعليمات الاستخراج (فلترة صافية جداً)
    extract_task = "Extract JSON: {'name': 'just name', 'phone': '07...', 'order': 'just product name'}"

    try:
        # 1. رد عباس الطبيعي للشاشة
        response = requests.post(url, headers=headers, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": sys_instruction}] + st.session_state.messages,
            "temperature": 0.7
        }, timeout=12)
        
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
            
            # 2. فحص وجود رقم هاتف عراقي في الرسالة
            phone_found = re.search(r'07\d{8,9}', prompt)
            
            if phone_found:
                # 3. استخراج الاسم والمنتج بصورة صافية (بدون لغوة)
                extract_res = requests.post(url, headers=headers, json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "system", "content": extract_task}, {"role": "user", "content": prompt}]
                }, timeout=5)
                
                try:
                    data = json.loads(re.search(r'\{.*\}', extract_res.json()['choices'][0]['message']['content'], re.DOTALL).group())
                    # الإرسال الفعلي للإكسل
                    send_to_excel(
                        name=data.get('name', 'زبون جديد'),
                        phone=phone_found.group(),
                        order=data.get('order', prompt)
                    )
                except:
                    # في حال فشل الـ JSON، نرسل البيانات كما هي لضمان عدم ضياع الطلب
                    send_to_excel("زبون", phone_found.group(), prompt[:50])

            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 {EXPERT_NAME}:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول.")
