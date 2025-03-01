import streamlit as st
import requests
import datetime
from datetime import timedelta
import time

# Set page configuration with wider layout and custom theme
st.set_page_config(
    page_title="Ramadan Times",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with dark mode support
def local_css():
    st.markdown("""
    <style>
        /* CSS Variables for Light/Dark Mode */
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #ecf0f1;
            --text-primary: #2c3e50;
            --text-secondary: #34495e;
            --text-muted: #7f8c8d;
            --border-primary: #ecf0f1;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --suhoor-bg: #f5eef8;
            --suhoor-border: #9b59b6;
            --iftar-bg: #fef5ec;
            --iftar-border: #e67e22;
            --prayer-border: #3498db;
            --button-bg: #3498db;
            --button-hover: #2980b9;
        }
        
        /* Dark mode variables */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #1e1e1e;
                --bg-secondary: #2d3436;
                --bg-tertiary: #2c3e50;
                --text-primary: #ecf0f1;
                --text-secondary: #bdc3c7;
                --text-muted: #95a5a6;
                --border-primary: #34495e;
                --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                --suhoor-bg: #2c2440;
                --suhoor-border: #9b59b6;
                --iftar-bg: #3d2c17;
                --iftar-border: #e67e22;
                --prayer-border: #3498db;
                --button-bg: #2980b9;
                --button-hover: #3498db;
            }
            
            /* Override Streamlit's default dark mode styles */
            .stApp {
                background-color: var(--bg-primary);
            }
            
            .css-1d391kg, .css-12oz5g7 {
                background-color: var(--bg-primary);
            }
        }
        
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Header styling */
        h1 {
            color: var(--text-primary);
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        
        h2, h3 {
            color: var(--text-secondary);
            font-weight: 600;
        }
        
        /* Card styling */
        .css-1r6slb0, .css-keje6w {
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            padding: 1.5rem;
            margin-bottom: 1rem;
            background-color: var(--bg-primary);
        }
        
        /* Prayer time cards */
        .prayer-card {
            background-color: var(--bg-secondary);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            border-left: 4px solid var(--prayer-border);
            transition: transform 0.2s;
        }
        
        .prayer-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--card-shadow);
        }
        
        /* Special prayer highlights */
        .suhoor-card {
            border-left: 4px solid var(--suhoor-border);
            background-color: var(--suhoor-bg);
        }
        
        .iftar-card {
            border-left: 4px solid var(--iftar-border);
            background-color: var(--iftar-bg);
        }
        
        /* Countdown styling */
        .countdown {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text-primary);
            background-color: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1.5rem 0;
        }
        
        /* Responsive adjustments for mobile */
        @media (max-width: 768px) {
            .prayer-card {
                padding: 0.8rem;
                margin-bottom: 0.6rem;
            }
            
            .countdown {
                font-size: 1rem;
                padding: 0.8rem;
            }
        }
        
        /* Footer styling */
        footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-primary);
            color: var(--text-muted);
            font-size: 0.8rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-12oz5g7 {
            padding: 2rem 1rem;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            background-color: var(--button-bg);
            color: white;
            font-weight: 600;
        }
        
        .stButton>button:hover {
            background-color: var(--button-hover);
        }
        
        /* Links styling */
        a {
            color: var(--prayer-border);
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Text color adjustments for readability */
        p {
            color: var(--text-secondary);
        }
        
        .stTextInput>div>div>input {
            color: var(--text-primary);
            background-color: var(--bg-secondary);
        }
        
        .stSelectbox>div>div>div {
            color: var(--text-primary);
            background-color: var(--bg-secondary);
        }
    </style>
    """, unsafe_allow_html=True)

# Function to convert location name to coordinates using Nominatim API
def geocode_location(location_name):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
        headers = {'User-Agent': 'RamadanTimesApp/1.0'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data and len(data) > 0:
            lat = data[0]['lat']
            lon = data[0]['lon']
            display_name = data[0]['display_name']
            return float(lat), float(lon), display_name
        else:
            return None, None, None
    except Exception as e:
        st.error(f"Error geocoding location: {e}")
        return None, None, None

# Function to fetch prayer times from AlAdhan API
def fetch_prayer_times(lat, lon, method=2):
    today = datetime.date.today().strftime("%d-%m-%Y")
    url = f"http://api.aladhan.com/v1/timings/{today}?latitude={lat}&longitude={lon}&method={method}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["code"] == 200:
            return data["data"]
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Format time to 12-hour format
def format_time(time_str):
    time_obj = datetime.datetime.strptime(time_str, '%H:%M')
    return time_obj.strftime('%I:%M %p')

# Apply custom CSS
local_css()

# App title with emoji
st.markdown("<h1 style='text-align: center; color: var(--text-primary);'>🌙 Ramadan Prayer Times</h1>", unsafe_allow_html=True)

# Create a container for the main content
main_container = st.container()

# Sidebar for location input
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: var(--text-primary);'>📍 Your Location</h3>", unsafe_allow_html=True)
    
    location = st.text_input("Enter City, State/Country", "Douglasville, GA")
    
    st.markdown("<h3 style='text-align: center; color: var(--text-primary);'>⚙️ Settings</h3>", unsafe_allow_html=True)
    
    method = st.selectbox("Calculation Method", options=[
        (2, "Islamic Society of North America"),
        (1, "University of Islamic Sciences, Karachi"),
        (3, "Muslim World League"),
        (4, "Umm Al-Qura University, Makkah")
    ], format_func=lambda x: x[1])[0]
    
    fetch_clicked = st.button("Update Prayer Times")
    
    st.markdown("""
    <div style='margin-top: 2rem; padding: 1rem; background-color: var(--bg-secondary); border-radius: 10px;'>
        <h4 style='text-align: center; margin-bottom: 0.5rem; color: var(--text-primary);'>About</h4>
        <p style='font-size: 0.9rem; color: var(--text-muted);'>
            This app provides accurate prayer times for Ramadan based on your location.
            Times are calculated using established methods from Islamic authorities.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state to track if we need to fetch data
if 'timings' not in st.session_state:
    st.session_state.timings = None
if 'location_details' not in st.session_state:
    st.session_state.location_details = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None

# Auto-fetch on load or when button is clicked
if fetch_clicked or st.session_state.timings is None:
    with st.spinner("Finding location and fetching prayer timings..."):
        # First geocode the location
        lat, lon, display_name = geocode_location(location)
        
        if lat is not None and lon is not None:
            st.session_state.location_details = {
                "latitude": lat,
                "longitude": lon,
                "display_name": display_name
            }
            # Then fetch prayer times
            st.session_state.timings = fetch_prayer_times(lat, lon, method)
            st.session_state.last_update = datetime.datetime.now()
        else:
            st.error(f"Could not find coordinates for '{location}'. Please try a different location.")
            st.session_state.timings = None

# Display prayer times if available
with main_container:
    if st.session_state.timings and st.session_state.location_details:
        timings = st.session_state.timings
        location_details = st.session_state.location_details
        
        date_readable = timings['date']['readable']
        hijri_date = timings['date']['hijri']['date']
        hijri_month = timings['date']['hijri']['month']['en']
        hijri_year = timings['date']['hijri']['year']

        # Create two columns for the header information
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div style='background-color: var(--bg-secondary); padding: 1rem; border-radius: 10px; text-align: center;'>
                <h3 style='margin-bottom: 0.5rem;'>🗓️ {date_readable}</h3>
                <p style='color: var(--text-muted);'>{hijri_date} | {hijri_month} {hijri_year} Hijri</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style='background-color: var(--bg-secondary); padding: 1rem; border-radius: 10px; text-align: center;'>
                <h3 style='margin-bottom: 0.5rem;'>📍 Location</h3>
                <p style='color: var(--text-muted);'>{location_details['display_name']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Highlight Suhoor (Fajr) and Iftar (Maghrib) in a special section
        st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>🌅 Suhoor & Iftar Times</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div class='prayer-card suhoor-card' style='text-align: center;'>
                <h3 style='margin-bottom: 0.5rem;'>Suhoor Ends</h3>
                <p style='font-size: 1.5rem; font-weight: 700; color: var(--text-primary);'>{format_time(timings['timings']['Fajr'])}</p>
                <p style='color: var(--text-muted); font-size: 0.9rem;'>Stop eating before Fajr prayer</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class='prayer-card iftar-card' style='text-align: center;'>
                <h3 style='margin-bottom: 0.5rem;'>Iftar Time</h3>
                <p style='font-size: 1.5rem; font-weight: 700; color: var(--text-primary);'>{format_time(timings['timings']['Maghrib'])}</p>
                <p style='color: var(--text-muted); font-size: 0.9rem;'>Break your fast at Maghrib prayer</p>
            </div>
            """, unsafe_allow_html=True)

        # All prayer times in a clean layout
        st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>🕌 Today's Prayer Times</h2>", unsafe_allow_html=True)
        
        # Create a 3-column layout for prayer times
        cols = st.columns(3)
        
        # Define all prayer times with icons
        prayer_times = [
            ('Fajr', '🌅', timings['timings']['Fajr']),
            ('Sunrise', '☀️', timings['timings']['Sunrise']),
            ('Dhuhr', '🌞', timings['timings']['Dhuhr']),
            ('Asr', '🌇', timings['timings']['Asr']),
            ('Maghrib', '🌆', timings['timings']['Maghrib']),
            ('Isha', '🌃', timings['timings']['Isha']),
        ]
        
        # Display prayer times in columns
        for i, (prayer, icon, time) in enumerate(prayer_times):
            col_index = i % 3
            with cols[col_index]:
                st.markdown(f"""
                <div class='prayer-card' style='text-align: center;'>
                    <h3 style='margin-bottom: 0.5rem;'>{icon} {prayer}</h3>
                    <p style='font-size: 1.2rem; font-weight: 600; color: var(--text-primary);'>{format_time(time)}</p>
                </div>
                """, unsafe_allow_html=True)

        # Countdown to next prayer
        current_time = datetime.datetime.now()
        next_prayer, next_prayer_time, next_prayer_icon = None, None, None
        
        for prayer, icon, time in prayer_times:
            prayer_time_today = datetime.datetime.strptime(time, '%H:%M')
            prayer_datetime = current_time.replace(hour=prayer_time_today.hour, minute=prayer_time_today.minute, second=0, microsecond=0)
            if prayer_datetime > current_time:
                next_prayer = prayer
                next_prayer_time = prayer_datetime
                next_prayer_icon = icon
                break
        
        if next_prayer:
            diff = next_prayer_time - current_time
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            st.markdown(f"""
            <div class='countdown'>
                <p style='color: var(--text-secondary);'>⏳ Next Prayer: {next_prayer_icon} {next_prayer} in</p>
                <h2 style='color: var(--text-primary);'>{hours:02d}:{minutes:02d}:{seconds:02d}</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='countdown' style='background-color: var(--bg-tertiary);'>
                <p style='color: var(--text-secondary);'>🎉 All prayers completed for today!</p>
                <p style='color: var(--text-secondary);'>Check back tomorrow for new prayer times.</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Last updated info
        if st.session_state.last_update:
            st.markdown(f"""
            <p style='text-align: center; color: var(--text-muted); font-size: 0.8rem;'>
                Last updated: {st.session_state.last_update.strftime('%I:%M %p')}
            </p>
            """, unsafe_allow_html=True)

    elif st.session_state.timings is None and not fetch_clicked:
        st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem; background-color: var(--bg-secondary); border-radius: 10px; margin: 2rem 0;'>
            <h2 style='margin-bottom: 1rem; color: var(--text-primary);'>Welcome to Ramadan Prayer Times</h2>
            <p style='color: var(--text-muted); margin-bottom: 2rem;'>Enter your location in the sidebar and click 'Update Prayer Times' to get started.</p>
            <img src="https://img.icons8.com/fluency/96/000000/mosque.png" style='margin-bottom: 1rem;'>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<footer>
    <p style='text-align: center;'>
        Prayer times provided by <a href="https://aladhan.com/prayer-times-api" target="_blank">AlAdhan API</a> | 
        Geocoding by <a href="https://nominatim.openstreetmap.org/" target="_blank">OpenStreetMap Nominatim</a>
    </p>
    <p style='text-align: center;'>
        Made with ❤️ for Ramadan
    </p>
</footer>
""", unsafe_allow_html=True)
