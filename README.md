# 🌙 Ramadan Prayer Times App

A beautiful, mobile-friendly Streamlit application that displays accurate prayer times for Ramadan based on your location.

## Features

- 📍 Location-based prayer times using city/state input
- 🕌 Display of all daily prayer times with beautiful UI
- 🌅 Highlighted Suhoor (end time) and Iftar (break fast time)
- ⏳ Real-time countdown to the next prayer
- 📱 Responsive design that works on desktop and mobile devices
- 🌐 Support for multiple calculation methods from Islamic authorities

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Enter your location (city, state/country) in the sidebar

4. Click "Update Prayer Times" to fetch the prayer times for your location

## APIs Used

- [AlAdhan API](https://aladhan.com/prayer-times-api) - For prayer times calculation
- [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) - For geocoding location names to coordinates

## Customization

You can customize the calculation method for prayer times by selecting from the dropdown menu in the sidebar:
- Islamic Society of North America
- University of Islamic Sciences, Karachi
- Muslim World League
- Umm Al-Qura University, Makkah

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- Icons provided by [Icons8](https://icons8.com/)
- Built with [Streamlit](https://streamlit.io/) 