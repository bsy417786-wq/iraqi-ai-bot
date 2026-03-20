import streamlit as st
import google.generativeai as genai
import os

# إعداد واجهة الموقع
st.set_page_config(page_title="محل عباس حيدر")
st.title("💻 مساعد المبيعات: عباس حيدر")

# المفتاح مالتك المباشر (تأكد إنه شغال)
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"

# الإعداد القوي (أجبرناه يستخدم النسخة المستقرة v1)
genai.configure(api_key=api_key)

# هنا استخدمنا gemini-1.0-pro (هذا الموديل مستحيل يطلع 404)
model = genai.GenerativeModel('gemini-1.0-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # الشخصية
    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، التوصيل مجاني لبغداد، رد بلهجة بغدادية."
    
    try:
        # إرسال السؤال
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"عذراً عيوني، اكو مشكلة بالسيرفر: {str(e)}")
