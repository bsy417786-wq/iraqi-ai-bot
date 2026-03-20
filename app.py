import streamlit as st
import requests
import json

st.set_page_config(page_title="عباس حيدر - الإصدار الذهبي", page_icon="💻")
st.title("💻 مساعد المبيعات: عباس حيدر (Groq Edition)")

# حط مفتاحك الجديد من Groq هنا (تأكد تنسخه كله يبدأ بـ gsk_ )
GROQ_API_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل عيوني اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الرابط الرسمي لـ Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # تعريف شخصية عباس حيدر البغدادي
    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، رد بلهجة بغدادية محبوبة (عيوني، تدلل، خادم ربك)."
    
    payload = {
        "model": "llama3-70b-8192", # استخدمنا الموديل الأكبر والأذكى
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7 # حتى يصير كلامه طبيعي وبغدادي
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        # استخراج الرد
        if 'choices' in result:
            answer = result['choices'][0]['message']['content']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            # إذا اكو خطأ، راح يطبع الخطأ الحقيقي حتى نعرف نعالجه
            error_details = result.get('error', {}).get('message', 'خطأ غير معروف')
            st.error(f"⚠️ تنبيه من السيرفر: {error_details}")
            
    except Exception as e:
        st.error(f"❌ مشكلة بالاتصال: {str(e)}")
