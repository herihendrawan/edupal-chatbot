import streamlit as st
from groq import Groq
import os

# Ambil API Key dari Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Inisialisasi Groq client
client = Groq(api_key=GROQ_API_KEY)

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="EduPal - AI Learning Buddy",
    page_icon="🎓",
    layout="centered",
)

# --- JUDUL ---
st.title("🎓 EduPal")
st.markdown("*Your Friendly Learning Buddy — Powered by Groq AI*")
st.divider()

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """Kamu adalah EduPal, chatbot edukasi yang ramah dan menyenangkan untuk semua kalangan.
Tugasmu adalah membantu pengguna belajar berbagai topik dengan cara yang santai, mudah dipahami, dan interaktif.

Panduan gaya bicara:
- Gunakan bahasa Indonesia yang santai dan friendly
- Sapa pengguna dengan hangat
- Berikan penjelasan yang sederhana tapi tetap akurat
- Gunakan emoji secukupnya agar terasa lebih hidup
- Selalu semangati pengguna untuk terus belajar
"""

# --- INISIALISASI SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! 👋 Aku **EduPal**, teman belajar kamu!\nMau belajar apa hari ini? Tanya aja, aku siap bantu! 😊",
        }
    ]

# --- TAMPILKAN SEMUA PESAN ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🧑"):
        st.markdown(msg["content"])

# --- INPUT DARI USER ---
if prompt := st.chat_input("Tanya apa saja... 💬"):
    # Tambah pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    # Generate response dari Groq
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("EduPal lagi mikir... 🤔"):
            try:
                # Siapkan history chat
                chat_history = []
                for msg in st.session_state.messages[:-1]:
                    chat_history.append({"role": msg["role"], "content": msg["content"]})
                
                # Kirim request ke Groq
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *chat_history,
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                
            except Exception as e:
                reply = f"Maaf, terjadi kesalahan: {str(e)}"
                st.markdown(reply)
    
    # Simpan response ke history
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ EduPal Info")
    st.markdown("""
    **🤖 Model:** Llama 3.3 70B (via Groq)
    **🎯 Use Case:** Edukasi & Belajar
    **👥 Target:** Semua Kalangan
    **🗣️ Bahasa:** Indonesia (Santai)
    """)
    st.divider()
    st.markdown("**💡 Contoh pertanyaan:**")
    st.markdown("""
    - Apa itu fotosintesis?
    - Jelaskan rumus luas lingkaran
    - Ceritakan sejarah kemerdekaan RI
    - Cara belajar yang efektif itu gimana?
    """)
    st.divider()
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Halo! 👋 Aku **EduPal**, teman belajar kamu!\nMau belajar apa hari ini? 😊",
            }
        ]
        st.rerun()
