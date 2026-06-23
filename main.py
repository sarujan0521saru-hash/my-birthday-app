import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import json

# Page configuration
st.set_page_config(page_title="Happy Birthday Akkachi! ❤️", page_icon="🎂", layout="centered")

# Initialize Session State for Chat History
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
    st.title("🎂 Welcome to Akkachi Birthday App! 🎈")
    st.subheader("Please Login")
    
    password = st.text_input("Enter Password:", type="password")
    
    if st.button("Login 🚀", type="primary"):
        if password == "0625":
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = 'akka'
            st.session_state['page'] = 'wish'
            st.rerun()
        elif password == "0421":
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = 'developer'
            st.session_state['page'] = 'wish'
            st.rerun()
        else:
            st.error("Thappuuuuuuu.")

# --- IF AUTHENTICATED ---
elif st.session_state['authenticated']:
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("🎉 for my akka", use_container_width=True):
        st.session_state['page'] = 'wish'
        st.rerun()
    if st.sidebar.button("🧩 Quiz Game", use_container_width=True):
        st.session_state['page'] = 'quiz'
        st.rerun()
    if st.sidebar.button("💬 Live Chat Room", use_container_width=True):
        st.session_state['page'] = 'live_chat'
        st.rerun()
    if st.sidebar.button("🎁 Gift", use_container_width=True):
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
        st.write("first happy birthday akkachi enakku romba nan romba nampura person nee akka nan alampurathellam keaddu en meala paasam vachu enkuuda pirantha akka maari enna paathu enakku elamave irunthane love you so much akka and i wise for this day was happiest birthday ever and forever your life!! 💖")
        if lottie_cake:
            st.components.v1.html(f'<iframe src="https://lottie.host/embed/8ba478b0-b530-4e50-bf6c-67c13cb28188/ecvY38A24J.json" style="border:none; width:100%; height:400px;"></iframe>', height=400)

    # --- PAGE 3: QUIZ ---
    elif st.session_state['page'] == 'quiz':
        st.title("🧩 Akkachi's Birthday Quiz!")
        ans1 = st.radio("Question 1: unnakku romba pidicha person yaru? 🤷", ["Friends", "Me", "No one"], key="q1")
        if st.button("Submit Answers", type="primary"):
            if ans1 == "Me":
                st.balloons()
                st.success("good girl! ❤️✨")
            else:
                st.error("thappu thappu! 😜")

    # --- PAGE 4: LIVE CHAT (100% Safe Local Storage Method) ---
    elif st.session_state['page'] == 'live_chat':
        st.markdown("<h3 style='color: #4a90e2;'>💬 Live Chat Room</h3>", unsafe_allow_html=True)
        st.write("***Chat History:***")
        
        # ஜாவாஸ்கிரிப்ட் மூலம் பிரவுசர் மெமரியில் இருந்து பழைய மெசேஜ்களைப் படிக்கும் பகுதி
        # இது பக்கத்தை ரீஃப்ரெஷ் செய்தாலும் மெசேஜ் அழியாமல் பாதுகாக்கும்
        js_get_code = """
        <script>
            const chats = localStorage.getItem('birthday_chat_history') || '[]';
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: chats
                }, '*');
            }
        </script>
        """
        # பிரவுசரில் இருந்து பெறப்படும் தரவை வாங்குதல்
        raw_chats = st.components.v1.html(js_get_code, height=0)
        
        # ஒருவேளை லோக்கல் மெமரியில் டேட்டா இருந்தால் அதை சாட் லிஸ்டில் இணைப்போம்
        if raw_chats and isinstance(raw_chats, str) and raw_chats != '[]':
            try:
                st.session_state['chat_messages'] = json.loads(raw_chats)
            except Exception:
                pass

        chat_container = st.container(height=300)
        
        with chat_container:
            if not st.session_state['chat_messages']:
                st.caption("Innum yaarum message seiyavillai. Neeye muthal msg podu! 👇")
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
                
                # புதிய மெசேஜை செஷனில் சேர்த்தல்
                st.session_state['chat_messages'].append({
                    "sender": sender_name,
                    "message": user_msg,
                    "time": current_time
                })
                
                # பிரவுசரின் சொந்த Local Storage மெமரியில் மெசேஜ்களைப் பத்திரமாகச் சேமிக்கும் பகுதி
                clean_json = json.dumps(st.session_state['chat_messages']).replace("'", "\\'")
                js_save = f"""
                <script>
                    localStorage.setItem('birthday_chat_history', '{clean_json}');
                </script>
                """
                st.components.v1.html(js_save, height=0)
                st.rerun()

    # --- PAGE 5: GIFT ---
    elif st.session_state['page'] == 'gift':
        st.title("🎁 A Special Gift For You, Akkachi!")
        try:
            st.image("gift_photo.jpg", caption="Happy Birthday Akkachi! 💖", use_container_width=True)
        except Exception:
            try:
                st.image("gift_photo.jpeg", caption="Happy Birthday Akkachi! 💖", use_container_width=True)
            except Exception:
                st.image("https://images.unsplash.com/photo-1513201099705-a9746e1e201f", caption="Gift Box 🎁", use_container_width=True)
