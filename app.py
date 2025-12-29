import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# --- CẤU HÌNH ---
st.set_page_config(page_title="Giáo Sư Pi - Gia sư Voice AI", page_icon="🎙️")

# Hàm chuyển văn bản thành giọng nói và phát âm thanh
def speak(text):
    # Xử lý văn bản: bỏ các ký tự đặc biệt của Markdown để giọng đọc tự nhiên hơn
    clean_text = text.replace("*", "").replace("#", "")
    tts = gTTS(text=clean_text, lang='vi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- PHẦN KẾT NỐI AI (Giữ nguyên như bản trước) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("Vui lòng nhập API Key!")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
st.title("🎓 Giáo Sư Pi - Gia Sư Biết Nói")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- NHẬP LIỆU ---
with st.sidebar:
    uploaded_file = st.file_uploader("📸 Gửi ảnh bài tập", type=["jpg", "png"])

if prompt := st.chat_input("Hỏi Thầy Pi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Gửi dữ liệu cho AI
        content = [prompt]
        if uploaded_file:
            content.append(Image.open(uploaded_file))
        
        response = model.generate_content(content)
        ai_text = response.text
        
        # 1. Hiển thị văn bản
        st.markdown(ai_text)
        
        # 2. Tạo giọng nói và hiển thị trình phát nhạc
        audio_fp = speak(ai_text)
        st.audio(audio_fp, format='audio/mp3')
        
        # Lưu vào lịch sử
        st.session_state.messages.append({"role": "assistant", "content": ai_text})

# Tự động cuộn xuống dưới cùng
st.empty()
