import streamlit as st
from sqlalchemy import create_engine, text

conn = st.connection("postgresql", type="sql")
player = "11 - Micah Moo"
points_scored = 3
insert_query = text(f"INSERT INTO scoring (player, points_scored) VALUES (:player, :points_scored);")
if st.button("Triple!"):
    # with conn.session as session:
    #     session.execute(insert_query, {"player": player, "points_scored": points_scored})
    #     session.commit()

# import streamlit as st
# import psycopg2
# import sqlalchemy
# import toml
# 
# # Read database connection details from the .toml file
# config = toml.load(".streamlit/secrets.toml")
# connection_config = config.get("connections", {}).get("postgresql", {})
# 
# # Extract database parameters
# database_name = connection_config.get("database", "")
# user = connection_config.get("username", "")
# password = connection_config.get("password", "")
# host = connection_config.get("host", "")
# port = connection_config.get("port", "")
# 
# # Establish a connection to the PostgreSQL database
# conn = psycopg2.connect(
#     database=database_name,
#     user=user,
#     password=password,
#     host=host,
#     port=port
# )
# 
# # Display widgets for user input
# selected_jersey_number = st.selectbox("Select Jersey Number", [1, 2, 3])
# selected_full_name = st.text_input("Enter Full Name")
# 
# # Insert data into the database
# insert_query = f"INSERT INTO roster (jersey_number, full_name) VALUES ({selected_jersey_number}, '{selected_full_name}')"
# 
# # Execute the SQL query
# with conn.cursor() as cursor:
#     cursor.execute(insert_query)
# 
# # Commit the transaction
# conn.commit()
# 
# # Display a success message
# st.success("Data inserted successfully!")
# 
# # Close the connection (important!)
# conn.close()
