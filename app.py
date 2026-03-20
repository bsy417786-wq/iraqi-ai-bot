import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="مساعد المبيعات الذكي", page_icon="🤖")
st.title("🤖 مساعد المبيعات (علوش)")
st.markdown("مرحباً! أنا علوش، مساعدك الذكي للإجابة على استفسارات الزبائن.")

# جلب المفتاح من إعدادات الموقع (للأمان)
# ملاحظة: سنضع المفتاح في إعدادات Streamlit لاحقاً
api_key = "AIzaSyDD0LpYzy-Jnzbf_vyGSvVAup6JS4Rr_I4"
model = genai.GenerativeModel('gemini-1.5-flash')

# ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الكتابة
if prompt := st.chat_input("تفضل اسألني أي شيء.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تعليمات الشخصية العراقية
    context = "أنت موظف مبيعات عراقي شاطر اسمه علوش، رد بلهجة بغدادية محبوبة وقصيرة."
    
    response = model.generate_content(f"{context}\nالزبون: {prompt}")
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
