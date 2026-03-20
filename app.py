import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="عباس حيدر للكيمنك", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء الزوائد */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }

    .stApp { background: #0b141a; color: #e9edef; }

    /* أنيميشن الظهور */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    .chat-row { display: flex; margin: 15px 0; width: 100%; animation: fadeIn 0.4s ease-out; }
    .user-row { justify-content: flex-start; } /* أنت يسار */
    .abbas-row { justify-content: flex-end; }  /* عباس يمين */

    .bubble {
        padding: 12px 18px; border-radius: 18px; max-width: 75%;
        font-size: 16px; line-height: 1.6; position: relative;
    }

    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }

    /* صندوق الكتابة - ضبطناه حتى ما يغطي الردود */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 150px !important; /* رفعة أمان */
        z-index: 1001 !important;
        background: #202c33 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
    }

    /* الفوتر الثابت (العنوان والرقم والصور) */
    .fixed-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0b141a; padding: 10px 0;
        z-index: 1000; border-top: 2px solid #38bdf8;
        text-align: center;
    }

    .footer-imgs { display: flex; justify-content: center; gap: 10px; margin-bottom: 5px; }
    .footer-imgs img { width: 90px; height: 55px; object-fit: cover; border-radius: 5px; border: 1px solid #38bdf8; }

    .stChatContainer { padding-bottom: 300px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية البغدادية
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🎮 عباس حيدر - خبير الكيمنك</h2>", unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>أنت:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال
if prompt := st.chat_input("اسأل عباس.. عروضنا نار وشرار!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# توليد رد عباس (إذا كانت آخر رسالة من المستخدم)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # حصر اللهجة بالعراقي البغدادي فقط
    context = (
        "أنت عباس حيدر من بغداد، صاحب محل كمبيوترات بشارع الصناعة. "
        "ممنوع تتحدث أي لهجة غير العراقية البغدادية. لا سوري، لا لبناني، لا فصحى خشبية. "
        "استخدم كلمات مثل: (عيوني، لوز، تدلل، نار وشرار، يا وحش، لقطة، ما مطروقة، بشدة). "
        "شجع الزبون يشتري أقوى التجميعات ودمك خفيف ومرح جداً. "
        "عنوانك: بغداد - شارع الصناعة. رقمك: 07700000000."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.8
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        ans = response.json()['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()
    except:
        st.error("عيني السيرفر گيم.. انتظر ثواني!")

# 6. الفوتر الثابت (العنوان والرقم)
st.markdown("""
    <div class="fixed-footer">
        <div style="color:#facc15; font-size:14px; font-weight:bold; margin-bottom:5px;">
            📍 بغداد - شارع الصناعة | 📞 07700000000
        </div>
        <div class="footer-imgs">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=200">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=200">
        </div>
        <div style="color:#94a3b8; font-size:10px;">© 2026 ABBAS HAIDER - GAMING EXPERT</div>
    </div>
""", unsafe_allow_html=True)
