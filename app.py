import streamlit as st
import requests

st.set_page_config(page_title="عباس حيدر - الإصدار الحديث 2026", page_icon="💻")
st.title("💻 مساعد المبيعات: عباس حيدر (Llama 3.3)")

# المفتاح مالتك من Groq (تأكد يبدأ بـ gsk_)
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

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، رد بلهجة بغدادية محبوبة جداً."
    
    payload = {
        "model": "llama-3.3-70b-versatile", # هذا هو الموديل الجديد والبديل الرسمي
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if 'choices' in result:
            answer = result['choices'][0]['message']['content']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            error_msg = result.get('error', {}).get('message', 'اكو خلل بالمفتاح أو الموديل')
            st.error(f"⚠️ تنبيه: {error_msg}")
            
    except Exception as e:
        st.error(f"❌ مشكلة بالاتصال: {str(e)}")
