import streamlit as st
import requests
import json

# 1. إعداد واجهة الموقع
st.set_page_config(page_title="محل عباس حيدر للابتوبات", page_icon="💻")
st.title("💻 عباس حيدر للمبيعات (النسخة الذكية 2.0)")
st.markdown("مرحباً بك! أنا عباس حيدر، حاضر لأي استفسار عن اللابتوبات والتوصيل.")

# 2. المفتاح مالتك المباشر
api_key = "AIzaSyB99jUQomPgJHpAZz5bQXe4hSeJucmKQW0"

# 3. نظام ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة الكتابة
if prompt := st.chat_input("تفضل اسأل عباس حيدر عيوني.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الرابط المباشر لأحدث موديل Gemini 2.0 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # تعريف الشخصية والمعلومات (عباس حيدر)
    context = (
        "أنت موظف مبيعات عراقي اسمك عباس حيدر. تشتغل بمحل لابتوبات. "
        "الأسعار تبدأ من 100 ألف وتوصل للمليون دينار عراقي. "
        "عندك تخفيضات قوية لعيون الزبائن، والتوصيل لبغداد مجاني 100%. "
        "رد بلهجة بغدادية محبوبة وكريمة (تدلل عيني، عيوني الك، خادم ربك)."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{context}\nالزبون: {prompt}"}]
        }]
    }

    try:
        # إرسال الطلب لجوجل
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        # استخراج الرد
        if 'candidates' in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            error_msg = result.get('error', {}).get('message', 'خطأ غير معروف')
            st.error(f"جوجل تگول: {error_msg}")
            
    except Exception as e:
        st.error(f"عذراً عيوني، اكو مشكلة بالاتصال: {str(e)}")
    
