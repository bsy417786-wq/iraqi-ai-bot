import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الموقع
st.set_page_config(page_title="محل لابتوبات عباس حيدر", page_icon="💻")
st.title("💻 مساعد المبيعات الذكي (عباس حيدر)")
st.markdown("مرحباً بك في محلنا! أنا عباس حيدر، حاضر لأي استفسار.")

# 2. المفتاح اللي عطيته إلي
api_key = "AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"
genai.configure(api_key=api_key)

# التعديل هنا: استخدمنا اسم الموديل بدون v1beta لضمان التوافق
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. نظام الذاكرة للدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة الكتابة للزبون
if prompt := st.chat_input("تفضل اسألني عن أسعار اللابتوبات أو التوصيل.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. تعليمات شخصية عباس حيدر
    context = """
    أنت موظف مبيعات عراقي شاطر ومحترم اسمك (عباس حيدر). 
    تشتغل بمحل لابتوبات بأسعار من 100 ألف للمليون دينار عراقي.
    عندك تخفيضات لعيون الزبائن الحلوة، والتوصيل لبغداد مجاني.
    جاوب بلهجة بغدادية محبوبة (تدلل عيني، عيوني الك، خادم ربك).
    """
    
    try:
        # إرسال السؤال لجوجل
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # إذا طلع خطأ، راح يطبع لنا شنو هو بالضبط
        st.error(f"عذراً عيوني، اكو مشكلة بسيطة بالاتصال: {str(e)}")
