import streamlit as st
# import psycopg2
import sqlalchemy

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query("SELECT jersey_number || ' - ' || full_name as player FROM roster;", ttl="10m")

# Print results.
# for row in df.itertuples():
#     st.write(f"{row.number}: {row.name}")


# Main Streamlit app
def main():
    if 'score' not in st.session_state:
        st.session_state.score = 0

    # st.write(st.session_state.score)
    st.write('')
    st.write('')

    free_throw = 1
    jumper = 2
    triple = 3
    current_shot = 0

    col1, col2, col3 = st.columns(3)

    if col1.button('Free Throw'):
        current_shot = free_throw
        st.session_state.score += free_throw

    if col2.button('Jumper'):
        current_shot = jumper
        st.session_state.score += jumper

    if col3.button('Triple!'):
        current_shot = triple
        st.session_state.score += triple

    st.title("Roster Dropdowns from hoops database")

    # Create a Streamlit dropdown with the read data
    selected_option1 = st.selectbox("Select 5 Players:", df)
    selected_option2 = st.selectbox("", df)
    selected_option3 = st.selectbox(" ", df)
    selected_option4 = st.selectbox("  ", df)
    selected_option5 = st.selectbox("   ", df)

    scorer1 = st.checkbox('Player 1 Scored')
    scorer2 = st.checkbox('Player 2 Scored')
    scorer3 = st.checkbox('Player 3 Scored')
    scorer4 = st.checkbox('Player 4 Scored')
    scorer5 = st.checkbox('Player 5 Scored')

    st.write("")

    # SQL INSERT statement
    insert_query = "INSERT INTO scoring (player, points_scored, scorer) VALUES (%s, %s, %s);"

    # Data to be inserted
    data_to_insert = (selected_option1, current_shot, scorer1)

    ins = conn.query(insert_query, data_to_insert)
    

    # Execute the INSERT statement
    st.sql(insert_query, data_to_insert)

    # Commit the transaction
    conn.commit()

    st.success("Data inserted successfully!")

    # Display the selected option
    st.write(f"Player 1:  {selected_option1}")
    st.write(f"Player 2:  {selected_option2}")
    st.write(f"Player 3:  {selected_option3}")
    st.write(f"Player 4:  {selected_option4}")
    st.write(f"Player 5:  {selected_option5}")


if __name__ == "__main__":
    main()
