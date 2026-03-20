
# 3. عرض الرسايل (يسار ويمين)
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 أنت" if msg["role"] == "user" else "🎮 عباس حيدر"
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 4. منطق الإدخال والرد (مع حماية من توقف السيرفر)
if prompt := st.chat_input("تفضل بطرح استفسارك عيوني..."):
    # عرض رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 أنت:</b><br>{prompt}</div></div>', unsafe_allow_html=True)

    # طلب الرد من السيرفر
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    context = (
        "أنت عباس حيدر، صاحب متجر كمبيوتر في بغداد. تتحدث فصحى محترمة مع كلمات بغدادية (عيوني، تدلل، يا بطل). "
        "مهمتك بيع تجميعات الكيمنك القوية. إذا سألك الزبون عن الشراء، اطلب منه معلومات التوصيل فوراً. "
        "نحن متواجدون 24/7."
    )
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": context}] + st.session_state.messages,
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
        else:
            ans = "اعتذر منك عيوني، يبدو أن هناك ضغطاً كبيراً على المتجر الآن. تدلل عليّ، اترك رسالتك وسأرد عليك فوراً يا بطل!"
            
        st.markdown(f'<div class="chat-row abbas-row"><div class="bubble abbas-bubble"><b>🎮 عباس حيدر:</b><br>{
