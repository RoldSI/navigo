import streamlit as st
import requests

GRAPHHOPPER_API_KEY = 'PUT_HERE'

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

def main():
    st.title("Route Calculator")

    origin_lat = st.number_input("Origin Latitude")
    origin_lng = st.number_input("Origin Longitude")
    destination_lat = st.number_input("Destination Latitude")
    destination_lng = st.number_input("Destination Longitude")

    origin = {'lat': origin_lat, 'lng': origin_lng}
    destination = {'lat': destination_lat, 'lng': destination_lng}

    vehicle = st.selectbox("Mode of Transport", ['car', 'bike', 'foot', 'bus', 'as_the_crow_flies'])

    if st.button("Calculate Route"):
        calculate_route_using_graphhopper(origin, destination, vehicle)


if __name__ == "__main__":
    main()
