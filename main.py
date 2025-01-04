import os
from geopy.geocoders import GoogleV3
from yelpapi import YelpAPI
import requests
import urllib3
import numpy as np
from dotenv import load_dotenv
load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

YELP_API_KEY = os.getenv('YELP_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def get_coordinates(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if not data.get('results'):
        raise ValueError(f"No results found for address: {address}")
    location = data['results'][0]['geometry']['location']
    return (location['lat'], location['lng'])


def weiszfeld_algorithm(coordinates_list):
    guess = np.mean(coordinates_list, axis=0)
    
    max_iterations = 100
    tolerance = 1e-6

    for iteration in range(max_iterations):
        distances = np.linalg.norm(coordinates_list - guess, axis=1)
        if np.any(distances == 0):
            return tuple(guess)
        
        weights = 1 / distances
        new_guess = np.sum(weights[:, np.newaxis] * coordinates_list, axis=0) / np.sum(weights)
        
        if np.linalg.norm(new_guess - guess) < tolerance:
            break

        guess = new_guess

    return tuple(guess)

def find_nearest_major_city(coordinates):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={','.join(map(str, coordinates))}&sensor=false&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    address_components = data['results'][0]['address_components']
    major_city = next((component['long_name'] for component in address_components if 'locality' in component['types']), None)
    return major_city


def get_yelp_recommendations(api_key, term, location):
    yelp_api = YelpAPI(api_key)
    search_results = yelp_api.search_query(term=term, location=location, limit=5)
    return search_results['businesses']


if __name__ == '__main__':
    addresses = []
    num_addresses = int(input("Enter the number of addresses: "))

    for i in range(num_addresses):
        address = input(f"Enter address {i + 1}: ")
        try:
            coordinates = get_coordinates(address)
            addresses.append(coordinates)
        except ValueError as e:
            print(e)
            print("Enter a valid address.")
            exit()
        except Exception as e:
            print(f"Error: {e}")
            exit()

    geometric_median = weiszfeld_algorithm(np.array(addresses))
    nearest_major_city = find_nearest_major_city(geometric_median)

    print(f"\nMeetup Location: {geometric_median}")
    print(f"Nearest Major City: {nearest_major_city}")
    
    try:
        yelp_results = get_yelp_recommendations(YELP_API_KEY, 'food', nearest_major_city)
        print("\nYelp Recommendations:")
        for result in yelp_results:
            print(f"{result['name']} - {result['rating']} stars")
    except Exception as e:
        print(f"An error occurred fetching Yelp recommendations: {e}")



def get_coordinates(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    location = data['results'][0]['geometry']['location']
    return (location['lat'], location['lng'])


def weiszfeld_algorithm(coordinates_list):
    guess = np.mean(coordinates_list, axis=0)
    max_iterations = 100
    tolerance = 1e-6
    for iteration in range(max_iterations):
        distances = np.linalg.norm(coordinates_list - guess, axis=1)
        weights = 1/distances
        new_guess = np.sum(weights[:, np.newaxis] * coordinates_list, axis=0) / np.sum(weights)
        if np.linalg.norm(new_guess - guess) < tolerance:
            break
        guess = new_guess
    return tuple(guess)


def find_nearest_major_city(coordinates):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={','.join(map(str, coordinates))}&sensor=false&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    address_components = data['results'][0]['address_components']
    major_city = next((component['long_name'] for component in address_components if 'locality' in component['types']), None)
    return major_city


def get_yelp_recommendations(api_key, term, location):
    yelp_api = YelpAPI(api_key)
    search_results = yelp_api.search_query(term=term, location=location, limit=5)
    return search_results['businesses']


if __name__ == '__main__':
    addresses = []
    num_addresses = int(input("Enter the number of addresses: "))

    for i in range(num_addresses):
        address = input(f"Enter address {i + 1}: ")
        addresses.append(get_coordinates(address))

    geometric_median = weiszfeld_algorithm(np.array(addresses))
    nearest_major_city = find_nearest_major_city(geometric_median)

    print(f"Geometric Median (Meetup Location): {geometric_median}")
    print(f"Nearest Major City: {nearest_major_city}")

    yelp_results = get_yelp_recommendations(YELP_API_KEY, 'food', nearest_major_city)
    print("\nYelp Recommendations:")
    for result in yelp_results:
        print(result['name'], "-", result['rating'])