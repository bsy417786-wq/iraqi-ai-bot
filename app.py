import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="محل لابتوبات عباس حيدر", page_icon="💻")
st.title("💻 مساعد المبيعات الذكي (عباس حيدر)")
st.markdown("مرحباً بك في محلنا! أنا عباس حيدر، حاضر لأي استفسار عن اللابتوبات.")

# وضع المفتاح مباشرة لضمان التشغيل السريع
api_key = "AIzaSyCpceO6ad-PwvrF0Fn8FqYA-jxjc0e20tg"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# ذاكرة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الكتابة
if prompt := st.chat_input("تفضل اسألني عن أسعار اللابتوبات أو التوصيل.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تعليمات الشخصية الجديدة (عباس حيدر)
    context = """
    أنت موظف مبيعات عراقي شاطر ومحترم اسمك (عباس حيدر). 
    تشتغل بمحل لابتوبات. 
    معلومات المحل:
    1. الأسعار تبدأ من 100 ألف وتوصل للمليون دينار عراقي.
    2. عندنا تخفيضات قوية (لعيون الزبائن الحلوة).
    3. التوصيل داخل بغداد مجاني 100%.
    طريقة الرد: بلهجة بغدادية محبوبة، خليك كريم بالكلام، واستخدم عبارات مثل (تدلل عيني، عيوني الك، خادم ربك).
    إذا سألك الزبون عن لابتوب غالي، قله موجود لابتوبات قيمنق ومونتاج توصل للمليون.
    """
    
    try:
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("عذراً عيوني، صارت مشكلة صغيرة بالاتصال. جرب مرة ثانية.")
