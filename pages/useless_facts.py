import streamlit as st
import requests

# Example URL containing JSON data
url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

# Fetch data from the URL
response = requests.get(url)

# Create button to request a new fact
if st.button('Display NEW Fact'):
    response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON data
    data = response.json()

    # Specify the key you want to display
    target_key = "text"  # Replace with your specific key

    # Get the value for the specified key
    value = data.get(target_key, 'Key not found')

    # Replace single quotes with double single quotes
    value_without_backticks = value.replace("`", "'")

    # Display the value for the specified key
    # st.write(f"## Displaying Data from a URL")
    st.markdown(f"{value_without_backticks}")

else:
    st.write(f"Failed to fetch data from the URL. Status code: {response.status_code}")
