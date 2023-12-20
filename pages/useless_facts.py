import streamlit as st
import requests

# Example URL containing JSON data
url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

# Fetch data from the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON data
    data = response.json()

    # Specify the key you want to display
    target_key = "text"  # Replace with your specific key

    # Display the value for the specified key
    # st.write(f"## Displaying Data from a URL")
    st.write(f"{data.get(target_key, 'Key not found')}")

else:
    st.write(f"Failed to fetch data from the URL. Status code: {response.status_code}")
