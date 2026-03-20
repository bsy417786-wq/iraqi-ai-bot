import streamlit as st
import requests
import json

# إعداد واجهة الموقع
st.set_page_config(page_title="عباس حيدر للابتوبات")
st.title("💻 مساعد المبيعات: عباس حيدر")

# المفتاح مالتك المباشر
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الحل القاتل: استعملنا رابط v1 المستقر مباشرة (بدون كلمة models)
    # وجبرناه يروح للموديل gemini-pro اللي هو أضمن شي
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، التوصيل مجاني، رد بلهجة بغدادية. الزبون يقول: {prompt}"
            }]
        }]
    }

    try:
        # إرسال الطلب
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # استخراج الرد غصباً على السيرفر
        if 'candidates' in response_json:
            answer = response_json['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"اكو مشكلة بالرد: {response_json.get('error', {}).get('message', 'خطأ غير معروف')}")
            
    except Exception as e:
        st.error(f"عذراً عيوني، اكو مشكلة: {str(e)}")
    
