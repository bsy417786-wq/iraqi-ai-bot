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

if prompt := st.chat_input("اسأل عباس حيدر عيوني.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الحل النهائي: استخدمنا أحدث موديل flash وأحدث نسخة رابط v1
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # المعلومات اللي ردتها عن عباس حيدر
    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، التوصيل مجاني لبغداد، رد بلهجة بغدادية محبوبة (تدلل، عيوني، خادم ربك)."
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{context}\nالزبون: {prompt}"}]
        }]
    }

    try:
        # إرسال الطلب المباشر
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        # استخراج النص من الرد الجديد
        if 'candidates' in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"جوجل تگول: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
            
    except Exception as e:
        st.error(f"عذراً عيوني، اكو مشكلة: {str(e)}")
    
