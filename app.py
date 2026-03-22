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

# --- التصميم المريح ---
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
    try: requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=5)
    except: pass

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

# 5. المنطق البرمجي
if prompt := st.chat_input("سولف ويا عباس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 الزبون:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # تعليمات عباس: كن مؤدب، شرح وافي، ولا تطلب الرقم إذا موجود بالرسالة
    sys_instruction = (
        f"أنت المساعد '{EXPERT_NAME}' لشركة '{BRAND_NAME}'. بلهجة بغدادية مؤدبة. "
        "1. إذا ذكر الزبون اسمه ورقم هاتفه في الرسالة، سجل الطلب فوراً وقل [تم تسجيل طلبك يا بطل]. "
        "2. إذا طلب شيئاً ولم يذكر الرقم أو الاسم، اطلبهم منه بلباقة. "
        "3. جاوب على كل أسئلة الزبون بمرونة."
    )
    
    # تعليمات الاستخراج: استخراج "الزبدة" فقط للطلب
    extract_instruction = (
        "Analyze the user message. Extract: "
        "1. Name (as a string) "
        "2. Phone (as a string) "
        "3. Order (Extract ONLY the product name, e.g., 'iPhone 15' instead of the whole sentence). "
        "Return ONLY a clean JSON object."
    )

    try:
        # 1. استخراج "الزبدة"
        extract_res = requests.post(url, headers=headers, json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": extract_instruction}, {"role": "user", "content": prompt}]
        }, timeout=7)
        
        # 2. رد عباس الطبيعي
        response = requests.post(url, headers=headers, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": sys_instruction}] + st.session_state.messages,
            "temperature": 0.7
        }, timeout=12)
        
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
            
            # 3. منطق الإرسال الذكي للإكسل
            has_phone = re.search(r'07\d{8,9}', prompt)
            
            if has_phone:
                try:
                    # تنظيف وتجهيز الـ JSON
                    raw_data = extract_res.json()['choices'][0]['message']['content']
                    json_match = re.search(r'\{.*\}', raw_data, re.DOTALL)
                    if json_match:
                        clean_json = json.loads(json_match.group())
                        
                        # نرسل "الزبدة" فقط للإكسل
                        send_to_excel(
                            clean_json.get('name', 'زبون جديد'),
                            clean_json.get('phone', '07xxxxxxx'),
                            clean_json.get('order', 'طلب عام') # هنا صار يكتب بس المنتج
                        )
                except:
                    send_to_excel("زبون جديد", "07xxxxxxx", "طلب غير محدد")
            
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 {EXPERT_NAME}:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول حالياً.")
