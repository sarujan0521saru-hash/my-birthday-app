import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import time

# Page configuration
st.set_page_config(page_title="Happy Birthday Akkachi! ❤️", page_icon="🎂", layout="centered")

# --- SUPABASE REST API CONFIGURATION ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    st.error("Streamlit Secrets இல் SUPABASE_URL மற்றும் SUPABASE_KEY ஐ இன்னும் சேர்க்கவில்லை!")
    st.stop()

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# டேட்டாபேஸில் இருந்து மெசேஜ்களைப் படிக்கும் ஃபங்க்ஷன் (Cache மெமரி முற்றிலும் தவிர்க்கப்பட்டுள்ளது)
# --- PAGE 4: LIVE CHAT (Supabase Realtime Chat Method - Sync Delay Fixed) ---
    elif st.session_state['page'] == 'live_chat':
        st.markdown("<h3 style='color: #4a90e2;'>💬 Live Chat Room</h3>", unsafe_allow_html=True)
        st.write("***Chat History:***")
        
        # Supabase டேட்டாவை வாசித்தல்
        db_messages = fetch_messages()
        
        chat_container = st.container(height=300)
        
        with chat_container:
            if not db_messages:
                st.caption("Innum yaarum message seiyavillai. Neeye muthal msg podu! 👇")
            else:
                for msg in db_messages:
                    if msg.get('sender') == 'Akka':
                        st.markdown(f"**👩‍🦰 Akka [{msg.get('time', '')}]:** {msg.get('message', '')}")
                    else:
                        st.markdown(f"**👨‍💻 Me [{msg.get('time', '')}]:** {msg.get('message', '')}")

        sender_title = "Akka" if st.session_state['user_role'] == 'akka' else "Me (Developer)"
        
        # Form வடிவமைப்பு மூலம் மெசேஜ் அனுப்புதல்
        with st.form(key="chat_form_final_sync", clear_on_submit=True):
            user_msg = st.text_input(f"Send message as *{sender_title}*:", placeholder="Type a message...")
            submit_button = st.form_submit_button(label="Send ✈️", type="primary")
            
            if submit_button:
                if user_msg and user_msg.strip() != "":
                    current_time = datetime.now().strftime("%H:%M")
                    sender_name = "Akka" if st.session_state['user_role'] == 'akka' else "Me"
                    
                    # Supabase டேட்டாபேஸிற்குள் மெசேஜை அனுப்புதல்
                    success = send_message_to_db(sender_name, user_msg.strip(), current_time)
                    if success:
                        # --- FIX: Supabase-இல் டேட்டா விழ 1 செகண்ட் டைம் கொடுத்துவிட்டு பக்கத்தை ரீபிரெஷ் செய்தல் ---
                        import time
                        time.sleep(1)
                        st.rerun()        
# டேட்டாவைச் சேர்க்கும் ஃபங்க்ஷன் 
def send_message_to_db(sender, message, time_str):
    url = f"{SUPABASE_URL}/rest/v1/chat_table"
    data = {
        "sender": sender,
        "message": message,
        "time": time_str
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code in [200, 201]:
            return True
        else:
            st.error(f"Database Reject பண்ணுகிறது: {response.text}")
            return False
    except Exception as e:
        st.error(f"Network Error: {e}")
        return False

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
            st.error("Thappuuuuuuuuuuuuuuuuu.")

# --- IF AUTHENTICATED ---
elif st.session_state['authenticated']:
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("🎉 for my sister", use_container_width=True):
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
        ans1 = st.radio("Question 1: Ammakku romba pidicha person yaru? 🤷", ["Friends", "Me", "No one"], key="q1")
        if st.button("Submit Answers", type="primary"):
            if ans1 == "Me":
                st.balloons()
                st.success("good girl! ❤️✨")
            else:
                st.error("thappu thappu! 😜")

    # --- PAGE 4: LIVE CHAT (Supabase Realtime Chat Method Fixed) ---
# --- PAGE 4: LIVE CHAT (Supabase Realtime Chat Method - Final Fixed Form) ---
    elif st.session_state['page'] == 'live_chat':
        st.markdown("<h3 style='color: #4a90e2;'>💬 Live Chat Room</h3>", unsafe_allow_html=True)
        st.write("***Chat History:***")
        
        # Supabase டேட்டாவை புதிய முறையில் வாசித்தல்
        db_messages = fetch_messages()
        
        chat_container = st.container(height=300)
        
        with chat_container:
            if not db_messages:
                st.caption("Innum yaarum message seiyavillai. Neeye muthal msg podu! 👇")
            else:
                for msg in db_messages:
                    if msg.get('sender') == 'Akka':
                        st.markdown(f"**👩‍🦰 Akka [{msg.get('time', '')}]:** {msg.get('message', '')}")
                    else:
                        st.markdown(f"**👨‍💻 Me [{msg.get('time', '')}]:** {msg.get('message', '')}")

        sender_title = "Akka" if st.session_state['user_role'] == 'akka' else "Me (Developer)"
        
        # --- 100% எரர் இல்லாத Form முறை (clear_on_submit பாக்ஸை காலி செய்யும்) ---
        with st.form(key="chat_form_fixed", clear_on_submit=True):
            user_msg = st.text_input(f"Send message as *{sender_title}*:", placeholder="Type a message...")
            submit_button = st.form_submit_button(label="Send ✈️", type="primary")
            
            if submit_button:
                if user_msg and user_msg.strip() != "":
                    current_time = datetime.now().strftime("%H:%M")
                    sender_name = "Akka" if st.session_state['user_role'] == 'akka' else "Me"
                    
                    # டேட்டாபேஸிற்குள் மெசேஜை அனுப்புதல்
                    success = send_message_to_db(sender_name, user_msg.strip(), current_time)
                    if success:
                        # பக்கத்தை உடனடியாகப் புதுப்பித்தல் (உடனே மேலே மெசேஜ் காட்டும்)
                        st.rerun()
        # --- PAGE 5: GIFT ---
    elif st.session_state['page'] == 'gift':
        st.title("🎁 A Special Gift For You, Akka!")
        try:
            st.image("gift_photo.jpg", caption="Happy Birthday Akkachi! 💖", use_container_width=True)
        except Exception:
            try:
                st.image("gift_photo.jpeg", caption="Happy Birthday Akkachi! 💖", use_container_width=True)
            except Exception:
                st.image("https://images.unsplash.com/photo-1513201099705-a9746e1e201f", caption="Gift Box 🎁", use_container_width=True)
