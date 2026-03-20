import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="دردشة عباس حيدر", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء زوائد ستريمليت */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"], iframe[title="manage-app"] { 
        visibility: hidden; display: none !important; 
    }

    /* خلفية الدارك مود */
    .stApp { background: #0b141a; color: #e9edef; }

    /* أنيميشن الظهور التدريجي */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* تنسيق الحاويات لليمين واليسار */
    .chat-row {
        display: flex;
        margin: 10px 0;
        width: 100%;
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    .user-row { justify-content: flex-start; } /* المستخدم يسار */
    .abbas-row { justify-content: flex-end; }  /* عباس يمين */

    .bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 75%;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }

    /* صندوق الكتابة في الأسفل فوق الفوتر */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 120px !important;
        z-index: 1001 !important;
        background: #202c33 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 12px !important;
    }

    /* الفوتر الثابت (الصور) */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0b141a; padding: 10px 0;
        z-index: 1000; border-top: 1px solid #202c33;
        text-align: center;
    }

    .footer-imgs { display: flex; justify-content: center; gap: 8px; }
    .footer-imgs img { width: 100px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #38bdf8; }

    .stChatContainer { padding-bottom: 250px !important; }

    /* أنيميشن النقاط */
    .typing { display: flex; gap: 4px; padding: 5px; }
    .dot { width: 6px; height: 6px; background: #38bdf8; border-radius: 50%; animation: blink 1.4s infinite; }
    @keyframes blink { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر - Tech Chat</h2>", unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة (اليسار لليوزر واليمين لعباس)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">👤 أنت:<br>{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble">🎮 عباس حيدر:<br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال
if prompt := st.chat_input("سولف وي عباس.. العروض نار!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">👤 أنت:<br>{prompt}</div></div>', unsafe_allow_html=True)

    # رد عباس
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، خبير كمبيوتر عراقي. تتحدث بلهجة بغدادية محترمة ودمك خفيف جداً. "
        "شجع الزبون على أقوى القطع (RTX 4090، معالجات الجيل الأخير) وقول له عروضنا (لوز) و (نار وشرار). "
        "أنت ذكي جداً ومثل (جيميني) في الذكاء ولكن بروح عراقية."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.8
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        ans = response.json()['choices'][0]['message']['content']
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble">🎮 عباس حيدر:<br>{ans}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun() # لإعادة الترتيب بعد الرد
    except:
        st.error("عيني صار لود على السيرفر، جرب مرة ثانية!")

# 6. الفوتر الثابت (الصور بالأسفل)
st.markdown("""
    <div class="fixed-footer">
        <p style="color:#facc15; font-size:12px; margin-bottom:5px;">🔥 عروض الكيمنك الأقوى عند عباس حيدر 🔥</p>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
    </div>
""", unsafe_allow_html=True)
