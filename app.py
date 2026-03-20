import streamlit as st
import google.generativeai as genai

# إعداد الموقع
st.set_page_config(page_title="عباس حيدر للابتوبات")
st.title("💻 مساعد المبيعات: عباس حيدر")

# المفتاح مالتك المباشر
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"

# إعداد الاتصال (هنا الحل: جبرناه يترك الـ v1beta ويروح للمستقر)
genai.configure(api_key=api_key, transport='rest') # كلمة rest هي الحل

# تعريف الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

# نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة السؤال
if prompt := st.chat_input("اسأل عباس حيدر عن اللابتوبات.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تعليمات عباس حيدر
    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، التوصيل مجاني لبغداد، رد بلهجة بغدادية."
    
    try:
        # إرسال السؤال
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"عذراً عيوني، اكو مشكلة: {str(e)}")
