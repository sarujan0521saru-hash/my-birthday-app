import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(page_title="Happy Birthday Akkachi! ❤️", page_icon="🎂", layout="centered")

# Initialize Session State for Chat History if it doesn't exist
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = []

# Function to load Lottie animations safely
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

lottie_cake = load_lottieurl("https://lottie.host/embed/8ba478b0-b530-4e50-bf6c-67c13cb28188/ecvY38A24J.json")

# Initialize Session States for Login/Pages
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --- PAGE 1: LOGIN ---
if st.session_state['page'] == 'login':
    st.title("🎂 Welcome to Akkachi's Birthday App! 🎈")
    st.subheader("Please Login")
    
    password = st.text_input("Enter Password:", type="password")
    
    if st.button("Login 🚀", type="primary"):
        if password == "0625":  # உங்கள் अकाவின் பாஸ்வேர்ட்
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = 'akka'
            st.session_state['page'] = 'wish'
            st.rerun()
        elif password == "0421":  # உங்களுடைய பாஸ்வேர்ட்
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = 'developer'
            st.session_state['page'] = 'wish'
            st.rerun()
        else:
            st.error("thappuuuuuuuuuu")

# --- IF AUTHENTICATED ---
elif st.session_state['authenticated']:
    
    # Sidebar Navigation (இடது பக்க மெனு)
    st.sidebar.title("Navigation")
    if st.sidebar.button("🎉 for you Akka", use_container_width=True):
        st.session_state['page'] = 'wish'
        st.rerun()
    if st.sidebar.button("🧩 Quiz Game", use_container_width=True):
        st.session_state['page'] = 'quiz'
        st.rerun()
    if st.sidebar.button("💬 Live Chat Room", use_container_width=True):
        st.session_state['page'] = 'live_chat'
        st.rerun()
    if st.sidebar.button("🎁 gift", use_container_width=True):  # புதிய Gift பட்டன்
        st.session_state['page'] = 'gift'
        st.rerun()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout 🚪", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['user_role'] = None
        st.session_state['page'] = 'login'
        st.rerun()

    # --- PAGE 2: WISH ---
    if st.session_state['page'] == 'wish':
        st.title("🎉 Happy Birthday Akkachi! 🎂")
        st.write("first happy birthday akka enakku romba pidicha and nan romba nampura person nee ena eapavum happy ahh vachu irunthu irukaa enakku oru kuuda pirantha akka maari ena paathukidda enakku oru pirachanandaa athukku aaruthal thaarathum nee than ena comfert panrathum nee than enda cella akkakku happiest birthday wish 💖")
        if lottie_cake:
            st.components.v1.html(f'<iframe src="https://lottie.host/embed/8ba478b0-b530-4e50-bf6c-67c13cb28188/ecvY38A24J.json" style="border:none; width:100%; height:400px;"></iframe>', height=400)

    # --- PAGE 3: QUIZ ---
    elif st.session_state['page'] == 'quiz':
        st.title("🧩 Akkachi's Birthday Quiz!")
        
        ans1 = st.radio("Question 1: unnakku romba pidicha person yaru? 🤷", ["Friends", "Me", "No one"], key="q1")
        if st.button("Submit Answers", type="primary"):
            if ans1 == "Me":
                st.balloons()
                st.success("sariyaana pathil ! ❤️✨")
            else:
                st.error("thappu thappu! 😜")

    # --- PAGE 4: LIVE CHAT ---
    elif st.session_state['page'] == 'live_chat':
        st.markdown("<h3 style='color: #4a90e2;'>💬 Live Chat Room</h3>", unsafe_allow_html=True)
        st.write("***Chat History:***")
        
        chat_container = st.container(height=300)
        
        with chat_container:
            if not st.session_state['chat_messages']:
                st.caption("neeye muthal msg poodu")
            else:
                for msg in st.session_state['chat_messages']:
                    if msg['sender'] == 'Akka':
                        st.markdown(f"**👩‍🦰 Akka [{msg['time']}]:** {msg['message']}")
                    else:
                        st.markdown(f"**👨‍💻 Me [{msg['time']}]:** {msg['message']}")

        sender_title = "Akka" if st.session_state['user_role'] == 'akka' else "Me (Developer)"
        user_msg = st.text_input(f"Send message as *{sender_title}*:", key="chat_input", placeholder="Type a message...")

        if st.button("Send ✈️", type="primary"):
            if user_msg.strip() != "":
                current_time = datetime.now().strftime("%H:%M")
                sender_name = "Akka" if st.session_state['user_role'] == 'akka' else "Me"
                
                st.session_state['chat_messages'].append({
                    "sender": sender_name,
                    "message": user_msg,
                    "time": current_time
                })
                st.rerun()

    # --- PAGE 5: GIFT (புதிய பக்கம்) ---
    elif st.session_state['page'] == 'gift':
        st.title("🎁 A Special Gift For You, Akkachi!")
        st.write("it's my small gift for my best person! ✨")
        
        # உங்கள் புகைப்படத்தை அப்லோடு செய்ய வேண்டிய பகுதி
        # "gift_photo.jpg" என்ற பெயரில் உங்கள் போட்டோவை GitHub-இல் அப்லோடு செய்துவிட்டால் அது இங்கே காட்டும்.
        try:
            st.image("gift_photo.jpeg", caption="Happy Birthday Akkachi! 💖", use_container_width=True)
        except Exception:
            # ஒருவேளை போட்டோ இன்னும் அப்லோடு செய்யப்படவில்லை என்றால் தற்காலிகமாக இந்த ஆன்லைன் போட்டோ காட்டும்.
            st.image("https://images.unsplash.com/photo-1513201099705-a9746e1e201f", caption="Gift Box 🎁", use_container_width=True)
            st.info("குறிப்பு: உங்கள் சொந்த புகைப்படத்தைக் காட்ட, GitHub-இல் 'gift_photo.jpg' என்ற பெயரில் ஒரு போட்டோவை அப்லோடு செய்யவும்.")
