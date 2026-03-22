import streamlit as st
import requests
import json
import re

# 1. الإعدادات الأساسية
BRAND_NAME = "عباس حيدر للذكاء الاصطناعي"
EXPERT_NAME = "عباس"
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzboWW6szwgFDiHOc9-nETt--8F33WZHimWRvJmT-ZHE-Y7TTjUFx4dC_OeIAwp7gcVVQ/exec"
MY_KEY = "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"

st.set_page_config(page_title=BRAND_NAME, page_icon="🤖", layout="centered")

# --- تصميم الواجهة (صندوق الكتابة صاعد) ---
st.markdown("""
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
""", unsafe_allow_html=True)

def send_to_excel(name, phone, order):
    payload = {"name": name, "phone": phone, "order": order}
    try: requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=10)
    except: pass

# 2. عرض الهوية والرسائل
st.markdown(f"<h3 style='text-align:center; color:#38bdf8;'>🛡️ {BRAND_NAME}</h3>", unsafe_allow_html=True)
if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{"👤 الزبون" if msg["role"]=="user" else "🎮 "+EXPERT_NAME}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 3. المنطق (استخراج جراحي)
if prompt := st.chat_input("سولف ويا عباس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 الزبون:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}

    # تعليمات الاستخراج (ممنوع الغلط)
    extract_system = (
        "You are a data extractor. Extract ONLY 3 things in Arabic: "
        "1. name: Only the person's name (e.g. 'أحمد'). "
        "2. phone: The Iraqi phone number starting with 07. "
        "3. order: ONLY the product name (e.g. 'ايفون 13'). Delete ALL other words. "
        "Return ONLY clean JSON."
    )

    try:
        # أ: استخراج البيانات الصافية
        ex_res = requests.post(url, headers=headers, json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": extract_system}, {"role": "user", "content": prompt}]
        }, timeout=5)
        
        # ب: رد عباس الطبيعي
        chat_res = requests.post(url, headers=headers, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": f"أنت {EXPERT_NAME}، مساعد مبيعات بغدادي مؤدب. اطلب الاسم والرقم بذكاء."}] + st.session_state.messages,
            "temperature": 0.7
        }, timeout=10)

        if chat_res.status_code == 200:
            ans = chat_res.json()['choices'][0]['message']['content']
            
            # ج: فحص الرقم وإرسال الصافي للإكسل
            if re.search(r'07\d{8,9}', prompt):
                try:
                    data = json.loads(re.search(r'\{.*\}', ex_res.json()['choices'][0]['message']['content'], re.DOTALL).group())
                    send_to_excel(
                        name=data.get('name', 'زبون جديد'),
                        phone=data.get('phone', re.search(r'07\d{8,9}', prompt).group()),
                        order=data.get('order', 'منتج غير محدد')
                    )
                except:
                    send_to_excel("زبون", "07xxxxxxxx", "طلب")

            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 {EXPERT_NAME}:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول.")
