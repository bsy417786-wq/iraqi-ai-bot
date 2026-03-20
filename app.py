
import streamlit as st
import requests

# 1. إعدادات الصفحة واللون الجديد (Charcoal & Gold)
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")

design = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}
    
    /* لون الخلفية الجديد - رمادي فحمي فخم */
    .stApp {
        background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%);
        color: #e0e0e0;
    }
    
    /* تنسيق النصوص باللون الذهبي والأبيض */
    .main-title { color: #d4af37; font-size: 38px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-info { color: #a0a0a0; font-size: 15px; text-align: center; margin-bottom: 2px; }
    .catch-phrase { color: #d4af37; font-size: 17px; text-align: center; font-style: italic; margin-top: 10px; opacity: 0.8; }
    
    /* فقاعات الدردشة - ألوان محايدة */
    [data-testid="stChatMessage"] { border-radius: 15px !important; }
    [data-testid="stChatMessageUser"] { background-color: #3d3d3d !important; border: 1px solid #4d4d4d; }
    [data-testid="stChatMessageAssistant"] { background-color: #262626 !important; border: 1px solid #d4af37; }
    
    /* تنسيق الصور */
    .logo-img img { border-radius: 50%; border: 2px solid #d4af37; }
    .laptop-img img { border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# 2. الهوية البصرية
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # اللوجو مالتك
        st.image("Gemini_Generated_Image_xhf51axhf51axhf5.jpg", width=160)
    except:
        st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png", width=160)

st.markdown('<div class="main-title">عباس حيدر</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">📍 بغداد - الكرادة - شارع الصناعة</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-info">📞 07700000000</div>', unsafe_allow_html=True)
st.markdown('<div class="catch-phrase">"نصحبكم في اختيار الأفضل لمستقبلكم التقني"</div>', unsafe_allow_html=True)

# صورة اللابتوبات الاحترافية
st.image("https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
st.markdown("<hr style='border: 0.5px solid #3d3d3d;'>", unsafe_allow_html=True)

# 3. المفتاح والرسائل
MY_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطق الدردشة (باللغة الفصحى لضمان الاحترافية)
if prompt := st.chat_input("كيف يمكننا مساعدتكم في اختيار حاسوبكم الجديد؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = { "Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json" }
    
    context = (
        "أنت عباس حيدر، مستشار تقني خبير في أجهزة الحاسوب المحمول بمركز مبيعاتنا في بغداد. "
        "تحدث باللغة العربية الفصحى السليمة حصراً. كن رسمياً، مهذباً، ودقيقاً جداً في وصف المواصفات التقنية. "
        "لا تستخدم أي لهجات عامية. هدفك هو مساعدة العميل على اختيار الجهاز الأنسب لميزانيته واحتياجه."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}, *st.session_state.messages],
        "temperature": 0.3 
    }

    try:
        with st.spinner("جاري مراجعة المواصفات..."):
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عذراً، يرجى المحاولة مرة أخرى لاحقاً.")
