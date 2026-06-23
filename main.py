import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import json

# Page configuration
st.set_page_config(page_title="Happy Birthday Akkachi! ❤️", page_icon="🎂", layout="centered")

# --- JAVASCRIPT LOCAL STORAGE MANAGEMENT ---
# பிரவுசர் மெமரியில் இருந்து சாட்டைப் படிக்கவும் எழுதவும் உதவும் எளிய JS கம்போனென்ட்


st.components.v1.html(js_code, height=0)

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
    st.title("🎂 Welcome to Akkachi's Birthday App! 🎈")
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
            st.error("thappuuuuuuuuu")

# --- IF AUTHENTICATED ---
elif st.session_state['authenticated']:
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("🎉 for my akkachiiii", use_container_width=True):
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
        st.write("first happy birthday akka nee life full ah happy ah irukkanum enaku rompa pidicha nan romba nampura person nee akka nan ena alampinaalum keaddu kondu enakku sappadu theethi viddu nan kavalaila iruntha athukkum aaruthal solli enakku kuuda pirantha akka maari ena pathu kidda ovve you sooo much akka and happiest birthday for you! 💖")
        if lottie_cake:
            st.components.v1.html(f'<iframe src="https://lottie.host/embed/8ba478b0-b530-4e50-bf6c-67c13cb28188/ecvY38A24J.json" style="border:none; width:100%; height:400px;"></iframe>', height=400)

    # --- PAGE 3: QUIZ ---
    elif st.session_state['page'] == 'quiz':
        st.title("🧩 Akkachi's Birthday Quiz!")
        ans1 = st.radio("Question 1: Ammakku romba pidicha person yaru? 🤷", ["Friends", "Me", "No one"], key="q1")
        if st.button("Submit Answers", type="primary"):
            if ans1 == "Me":
                st.balloons()
                st.success("good girl ❤️✨")
            else:
                st.error("thappu thappu! 😜")

    # --- PAGE 4: LIVE CHAT (Safe Local Storage Method) ---
# --- PAGE 4: LIVE CHAT (Simple Safe JavaScript Storage) ---
    elif st.session_state['page'] == 'live_chat':
        st.markdown("<h3 style='color: #4a90e2;'>💬 Live Chat Room</h3>", unsafe_allow_html=True)
        st.write("***Chat History:***")
        
        # ஜாவாஸ்கிரிப்ட் மூலம் பிரவுசர் மெமரியில் இருந்து மெசேஜ்களை செஷன் ஸ்டேட்டிற்குள் கொண்டு வரும் எளிய தந்திரம்
        import streamlit.components.v1 as components
        
        # 1. பிரவுசரில் மெசேஜ் இருந்தால் அதை எடுக்க ஒரு மறைமுக பட்டன்
        if 'js_loaded' not in st.session_state:
            js_script = """
            <script>
                const data = localStorage.getItem('birthday_chat_history') || '[]';
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: data
                }, '*');
            </script>
            """
            components.html(js_script, height=0)
            st.session_state['js_loaded'] = True
            
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
                
                # புதிய மெசேஜை லிஸ்டில் சேர்த்தல்
                st.session_state['chat_messages'].append({
                    "sender": sender_name,
                    "message": user_msg,
                    "time": current_time
                })
                
                # பிரவுசரின் சொந்த Local Storage-இல் ஜாவாஸ்கிரிப்ட் மூலம் நேரடியாக சேமித்தல்
                clean_json = json.dumps(st.session_state['chat_messages']).replace("'", "\\'")
                js_save = f"<script>localStorage.setItem('birthday_chat_history', '{clean_json}');</script>"
                components.html(js_save, height=0)
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
