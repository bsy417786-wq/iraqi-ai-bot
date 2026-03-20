import streamlit as st
import requests

st.set_page_config(page_title="عباس حيدر - للتعامل مع الزبائن", page_icon="💻")
st.title("💻 مساعد المبيعات: عباس حيدر (Llama 3)")

# المفتاح الجديد من Groq (حطه هنا)
GROQ_API_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رابط الاتصال بـ Groq (أسرع سيرفر بالعالم)
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    context = "أنت عباس حيدر، صاحب محل لابتوبات ببغداد، أسعارك من 100 ألف للمليون، رد بلهجة بغدادية محبوبة (تدلل عيني، عيوني الك )
    
    payload = {
        "model": "llama3-8b-8192", # هذا الموديل طيارة
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except:
        st.error("أكو ضغط عالسيرفر، جرب مرة ثانية عيوني.")
