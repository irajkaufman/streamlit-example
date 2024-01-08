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
    def log_shot_then_clear_selection(current_shot, button_clicked):
        log_shot(current_shot,
                 team,
                 opponent_team,
                 insert_query1,
                 insert_query2,
                 insert_query3,
                 insert_query4,
                 insert_query5,
                 selected_option1,
                 selected_option2,
                 selected_option3,
                 selected_option4,
                 selected_option5,
                 selected_option_opp,
                 schedule_id,
                 vid_time,
                 button_clicked)
        print("Re-setting checkboxes, BEFORE")
        for key in st.session_state.keys():
            if key.startswith("scorer"):
                print("key = ", key)
                print("st.session_state[key] =", st.session_state[key])
                st.session_state[key] = False
        print("Re-seting checkboxes, AFTER")

    print("Entering Main")

    if 'score' not in st.session_state:
        st.session_state.score = 0

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "collapsed"
        st.session_state.disabled = False

    free_throw = 1
    jumper = 2
    triple = 3
    team = 'Campolindo'
    button_clicked = False

    col_a, col_b, col_c = st.columns(3)
    col_m, col_o, col_z = st.columns(3)

    st.write("")

    col1, col2, col3 = st.columns(3)

    if col1.button("Free Throw", key='ft', on_click=log_shot_then_clear_selection, args=[free_throw, True]):
        pass

    if col2.button("Jumper", key='jmp', on_click=log_shot_then_clear_selection, args=[jumper, True]):
        pass

    if col3.button("Triple!", key='tri', on_click=log_shot_then_clear_selection, args=[triple, True]):
        pass

    # st.title("Roster Dropdowns from Hoops DB")

    col4, col5, col3a, col4a = st.columns(4)
    col6, col7, col3b, col4b = st.columns(4)
    col8, col9, col3c, col4c = st.columns(4)
    col10, col11, col3d, col4d = st.columns(4)
    col12, col13, col3e, col4e = st.columns(4)

    # Initialize session state
    if 'clicked_button' not in st.session_state:
        st.session_state.clicked_button = False
        # st.session_state.k1 = False
        # st.session_state.k2 = False
        # st.session_state.k3 = False
        # st.session_state.k4 = False
        # st.session_state.k5 = False
        # st.session_state.ko = False
        st.session_state.scorer1 = False
        st.session_state.scorer2 = False
        st.session_state.scorer3 = False
        st.session_state.scorer4 = False
        st.session_state.scorer5 = False
        st.session_state.scorer_opp = False
    # else:
    #     scorer1 = st.session_state.scorer1
    #     scorer2 = st.session_state.scorer2
    #     scorer3 = st.session_state.scorer3
    #     scorer4 = st.session_state.scorer4
    #     scorer5 = st.session_state.scorer5
    #     scorer_opp = st.session_state.scorer_opp

    # Perform queries.

    # My Team
    mt = conn.query("SELECT DISTINCT team FROM schedule s;", ttl="10m")

    # My Team's Players
    df = conn.query("SELECT jersey_number || ' - ' || full_name as player FROM roster where team = 'Campo';", ttl="10m")

    # Opponent Team
    ot = conn.query("SELECT DISTINCT replace(opponent, '''', '''''') FROM schedule;", ttl="10m")

    with col_a:
        my_team = st.selectbox("My Team", mt)

    with col_b:
        opponent_team = st.selectbox("Opponent Team", ot)
        # st.write(opponent_team)

    gd = conn.query(f"SELECT DISTINCT game_date FROM schedule where team = '{my_team}' "
                    f"and opponent = '{opponent_team}';", ttl="10m")
                    # f"and opponent = 'Bishop O''Dowd';", ttl="10m")

    # Opponent's Team's Players
    df_opp = conn.query(f"SELECT jersey_number || ' - ' || full_name as player "
                        f"FROM roster "
                        f"where team = '{opponent_team}' "
                        f"order by jersey_number;", ttl="10m")
                        # f"where team = 'Bishop O''''Dowd';", ttl="10m")
    # st.write(df_opp)

    with col_c:
        game_date = st.selectbox("Game Date", gd)

    sid = conn.query(f"SELECT schedule_id FROM schedule WHERE team = '{my_team}' "
                     f"and opponent = '{opponent_team}' and game_date = '{game_date}';", ttl="10m")

    if not sid.empty:
        # Extract the 'schedule_id' column
        schedule_id = int(sid['schedule_id'].iloc[0])

        # Display the extracted values
        # st.write(f"Captured schedule_ids: {schedule_id}")

    mp = conn.query(f"select sum(points_scored) as my_team_points"
                    f"  from ("
                    f"select distinct p.video_time, p.points_scored"
                    f"  from scoring p"
                    f"  join schedule s"
                    f"    on p.schedule_id = s.schedule_id"
                    f" where points_scored > 0"
                    f"   and s.team = '{my_team}'"
                    f"   and s.opponent = '{opponent_team}') m;", ttl="5")

    if not mp.empty:
        with col_m:
            my_points = mp['my_team_points'].iloc[0]
            st.write('### ', my_points)
    else:
        st.write('###')

    op = conn.query(f"select sum(points_scored)*-1 as opponent_team_points"
                    f"  from ("
                    f"select distinct p.video_time, p.points_scored"
                    f"  from scoring p"
                    f"  join schedule s"
                    f"    on p.schedule_id = s.schedule_id"
                    f" where points_scored < 0"
                    f"   and s.team = '{my_team}'"
                    f"   and s.opponent = '{opponent_team}') m;", ttl="5")

    if not op.empty:
        with col_o:
            opponent_points = op['opponent_team_points'].iloc[0]
            st.write('### ', opponent_points)
    else:
        st.write('###')

    # Create Streamlit dropdown with the read data for Player 1
    with col4:
        st.write("My Team's 5 Players:")
        selected_option1 = st.selectbox("Player 1:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)

    # Create corresponding checkbox for Player 1
    with col5:
        st.write("Scored:")
        st.checkbox("Scored 1",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer1",
                    value=False)

    # Time Elapsed text box input and align with Player 1
    with col3a:
        st.write("Time Elapsed (min : sec)")
        vid_time = st.text_input("(per Hudl min|sec)",
                                 label_visibility=st.session_state.visibility,
                                 disabled=st.session_state.disabled,
                                 value='00:00')
        vid_time = '00:'+vid_time

    with col6:
        selected_option2 = st.selectbox("Player 2:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col7:
        st.checkbox("Scored 2",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer2",
                    value=False)

    # Opponent Team Label and align with Players 2 (Moved to TOP of Page)
    # with col4b:
    #     st.write("Opponent:")

    with col8:
        selected_option3 = st.selectbox("Player 3:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col9:
        st.checkbox("Scored 3",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer3",
                    value=False)

    # Opponent Team text box input and align with Player 3 (Moved to TOP of Page)
    # with col4c:
    #     opponent_team = st.text_input("Enter Opponent Team Name",
    #                                   label_visibility=st.session_state.visibility,
    #                                   disabled=st.session_state.disabled,
    #                                   value='De La Salle')

    with col10:
        selected_option4 = st.selectbox("Player 4:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col11:
        st.checkbox("Scored 4",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer4",
                    value=False)

    # Opponent Player Label and align with Players 4
    with col3d:
        st.write("Opponent Player #:")

    # Opponent Scorer Label and align with Players 4
    with col4d:
        st.write("Scored:")

    with col12:
        selected_option5 = st.selectbox("Player 5:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col13:
        st.checkbox("Scored 5",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer5",
                    value=False)

    # Opponent Player dropdown and align with Player 5
    with col3e:
        selected_option_opp = st.selectbox("Opponent Player:", df_opp,
                                           label_visibility=st.session_state.visibility,
                                           disabled=st.session_state.disabled)
        # st.write(selected_option_opp)

    # Opponent Player checkbox and align with Player 5
    with col4e:
        st.checkbox("Opponent Scored",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer_opp",
                    value=False)

    # st.write("")
    # st.write("NOTE: 'Time Elapsed' and 'Opponent' are required fields")

    insert_query1 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player, "
                         f"schedule_id) VALUES (:selected_option1, :current_shot, :team, :scorer1, :vid_time, "
                         f":selected_option_opp, :schedule_id);")
    insert_query2 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player, "
                         f"schedule_id) VALUES (:selected_option2, :current_shot, :team, :scorer2, :vid_time, "
                         f":selected_option_opp, :schedule_id);")
    insert_query3 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player, "
                         f"schedule_id) VALUES (:selected_option3, :current_shot, :team, :scorer3, :vid_time, "
                         f":selected_option_opp, :schedule_id);")
    insert_query4 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player, "
                         f"schedule_id) VALUES (:selected_option4, :current_shot, :team, :scorer4, :vid_time, "
                         f":selected_option_opp, :schedule_id);")
    insert_query5 = text(f"INSERT INTO scoring (player, points_scored, team, scorer, video_time, opponent_player, "
                         f"schedule_id) VALUES (:selected_option5, :current_shot, :team, :scorer5, :vid_time, "
                         f":selected_option_opp, :schedule_id);")

    # st.write(st.session_state)


def log_shot(current_shot,
             team,
             opponent_team,
             insert_query1,
             insert_query2,
             insert_query3,
             insert_query4,
             insert_query5,
             selected_option1,
             selected_option2,
             selected_option3,
             selected_option4,
             selected_option5,
             selected_option_opp,
             schedule_id,
             vid_time,
             button_clicked):
    print(f"In the callback function {current_shot}")
    if button_clicked:
        print(f"In the button_clicked condition {current_shot}")
        if not st.session_state.scorer_opp:
            selected_option_opp = ""
            st.session_state.score += current_shot
        if st.session_state.scorer_opp:
            current_shot = current_shot * -1
            team = opponent_team
            st.session_state.score -= current_shot
        if st.session_state.scorer1 or st.session_state.scorer2 or st.session_state.scorer3 or st.session_state.scorer4 \
                or st.session_state.scorer5 or st.session_state.scorer_opp:
            with conn.session as session:
                # import ipdb
                # ipdb.set_trace()
                session.execute(insert_query1, {"selected_option1": selected_option1, "current_shot": current_shot,
                                                "team": team, "scorer1": st.session_state.scorer1, "vid_time": vid_time,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id})
                session.execute(insert_query2, {"selected_option2": selected_option2, "current_shot": current_shot,
                                                "team": team, "scorer2": st.session_state.scorer2, "vid_time": vid_time,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id})
                session.execute(insert_query3, {"selected_option3": selected_option3, "current_shot": current_shot,
                                                "team": team, "scorer3": st.session_state.scorer3, "vid_time": vid_time,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id})
                session.execute(insert_query4, {"selected_option4": selected_option4, "current_shot": current_shot,
                                                "team": team, "scorer4": st.session_state.scorer4, "vid_time": vid_time,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id})
                session.execute(insert_query5, {"selected_option5": selected_option5, "current_shot": current_shot,
                                                "team": team, "scorer5": st.session_state.scorer5, "vid_time": vid_time,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id})
                session.commit()
            # st.rerun()
            # st.session_state.k1.value = False
            # st.session_state.k2.value = False
            # st.session_state.k3.value = False
            # st.session_state.k4.value = False
            # st.session_state.k5.value = False
            # st.session_state.ko.value = False
            # st.session_state.scorer1 = False
            # st.session_state.scorer2 = False
            # st.session_state.scorer3 = False
            # st.session_state.scorer4 = False
            # st.session_state.scorer5 = False
            # st.session_state.scorer_opp = False
            # st.rerun()


if __name__ == "__main__":
    main()
