import streamlit as st
import requests
import datetime

# 1. إعدادات الصفحة والستايل (نفس الفخامة السابقة مع تعديلات)
st.set_page_config(page_title="عباس حيدر - نظام البيع الذكي", page_icon="💰", layout="centered")

design = """
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] { visibility: hidden; display: none !important; }
    .stApp { background: #0b141a; color: #e9edef; }
    .chat-row { display: flex; margin: 20px 0; width: 100%; animation: fadeIn 0.5s ease-out; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 
    .bubble { padding: 15px 20px; border-radius: 20px; max-width: 80%; font-size: 17px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .user-bubble { background-color: #005c4b; color: white; }
    .abbas-bubble { background-color: #202c33; color: white; border: 1px solid #38bdf8; }
    div[data-testid="stChatInput"] { position: fixed !important; bottom: 140px !important; left: 10%; width: 80%; z-index: 1001; background: #202c33 !important; border: 2px solid #38bdf8 !important; border-radius: 15px !important; }
    .fixed-footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0b141a; padding: 10px 0; z-index: 1000; border-top: 2px solid #38bdf8; text-align: center; }
    .stChatContainer { padding-bottom: 480px !important; }
    .order-card { background: #1e293b; border: 1px solid #facc15; padding: 15px; border-radius: 10px; margin-top: 10px; text-align: center; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

# --- دالة إرسال الإشعار لصاحب المحل (تنبيه التوصيل) ---
def notify_owner(order_details):
    # هنا ممكن نربطها بـ Telegram API أو إيميل
    # حالياً راح نطبعها كـ "سجل مبيعات" داخلي
    with open("orders_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] طلب جديد: {order_details}\n")
    return True

# 2. العنوان
st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🎮 نظام مبيعات عباس حيدر</h1>", unsafe_allow_html=True)

# 3. الذاكرة والـ API
MY_KEY = "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"
if "messages" not in st.session_state: st.session_state.messages = []
if "order_pending" not in st.session_state: st.session_state.order_pending = False

# 4. عرض المحادثة
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 أنت" if msg["role"] == "user" else "🎮 عباس حيدر"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال
if prompt := st.chat_input("تحدث مع عباس لإتمام طلبك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # سياق "موظف المبيعات"
    context = (
        "أنت عباس حيدر، موظف مبيعات ذكي جداً في بغداد. "
        "مهمتك: إقناع الزبون بالقطع القوية (RTX, Intel i9, الخ). "
        "عندما يبدي الزبون رغبة في الشراء، اطلب منه (الاسم الكامل، العنوان، ورقم الهاتف). "
        "لغتك فصحى محترمة مع كلمات عراقية (عيوني، تدلل، نار وشرار). "
        "أخبره أن خدمة التوصيل جاهزة فور إتمام الطلب 24/7."
    )
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": context}] + st.session_state.messages}

    try:
        response = requests.post(url, headers=headers, json=payload)
        ans = response.json()['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
        # إذا عباس اكتشف إن الزبون يريد يشتري (ذكاء اصطناعي)
        if any(word in ans for word in ["عنوان", "هاتف", "توصيل", "سأقوم بتسجيل"]):
            st.session_state.order_pending = True
            
        st.rerun()
    except:
        st.error("السيرفر مشغول، حاول مرة ثانية يا بطل!")

# 6. زر "تأكيد البيع" لصاحب المحل
if st.session_state.order_pending:
    with st.container():
        st.markdown('<div class="order-card">', unsafe_allow_html=True)
        st.write("📦 هل ترغب في تأكيد طلب الشراء وإرسال شركة التوصيل فوراً؟")
        if st.button("✅ نعم، أكد الطلب الآن"):
            last_msg = st.session_state.messages[-2]["content"] if len(st.session_state.messages)>1 else "طلب غير محدد"
            notify_owner(f"زبون يريد شراء: {last_msg}")
            st.success("تم إرسال الطلب لشركة التوصيل! سيتم التواصل معكم خلال دقائق. عباس حيدر بخدمتكم 24 ساعة.")
            st.session_state.order_pending = False
        st.markdown('</div>', unsafe_allow_html=True)

# 7. الفوتر الثابت
st.markdown("""
    <div class="fixed-footer">
        <div style="color:#facc15; font-size:14px; font-weight:bold;">📍 شارع الصناعة | 📞 07700000000 | 🚚 التوصيل متاح 24/7</div>
        <div style="color:#94a3b8; font-size:10px; margin-top:5px;">© 2026 ABBAS HAIDER - نظام البيع والتحصيل الذكي</div>
    </div>
""", unsafe_allow_html=True)
