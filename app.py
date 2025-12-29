import streamlit as st
from openai import OpenAI

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Trạng Nguyên AI - Gia Sư Toán Tiểu Học", page_icon="🎓")

# --- CSS TÙY CHỈNH CHO ĐẸP MẮT ---
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    .user-msg {
        background-color: #e6f3ff;
    }
    h1 {
        color: #d35400;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=80) # Icon mũ trạng nguyên
with col2:
    st.title("Trạng Nguyên AI")
    st.caption("🎓 Gia sư Toán Tiểu học - Chuẩn bộ sách 'Kết Nối Tri Thức'")

st.markdown("---")

# --- SIDEBAR CẤU HÌNH ---
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập OpenAI API Key", type="password", help="Hỏi bố mẹ để lấy chìa khóa bí mật nhé!")
    st.warning("⚠️ Lưu ý: AI chỉ là công cụ hỗ trợ. Con hãy tự tư duy nhé!")
    
    st.divider()
    st.markdown("**Hướng dẫn:**")
    st.markdown("1. Nhập đề bài toán vào ô chat.")
    st.markdown("2. Trạng Nguyên sẽ gợi ý từng bước.")
    st.markdown("3. Đừng quên chuẩn bị giấy nháp!")

# --- LOGIC AI ---
if not api_key:
    st.info("👋 Chào phụ huynh và các bé! Vui lòng nhập **API Key** bên trái để bắt đầu buổi học.")
    st.stop()

client = OpenAI(api_key=api_key)

# SYSTEM PROMPT (BÍ KÍP CỦA BẠN NẰM Ở ĐÂY)
SYSTEM_PROMPT = """
### VAI TRÒ (ROLE)
Bạn là "Trạng Nguyên AI" - Một Giáo sư Toán học kiêm Nhà giáo ưu tú với 20 năm kinh nghiệm dạy Tiểu học tại Việt Nam. Bạn đang giảng dạy theo giáo trình "Kết Nối Tri Thức với Cuộc Sống" (KNTT).

### ĐỐI TƯỢNG (USER)
Học sinh tiểu học (Lớp 1 đến Lớp 5). Đặc điểm: Dễ mất tập trung, sợ sai, cần sự khích lệ.

### NGUYÊN TẮC BẤT DI BẤT DỊCH (CORE RULES)
1. KHÔNG BAO GIỜ đưa ra đáp án ngay lập tức.
2. Socratic Method: Luôn đặt câu hỏi ngược lại để dẫn dắt.
3. Tone & Voice: Ấm áp, hài hước, dùng nhiều Emoji (🌟, 🎉, 🤖). Xưng hô: "Thầy" và "Con".
4. Chuẩn Sách Giáo Khoa (KNTT):
   - Phải hướng dẫn tóm tắt.
   - Phải vẽ sơ đồ tư duy/đoạn thẳng (dùng text art) với bài toán lời văn.
   - Cấu trúc: [Gợi ý] -> [Hỏi lại] -> [Khen ngợi].

### QUY TRÌNH
Bước 1: Khen ngợi & Hỏi lớp (nếu chưa biết).
Bước 2: Phân tích đề bài (Tìm cái đã biết, cái cần tìm).
Bước 3: Gợi ý phương pháp (Vẽ sơ đồ, chọn phép tính).
Bước 4: Chỉ đưa bài giải mẫu khi học sinh đã làm đúng.
"""

# --- QUẢN LÝ HỘI THOẠI ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Chào con! Thầy là **Trạng Nguyên AI** đây! 👋🤖\n\nCon đang học lớp mấy và hôm nay bài toán nào làm khó con thế? Nói cho thầy nghe đi! 💪"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- XỬ LÝ CHAT ---
if prompt := st.chat_input("Nhập đề bài hoặc câu trả lời của con..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})