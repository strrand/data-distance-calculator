import streamlit as st
import googlemaps
import pandas as pd
from datetime import datetime
#from pathlib import Path
import os

excel_file_path = st.secrets['excel_path'] #['my_secrets']
#print(excel_file_path)

# Get the path of the directory where this script is located
#dirname = os.path.dirname(__file__)
#print(dirname)
# Define the relative path to the Excel file
#excel_file_path = os.path.join(dirname, "/home/strrand/code/strrand/data-distance-calculator/app/DAMAGE_GARAGE_LIST.xlsx")
#print(excel_file_path)
#pkl_path = Path(__file__).parents[1] / '/home/strrand/code/strrand/data-distance-calculator/data/DAMAGE_GARAGE_LIST.xlsx'

api_key = st.secrets['api_key'] #['my_secrets']

# Replace YOUR_API_KEY with your actual API key
gmaps = googlemaps.Client(key=api_key)

def filter_garage_list_by_car_model(excel_file_path, car_model):
    print("Excel file path:", excel_file_path)
    # read Excel file
    df = pd.read_excel(excel_file_path)

    # fill null values in the "Auktoriserade märken (OBS!)" column with "unknown"
    df['Auktoriserade märken (OBS!)'].fillna(value='unknown', inplace=True)

    # Convert car_model to lowercase
    car_model = car_model.lower()

    # Filter the rows where the specified car model is present in the "Auktoriserade märken (OBS!)" column
    filtered_df = df.loc[df["Auktoriserade märken (OBS!)"].str.lower().str.contains(fr"\b{car_model}\b", case=False, regex=True)]

    return filtered_df

def get_shortest_distances(filtered_df, destination):
    # Define an empty list to store the distances
    distances = []


    # Loop over the filtered addresses and get the distances
    for index, row in filtered_df.iterrows():
        # Get the origin and destination addresses
        origin = f"{row['Adress']}, {row['Ort / Stad']}"
        garage = f"{row['Verkstad']}"

        # Send a request to the API to get distance information
        now = datetime.now()
        directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=now)

        # Parse the response to extract the distance information
        distance = directions_result[0]['legs'][0]['distance']['text']

        # Add the distance to the list
        distances.append((origin, garage, distance))

    # Sort the distances in ascending order
    distances.sort(key=lambda x: x[2])

    # Display the top 3 shortest distances to the user
    st.write("The top 3 shortest garage distances are:")
    for i, (origin, garage, distance) in enumerate(distances[:3]):
        st.write(f"{i+1}. The distance between {garage}, {origin} and {destination} is {distance}")

# Set the page configuration
st.set_page_config(
    page_title="Preferred Garage Distance",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add the title and some instructions
col1, col2 = st.columns([2, 1])
with col1:
    st.title("Preferred Garage Distance")
with col2:
    st.image('https://ev-database.org/img/auto/Nissan_Leaf_2018/Nissan_Leaf_2018-01.jpg')

st.write("Enter the car model and current address below:")

# Use Streamlit text input widgets to get the car model and current address from the user
car_model = st.text_input("Car Model")
destination = st.text_input("Current Address")

# Use a Streamlit button to trigger the calculation
if st.button("Calculate Distance"):
    filtered_df = filter_garage_list_by_car_model(excel_file_path, car_model)
    get_shortest_distances(filtered_df, destination)
