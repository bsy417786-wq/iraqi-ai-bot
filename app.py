import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="عباس حيدر للتقنية", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء الزوائد */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }

    .stApp { background: #0b141a; color: #e9edef; }

    /* أنيميشن الظهور */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

    .chat-row { display: flex; margin: 20px 0; width: 100%; animation: fadeIn 0.5s ease-out; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 

    .bubble {
        padding: 15px 20px; border-radius: 20px; max-width: 80%;
        font-size: 17px; line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }

    /* صندوق الكتابة ثابت ومرتب */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 140px !important; 
        left: 10% !important;
        right: 10% !important;
        width: 80% !important;
        z-index: 1001 !important;
        background: #202c33 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 15px !important;
    }

    /* الفوتر الثابت */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0b141a; padding: 10px 0;
        z-index: 1000; border-top: 2px solid #38bdf8;
        text-align: center;
    }

    .footer-imgs { display: flex; justify-content: center; gap: 12px; margin-bottom: 8px; }
    .footer-imgs img { width: 110px; height: 70px; object-fit: cover; border-radius: 8px; border: 1px solid #38bdf8; }

    /* رفع المحادثة للأعلى بمسافة كبيرة جداً */
    .stChatContainer { padding-bottom: 450px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. العنوان
st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر للتقنية</h1>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة السابقة
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. الإدخال والرد الذكي
if prompt := st.chat_input("تفضل بطرح استفسارك يا بطل..."):
    # عرض رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{prompt}</div></div>', unsafe_allow_html=True)

    # طلب الرد من عباس
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، خبير تقني وصاحب متجر في بغداد - شارع الصناعة. "
        "تتحدث بلغة عربية فصحى بليغة مع لمسات دافئة من اللهجة العراقية (عيوني، تدلل، يا بطل، لوز، نار وشرار). "
        "أنت ذكي ومرح وتشجع الزبائن على اقتناء أقوى تجميعات الكيمنك بأسلوب مغري ومحترم. "
        "العنوان: بغداد - شارع الصناعة. الهاتف: 07700000000."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        ans = response.json()['choices'][0]['message']['content']
        # عرض رد عباس
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{ans}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
    except:
        st.error("نعتذر عيوني، السيرفر عليه ضغط حالياً، حاول مجدداً بعد ثواني.")

# 6. الفوتر الثابت
st.markdown("""
    <div class="fixed-footer">
        <div style="color:#facc15; font-size:15px; font-weight:bold; margin-bottom:8px;">
            📍 الموقع: بغداد - شارع الصناعة | 📞 للاستفسار: 07700000000
        </div>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
    </div>
""", unsafe_allow_html=True)
