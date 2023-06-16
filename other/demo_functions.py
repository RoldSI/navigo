import streamlit as st
import requests
import gmaps
import gmaps.datasets
from dotenv import dotenv_values
import pandas as pd
import numpy as np
import polyline
import folium
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app)
cors = CORS(app, origins='http://localhost:4200')


env_vars = dotenv_values("../.env")
GMAPS_KEY = env_vars["GMAPS_KEY"]
GRAPHHOPPER_API_KEY = env_vars["GRAPHHOPPER_API_KEY"]



def calculate_route_using_graphhopper(origin, destination, vehicle):
    url = f'https://graphhopper.com/api/1/route?point={origin["lat"]},{origin["lng"]}&point={destination["lat"]},{destination["lng"]}&vehicle={vehicle}&key={GRAPHHOPPER_API_KEY}'
    #  "https://graphhopper.com/api/1/route?point=51.131,12.414&point=48.224,3.867&profile=car&locale=de&calc_points=false&key=api_key"
    st.write(url)
    print(f"{url=}")
    response = requests.get(url)
    data = response.json()
    st.write(data)
    if 'paths' in data:
        route = data['paths'][0]['points']['coordinates']
        st.map(route)
    else:
        st.error('Unable to calculate the route.')

def calculate_route_gmaps(start, end, mode):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode={mode}&key={GMAPS_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        route = data["routes"][0]
        distance = route["legs"][0]["distance"]["text"]
        duration = route["legs"][0]["duration"]["text"]
        st.write(f"{route['copyrights']=}")
        

        polyline_points = route["overview_polyline"]["points"]
        decoded_points = polyline.decode(polyline_points)
        return decoded_points, data, distance, duration
    else:
        st.write("error")
        st.write(data)
        return None, data, None, None


def otherWorkingStuff():
   # if route_points:
    #     # Create folium map centered on the route
    #     route_map = folium.Map(location=route_points[0], zoom_start=13)

    #     # Create folium PolyLine from route points
    #     folium.PolyLine(route_points, color='blue', weight=2.5, opacity=1).add_to(route_map)

    #     # Add distance and duration as text annotations
    #     folium.Marker(location=route_points[0], popup=f"Distance: {distance}\nDuration: {duration}").add_to(route_map)

    #     # Display the map using Streamlit
    #     st.markdown(route_map._repr_html_(), unsafe_allow_html=True)
    # else:
    #     st.error("Unable to calculate the route.")



    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.map(df)

    origin_lat = st.number_input("Origin Latitude")
    origin_lng = st.number_input("Origin Longitude")
    destination_lat = st.number_input("Destination Latitude")
    destination_lng = st.number_input("Destination Longitude")

    origin = {'lat': origin_lat, 'lng': origin_lng}
    destination = {'lat': destination_lat, 'lng': destination_lng}

    vehicle = st.selectbox("Mode of Transport", ['car', 'bike', 'foot', 'bus', 'as_the_crow_flies'])

    if st.button("Calculate Route Using GraphHopper"):
        calculate_route_using_graphhopper(origin, destination, vehicle)
    
    # Use google maps api
    gmaps.configure(api_key=GMAPS_KEY) # Fill in with your API key
    # Get the dataset
    earthquake_df = gmaps.datasets.load_dataset_as_df('earthquakes')
    #Get the locations from the data set
    locations = earthquake_df[['latitude', 'longitude']]
    #Get the magnitude from the data
    weights = earthquake_df['magnitude']
    
    st.write(locations)
    st.write(weights)



    #Set up your map
    # fig = gmaps.figure()
    # fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
    # fig


def main():
    st.title("Route Calculator")
    # otherWorkingStuff()


    start = "Garching Forschungszentrum"
    end = "Munchen Hauptbahnhof"
    route_points, data, distance, duration = calculate_route_gmaps(start, end, "driving")

    if route_points:
        df_route = pd.DataFrame(route_points, columns=['LAT', 'LON'])

        st.map(df_route)
        st.write(f"Distance: {distance}")
        st.write(f"Duration: {duration}")
        with st.expander(f"Entire gmaps response"):
            st.write(f"{data=}", unsafe_allow_html=True)

    else:
        st.write(data)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from the backend api data hey!'}
    return jsonify(data)

@app.route('/', methods=['GET'])
def get_index():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)

 

if __name__ == "__main__":
    # main()
    app.run()
