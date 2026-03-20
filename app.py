import streamlit as st
import requests
import json
import re

# 1. إعدادات المتجر
STORE_NAME = "متجر النور للتقنية" 
EXPERT_NAME = "عباس"              
PRODUCT_TYPE = "أجهزة الموبايل والحاسبات" 
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzboWW6szwgFDiHOc9-nETt--8F33WZHimWRvJmT-ZHE-Y7TTjUFx4dC_OeIAwp7gcVVQ/exec"

st.set_page_config(page_title="نظام " + STORE_NAME, page_icon="🎮", layout="centered")

# --- تصميم الواتساب ---
design = """
    <style>
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
        visibility: hidden; display: none !important; 
    }
    .stApp { background: #0b141a; color: #e9edef; font-family: 'Segoe UI', sans-serif; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .chat-row { display: flex; margin: 15px 0; width: 100%; animation: fadeIn 0.4s ease-out; }
    .user-row { justify-content: flex-start; } 
    .abbas-row { justify-content: flex-end; } 
    .bubble {
        padding: 12px 18px; border-radius: 18px; max-width: 78%;
        font-size: 16px; line-height: 1.5; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .user-bubble { background-color: #005c4b; color: white; border-bottom-left-radius: 2px; }
    .abbas-bubble { background-color: #202c33; color: white; border-bottom-right-radius: 2px; border: 1px solid #38bdf8; }
    div[data-testid="stChatInput"] {
        position: fixed !important; bottom: 5px !important; 
        left: 15% !important; right: 15% !important;
        width: 70% !important; z-index: 1002 !important;
        background: #202c33 !important; border: 2px solid #38bdf8 !important; border-radius: 12px !important;
    }
    .stChatContainer { padding-bottom: 150px !important; }
    </style>
"""
st.markdown(design, unsafe_allow_html=True)

def send_to_excel(name, phone, order):
    payload = {"name": name, "phone": phone, "order": order}
    try:
        requests.post(GOOGLE_SHEET_URL, data=json.dumps(payload), timeout=5)
    except:
        pass

# 2. الهوية
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🎮 " + STORE_NAME + "</h2>", unsafe_allow_html=True)

# 3. الذاكرة
MY_KEY = "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"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for msg in st.session_state.messages:
    side = "user-row" if msg["role"] == "user" else "abbas-row"
    bubble = "user-bubble" if msg["role"] == "user" else "abbas-bubble"
    label = "👤 الزبون" if msg["role"] == "user" else "🎮 " + EXPERT_NAME
    st.markdown(f'<div class="chat-row {side}"><div class="bubble {bubble}"><b>{label}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)

# 5. منطق الإدخال والرد
if prompt := st.chat_input("سولف ويا عباس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>👤 الزبون:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MY_KEY}", "Content-Type": "application/json"}
    
    # تحويل النصوص لمتغيرات نظيفة تماماً
    sys_instruction = "You are a sales assistant named " + EXPERT_NAME + " for a shop called " + STORE_NAME + ". Speak in Iraqi Arabic dialect mixed with formal Arabic. Ask for customer name and phone. If you get a phone number, say: [تم تسجيل طلبك يا بطل]."
    extract_task = "Return JSON only with name, phone, order from this text: " + prompt

    try:
        # 1. تحليل البيانات
        extract_res = requests.post(url, headers=headers, json={
