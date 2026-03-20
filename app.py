import streamlit as st
import requests
import json

# 1. إعداد واجهة الموقع (التصميم الاحترافي)
st.set_page_config(page_title="عباس حيدر للابتوبات 💻", page_icon="💻", layout="centered")

# 2. عرض اللوجو الجديد
# ملاحظة: إذا الشركة عندها اللوجو كملف، تكدر تبدله برابط الملف. هسة استخدمت اللوجو اللي سويناه.
try:
    # هسة راح اعرض صورة تقريبية للوجو حتى يشتغل كدامي
    st.image("https://example.com/ عباس_حيدر_لوجو.png", width=150) # تبديل هذا برابط اللوجو الحقيقي لاحقاً
except:
    # إذا محملت الصورة، اعرض اسم المحل بشكل حلو
    st.title("💻 عباس حيدر")
    st.markdown("## محلات اللابتوبات العصرية في بغداد")

st.markdown("---")

# 3. المفتاح مالتك (الكنز)
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل اسأل عباس حيدر عيوني.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. الرابط المباشر لأحدث موديل 2.0 فلاش
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # تعريف شخصية عباس حيدر "المطورة"
    context = (
        "أنت عباس حيدر، خبير لابتوبات عراقي محترف. "
        "أسعارك من 100 ألف وتوصل للمليون دينار عراقي. "
        "عندك تخفيضات لعيون الزبائن، والتوصيل لبغداد مجاني. "
        "رد بلهجة بغدادية محبوبة (عيوني، تدلل، خادم ربك، صار)."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{context}\nالزبون يقول: {prompt}"}]
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
            st.warning("عذراً عيوني، عباس تعبان شوية. انتظر دقيقة وجرب.")
        else:
            st.error("السيرفر دا يتغلى علينا.")
            
    except Exception as e:
        st.error(f"مشكلة تقنية: {str(e)}")

