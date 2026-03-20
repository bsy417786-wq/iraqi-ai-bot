import streamlit as st
import requests
import json
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="عباس حيدر للتقنية", page_icon="🎮", layout="centered")

# --- رابط قوقل شيت الخاص بك ---
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzboWW6szwgFDiHOc9-nETt--8F33WZHimWRvJmT-ZHE-Y7TTjUFx4dC_OeIAwp7gcVVQ/exec"

design = """
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }
    .stApp { background: #0b141a; color: #e9edef; font-family: 'Segoe UI', sans-serif; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
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
        position: fixed !important; bottom: 5px !important; 
        left: 15% !important; right: 15% !important;
        width: 70% !important; z-index: 1002 !important;
        background: #202c33 !important; border: 2px solid #38bdf8 !important; border-radius: 12px !important;
    }
    .side-info-left { position: fixed; bottom: 15px; left: 10px; width: 13%; text-align: left; color: #facc15; font-size: 11px; font-weight: bold; z-index: 1003; }
    .side-info-right { position: fixed; bottom: 15px; right: 10px; width: 13%; text-align: right; color: #38bdf8; font-size: 11px; font-weight: bold; z-index: 1003; }
    .stChatContainer { padding-bottom: 150px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# دالة إرسال البيانات المرتبة للإكسل
def send_to_excel(name, phone, order):
    payload = {"name": name, "phone": phone, "order": order}
    try:
        requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=5)
    except:
        pass

# 2. الهوية
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر للتقنية</h2>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 أنت" if msg["role"] == "user" else "🎮 عباس حيدر"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. المعلومات الجانبية
st.markdown("""
    <div class="side-info-left">📍 شارع الصناعة<br>🚚 توصيل 24/7</div>
    <div class="side-info-right">📞 07700000000<br>💎 عروض نارية</div>
""", unsafe_allow_html=True)

# 6. منطق الإدخال والرد
if prompt := st.chat_input("سولف ويا عباس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # --- ذكاء اصطناعي إضافي لاستخراج البيانات الصافية ---
    extraction_prompt = (
        "حلل النص التالي واستخرج منه (الاسم، رقم الهاتف، والطلب) فقط. "
        "اجعل الرد بصيغة JSON حصراً كالتالي: "
        '{"name": "الاسم هنا", "phone": "الرقم هنا", "order": "الطلب الصافي هنا"}. '
        "إذا لم تجد الاسم اكتب 'زبون جديد'. إذا لم تجد الطلب اكتب 'استفسار'. "
        f"النص: {prompt}"
    )

    try:
        # 1. عملية استخراج البيانات (بالخلفية)
        extract_res = requests.post(url, headers=headers, json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": "You are a data extractor."}, {"role": "user", "content": extraction_prompt}]
        }, timeout=5)
        
        data_json = json.loads(extract_res.json()['choices'][0]['message']['content'])
        
        # 2. عملية الرد الطبيعي على الزبون
        context = (
            "أنت عباس حيدر، صاحب محل تقنيات في بغداد. "
            "تتحدث لغة عربية فصحى رصينة مع لمسات بغدادية (عيوني، تدلل، يابة). "
            "عند تسجيل الطلب قل: [تم تسجيل طلبك يا بطل]."
        )
        
        response = requests.post(url, headers=headers, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": context}] + st.session_state.messages,
            "temperature": 0.7
        }, timeout=10)
        
        ans = response.json()['choices'][0]['message']['content']

        # 3. إذا وجدنا رقم هاتف، نرسل البيانات المفصلة للإكسل
        # نستخدم regex للتأكد من وجود رقم هاتف فعلي قبل الإرسال
        if re.search(r'07\d{8,9}', prompt):
            send_to_excel(data_json['name'], data_json['phone'], data_json['order'])

        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول، حاول مرة ثانية!")
