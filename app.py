import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="عباس حيدر - Tech Expert", page_icon="🎮", layout="centered")

design = """
    <style>
    /* إخفاء زوائد ستريمليت */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"], iframe[title="manage-app"] { 
        visibility: hidden; display: none !important; 
    }

    /* خلفية مريحة وفخمة */
    .stApp { background: #0f172a; color: #f1f5f9; }

    .main-header {
        color: #38bdf8; font-size: 38px; font-weight: 800;
        text-align: center; margin-top: -30px;
    }
    
    /* أنيميشن الظهور التدريجي الناعم */
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 15px !important;
        margin-bottom: 12px !important;
        animation: fadeInSlide 0.6s ease-out forwards;
    }

    /* صندوق الكتابة فوق الصور */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 180px !important;
        z-index: 1001 !important;
        background: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 15px !important;
    }

    /* الفوتر الثابت بالأسفل (صور كيمنك) */
    .fixed-footer-box {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0f172a; padding: 15px 0;
        z-index: 1000; border-top: 1px solid #38bdf8;
        text-align: center;
    }

    .footer-images {
        display: flex; justify-content: center; gap: 12px; margin-bottom: 5px;
    }

    .footer-images img {
        width: 130px; height: 80px; object-fit: cover;
        border-radius: 10px; border: 2px solid #38bdf8;
    }

    .stChatContainer { padding-bottom: 320px !important; }

    /* أنيميشن النقاط */
    .typing { display: flex; align-items: center; gap: 5px; padding: 5px; }
    .dot { width: 6px; height: 6px; background: #38bdf8; border-radius: 50%; animation: blink 1.4s infinite both; }
    @keyframes blink { 0% { opacity: 0.2; } 20% { opacity: 1; } 100% { opacity: 0.2; } }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. العنوان
st.markdown('<div class="main-header">عباس حيدر للتقنية 🎮</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#94a3b8;">لأنك تستحق أفضل تجميعة بالعالم!</p>', unsafe_allow_html=True)

# 3. الذاكرة والمفاتيح
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    is_assistant = message["role"] == "assistant"
    avatar = ABBAS_AVATAR if is_assistant else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        label = "عباس حيدر" if is_assistant else "أنت"
        color = "#38bdf8" if is_assistant else "#facc15"
        st.markdown(f"<strong style='color:{color};'>{label}:</strong><br>{message['content']}", unsafe_allow_html=True)

# 5. منطق الإدخال والرد (شخصية عباس الجديدة)
if prompt := st.chat_input("تكلم مع عباس.. العروض بانتظارك!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(f"<strong style='color:#facc15;'>أنت:</strong><br>{prompt}", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar=ABBAS_AVATAR):
        st.markdown(f"<strong style='color:#38bdf8;'>عباس حيدر:</strong>", unsafe_allow_html=True)
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
        
        # سياق الشخصية (فصحى + لهجة + إغراء)
        context = (
            "أنت عباس حيدر، خبير تقني وصاحب محل كمبيوترات كيمنك في بغداد. "
            "شخصيتك: تتحدث بلغة فصحى أنيقة ومحترمة لكن مطعمة بكلمات عراقية محببة (عيني، تدلل، يا بطل، لوز، نار وشرار). "
            "أسلوبك: خفيف الظل، ذكي، وتعرف كيف تغري الزبون بأقوى العروض (مثلاً: هذا العرض لقطة، ستحصل على FPS يجعلك تطير في اللعبة). "
            "تخصصك: فقط أجهزة الكمبيوتر والكيمنك. إذا سألك عن شيء آخر، اعتذر بلباقة وقل له (دعنا في عالم الأداء الخارق)."
        )
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": context}] + st.session_state.messages,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            typing_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except:
            typing_placeholder.error("عذراً عيني، السيرفر أخذ استراحة محارب.. جرب مرة ثانية.")

# 6. الصور الثابتة (الفوتر)
footer_html = """
    <div class="fixed-footer-box">
        <div style="color:#facc15; font-size:13px; font-weight:bold; margin-bottom:10px;">🔥 أقوى عروض الكيمنك - جودة عالمية بلمسة عراقية 🔥</div>
        <div class="footer-images">
            <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=400">
            <img src="https://images.unsplash.com/photo-1603481546238-487240415921?q=80&w=400">
            <img src="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=400">
        </div>
        <div style="color:#94a3b8; font-size:10px;">📍 بغداد - شارع الصناعة | © 2026 ABBAS HAIDER</div>
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
