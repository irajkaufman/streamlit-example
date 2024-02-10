# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Function to authenticate with Google Sheets API
# def authenticate_gspread():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     credentials = ServiceAccountCredentials.from_json_keyfile_name("/Users/irajkaufman/Documents/Plus_Minus_Hoops_App/hoops-408623-3a75f7f7453b.json", scope)
#     return gspread.authorize(credentials)


# # Main Streamlit app
# def main():
#     if 'score' not in st.session_state:
#         st.session_state.score = 0

#     # st.write(st.session_state.score)
#     st.write('')
#     st.write('')

#     col1, col2, col3 = st.columns(3)

#     if col1.button('Free Throw'):
#         st.session_state.score += 1

#     if col2.button('Jumper'):
#         st.session_state.score += 2

#     if col3.button('Triple!'):
#         st.session_state.score += 3

#     st.write(st.session_state.score)

#     # score = 0
#     #
#     # st.write(score)
#     #
#     # if st.button('Scored'):
#     #     score += 1
#     #
#     # st.write(score)

#     st.title("Roster Dropdowns from G-Sheets")

#     # Authenticate with Google Sheets API
#     gc = authenticate_gspread()

#     # Replace "YourSheetName" with the actual name of your Google Sheet
#     sheet_name = "11/23/23 vs St. Patrick / St. Vincent"

#     # Open an existing Google Sheet
#     try:
#         sh = gc.open(sheet_name)
#     except gspread.SpreadsheetNotFound:
#         st.warning(f"Sheet '{sheet_name}' not found. Creating a new one.")
#         return

#     # List all worksheets in the Google Sheet
#     # worksheets = sh.worksheets()
#     # st.write("Available worksheets:", [ws.title for ws in worksheets])

#     # Replace "YourSheetTabName" with the actual name of your sheet
#     sheet_tab_name = "Roster"

#     # Select a worksheet by title (name)
#     try:
#         worksheet = sh.worksheet(sheet_tab_name)
#     except gspread.WorksheetNotFound:
#         st.warning(f"Worksheet '{sheet_tab_name}' not found.")
#         return

#     # Read data from Google Sheet
#     data = worksheet.col_values(1)  # Assuming data is in the first column

#     # Remove header if present
#     if data and data[0] == "Name":
#         data = data[1:]

#     # Create a Streamlit dropdown with the read data
#     selected_option1 = st.selectbox("Select 5 Players:", data)
#     selected_option2 = st.selectbox("", data)
#     selected_option3 = st.selectbox(" ", data)
#     selected_option4 = st.selectbox("  ", data)
#     selected_option5 = st.selectbox("   ", data)

#     st.write("")

#     # Display the selected option
#     st.write(f"Player 1: {selected_option1}")
#     st.write(f"Player 2: {selected_option2}")
#     st.write(f"Player 3: {selected_option3}")
#     st.write(f"Player 4: {selected_option4}")
#     st.write(f"Player 5: {selected_option5}")


# if __name__ == "__main__":
#     main()
