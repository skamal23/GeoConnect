# GeoConnect
GeoConnect allows multiple users to find the optimal meeting location (geometric median) between several addresses using Google Maps API/Weiszfeld's Algorithm and suggests nearby places to eat or visit using Yelp's API. 

## Prerequisites
**Before running main.py, ensure you have:**
- A Google Maps API key
- A Yelp Fusion API key.

## Installation
1. **git clone https://github.com/skamal23/GeoConnect.git**
2. **Create a file named '.env' in the project directory**
    * touch .env
    * Add your API keys to the '.env' file:
          GOOGLE_MAPS_API_KEY=your_google_maps_api_key
          YELP_API_KEY=your_yelp_api_key

## Usage
1. Run python main.py
2. Enter the number of addresses
3. Input each address when prompted
4. View results, which includes:
    * The geometric median between the addresses.
    * The nearest major city.
    * Yelp food recommendations at the nearest major city.