import streamlit as st
from sqlalchemy import create_engine, text

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# def score_insert(points_scored: int, team: str = 'Campo'):
#     """
#     Inserts 5 new records into the scoring table, per the points button that is clicked.
#
#     Takes the points made and applies them to the 5 players on the court at the time they were scored,
#     whether the home or away team scored them. If the home team scores, the person who scored is flagged
#     as the scorer. If the away team scores, the points inserted for the five players are negative,
#     such as -1, -2, -3
#
#     :param points_scored: 1 for a free throw, 2 for a jumper, 3 for a triple
#     :param team: home or away team name
#     :return: success or fail (of table insert)
#     """


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
    team = 'Campolindo'

    col1, col2, col3 = st.columns(3)

    st.title("Roster Dropdowns from Hoops DB")

    col4, col5 = st.columns(2)
    col6, col7 = st.columns(2)
    col8, col9 = st.columns(2)
    col10, col11 = st.columns(2)
    col12, col13 = st.columns(2)

    # Perform query.
    df = conn.query("SELECT jersey_number || ' - ' || full_name as player FROM roster;", ttl="10m")

    # Create a Streamlit dropdown with the read data
    selected_option1 = col4.selectbox("Select 5 Players:", df)
    scorer1 = col5.checkbox('Scored')
    selected_option2 = col6.selectbox("", df)
    scorer2 = col7.checkbox('')
    selected_option3 = col8.selectbox(" ", df)
    scorer3 = col9.checkbox(' ')
    selected_option4 = col10.selectbox("  ", df)
    scorer4 = col11.checkbox('  ')
    selected_option5 = col12.selectbox("   ", df)
    scorer5 = col13.checkbox('   ')

    insert_query1 = text(f"INSERT INTO scoring (player, points_scored, team, scorer) "
                         f"VALUES (:selected_option1, :current_shot, :team, :scorer1);")
    insert_query2 = text(f"INSERT INTO scoring (player, points_scored, team, scorer) "
                         f"VALUES (:selected_option2, :current_shot, :team, :scorer2);")
    insert_query3 = text(f"INSERT INTO scoring (player, points_scored, team, scorer) "
                         f"VALUES (:selected_option3, :current_shot, :team, :scorer3);")
    insert_query4 = text(f"INSERT INTO scoring (player, points_scored, team, scorer) "
                         f"VALUES (:selected_option4, :current_shot, :team, :scorer4);")
    insert_query5 = text(f"INSERT INTO scoring (player, points_scored, team, scorer) "
                         f"VALUES (:selected_option5, :current_shot, :team, :scorer5);")

    if col1.button('Free Throw'):
        current_shot = free_throw
        st.session_state.score += free_throw
        with conn.session as session:
            import ipdb
            ipdb.set_trace()
            # session.execute(insert_query1, {"player": selected_option1, "points_scored": current_shot,
            #                                 "team": team, "scorer": scorer1})
            session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                            "team": team, "scorer1": scorer1})
            session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                            "team": team, "scorer2": scorer2})
            session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                            "team": team, "scorer3": scorer3})
            session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                            "team": team, "scorer4": scorer4})
            session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                            "team": team, "scorer5": scorer5})
            session.commit()

    if col2.button('Jumper'):
        current_shot = jumper
        st.session_state.score += jumper
        with conn.session as session:
            session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                            "team": team, "scorer1": scorer1})
            session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                            "team": team, "scorer2": scorer2})
            session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                            "team": team, "scorer3": scorer3})
            session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                            "team": team, "scorer4": scorer4})
            session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                            "team": team, "scorer5": scorer5})
            session.commit()

    if col3.button('Triple!'):
        current_shot = triple
        st.session_state.score += triple
        with conn.session as session:
            session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                            "team": team, "scorer1": scorer1})
            session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                            "team": team, "scorer2": scorer2})
            session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                            "team": team, "scorer3": scorer3})
            session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                            "team": team, "scorer4": scorer4})
            session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                            "team": team, "scorer5": scorer5})
            session.commit()


if __name__ == "__main__":
    main()
