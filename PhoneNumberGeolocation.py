import phonenumbers
import folium
import sys
import os
from phonenumbers import geocoder, timezone, carrier
from colorama import init, Fore
from opencage.geocoder import OpenCageGeocode

init()

def process_number(number):
    try:
        global location
        parsed_number = phonenumbers.parse(number)
        print(f"{Fore.GREEN}[+] Attempting to track location of "
              f"{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}..")
        print(f"{Fore.GREEN}[+] Time Zone ID: {timezone.time_zones_for_number(parsed_number)}")
        
     
        location = geocoder.description_for_number(parsed_number, "en")
        if location:
            print(f"{Fore.GREEN}[+] Region: {location}")
        else:
            print(f"{Fore.RED}[-] Region: Unknown")
        
        carrier_name = carrier.name_for_number(parsed_number, 'en')
        if carrier_name:
            print(f"{Fore.GREEN}[+] Service Provider:  {carrier_name}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        sys.exit()

def get_approx_coordinates():
    global latitude, longitude
    try:
        # Using OpenCage API to get coordinates
        coder = OpenCageGeocode("use your own API key from OpenCage")  
        results = coder.geocode(location)
        if results:
            latitude = results[0]['geometry']['lat']
            longitude = results[0]['geometry']['lng']
            print(f"[+] Latitude: {latitude}, Longitude: {longitude}")
            address = coder.reverse_geocode(latitude, longitude)
            if address:
                print(f"{Fore.GREEN}[+] Approximate Location is {address[0]['formatted']}")
            else:
                print(f"{Fore.RED}[-] No address found for the given coordinates.")
        else:
            print(f"{Fore.RED}[-] No location data found.")
            sys.exit()
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        sys.exit()

def clean_phone_number(phone_number):
    return ''.join(char for char in phone_number if char.isdigit() or char == '+') or "unknown"

def draw_map():
    try:
        my_map = folium.Map(location=[latitude, longitude], zoom_start=9)
        folium.Marker([latitude, longitude], popup=location).add_to(my_map)
        file_name = f"{clean_phone_number(phone_number)}.html"
        my_map.save(file_name)
        print(f"[+] See Aerial Coverage at: {os.path.abspath(file_name)}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")

def get_user_input():
   
    phone_number = input("Please enter the phone number (include country code, e.g. +1234567890): ")
    return phone_number

if __name__ == "__main__":
    phone_number = get_user_input()
    process_number(phone_number)
    get_approx_coordinates()
    draw_map()
