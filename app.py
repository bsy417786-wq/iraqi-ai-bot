import streamlit as st
import requests

# 1. إخفاء خيارات Streamlit المزعجة (التشفير البصري)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.set_page_config(page_title="عباس حيدر للابتوبات", page_icon="💻", layout="centered")
st.markdown(hide_st_style, unsafe_allow_config=True)

# 2. عرض اللوجو مالتك (تأكد من وضع رابط الصورة الصح هنا)
st.image("https://i.ibb.co/v66Zz7r/Abbas-Haider-Logo.png", width=200) 
st.title("💻 مساعد المبيعات: عباس حيدر")
st.markdown("---")

# 3. الأمان (تأكد تحط مفتاح Groq هنا)
# نصيحة: للتقديم الرسمي حطه بملف .streamlit/secrets.toml
GROQ_API_KEY = "gsk_حط_مفتاح_GROQ_هنا"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل عيوني اسألني.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json"
    }
    
    # حصر المعلومات ومنع الغلط (السيستم برومبت)
    context = (
        "أنت عباس حيدر، صاحب محل لابتوبات بالكرادة، بغداد. "
        "قوانينك: 1. احجي بغدادي قح (هله بيك، عيوني، خادم، تدلل، ما يصير خاطرك إلا طيب). "
        "2. لا تحجي فصحى نهائياً. 3. أسعارك تبدأ من 150 ألف صعوداً. "
        "4. التوصيل لبغداد مجاني وللمحافظات 5 آلاف. 5. إذا سألوك عن شي ما تعرفه، كول 'والله عيوني هذي المواصفة لازم أتأكد من المخزن، لحظة' ولا تألف من جيبك. "
        "6. خلكك طويل ويه الزبون."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": context},
            *st.session_state.messages # هذي الذاكرة حتى ما ينسى الحجي السابق
        ],
        "temperature": 0.5 # تقليل العشوائية لمنع الأخطاء
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("عيوني السيرفر شوية تعبان، ثواني وارجع اسألني.")
