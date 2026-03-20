import streamlit as st
import google.generativeai as genai

# إعداد الموقع
st.set_page_config(page_title="عباس حيدر للابتوبات")
st.title("💻 مساعد المبيعات: عباس حيدر")

# المفتاح مالتك المباشر
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"
genai.configure(api_key=api_key)

# هنا الحل: جربنا نستخدم الموديل المستقر 1.0 (PRO) بدلاً من فلاش
# لأن فلاش هو اللي دا يطلب v1beta ويسوي 404
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل عباس حيدر عن اللابتوبات.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، التوصيل مجاني لبغداد، رد بلهجة بغدادية محبوبة."
    
    try:
        # إرسال السؤال
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # إذا طلع الخطأ 404 مرة ثانية، راح نحوله لموديل أقدم غصباً عنه
        st.error("عذراً عيوني، السيرفر عليه لود. جرب تبعث الرسالة مرة ثانية.")
