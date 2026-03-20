import streamlit as st
import requests
import json

# 1. واجهة المحل (التصميم الجديد)
st.set_page_config(page_title="عباس حيدر 2026", page_icon="🚀")
st.title("💻 عباس حيدر للمبيعات (أحدث إصدار)")
st.info("ملاحظة: إذا طلع لك خطأ Quota، انتظر دقيقة لأن جوجل محددة عدد الرسائل للنسخة المجانية.")

# 2. المفتاح مالتك (الكنز)
api_key = "AIzaSyAOYBa5hQvKPiJpsxAr4iCCPU6t7YG_CYg"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل عباس حيدر.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. هنا اللعبة: استخدمنا رابط الـ v1beta لضمان الوصول لأحدث الموديلات (مثل 2.0 حالياً)
    # ملاحظة: Gemini 2.5 بعده مموجود رسمياً، فاستخدمنا الـ 2.0-flash لأنه الأسرع عالمياً
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # تعريف شخصية عباس حيدر "المطورة"
    context = (
        "أنت عباس حيدر، خبير لابتوبات عراقي محترف. "
        "أسعارك تنافسية وتوصيلك بغدادي سريع ومجاني. "
        "رد بلهجة بغدادية راقية ومرحبة (عيوني، تدلل، صار، من رخصتك)."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{context}\nالزبون: {prompt}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if 'candidates' in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif 'error' in result:
            # إذا بعدها الكوتا قافلة، راح يگول لك انتظر كم ثانية
            st.warning(f"جوجل تگول: {result['error']['message']}")
        else:
            st.error("السيرفر دا يتغلى علينا، جرب مرة ثانية عيوني.")
            
    except Exception as e:
        st.error(f"مشكلة تقنية: {str(e)}")
