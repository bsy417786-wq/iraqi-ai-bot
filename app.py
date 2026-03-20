import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="اسأل عباس حيدر", page_icon="💻", layout="centered")

design = """
    <style>
    /* إخفاء كل زوائد ستريمليت بما فيها Manage app واليوزر */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }
    
    /* قفل الـ Manage app اللي يظهر بالزاوية */
    .stApp [data-testid="stActionButton"] { display: none; }
    iframe[title="manage-app"] { display: none !important; }

    /* خلفية تقنية فخمة */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #000000 100%);
        color: #ffffff;
    }

    /* العنوان الجديد */
    .main-header {
        color: #facc15;
        font-size: 50px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 15px rgba(250, 204, 21, 0.4);
        margin-top: -30px;
    }

    /* فقاعات الدردشة */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatMessage"] p {
        color: #f1f5f9 !important;
        font-size: 17px !important;
    }

    /* الفوتر بالزوايا */
    .f-left { position: fixed; bottom: 20px; left: 20px; color: #38bdf8; font-size: 13px; font-weight: bold; z-index: 100; }
    .f-right { position: fixed; bottom: 20px; right: 20px; color: #38bdf8; font-size: 13px; font-weight: bold; text-align: right; }
    
    .stChatInputContainer { padding-bottom: 80px; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية البصرية
st.image("https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
st.markdown('<div class="main-header">اسأل عباس حيدر</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="f-left">📍 بغداد - الكرادة - شارع الصناعة<br>📞 07700000000</div>
    <div class="f-right">🚀 لابتوبك يمنه.. والضمان بجيبك<br>© 2026 ABBAS HAIDER</div>
""", unsafe_allow_html=True)

# 3. المفتاح والروابط
MY_KEY = "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"
ABBAS_AVATAR = "https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png"
USER_AVATAR = "👤"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. منطق الدردشة
if prompt := st.chat_input("اكتب سؤالك هنا عيوني..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    # الـ System Prompt الجديد (لهجة عراقية + قفل اختصاص)
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات خبير في بغداد. "
        "شخصيتك: ابن ولاية، لسانك حلو، عندك لهجة عراقية خفيفة ومحبوبة (مو فصحى جافة ولا عامية مكسرة). "
        "قاعدة ذهبية: أنت اختصاصك فقط وفقط اللابتوبات والكمبيوترات. "
        "إذا سألك العميل عن أي شيء خارج هذا المجال (طب، طبخ، سياسة، رياضة، الخ)، "
        "اعتذر منه بأدب وگول له: 'اعتذر منك عيوني، أنا اختصاصي بس كمبيوترات ولابتوبات، بغير شي ما أگدر أفيدك حتى ما أنطيك معلومة غلط'. "
        "خليل شوية نكات خفيفة بخصوص التكنولوجيا والأسعار بأسلوب بغدادي رزن."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.6 # زيادة الحرارة شوية حتى تطلع اللهجة أحلى
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result
