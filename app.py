import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="اسأل عباس حيدر", page_icon="💻", layout="centered")

design = """
    <style>
    /* إخفاء كل زوائد ستريمليت واليوزر والـ Manage App */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"], iframe[title="manage-app"] { 
        visibility: hidden; display: none !important; 
    }
    
    /* خلفية تقنية فخمة */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #000000 100%);
        color: #ffffff;
    }

    /* العنوان الرئيسي */
    .main-header {
        color: #facc15;
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(250, 204, 21, 0.5);
        margin-top: -20px;
    }

    /* رفع مكان الكتابة للأعلى */
    div[data-testid="stChatInput"] {
        position: fixed;
        top: 150px; /* تحت العنوان */
        z-index: 1000;
        padding: 10px;
        background: rgba(15, 23, 42, 0.8);
        border-radius: 15px;
    }

    /* تنسيق المحادثة لتبدأ تحت صندوق الإدخال */
    .chat-container { margin-top: 180px; padding-bottom: 150px; }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatMessage"] p { color: #ffffff !important; font-size: 17px; }

    /* الجزء السفلي الجديد (صور وعبارات إغراء) */
    .bottom-promo {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: linear-gradient(0deg, #0f172a 0%, transparent 100%);
        padding: 20px;
        text-align: center;
        z-index: 100;
    }
    .promo-icons { font-size: 24px; margin-bottom: 5px; }
    .promo-text { color: #facc15; font-weight: bold; font-size: 18px; animation: glow 1.5s infinite alternate; }
    
    @keyframes glow {
        from { text-shadow: 0 0 5px #facc15; }
        to { text-shadow: 0 0 20px #facc15, 0 0 30px #eab308; }
    }

    .footer-info { color: #94a3b8; font-size: 12px; margin-top: 5px; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية والمقدمة
st.markdown('<div class="main-header">اسأل عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#38bdf8;">خبراء التكنولوجيا بين يديك</p>', unsafe_allow_html=True)

# 3. المفتاح والذاكرة
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. منطق الدردشة (الكتابة بالأعلى)
if prompt := st.chat_input("اطلب عرضك الخاص هسة من عباس..."):
    st.session_state.messages.insert(0, {"role": "user", "content": prompt})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، صاحب أشهر محل لابتوبات في شارع الصناعة ببغداد. "
        "لهجتك عراقية بغدادية أصلية، ابن ولاية، لسانك ينكط عسل ومعدل. "
        "مهمتك: فقط اللابتوبات. إذا سألك عن غير شي اعتذر بذكاء. "
        "أهم شي: أغري الزبون بالعروض! گوله 'لعيونك أسويلك خصم'، 'هذا الجهاز لقطة وما يتفوت'، "
        "'عندي وجبة جديدة واصلة هسة وبالباكيت'، 'تدلل عيوني السعر يم عباس ما يظل عائق'. "
        "خليل شوية نكات بغدادية خفيفة حتى يحبك الزبون."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages[::-1],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        if 'choices' in result:
            answer = result['choices'][0]['message']['content']
            st.session_state.messages.insert(0, {"role": "assistant", "content": answer})
        else:
            st.error("السيرفر تعبان شوية، اصبرلي ثواني عيوني.")
    except Exception:
        st.error("صار خلل بالاتصال، جرب مرة ثانية.")

# 5. عرض المحادثة (الجديد فوق)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    is_assistant = message["role"] == "assistant"
    avatar = ABBAS_AVATAR if is_assistant else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        label = "عباس حيدر" if is_assistant else "أنت"
        color = "#38bdf8" if is_assistant else "#facc15"
        st.markdown(f"<strong style='color:{color};'>{label}:</strong><br>{message['content']}", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. الجزء السفلي (صور الإغراء والعبارات)
st.markdown("""
    <div class="bottom-promo">
        <div class="promo-icons">💻 🚀 💎 ⚡ 🛠️</div>
        <div class="promo-text">عروض عباس حيدر ما تخلص.. اسأل هسة وحصل هدية وي كل لابتوب!</div>
        <div class="footer-info">📍 بغداد - الصناعة | 📞 07700000000 | © 2026 ABBAS HAIDER</div>
    </div>
""", unsafe_allow_html=True)
