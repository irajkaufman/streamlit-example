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

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "collapsed"
        st.session_state.disabled = False

    free_throw = 1
    jumper = 2
    triple = 3
    current_shot = 0
    team = 'Campolindo'

    col1, col2, col3 = st.columns(3)

    st.title("Roster Dropdowns from Hoops DB")

    col4, col5, col3a = st.columns(3)
    col6, col7, col3b = st.columns(3)
    col8, col9, col3c = st.columns(3)
    col10, col11, col3d = st.columns(3)
    col12, col13, col3e = st.columns(3)

    # Perform query.
    df = conn.query("SELECT jersey_number || ' - ' || full_name as player FROM roster;", ttl="10m")

    # Create a Streamlit dropdown with the read data
    with col4:
        st.write("Select 5 Players:")
        selected_option1 = st.selectbox("Player 1:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col5:
        st.write("Scored:")
        scorer1 = st.checkbox("Scored 1",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,)
    with col6:
        selected_option2 = st.selectbox("Player 2:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col7:
        scorer2 = st.checkbox("Scored 2",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,)
    with col8:
        selected_option3 = st.selectbox("Player 3:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col9:
        scorer3 = st.checkbox("Scored 3",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,)
    with col10:
        selected_option4 = st.selectbox("Player 4:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col11:
        scorer4 = st.checkbox("Scored 4",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,)
    with col12:
        selected_option5 = st.selectbox("Player 5:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col13:
        scorer5 = st.checkbox("Scored 5",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,)

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
        if "scorer1" in st.session_state:
            st.session_state.scorer1 = False
        if "scorer2" in st.session_state:
            st.session_state.scorer2 = False
        if "scorer3" in st.session_state:
            st.session_state.scorer3 = False
        if "scorer4" in st.session_state:
            st.session_state.scorer4 = False
        if "scorer5" in st.session_state:
            st.session_state.scorer5 = False
        with conn.session as session:
            # import ipdb
            # ipdb.set_trace()
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
