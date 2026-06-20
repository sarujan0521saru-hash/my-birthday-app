import streamlit as st
import requests
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Happy Birthday Akkachi! ❤️", page_icon="🎂", layout="centered")

# File to store chat history
CHAT_FILE = "chat_history.json"

def load_chat():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chat(chat_list):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_list, f, ensure_ascii=False, indent=4)

# Function to load Lottie animations safely
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Try loading alternative/stable Lottie animation URLs
lottie_cake = load_lottieurl("https://lottie.host/embed/8ba478b0-b530-4e50-bf6c-67c13cb28188/ecvY38A24J.json") or load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_myejiohb.json")

# Initialize Session States
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# --- 1. LOGIN PAGE ---
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🔒 Welcome!</h1>", unsafe_allow_html=True)
    st.subheader("Please choose who is logging in:")
    
    user_choice = st.radio("Who are you?:", ["1. For cella Akka 👩", "2. For Me (Developer) 👨‍💻"])
    password = st.text_input("Enter Password", type="password", placeholder="Enter your password here...")
    
    if st.button("Login 🚀", use_container_width=True):
        if user_choice == "1. For cella Akka 👩" and password == "0625":
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = 'akka'
            st.snow()
            st.rerun()
        elif user_choice == "2. For Me (Developer) 👨‍💻" and password == "0421":
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = 'me'
            st.rerun()
        else:
            st.error("pila veara password. ❌")

# --- 2. MAIN PAGE ---
else:
    if st.session_state['user_role'] == 'akka':
        st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎉 Happy Birthday Akkachi! 🎉</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #4a4a4a;'>An exclusive page for the best sister in the world! ❤️</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #4a90e2;'>👨‍💻 Welcome Back, My Dear Me!</h1>", unsafe_allow_html=True)

    # Show animation if loaded successfully
    if lottie_cake:
        try:
            from streamlit_lottie import st_lottie
            st_lottie(lottie_cake, height=200, key="cake_anim")
        except Exception:
            pass

    st.write("---")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        if st.button("✉️ My Love Letter", use_container_width=True):
            st.session_state['page'] = 'message'
    with col2:
        if st.button("📸 Sweet Memories (Photos)", use_container_width=True):
            st.session_state['page'] = 'photos'
    with col3:
        if st.button("🎮 Fun Quiz Game", use_container_width=True):
            st.session_state['page'] = 'game'
    with col4:
        if st.button("💬 Live Chat Room", use_container_width=True):
            st.session_state['page'] = 'live_chat'

    st.write("---")

    # --- Button 1: Love Letter ---
    if st.session_state['page'] == 'message':
        st.balloons()
        st.markdown("<h3 style='color: #ff4b4b;'>💌 A Letter I Wrote For You:</h3>", unsafe_allow_html=True)
        st.success("""
        **Dearest Akka,**\n
        first happy birthday akkachi enakku life la oru mukkiyamaana person nee enakku nalla friend ahh. 
        student ahh teacher ah amma va enkuuda pirantha akka maari ena ninachane love you soo much akka and.\n
        **Wish you a very Happy Birthday, Akka! 🎂💐**
        """)

    # --- Button 2: Photos ---
    elif st.session_state['page'] == 'photos':
        st.markdown("<h3 style='color: #ff4b4b;'>📸 Our Beautiful Memories:</h3>", unsafe_allow_html=True)
        try:
            col_img1, col_img2, col_img3 = st.columns(3)
            with col_img1: st.image("photo1.jpg", caption="happy cake day akkachi 👶", use_container_width=True)
            with col_img2: st.image("photo2.jpg", caption="love you ✨", use_container_width=True)
            with col_img3: st.image("photo3.jpg", caption="with my best sister 👨‍👩‍👦", use_container_width=True)
        except Exception:
            st.info("💡 **Note:** Please save 'photo1.jpg', 'photo2.jpg', and 'photo3.jpg' inside your project folder.")

    # --- Button 3: Quiz Game ---
    elif st.session_state['page'] == 'game':
        st.markdown("<h3 style='color: #ff4b4b;'>🎮 Akkakku Quiz:</h3>", unsafe_allow_html=True)
        
        st.write("### **Question 1: unakuu yara romba pidikkum?** 😎")
        ans1 = st.radio("Choose the correct answer:", ["Friends", "Me", "No one"], key="q1")
        
        
        
        if st.button("Submit Answers", type="primary"):
            if ans1 == "Me":
                st.balloons()
                st.success("nalla pilla! 💖🥳🎉")
            else:
                st.error("athellam ila vera vida! 😜")

    # --- Button 4: Live Chat Box ---
    elif st.session_state['page'] == 'live_chat':
        st.markdown("<h3 style='color: #4a90e2;'>💬 Live Chat Room</h3>", unsafe_allow_html=True)
        
        chat_history = load_chat()
        st.write("**Chat History:**")
        chat_container = st.container(height=300)
        
        with chat_container:
            if not chat_history:
                st.caption("No messages yet. Be the first to start the conversation!")
            for chat in chat_history:
                if chat['sender'] == 'Akka':
                    st.markdown(f"**👩 Akka [{chat['time']}]:** {chat['message']}")
                else:
                    st.markdown(f"**👨‍💻 Me [{chat['time']}]:** {chat['message']}")
                    
        st.write("---")
        sender_title = "Akka" if st.session_state['user_role'] == 'akka' else "Me (Developer)"
        user_msg = st.text_input(f"Send message as **{sender_title}**:", key="chat_input", placeholder="Type a message...")
        
        if st.button("Send ✈️", type="primary"):
            if user_msg.strip() != "":
                current_time = datetime.now().strftime("%H:%M")
                sender_name = "Akka" if st.session_state['user_role'] == 'akka' else "Me"
                
                new_message = {
                    "sender": sender_name,
                    "message": user_msg,
                    "time": current_time
                }
                chat_history.append(new_message)
                save_chat(chat_history)
                st.rerun()

    # Back to Home button
    if st.session_state['page'] != 'home':
        st.write("")
        if st.button("🔙 Go Back to Home Page", use_container_width=True):
            st.session_state['page'] = 'home'
            st.rerun()