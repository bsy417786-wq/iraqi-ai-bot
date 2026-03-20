import streamlit as st
import google.generativeai as genai

# 1. إعدادات واجهة الموقع (التصميم)
st.set_page_config(page_title="محل لابتوبات عباس حيدر", page_icon="💻")
st.title("💻 مساعد المبيعات الذكي (عباس حيدر)")
st.markdown("مرحباً بك في محلنا! أنا عباس حيدر، حاضر لأي استفسار عن اللابتوبات.")

# 2. جلب مفتاح الـ API من الخزنة السرية (Secrets) لضمان الأمان وعدم الحظر
try:
    api_key = st.secrets["AIzaSyCCJtpyUJ79Xa9xsb9pIWLlQDFkssUc_Zc"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("عذراً عيوني، اكو مشكلة بمفتاح الـ API. تأكد إنك ضفته بالـ Secrets.")

# 3. ذاكرة الدردشة (حتى يتذكر عباس شنو حجينا وياه)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة إدخال النص (من الزبون)
if prompt := st.chat_input("تفضل اسألني عن أسعار اللابتوبات أو التوصيل.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. تعليمات الشخصية (الذكاء الاصطناعي)
    context = """
    أنت موظف مبيعات عراقي شاطر ومحترم اسمك (عباس حيدر). 
    تشتغل بمحل لابتوبات. 
    معلومات المحل اللي لازم تلتزم بيها:
    1. الأسعار تبدأ من 100 ألف وتوصل للمليون دينار عراقي حسب المواصفات.
    2. عندنا تخفيضات قوية ومميزة (لعيون الزبائن الحلوة).
    3. التوصيل داخل بغداد مجاني 100%.
    طريقة الرد: بلهجة بغدادية محبوبة وكريمة، استخدم عبارات مثل (تدلل عيني، عيوني الك، خادم ربك، صار وتدلل).
    إذا سألك الزبون عن لابتوب غالي، قله موجود لابتوبات قيمنق ومونتاج قوية توصل للمليون.
    """
    
    try:
        # إرسال التعليمات مع سؤال الزبون للجيمناي
        response = model.generate_content(f"{context}\nالزبون: {prompt}")
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("عذراً عيوني، صارت مشكلة بالاتصال بالسيرفر. جرب مرة ثانية بعد شوية.")
