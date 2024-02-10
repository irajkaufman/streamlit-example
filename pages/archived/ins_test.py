import datetime
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

    # st.title("Roster Dropdowns from Hoops DB")

    col4, col5, col3a, col4a = st.columns(4)
    col6, col7, col3b, col4b = st.columns(4)
    col8, col9, col3c, col4c = st.columns(4)
    col10, col11, col3d, col4d = st.columns(4)
    col12, col13, col3e, col4e = st.columns(4)

    # Initialize scorer checkboxes
    scorer1 = False
    scorer2 = False
    scorer3 = False
    scorer4 = False
    scorer5 = False
    scorer_opp = False

    # Initialize session state
    # if 'clicked_button' not in st.session_state:
    #     st.session_state.clicked_button = None
    #     scorer1 = False
    #     scorer2 = False
    #     scorer3 = False
    #     scorer4 = False
    #     scorer5 = False
    #     scorer_opp = False
    # else:
    #     scorer1 = st.session_state.scorer1
    #     scorer2 = st.session_state.scorer2
    #     scorer3 = st.session_state.scorer3
    #     scorer4 = st.session_state.scorer4
    #     scorer5 = st.session_state.scorer5
    #     scorer_opp = st.session_state.scorer_opp

    # Perform query.
    df = conn.query("SELECT jersey_number || ' - ' || full_name as player FROM roster where team = 'Campo';", ttl="10m")

    opponent_team = ""

    df_opp = conn.query("SELECT jersey_number || ' - ' || full_name as player FROM roster "
                        "where team = 'De La Salle';", ttl="10m")

    # Create Streamlit dropdown with the read data for Player 1
    with col4:
        st.write("Select 5 Players:")
        selected_option1 = st.selectbox("Player 1:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)

    # Create corresponding checkbox for Player 1
    with col5:
        st.write("Scored:")
        scorer1 = st.checkbox("Scored 1",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,
                              value=scorer1)

    # Time Elapsed text box input and align with Player 1
    with col4a:
        st.write("Time Elapsed (min : sec)")
        vid_time = st.text_input("(per Hudl min|sec)",
                                 label_visibility=st.session_state.visibility,
                                 disabled=st.session_state.disabled,)

    with col6:
        selected_option2 = st.selectbox("Player 2:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col7:
        scorer2 = st.checkbox("Scored 2",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,
                              value=scorer2)

    # Opponent Team Label and align with Players 2
    with col4b:
        st.write("Opponent:")

    with col8:
        selected_option3 = st.selectbox("Player 3:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col9:
        scorer3 = st.checkbox("Scored 3",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,
                              value=scorer3)

    # Opponent Team text box input and align with Player 3
    with col4c:
        opponent_team = st.text_input("Enter Opponent Team Name",
                                      label_visibility=st.session_state.visibility,
                                      disabled=st.session_state.disabled,)

    with col10:
        selected_option4 = st.selectbox("Player 4:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col11:
        scorer4 = st.checkbox("Scored 4",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,
                              value=scorer4)

    # Opponent Scorer Label and align with Players 4
    with col3d:
        st.write("Scored:")

    # Opponent Player Label and align with Players 4
    with col4d:
        st.write("Opponent Player #:")

    with col12:
        selected_option5 = st.selectbox("Player 5:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)
    with col13:
        scorer5 = st.checkbox("Scored 5",
                              label_visibility=st.session_state.visibility,
                              disabled=st.session_state.disabled,
                              value=scorer5)

    # Opponent Player checkbox and align with Player 5
    with col3e:
        scorer_opp = st.checkbox("Opponent Scored",
                                 label_visibility=st.session_state.visibility,
                                 disabled=st.session_state.disabled,
                                 value=scorer_opp)

    # Opponent Player dropdown and align with Player 5
    with col4e:
        selected_option_opp = st.selectbox("Opponent Player:", df_opp,
                                           label_visibility=st.session_state.visibility,
                                           disabled=st.session_state.disabled,)

    st.write("")
    st.write("NOTE: 'Time Elapsed' and 'Opponent' are required fields")
    
    insert_query1 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player) "
                         f"VALUES (:selected_option1, :current_shot, :team, :scorer1, :vid_time, "
                         f":selected_option_opp);")
    insert_query2 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player) "
                         f"VALUES (:selected_option2, :current_shot, :team, :scorer2, :vid_time, "
                         f":selected_option_opp);")
    insert_query3 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player) "
                         f"VALUES (:selected_option3, :current_shot, :team, :scorer3, :vid_time, "
                         f":selected_option_opp);")
    insert_query4 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player) "
                         f"VALUES (:selected_option4, :current_shot, :team, :scorer4, :vid_time, "
                         f":selected_option_opp);")
    insert_query5 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player) "
                         f"VALUES (:selected_option5, :current_shot, :team, :scorer5, :vid_time, "
                         f":selected_option_opp);")


    if col1.button("Free Throw"):
        if not scorer_opp:
            current_shot = free_throw
            selected_option_opp = ""
            st.session_state.score += free_throw
        if scorer_opp:
            current_shot = free_throw * -1
            team = opponent_team
            st.session_state.score -= free_throw
        with conn.session as session:
            # import ipdb
            # ipdb.set_trace()
            session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                            "team": team, "scorer1": scorer1, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                            "team": team, "scorer2": scorer2, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                            "team": team, "scorer3": scorer3, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                            "team": team, "scorer4": scorer4, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                            "team": team, "scorer5": scorer5, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.commit()
        scorer1 = False
        scorer2 = False
        scorer3 = False
        scorer4 = False
        scorer5 = False
        scorer_opp = False

    if col2.button("Jumper"):
        if not scorer_opp:
            current_shot = jumper
            selected_option_opp = ""
            st.session_state.score += jumper
        if scorer_opp:
            current_shot = jumper * -1
            team = opponent_team
            st.session_state.score -= jumper
        with conn.session as session:
            session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                            "team": team, "scorer1": scorer1, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                            "team": team, "scorer2": scorer2, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                            "team": team, "scorer3": scorer3, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                            "team": team, "scorer4": scorer4, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                            "team": team, "scorer5": scorer5, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.commit()
        scorer1 = False
        scorer2 = False
        scorer3 = False
        scorer4 = False
        scorer5 = False
        scorer_opp = False

    if col3.button("Triple!"):
        if not scorer_opp:
            current_shot = triple
            selected_option_opp = ""
            st.session_state.score += triple
        if scorer_opp:
            current_shot = triple * -1
            team = opponent_team
            st.session_state.score -= triple
        with conn.session as session:
            session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                            "team": team, "scorer1": scorer1, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                            "team": team, "scorer2": scorer2, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                            "team": team, "scorer3": scorer3, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                            "team": team, "scorer4": scorer4, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                            "team": team, "scorer5": scorer5, "vid_time": vid_time,
                                            "selected_option_opp": selected_option_opp})
            session.commit()
        scorer1 = False
        scorer2 = False
        scorer3 = False
        scorer4 = False
        scorer5 = False
        scorer_opp = False

    scorer1 = False
    scorer2 = False
    scorer3 = False
    scorer4 = False
    scorer5 = False
    scorer_opp = False

    # Update session state
    st.session_state.scorer1 = False
    st.session_state.scorer2 = False
    st.session_state.scorer3 = False
    st.session_state.scorer4 = False
    st.session_state.scorer5 = False
    st.session_state.scorer_opp = False


if __name__ == "__main__":
    main()
