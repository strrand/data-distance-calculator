import streamlit as st
import googlemaps
from datetime import datetime

# Replace YOUR_API_KEY with your actual API key
gmaps = googlemaps.Client(key='AIzaSyDfAsXwd2-eoRG121tgo766uqkuToEBpBc')

# Add a title and some instructions
st.title("Distance Calculator")
st.write("Enter the origin and destination addresses below:")

# Use Streamlit text input widgets to get the origin and destination addresses from the user
origin = st.text_input("Origin")
destination = st.text_input("Destination")

# Use a Streamlit button to trigger the calculation
if st.button("Calculate Distance"):
    # Use the Google Maps Directions API to get the distance between the two addresses
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())

    # Extract the distance from the result
    distance = directions_result[0]['legs'][0]['distance']['value']
    distance_in_km = distance / 1000

    # Display the result to the user
    st.write(f"The distance between {origin} and {destination} is {distance_in_km:.2f} km.")
