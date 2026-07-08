import streamlit as st
from google import genai
from google.genai import types  # नवीन सुधारित लायब्ररी
from pydantic import BaseModel, Field
import sqlite3
import json
from datetime import datetime

# --- १. डेटाबेस सेट करणे (SQLite) ---
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_expense(amount, category, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('''
        INSERT INTO expenses (date, amount, category, description)
        VALUES (?, ?, ?, ?)
    ''', (current_date, amount, category, description))
    conn.commit()
    conn.close()

# ॲप सुरू होताच डेटाबेस तयार करणे
init_db()

# --- २. Gemini क्लायंट आणि Pydantic स्ट्रक्चर ---
# !!! तुमची API KEY इथे टाका !!!
client = genai.Client(api_key="os.getenv("MY_API_KEY")'" \
"")

class Expense(BaseModel):
    amount: float = Field(description="एकूण खर्च केलेली रक्कम संख्या स्वरूपात (उदा. 500)")
    category: str = Field(description="खर्चाची कॅटेगरी जसे की Food, Travel, Shopping, Medical")
    description: str = Field(description="खर्चाचे कारण किंवा वर्णन")

# --- ३. युझर इंटरफेस (UI) डिझाईन ---
st.set_page_config(page_title="AI Voice Expense Manager", page_icon="🎙️")
st.title("🎙️ AI Voice Expense Manager")
st.write("Gemini च्या मदतीने आवाज ओळखून हिशोब ठेवणारे स्मार्ट ॲप")

# --- ४. ऑडिओ इनपुट घटक (याला PyAudio ची गरज नाही) ---
st.markdown("### 🎙️ तुमचा खर्च रेकॉर्ड करा")
audio_value = st.audio_input("खालील बटणावर क्लिक करून बोला (उदा: 'पेट्रोलसाठी ३०० रुपये दिले')")

if audio_value is not None:
    with st.spinner("Gemini AI आवाज आणि डेटा प्रोसेस करत आहे..."):
        try:
            # ऑडिओ फाईलचे बाइट्स वाचणे
            audio_bytes = audio_value.read()
            
            # नवीन SDK नुसार ऑडिओ फाईल पॅक करणे
            audio_part = types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/wav"
            )
            
            prompt = "या ऑडिओ फाईलमधून खर्च (amount), कॅटेगरी (category) आणि कारण (description) शोधून काढा."
            
            # Gemini 2.5 Flash ला डेटा पाठवणे
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt, audio_part],
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    response_schema=Expense
                )
            )
            
            # आलेला JSON डेटा लोड करणे
            data = json.loads(response.text)
            
            # डेटाबेसमध्ये सेव्ह करणे
            save_expense(data['amount'], data['category'], data['description'])
            st.success(f"✅ खर्च यशस्वीरित्या सेव्ह झाला! (रक्कम: ₹{data['amount']}, कॅटेगरी: {data['category']})")
            
        except Exception as e:
            st.error(f"त्रुटी: {e}")

# --- ५. डॅशबोर्ड आणि ग्राफ विश्लेषण (Analytics) ---
st.markdown("---")
st.subheader("📊 तुमचा खर्च डॅशबोर्ड (Analytics)")

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("SELECT date, amount, category, description FROM expenses ORDER BY id DESC")
records = cursor.fetchall()
conn.close()

if records:
    # एकूण खर्च मोजणे
    total_expense = sum(row[1] for row in records)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="💰 एकूण खर्च", value=f"₹{total_expense:,.2f}")
    with col2:
        st.metric(label="📝 एकूण नोंदी", value=len(records))
        
    st.markdown("### 📈 कॅटेगरीनुसार खर्च")
    category_data = {}
    for row in records:
        cat = row[2]  # Category
        amt = row[1]  # Amount
        category_data[cat] = category_data.get(cat, 0) + amt
        
    # आलेख (Chart) दाखवणे
    st.bar_chart(category_data)
    
    st.markdown("### 📋 खर्चाचा इतिहास (History)")
    for row in records:
        st.write(f"📅 **{row[0]}** | 💰 ₹{row[1]} | 🗂️ {row[2]} | 📝 {row[3]}")
else:
    st.info("अद्याप कोणताही खर्च रेकॉर्ड केलेला नाही. वर आवाज रेकॉर्ड करून पहिली नोंद करा!")
