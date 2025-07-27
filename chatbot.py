
import json
import requests
import time
from datetime import datetime
import csv
import os
from typing import Dict, List, Any
import google.generativeai as genai
from transformers import pipeline
import pandas as pd
from dotenv import load_dotenv
import sys
import types

# Monkey-patch torch to prevent Streamlit from walking its internals
import torch

if isinstance(torch, types.ModuleType):
    torch.__path__ = []
import streamlit as st
# Load environment variables
load_dotenv()

class DisasterResponseBot:
    def __init__(self):
        # API Keys from environment variables
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        
        # Validate API keys
        if not self.gemini_api_key:
            st.error("❌ GEMINI_API_KEY not found in environment variables!")
            st.info("Please add your Gemini API key to the .env file")
            st.stop()
            
        if not self.weather_api_key:
            st.error("❌ WEATHER_API_KEY not found in environment variables!")
            st.info("Please add your Weather API key to the .env file")
            st.stop()
        
        # Initialize Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize Granite LLM (via HuggingFace) - Cached loading
        if 'granite_llm' not in st.session_state:
            try:
                with st.spinner("Loading Granite LLM... (This may take a moment first time)"):
                    st.session_state.granite_llm = pipeline(
                        "text-generation", 
                        model="ibm-granite/granite-3b-code-instruct", 
                        trust_remote_code=True,
                        device_map="auto"
                    )
            except Exception as e:
                st.session_state.granite_llm = None
                st.warning("Granite LLM not available, using Gemini for all responses")
        
        self.granite_llm = st.session_state.granite_llm
        
        # Language support
        self.languages = {
            "English": {"code": "en", "flag": "🇺🇸"},
            "हिंदी": {"code": "hi", "flag": "🇮🇳"},
            "ಕನ್ನಡ": {"code": "kn", "flag": "🇮🇳"},
            "తెలుగు": {"code": "te", "flag": "🇮🇳"},
            "தமிழ்": {"code": "ta", "flag": "🇮🇳"},
            "বাংলা": {"code": "bn", "flag": "🇧🇩"}
        }
        
        # Disaster knowledge base
        self.knowledge_base = {
            "flood": {
                "en": "🌊 **FLOOD SAFETY:**\n• Move to higher ground immediately\n• Avoid walking/driving through flooded areas\n• Stay away from electrical equipment if you're wet\n• Listen to emergency broadcasts\n• Have emergency supplies ready",
                "hi": "🌊 **बाढ़ की सुरक्षा:**\n• तुरंत ऊंची जगह पर जाएं\n• बाढ़ के पानी में चलने/गाड़ी चलाने से बचें\n• गीले होने पर बिजली के उपकरणों से दूर रहें\n• आपातकालीन प्रसारण सुनें\n• आपातकालीन सामान तैयार रखें",
                "kn": "🌊 **ಪ್ರವಾಹ ಸುರಕ್ಷತೆ:**\n• ತಕ್ಷಣ ಎತ್ತರದ ಸ್ಥಳಕ್ಕೆ ಹೋಗಿ\n• ಪ್ರವಾಹದ ನೀರಿನಲ್ಲಿ ನಡೆಯುವುದು/ವಾಹನ ಚಲಾಯಿಸುವುದನ್ನು ತಪ್ಪಿಸಿ\n• ಒದ್ದೆಯಾಗಿದ್ದರೆ ವಿದ್ಯುತ್ ಉಪಕರಣಗಳಿಂದ ದೂರವಿರಿ\n• ತುರ್ತು ಪ್ರಸಾರವನ್ನು ಕೇಳಿ\n• ತುರ್ತು ಸಾಮಗ್ರಿಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ"
            },
            "earthquake": {
                "en": "🏠 **EARTHQUAKE SAFETY:**\n• Drop, Cover, Hold On!\n• Get under a sturdy table\n• Stay away from windows and heavy objects\n• If outdoors, move away from buildings\n• After shaking stops, evacuate if building is damaged",
                "hi": "🏠 **भूकंप की सुरक्षा:**\n• झुकें, छुपें, पकड़ें!\n• मजबूत मेज के नीचे जाएं\n• खिड़कियों और भारी वस्तुओं से दूर रहें\n• बाहर हों तो इमारतों से दूर जाएं\n• हिलना बंद होने पर क्षतिग्रस्त इमारत से बाहर निकलें",
                "kn": "🏠 **ಭೂಕಂಪ ಸುರಕ್ಷತೆ:**\n• ಕೆಳಗೆ ಬಿದ್ದು, ಮರೆಯಾಗಿ, ಹಿಡಿದುಕೊಳ್ಳಿ!\n• ದೃಢವಾದ ಮೇಜಿನ ಕೆಳಗೆ ಹೋಗಿ\n• ಕಿಟಕಿಗಳು ಮತ್ತು ಭಾರವಾದ ವಸ್ತುಗಳಿಂದ ದೂರವಿರಿ\n• ಹೊರಗಿದ್ದರೆ ಕಟ್ಟಡಗಳಿಂದ ದೂರ ಹೋಗಿ\n• ಅಲುಗಾಟ ನಿಂತ ನಂತರ ಹಾನಿಗೊಳಗಾದ ಕಟ್ಟಡದಿಂದ ಹೊರಬನ್ನಿ"
            },
            "heatwave": {
                "en": "☀️ **HEATWAVE SAFETY:**\n• Stay indoors during peak hours (10am-4pm)\n• Drink plenty of water regularly\n• Wear light-colored, loose clothing\n• Use fans, AC, or cool showers\n• Check on elderly neighbors",
                "hi": "☀️ **लू की सुरक्षा:**\n• चरम घंटों (सुबह 10-शाम 4) के दौरान घर के अंदर रहें\n• नियमित रूप से भरपूर पानी पिएं\n• हल्के रंग के ढीले कपड़े पहनें\n• पंखे, AC, या ठंडे पानी से नहाएं\n• बुजुर्ग पड़ोसियों की जांच करें",
                "kn": "☀️ **ಶಾಖದ ಅಲೆ ಸುರಕ್ಷತೆ:**\n• ಗರಿಷ್ಠ ಸಮಯದಲ್ಲಿ (ಬೆಳಿಗ್ಗೆ 10-ಸಂಜೆ 4) ಮನೆಯೊಳಗೆ ಇರಿ\n• ನಿಯಮಿತವಾಗಿ ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ\n• ತಿಳಿ ಬಣ್ಣದ, ಸಡಿಲವಾದ ಬಟ್ಟೆಗಳನ್ನು ಧರಿಸಿ\n• ಫ್ಯಾನ್, AC, ಅಥವಾ ತಣ್ಣನೆಯ ಸ್ನಾನ ಮಾಡಿ\n• ವಯಸ್ಸಾದ ನೆರೆಹೊರೆಯವರನ್ನು ಪರಿಶೀಲಿಸಿ"
            },
            "cyclone": {
                "en": "🌪️ **CYCLONE SAFETY:**\n• Stay indoors and away from windows\n• Store water and non-perishable food\n• Charge all electronic devices\n• Keep battery radio for updates\n• Secure outdoor items",
                "hi": "🌪️ **चक्रवात की सुरक्षा:**\n• घर के अंदर रहें और खिड़कियों से दूर रहें\n• पानी और सूखा खाना स्टोर करें\n• सभी उपकरण चार्ज करें\n• अपडेट के लिए बैटरी रेडियो रखें\n• बाहरी वस्तुओं को सुरक्षित करें",
                "kn": "🌪️ **ಚಂಡಮಾರುತ ಸುರಕ್ಷತೆ:**\n• ಮನೆಯೊಳಗೆ ಇರಿ ಮತ್ತು ಕಿಟಕಿಗಳಿಂದ ದೂರವಿರಿ\n• ನೀರು ಮತ್ತು ಕೆಡದ ಆಹಾರವನ್ನು ಶೇಖರಿಸಿ\n• ಎಲ್ಲಾ ಸಾಧನಗಳನ್ನು ಚಾರ್ಜ್ ಮಾಡಿ\n• ಅಪ್‌ಡೇಟ್‌ಗಳಿಗಾಗಿ ಬ್ಯಾಟರಿ ರೇಡಿಯೋ ಇರಿಸಿ\n• ಹೊರಗಿನ ವಸ್ತುಗಳನ್ನು ಸುರಕ್ಷಿತಗೊಳಿಸಿ"
            }
        }
        
        # Emergency contacts
        self.emergency_contacts = {
            "en": """🚨 **EMERGENCY NUMBERS:**
            
**India Emergency Services:**
• **Police:** 100 📞
• **Fire Brigade:** 101 🚒
• **Ambulance:** 108 🚑
• **Disaster Management:** 1070 🌪️
• **Women Helpline:** 1091 👩
• **Child Helpline:** 1098 👶
• **Tourist Emergency:** 1363 🧳

**Additional Resources:**
• **Blood Bank:** 104
• **Poison Control:** 1066""",
            
            "hi": """🚨 **आपातकालीन नंबर:**
            
**भारत आपातकालीन सेवाएं:**
• **पुलिस:** 100 📞
• **दमकल:** 101 🚒
• **एम्बुलेंस:** 108 🚑
• **आपदा प्रबंधन:** 1070 🌪️
• **महिला हेल्पलाइन:** 1091 👩
• **बाल हेल्पलाइन:** 1098 👶
• **पर्यटक आपातकाल:** 1363 🧳

**अतिरिक्त संसाधन:**
• **ब्लड बैंक:** 104
• **जहर नियंत्रण:** 1066""",
            
            "kn": """🚨 **ತುರ್ತು ಸಂಖ್ಯೆಗಳು:**
            
**ಭಾರತದ ತುರ್ತು ಸೇವೆಗಳು:**
• **ಪೊಲೀಸ್:** 100 📞
• **ಅಗ್ನಿಶಾಮಕ:** 101 🚒
• **ಆಂಬ್ಯುಲೆನ್ಸ್:** 108 🚑
• **ವಿಪತ್ತು ನಿರ್ವಹಣೆ:** 1070 🌪️
• **ಮಹಿಳಾ ಸಹಾಯವಾಣಿ:** 1091 👩
• **ಮಕ್ಕಳ ಸಹಾಯವಾಣಿ:** 1098 👶
• **ಪ್ರವಾಸಿ ತುರ್ತು:** 1363 🧳

**ಹೆಚ್ಚುವರಿ ಸಂಪನ್ಮೂಲಗಳು:**
• **ರಕ್ತ ಬ್ಯಾಂಕ್:** 104
• **ವಿಷ ನಿಯಂತ್ರಣ:** 1066"""
        }
        
        # Initialize feedback storage
        self.feedback_file = "disaster_bot_feedback.csv"
        self.init_feedback_storage()
    
    def init_feedback_storage(self):
        """Initialize CSV file for feedback storage"""
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['timestamp', 'language', 'location', 'safety_status', 'govt_rating', 'feedback'])
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Simple translation using LibreTranslate"""
        if target_lang == "en":
            return text
        
        try:
            url = "https://libretranslate.de/translate"
            data = {
                "q": text,
                "source": "en",
                "target": target_lang,
                "format": "text"
            }
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                return response.json()["translatedText"]
        except:
            pass
        
        return text
    
    def get_weather(self, location: str) -> str:
        """Get current weather information"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description'].title()
                humidity = data['main']['humidity']
                feels_like = data['main']['feels_like']
                wind_speed = data['wind']['speed']
                
                return f"""🌤️ **Current Weather in {location}:**
                
**Temperature:** {temp}°C (Feels like {feels_like}°C)
**Condition:** {description}
**Humidity:** {humidity}%
**Wind Speed:** {wind_speed} m/s
                
*Last updated: {datetime.now().strftime('%I:%M %p')}*"""
        except Exception as e:
            return f"❌ Unable to fetch weather for {location}. Please check the location name."
    
    def get_disaster_advice(self, disaster_type: str, language: str) -> str:
        """Get disaster-specific advice from knowledge base"""
        disaster_type = disaster_type.lower()
        for key in self.knowledge_base:
            if key in disaster_type:
                return self.knowledge_base[key].get(language, self.knowledge_base[key]["en"])
        return None
    
    def use_granite_llm(self, prompt: str) -> str:
        """Use Granite LLM for technical/coding questions"""
        if not self.granite_llm:
            return None
        
        try:
            response = self.granite_llm(prompt, max_length=300, do_sample=True, temperature=0.7, pad_token_id=50256)
            return response[0]['generated_text'][len(prompt):].strip()
        except:
            return None
    
    def use_gemini(self, prompt: str) -> str:
        """Use Gemini for general questions"""
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I'm having trouble connecting to my knowledge base: {str(e)}"
    
    def get_ai_response(self, question: str, language: str) -> str:
        """Get AI response using RAG-like approach"""
        # Check knowledge base first
        disaster_advice = self.get_disaster_advice(question, language)
        if disaster_advice:
            return disaster_advice
        
        # For technical/coding questions, try Granite LLM
        if any(word in question.lower() for word in ['code', 'programming', 'technical', 'software', 'python', 'javascript']):
            granite_response = self.use_granite_llm(question)
            if granite_response:
                return f"🔧 **Technical Response:**\n\n{granite_response}"
        
        # Use Gemini for general questions
        prompt = f"""You are a helpful disaster response assistant. Answer this question briefly and helpfully: {question}
        
        Focus on:
        - Safety and emergency information
        - Practical, actionable advice
        - Keep response under 250 words
        - Use emojis where appropriate
        - Be supportive and reassuring
        """
        
        response = self.use_gemini(prompt)
        
        # Translate if needed
        if language != "en":
            response = self.translate_text(response, language)
        
        return response
    
    def save_feedback(self, safety_status: str, govt_rating: str, feedback: str, language: str, location: str):
        """Save user feedback to CSV"""
        with open(self.feedback_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().isoformat(),
                language,
                location,
                safety_status,
                govt_rating,
                feedback
            ])

# Initialize the bot
@st.cache_resource
def load_bot():
    return DisasterResponseBot()

def main():
    # Page configuration
    st.set_page_config(
        page_title="🚨 Disaster Response Bot",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4ecdc4;
        margin: 10px 0;
    }
    .emergency-number {
        background: #ffe6e6;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid red;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'bot' not in st.session_state:
        st.session_state.bot = load_bot()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    if 'location' not in st.session_state:
        st.session_state.location = ''
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    bot = st.session_state.bot
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🚨 Disaster Response Bot</h1>
        <p>Your AI-powered emergency assistant for safety and support</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    st.sidebar.header("⚙️ Settings")
    
    # Language selection
    selected_language = st.sidebar.selectbox(
        "🌍 Select Language",
        options=list(bot.languages.keys()),
        format_func=lambda x: f"{bot.languages[x]['flag']} {x}"
    )
    st.session_state.language = bot.languages[selected_language]['code']
    
    # Location input
    st.session_state.location = st.sidebar.text_input(
        "📍 Your Location/City",
        value=st.session_state.location,
        placeholder="Enter your city name"
    )
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 AI Assistant",
        "🌤️ Weather",
        "⚠️ Disaster Guide",
        "📞 Emergency",
        "📝 Feedback"
    ])
    
    # Tab 1: AI Assistant (Chat Interface)
    with tab1:
        st.header("💬 Chat with AI Assistant")
        
        # Chat container
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
                st.chat_message("user").write(user_msg)
                st.chat_message("assistant").write(bot_msg)
        
        # Chat input
        user_question = st.chat_input("Ask me anything about disasters, safety, or emergency preparedness...")
        
        if user_question:
            # Add user message to history
            st.session_state.chat_history.append((user_question, ""))
            
            # Display user message
            st.chat_message("user").write(user_question)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = bot.get_ai_response(user_question, st.session_state.language)
                st.write(response)
            
            # Update chat history
            st.session_state.chat_history[-1] = (user_question, response)
    
    # Tab 2: Weather Information
    with tab2:
        st.header("🌤️ Weather Information")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            weather_location = st.text_input(
                "Enter location for weather update:",
                value=st.session_state.location,
                placeholder="e.g., Bangalore, Mumbai, Delhi"
            )
        
        with col2:
            if st.button("🔄 Get Weather", type="primary"):
                if weather_location:
                    weather_info = bot.get_weather(weather_location)
                    st.markdown(weather_info)
                else:
                    st.warning("Please enter a location")
    
    # Tab 3: Disaster Guide
    with tab3:
        st.header("⚠️ Disaster Safety Guide")
        
        disaster_type = st.selectbox(
            "Select disaster type for safety information:",
            ["Select...", "Flood", "Earthquake", "Heatwave", "Cyclone"]
        )
        
        if disaster_type != "Select...":
            advice = bot.get_disaster_advice(disaster_type.lower(), st.session_state.language)
            if advice:
                st.markdown(f"""
                <div class="feature-card">
                {advice}
                </div>
                """, unsafe_allow_html=True)
        
        # Additional safety tips
        st.subheader("📋 General Emergency Preparedness")
        st.markdown("""
        - **Emergency Kit:** Water, non-perishable food, flashlight, battery radio
        - **Important Documents:** Keep copies in waterproof container
        - **Communication Plan:** Establish meeting points and contact methods
        - **Stay Informed:** Monitor weather alerts and emergency broadcasts
        - **First Aid:** Learn basic first aid and CPR
        """)
    
    # Tab 4: Emergency Contacts
    with tab4:
        st.header("📞 Emergency Contacts")
        
        contacts = bot.emergency_contacts.get(st.session_state.language, bot.emergency_contacts["en"])
        st.markdown(contacts)
        
        # Quick dial buttons
        st.subheader("🚨 Quick Dial")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚔 Police\n100", help="Call Police"):
                st.info("Dial 100 for Police emergency")
        
        with col2:
            if st.button("🚒 Fire\n101", help="Call Fire Brigade"):
                st.info("Dial 101 for Fire emergency")
        
        with col3:
            if st.button("🚑 Ambulance\n108", help="Call Ambulance"):
                st.info("Dial 108 for Medical emergency")
        
        with col4:
            if st.button("🌪️ Disaster\n1070", help="Call Disaster Management"):
                st.info("Dial 1070 for Disaster Management")
    
    # Tab 5: Safety Check & Feedback
    with tab5:
        st.header("📝 Safety Check & Feedback")
        
        with st.form("feedback_form"):
            st.subheader("Are you safe?")
            
            safety_status = st.radio(
                "Current safety status:",
                ["I am safe", "I need help", "Others need help", "Uncertain"]
            )
            
            govt_rating = st.slider(
                "Rate government response (1-5):",
                min_value=1,
                max_value=5,
                value=3
            )
            
            feedback_text = st.text_area(
                "Additional feedback or situation report:",
                placeholder="Describe the situation, needs, or any observations..."
            )
            
            if st.form_submit_button("📤 Submit Feedback", type="primary"):
                bot.save_feedback(
                    safety_status,
                    str(govt_rating),
                    feedback_text,
                    st.session_state.language,
                    st.session_state.location
                )
                st.success("✅ Feedback submitted successfully! Thank you for the information.")
        
        # Display feedback summary (if admin)
        if st.checkbox("🔍 View Feedback Summary (Admin)"):
            try:
                df = pd.read_csv(bot.feedback_file)
                if not df.empty:
                    st.subheader("📊 Feedback Analytics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Safety Status Distribution:**")
                        safety_counts = df['safety_status'].value_counts()
                        st.bar_chart(safety_counts)
                    
                    with col2:
                        st.write("**Government Rating Average:**")
                        avg_rating = df['govt_rating'].astype(float).mean()
                        st.metric("Average Rating", f"{avg_rating:.1f}/5")
                    
                    st.write("**Recent Feedback:**")
                    st.dataframe(df.tail(10), use_container_width=True)
                else:
                    st.info("No feedback data available yet.")
            except FileNotFoundError:
                st.info("No feedback data available yet.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚨 <strong>Disaster Response Bot</strong> | Stay Safe, Stay Informed</p>
        <p>For immediate emergencies, always call local emergency services first!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()