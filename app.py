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

    /* حاوية المحادثة - رفعناها 350 بكسل حتى ما تنحجب */
    .stChatContainer { 
        padding-bottom: 350px !important; 
    }

    .chat-row { display: flex; margin: 15px 0; width: 100%; animation: fadeIn 0.4s ease-out; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 

    .bubble {
        padding: 12px 18px; border-radius: 18px; max-width: 78%;
        font-size: 16px; line-height: 1.5; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }

    /* صندوق الكتابة - ثابت فوق الفوتر */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 130px !important; 
        left: 5% !important;
        right: 5% !important;
        width: 90% !important;
        z-index: 1001 !important;
        background: #202c33 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
    }

    /* الفوتر الثابت (الصور والمعلومات) */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0b141a; padding: 10px 0;
        z-index: 1000; border-top: 1px solid #38bdf8;
        text-align: center;
    }

    .footer-imgs { display: flex; justify-content: center; gap: 10px; margin-bottom: 5px; }
    .footer-imgs img { width: 85px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #38bdf8; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر للتقنية</h2>", unsafe_allow_html=True)

# 3. الذاكرة والـ Key
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة (يسار ويمين)
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 أنت" if msg["role"] == "user" else "🎮 عباس حيدر"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال والرد
if prompt := st.chat_input("تفضل بسؤالك يا وحش..."):
    # إضافة رسالة المستخدم وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    # طلب الرد من السيرفر
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، خبير تقني وصاحب متجر في بغداد - شارع الصناعة. "
        "تتحدث بلغة عربية فصحى رزينة مع لمسات عراقية (عيوني، تدلل، يا بطل، لوز). "
        "ممنوع استخدام لهجات أخرى. التوصيل متاح 24/7."
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
            ans = "اعتذر منك عيوني، السيرفر عليه ضغط حالياً. تدلل، اترك رسالتك وسأرد عليك فوراً!"
            
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{ans}</div></div>', unsafe_allow_html=True)
    except:
        st.error("السيرفر مشغول شوية عيوني، انتظر ثانية وجرب مرة ثانية!")

# 6. الفوتر الثابت
st.markdown("""
    <div class="fixed-footer">
        <div style="color:#facc15; font-size:13px; font-weight:bold; margin-bottom:5px;">
            📍 بغداد - شارع الصناعة | 📞 07700000000 | 🚚 توصيل 24/7
        </div>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
    </div>
""", unsafe_allow_html=True)
