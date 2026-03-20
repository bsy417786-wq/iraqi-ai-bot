import streamlit as st
import requests
import datetime

# 1. إعدادات الصفحة والجمالية (واتساب ستايل)
st.set_page_config(page_title="عباس حيدر - موظف المبيعات الذكي", page_icon="💰", layout="centered")

design = """
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] { visibility: hidden; display: none !important; }
    .stApp { background: #0b141a; color: #e9edef; }
    
    /* ستايل المحادثة (يسار ويمين) */
    .chat-row { display: flex; margin: 15px 0; width: 100%; animation: fadeIn 0.4s ease-out; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 
    .bubble { padding: 12px 18px; border-radius: 18px; max-width: 75%; font-size: 16px; line-height: 1.5; }
    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border: 1px solid #38bdf8; border-bottom-right-radius: 2px; }

    /* صندوق الكتابة في المنتصف تماماً */
    div[data-testid="stChatInput"] {
        position: fixed !important; bottom: 130px !important;
        left: 10% !important; right: 10% !important; width: 80% !important;
        z-index: 1001 !important; background: #202c33 !important;
        border: 2px solid #38bdf8 !important; border-radius: 12px !important;
    }

    /* الفوتر والصور */
    .fixed-footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0b141a; padding: 10px 0; z-index: 1000; border-top: 1px solid #38bdf8; text-align: center; }
    .footer-imgs { display: flex; justify-content: center; gap: 10px; margin-bottom: 5px; }
    .footer-imgs img { width: 90px; height: 55px; object-fit: cover; border-radius: 5px; border: 1px solid #38bdf8; }
    
    /* مسافة أمان عالية جداً للمحادثة */
    .stChatContainer { padding-bottom: 450px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية والذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. عرض الرسايل (يسار ويمين)
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 أنت" if msg["role"] == "user" else "🎮 عباس حيدر"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 4. منطق الإدخال والرد (مع حماية من توقف السيرفر)
if prompt := st.chat_input("تفضل بطرح استفسارك عيوني..."):
    # عرض رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{prompt}</div></div>', unsafe_allow_html=True)

    # طلب الرد من السيرفر
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، صاحب متجر كمبيوتر في بغداد. تتحدث فصحى محترمة مع كلمات بغدادية (عيوني، تدلل، يا بطل). "
        "مهمتك بيع تجميعات الكيمنك القوية. إذا سألك الزبون عن الشراء، اطلب منه معلومات التوصيل فوراً. "
        "نحن متواجدون 24/7."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
        else:
            ans = "اعتذر منك عيوني، يبدو أن هناك ضغطاً كبيراً على المتجر الآن. تدلل عليّ، اترك رسالتك وسأرد عليك فوراً يا بطل!"
            
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{ans}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
    except:
        error_msg = "عذراً يا بطل، يبدو أن الإنترنت ضعيف شوية. أنا معك، أعد إرسال رسالتك وتدلل!"
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{error_msg}</div></div>', unsafe_allow_html=True)

# 5. الفوتر الثابت (العنوان والتوصيل)
st.markdown("""
    <div class="fixed-footer">
        <div style="color:#facc15; font-size:14px; font-weight:bold; margin-bottom:5px;">
            📍 بغداد - شارع الصناعة | 📞 07700000000 | 🚚 التوصيل متاح 24/7
        </div>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
        <div style="color:#94a3b8; font-size:10px;">© 2026 ABBAS HAIDER - خبير الكيمنك الأول</div>
    </div>
""", unsafe_allow_html=True)
