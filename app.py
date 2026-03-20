import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="محل لابتوبات عباس حيدر")
st.title("💻 عباس حيدر للمبيعات")

# المفتاح مالتك
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل اسألني عيوني.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، التوصيل مجاني لبغداد، رد بلهجة بغدادية."
    
    try:
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"مشكلة بالاتصال: {str(e)}")
