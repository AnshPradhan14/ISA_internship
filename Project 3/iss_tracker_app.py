# iss_tracker_app.py

# %% [markdown]
# # Python in Astronomy: Tracking the International Space Station (ISS) - Streamlit Dashboard
#
# This file consolidates the functionality developed in the Jupyter Notebook for a real-time Streamlit web application.
# It includes:
# - Fetching live TLE data for the ISS.
# - Detecting or allowing manual input for observer location.
# - Displaying the ISS's current live position on a map.
# - Predicting upcoming ISS passes over the observer's location.
# - Auto-updating the data periodically for a "real-time" experience.

# %% [python]
# --- Imports ---
import streamlit as st
import pandas as pd
import time
import requests
import pytz
from datetime import datetime, timedelta, timezone
from skyfield.api import load, EarthSatellite, Topos
import numpy as np # For np.degrees, np.pi
import json # Used for IP geolocation response handling

# --- Configuration and Global Variables ---
# Define the CelesTrak ISS TLE API endpoint
TLE_URL = "https://celestrak.org/NORAD/elements/stations.txt"
ISS_NORAD_ID = "25544" # NORAD ID for the International Space Station

# Define a fixed timezone for all local time displays (e.g., IST)
LOCAL_TIMEZONE = pytz.timezone('Asia/Kolkata') # Surat is in Asia/Kolkata

# --- Streamlit Page Setup ---
st.set_page_config(layout="wide", page_title="Real-Time ISS Tracker", page_icon="🛰️")

st.title("🛰️ Real-Time ISS Tracker")
st.markdown("Welcome to the **INDIA SPACE LAB Interns** ISS Tracking Dashboard!")
st.markdown("This application displays the International Space Station's current position and predicts its upcoming passes over your location.")

# --- Functions for Core Logic ---

@st.cache_data(ttl=3600) # Cache TLE data for 1 hour to avoid frequent API calls
def fetch_iss_tle():
    """
    Fetches the latest ISS TLE data from CelesTrak.
    This function is cached to prevent repeated network requests.
    """
    st.info("Fetching latest ISS TLE data...", icon="📡")
    try:
        response = requests.get(TLE_URL, timeout=10) # Set a timeout for the request
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        tle_data_text = response.text
        lines = tle_data_text.strip().splitlines()

        iss_tle_name = "INTERNATIONAL SPACE STATION (ISS)" # Default name for display
        iss_tle_line1 = None
        iss_tle_line2 = None

        found_iss = False
        for i in range(len(lines)):
            line_content = lines[i].strip()
            # TLE Line 1 always starts with '1' and contains the NORAD ID
            if line_content.startswith('1') and ISS_NORAD_ID in line_content:
                if i > 0 and i + 1 < len(lines):
                    iss_tle_name = lines[i-1].strip() # Name is on the line preceding Line 1
                    iss_tle_line1 = line_content
                    iss_tle_line2 = lines[i+1].strip()
                    found_iss = True
                    break
        
        if found_iss:
            # Basic validation: Check if lines start with '1' and '2' and have correct length (69 characters)
            if iss_tle_line1.startswith('1') and len(iss_tle_line1) == 69 and \
               iss_tle_line2.startswith('2') and len(iss_tle_line2) == 69:
                st.success(f"ISS TLE data fetched successfully for **{iss_tle_name}**!")
                return iss_tle_name, iss_tle_line1, iss_tle_line2
            else:
                st.warning("TLE data format might be incorrect based on starting characters or length. Attempting to proceed.")
                return iss_tle_name, iss_tle_line1, iss_tle_line2
        else:
            st.error(f"Error: ISS TLE (NORAD ID {ISS_NORAD_ID}) not found in the CelesTrak data.")
            return None, None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch TLE data: {e}. Please check your internet connection or the TLE source.")
        return None, None, None
    except Exception as e:
        st.error(f"An unexpected error occurred during TLE processing: {e}")
        return None, None, None

@st.cache_resource # Cache Skyfield timescale and satellite object
def initialize_skyfield_objects(tle_name, tle_line1, tle_line2):
    """Initializes Skyfield timescale and EarthSatellite object from TLE data."""
    try:
        ts = load.timescale() # Load Skyfield's timescale
        station = EarthSatellite(tle_line1, tle_line2, tle_name, ts) # Create EarthSatellite object
        return ts, station
    except Exception as e:
        st.error(f"Error initializing Skyfield objects: {e}. Please ensure valid TLE data.")
        return None, None

def get_observer_location():
    """
    Attempts to get observer location via IP geolocation and provides manual input.
    Uses Streamlit widgets for user interaction.
    """
    st.sidebar.subheader("Your Location (Observer)")
    latitude = None
    longitude = None
    city_name = "Unknown Location"

    # Attempt IP geolocation
    st.sidebar.info("Attempting to get your approximate location via IP address...", icon="📍")
    try:
        ip_api_url = "http://ip-api.com/json"
        geo_response = requests.get(ip_api_url, timeout=5) # Set a timeout
        geo_response.raise_for_status() # Raise an exception for HTTP errors
        geo_data = geo_response.json()

        if geo_data.get('status') == 'success':
            latitude = geo_data['lat']
            longitude = geo_data['lon']
            city_name = geo_data.get('city', 'Unknown City')
            region_name = geo_data.get('regionName', '')
            country_name = geo_data.get('country', '')
            
            st.sidebar.success(f"Detected: **{city_name}, {region_name}, {country_name}**")
            st.sidebar.caption(f"Lat: {latitude:.4f}, Lon: {longitude:.4f}")
            st.sidebar.warning("Note: IP-based geolocation might not be perfectly accurate.")
        else:
            st.sidebar.warning(f"IP geolocation failed: {geo_data.get('message', 'Unknown error')}. Please enter manually.")
    except requests.exceptions.RequestException as e:
        st.sidebar.warning(f"Could not connect to IP geolocation service: {e}. Please enter manually.")
    except json.JSONDecodeError:
        st.sidebar.warning(f"Could not parse IP geolocation response. Please enter manually.")
    except Exception as e:
        st.sidebar.warning(f"An unexpected error occurred during IP geolocation: {e}. Please enter manually.")

    # Manual override/input in sidebar
    with st.sidebar.expander("Manually Enter/Adjust Location"):
        # Default to Surat, Gujarat, India if IP failed
        default_lat = latitude if latitude is not None else 21.1702
        default_lon = longitude if longitude is not None else 72.8311

        manual_latitude = st.number_input("Latitude (°N):", value=default_lat, format="%.4f", min_value=-90.0, max_value=90.0, key="manual_lat")
        manual_longitude = st.number_input("Longitude (°E):", value=default_lon, format="%.4f", min_value=-180.0, max_value=180.0, key="manual_lon")
        manual_elevation = st.number_input("Elevation (meters):", value=0.0, format="%.1f", min_value=-500.0, max_value=9000.0, key="manual_elev")
    
    # Create Topos object for observer
    observer = Topos(latitude_degrees=manual_latitude, longitude_degrees=manual_longitude, elevation_m=manual_elevation)
    return observer, manual_latitude, manual_longitude # Return the Topos object and the exact lat/lon used

def calculate_iss_passes(observer, station, ts):
    """Calculates upcoming ISS passes for a given observer for the next 7 days."""
    t0 = ts.now() # Current time
    t1 = ts.utc(t0.utc.year, t0.utc.month, t0.utc.day + 7) # 7 days from now

    # Find events where ISS is above 10 degrees altitude for observer
    t, events = station.find_events(observer, t0, t1, altitude_degrees=10)

    event_names = ['Rise', 'Culmination', 'Set']
    passes_data = []
    current_pass_info = {}
    pass_counter = 0

    for ti, event in zip(t, events):
        event_name = event_names[event]
        dt_utc = ti.utc_datetime()
        dt_local = dt_utc.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIMEZONE) # Convert to local timezone

        if event_name == 'Rise':
            current_pass_info = {'Pass #': 0, 'Rise Time (IST)': dt_local, 'rise_skyfield_time': ti}
        elif event_name == 'Culmination' and current_pass_info:
            current_pass_info['Peak Time (IST)'] = dt_local
            current_pass_info['peak_skyfield_time'] = ti
            alt, az, distance = (station - observer).at(ti).altaz() # Calculate altitude at culmination
            current_pass_info['Peak Elev. (deg)'] = alt.degrees
        elif event_name == 'Set' and current_pass_info and 'Rise Time (IST)' in current_pass_info:
            current_pass_info['Set Time (IST)'] = dt_local
            current_pass_info['set_skyfield_time'] = ti
            duration_seconds = (current_pass_info['Set Time (IST)'] - current_pass_info['Rise Time (IST)']).total_seconds()
            current_pass_info['Duration (min)'] = duration_seconds / 60
            
            pass_counter += 1
            current_pass_info['Pass #'] = pass_counter
            
            passes_data.append(current_pass_info)
            current_pass_info = {} # Reset for next pass
    
    # Format datetimes and floats for display in DataFrame
    for p in passes_data:
        if 'Rise Time (IST)' in p: p['Rise Time (IST)'] = p['Rise Time (IST)'].strftime('%Y-%m-%d %H:%M:%S')
        if 'Peak Time (IST)' in p: p['Peak Time (IST)'] = p['Peak Time (IST)'].strftime('%Y-%m-%d %H:%M:%S')
        if 'Set Time (IST)' in p: p['Set Time (IST)'] = p['Set Time (IST)'].strftime('%Y-%m-%d %H:%M:%S')
        if 'Duration (min)' in p: p['Duration (min)'] = f"{p['Duration (min)']:.2f}"
        if 'Peak Elev. (deg)' in p: p['Peak Elev. (deg)'] = f"{p['Peak Elev. (deg)']:.2f}"

    return passes_data

# --- Main Application Logic ---

# Fetch TLE data once at the start of the app (cached)
iss_tle_name, iss_tle_line1, iss_tle_line2 = fetch_iss_tle()

if iss_tle_line1 and iss_tle_line2:
    # Initialize Skyfield objects once (cached)
    ts, station = initialize_skyfield_objects(iss_tle_name, iss_tle_line1, iss_tle_line2)

    if ts and station:
        # Get observer location (interactive input in sidebar)
        observer, obs_lat, obs_lon = get_observer_location()

        st.subheader("Live ISS Tracking")

        # Create placeholders for real-time map and data
        # This allows us to update parts of the page without re-running the whole script
        map_col, data_col = st.columns([2, 1]) # Divide layout for map and text data
        
        pass_table_placeholder = st.empty() # Placeholder for the passes table
        
        # Real-time update loop
        while True:
            current_time_local_str = datetime.now(LOCAL_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z%z')
            
            with data_col: # Current ISS data in the right column
                st.markdown(f"**Last Updated:** {current_time_local_str}")
                
                # Get current ISS position
                t_now = ts.now()
                current_iss_pos_at_tnow = station.at(t_now)
                current_iss_subpoint = current_iss_pos_at_tnow.subpoint() # Get geographical subpoint
                current_iss_lat = current_iss_subpoint.latitude.degrees
                current_iss_lon = current_iss_subpoint.longitude.degrees
                current_iss_alt_km = current_iss_subpoint.elevation.km # Altitude above ellipsoid

                st.metric(label="ISS Latitude", value=f"{current_iss_lat:.2f}°")
                st.metric(label="ISS Longitude", value=f"{current_iss_lon:.2f}°")
                st.metric(label="ISS Altitude", value=f"{current_iss_alt_km:.1f} km")

            with map_col: # Map in the left column
                # Prepare data for st.map
                map_data = pd.DataFrame([
                    {'lat': current_iss_lat, 'lon': current_iss_lon, 'name': 'ISS'},
                    {'lat': obs_lat, 'lon': obs_lon, 'name': 'You'}
                ])
                
                # Streamlit's built-in map. Set initial view centered between ISS and observer.
                avg_lat = (current_iss_lat + obs_lat) / 2
                avg_lon = (current_iss_lon + obs_lon) / 2
                
                st.map(map_data, zoom=1) # Adjust zoom as needed. st.map handles automatic recentering.

            with pass_table_placeholder: # Passes table below the map and data
                st.subheader(f"Upcoming ISS Passes for Your Location (Next 7 Days, IST)")
                passes = calculate_iss_passes(observer, station, ts) # Recalculate passes
                if passes:
                    df_passes = pd.DataFrame(passes)
                    # Drop skyfield time columns as they are not for display
                    df_passes = df_passes.drop(columns=['rise_skyfield_time', 'peak_skyfield_time', 'set_skyfield_time'], errors='ignore')
                    st.dataframe(df_passes, use_container_width=True) # Display as interactive table
                else:
                    st.info("No upcoming ISS passes found above 10 degrees elevation in the next 7 days for your location.")

            time.sleep(10) # Update every 10 seconds
    else:
        st.error("Skyfield initialization failed. Cannot proceed with tracking.")
else:
    st.error("Failed to fetch valid ISS TLE data. Cannot start the tracker.")