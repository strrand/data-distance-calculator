import streamlit as st
import googlemaps
import pandas as pd
from datetime import datetime

api_key = st.secrets['api_key'] #['my_secrets']

# Replace YOUR_API_KEY with your actual API key
gmaps = googlemaps.Client(key=api_key)

def filter_garage_list_by_car_model(excel_file_path, car_model):
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
        origin = f"{row['Adress']}"
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

# Set the theme configuration
#st.set_theme({'primaryColor': 'orange'})

#api_key = st.secrets['api_key']
# Add a title and some instructions
st.title("Distance Calculator Garages")
st.write("Enter the car model and current address below:")

# Use Streamlit text input widgets to get the car model and current address from the user
car_model = st.text_input("Car Model")
destination = st.text_input("Current Address")

# Use a Streamlit button to trigger the calculation
if st.button("Calculate Distance"):
    filtered_df = filter_garage_list_by_car_model('/home/strrand/code/strrand/data-distance-calculator/data/DAMAGE_GARAGE_LIST.xlsx', car_model)
    get_shortest_distances(filtered_df, destination)
