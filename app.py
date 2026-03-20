import streamlit as st
import requests

# 1. إعدادات الصفحة والستايل الحديث (Modern Dark Tech)
st.set_page_config(page_title="عباس حيدر | Tech Advisor", page_icon="💻", layout="centered")

design = """
    <style>
    /* إخفاء كل أدوات ستريمليت واليوزر والمنيو */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* خلفية عصرية - رمادي غامق جداً مع تدرج ذهبي خفيف */
    .stApp {
        background: radial-gradient(circle at top, #1e1e1e 0%, #0a0a0a 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* تصميم الهيدر (العنوان) */
    .main-title { 
        background: linear-gradient(90deg, #d4af37, #f7e08b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 45px; font-weight: 900; text-align: center; margin-bottom: 0px; 
    }
    .sub-info { color: #888; font-size: 14px; text-align: center; letter-spacing: 1px; }
    .catch-phrase { color: #d4af37; font-size: 16px; text-align: center; margin-top: 5px; opacity: 0.9; }

    /* تأثير الزجاج لفقاعات الدردشة (Glassmorphism) */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
        margin-bottom: 15px !important;
    }
    
    /* تمييز رسالة المستخدم */
    [data-testid="stChatMessageUser"] {
        border-left: 4px solid #d4af37 !important;
    }

    /* تنسيق صورة البروفايل داخل الدردشة */
    [data-testid="stChatMessageAssistant"] img {
        border: 2px solid #d4af37;
        border-radius: 50% !important;
    }

    /* زر الإدخال */
    .stChatInputContainer { padding-bottom: 30px; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية البصرية (اللوجو والمعلومات)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("Gemini_Generated_Image_xhf51axhf51axhf5.jpg", width=140)
    except:
        st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png", width=140)

st.markdown('<div class="main-title">عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">💻 TECH ADVISOR | BAGHDAD</div>', unsafe_allow_html=True)
st.markdown('<div class="catch-phrase">"نصحبكم في اختيار الأفضل لمستقبلكم التقني"</div>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0.1px solid rgba(212,175,55,0.2); margin: 25px 0;'>", unsafe_allow_html=True)

# 3. المفتاح والرسائل
MY_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة (البروفايل صار بجانب رسالة عباس تلقائياً)
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="Gemini_Generated_Image_xhf51axhf51axhf5.jpg"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])

# 4. منطق الدردشة (الفصحى الرزنة)
if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، مستشار تقني محترف في أجهزة اللابتوب. "
        "تحدث بالفصحى فقط وبأسلوب رسمي راقٍ يليق بشركة تقنية حديثة. "
        "كن مباشراً في تقديم المواصفات والأسعار، واجعل العميل يشعر بالثقة."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}, *st.session_state.messages],
        "temperature": 0.3
    }

    try:
        with st.spinner("جاري المراجعة..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            with st.chat_message("assistant", avatar="Gemini_Generated_Image_xhf51axhf51axhf5.jpg"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عذراً، يرجى إعادة المحاولة لاحقاً.")
