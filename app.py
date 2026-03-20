import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="عباس حيدر للتقنية", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء الزوائد */
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }

    .stApp { background: #0b141a; color: #e9edef; font-family: 'Segoe UI', sans-serif; }

    /* أنيميشن الظهور */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

    .chat-row { display: flex; margin: 25px 0; width: 100%; animation: fadeIn 0.5s ease-out forwards; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 

    .bubble {
        padding: 15px 22px; border-radius: 22px; max-width: 80%;
        font-size: 17px; line-height: 1.6; position: relative;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
    }

    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }

    /* صندوق الكتابة - ثابت بالمنتصف وفوق الفوتر */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 150px !important; 
        left: 10% !important;
        right: 10% !important;
        width: 80% !important;
        z-index: 1001 !important;
        background: #202c33 !important;
        border: 2.5px solid #38bdf8 !important;
        border-radius: 15px !important;
    }

    /* الفوتر الثابت بالأسفل */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0b141a; padding: 12px 0;
        z-index: 1000; border-top: 2px solid #38bdf8;
        text-align: center;
    }

    .footer-imgs { display: flex; justify-content: center; gap: 15px; margin-bottom: 10px; }
    .footer-imgs img { width: 110px; height: 70px; object-fit: cover; border-radius: 10px; border: 1.5px solid #38bdf8; }

    /* الارتفاع العالي جداً لضمان عدم حجب الرسايل */
    .stChatContainer { padding-bottom: 550px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية
st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر للتقنية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; margin-top:-15px;'>خبير تجميعات الحاسوب - بغداد، شارع الصناعة</p>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة (تصليح الخطأ هنا)
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 أنت" if msg["role"] == "user" else "🎮 عباس حيدر"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال والرد
if prompt := st.chat_input("تفضل بطرح استفسارك التقني يا بطل..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، صاحب متجر تقني في بغداد. لغتك فصحى محترمة ومطعمة بكلمات عراقية دافئة. "
        "مهمتك هي تقديم نصائح حول تجميعات الكمبيوتر وإغراء الزبائن بأقوى القطع. "
        "التوصيل متاح 24/7."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
        else:
            ans = "اعتذر منك عيوني، السيرفر عليه ضغط حالياً. تدلل، اترك رسالتك وسأرد عليك فوراً!"
            
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{ans}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
    except:
        error_msg = "عذراً يا بطل، يبدو أن الإنترنت ضعيف. أعد إرسال رسالتك وتدلل عليّ!"
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{error_msg}</div></div>', unsafe_allow_html=True)

# 6. الفوتر الثابت
st.markdown("""
    <div class="fixed-footer">
        <div style="color:#facc15; font-size:15px; font-weight:bold; margin-bottom:8px;">
            📍 بغداد - شارع الصناعة | 📞 07700000000 | 🚚 التوصيل متاح 24/7
        </div>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
    </div>
""", unsafe_allow_html=True)
