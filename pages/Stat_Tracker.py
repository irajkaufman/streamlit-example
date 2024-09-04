import streamlit as st
from sqlalchemy import create_engine, text
import utilities as ut

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# def score_insert(points_scored: int, team: str = 'Campolindo'):
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
                # st.rerun
        print("Re-seting checkboxes, AFTER")

    print("Entering Main")

    # Custom CSS to adjust the height and appearance of elements
    st.markdown("""
        <style>
        /* Reduce height of the select box */
        div[data-baseweb="select"] {
            /* min-height: 20px; */
            height: 20px;
            font-size: 12px;
            padding: 0px;
            display: flex;
            align-items: center;
        }

        /* Ensure label has proper spacing and does not overlap */
        label.css-16huue1 {
            font-size: 12px;
            margin-bottom: 4px;
            display: block;
        }

        /* Adjust padding inside the select box content */
        div[data-baseweb="select"] > div {
            padding: 0px 10px;
            height: 100%;
            align-items: center;
        }

        /* Adjust the dropdown menu options to be smaller */
        div[data-baseweb="menu"] {
            font-size: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'score' not in st.session_state:
        st.session_state.score = 0

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "collapsed"
        st.session_state.disabled = False

    free_throw = 1
    jumper = 2
    triple = 3
    rebound = 1
    block = 1
    steal = 1
    turnover = 1
    # team = 'Campolindo'
    button_clicked = False

    col_team, col_level, col_season = st.columns(3)
    col_a, col_b, col_c = st.columns(3)  # mascot, opponent, date
    col_m, col_o, col_z = st.columns(3)  # my team's score, opponent team's score, Win/Loss

    # HTML and CSS to draw a horizontal line
    st.markdown(
        """
        <style>
        .divider {
            margin-top: 20px; /* Adjust margin as needed */
            margin-bottom: 20px; /* Adjust margin as needed */
            border-top: 1px solid #ccc; /* Line color and style */
        }
        </style>
        <hr class="divider">
        """,
        unsafe_allow_html=True
    )

    # st.write("")

    col_scoring, col_non_scoring = st.columns(2)  # scoring headers

    with col_scoring:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 29px;">Scoring Stats</span>', unsafe_allow_html=True)

    with col_non_scoring:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 29px;">Non-Scoring Stats</span>', unsafe_allow_html=True)

    col_scoring_1, col_scoring_2, col_scoring_3, col_scoring_4 = st.columns(4)

    # button1, button2, button3 = st.columns(3)

    with col_scoring_1:
        if st.button("Free Throw", key='ft', on_click=log_shot_then_clear_selection, args=[free_throw, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("2 points", key='jmp', on_click=log_shot_then_clear_selection, args=[jumper, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("3 points", key='tri', on_click=log_shot_then_clear_selection, args=[triple, True],
                     use_container_width=True):
            pass

    with col_scoring_2:
        st.selectbox("Drop-down 1", ["Make", "Miss"],
                     label_visibility=st.session_state.visibility,
                     disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        st.selectbox("Drop-down 2", ["1/2 Court Offense", "One-on-One", "Inbounds Play", "Fast Break",
                                     "Buzzer Beater"],
                     label_visibility=st.session_state.visibility,
                     disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        st.selectbox("Drop-down 3", ["Jumper", "Layup", "Floater", "Putback", "Dunk", "Heave"],
                     label_visibility=st.session_state.visibility,
                     disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        st.checkbox("Contested?")

    with col_scoring_3:
        if st.button("Rebound", key='reb', on_click=log_shot_then_clear_selection, args=[rebound, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("Block", key='blk', on_click=log_shot_then_clear_selection, args=[block, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("Steal", key='stl', on_click=log_shot_then_clear_selection, args=[steal, True],
                     use_container_width=True):
            pass

    with col_scoring_4:
        st.selectbox("Drop-down 4", ["Offensive", "Defensive"],
                     label_visibility=st.session_state.visibility,
                     disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 106px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("Turnover", key='to', on_click=log_shot_then_clear_selection, args=[turnover, True],
                     use_container_width=True):
            pass

    # Time Elapsed text box input, centered above Player 1
    tm_elpsd1, tm_elpsd2, tm_elpsd3 = st.columns(3)

    # st.title("Roster Dropdowns from Hoops DB")
    col4, col5, asst1, col3a, col4a = st.columns(5)
    col6, col7, asst2, col3b, col4b = st.columns(5)
    col8, col9, asst3, col3c, col4c = st.columns(5)
    col10, col11, asst4, col3d, col4d = st.columns(5)
    col12, col13, asst5, col3e, col4e = st.columns(5)

    # Initialize session state
    if 'clicked_button' not in st.session_state:
        st.session_state.clicked_button = False
        st.session_state.scorer1 = False
        st.session_state.scorer2 = False
        st.session_state.scorer3 = False
        st.session_state.scorer4 = False
        st.session_state.scorer5 = False
        st.session_state.scorer_opp = False

    # My Team
    mt = conn.query("SELECT DISTINCT team_name FROM team;", ttl="10m")

    with col_team:
        my_team = st.selectbox("My Team", mt)


    # My Level
    ml = conn.query(f"SELECT team_level FROM team WHERE team_name = '{my_team}' ;", ttl="10m")

    with col_level:
        my_level = st.selectbox("Level", ml)

    # My Season
    ms = conn.query(f"SELECT season FROM team where team_name = '{my_team}' "
                    f"   AND team_level = '{my_level}' ;", ttl="10m")

    with col_season:
        my_season = st.selectbox("Season", ms)

    tid = conn.query(f"SELECT team_id FROM team WHERE team_name = '{my_team}' "
                     f"   AND team_level = '{my_level}'"
                     f"   AND season = '{my_season}' ;", ttl="10m")

    team_id = int(tid['team_id'].iloc[0])

    mascot = ut.my_mascot_fn(team_id)

    # Opponent Team
    ot = conn.query(f"SELECT distinct opponent "
                    f"  FROM public.schedule"
                    f" WHERE team_id = '{team_id}' ;", ttl="10m")

    with col_a:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 40px;">{mascot}</span>', unsafe_allow_html=True)

    with col_b:
        opp_team = st.selectbox("Opponent Team", ot)
        if opp_team is not None:
            opponent_team = opp_team.replace("'", "''")
        else:
            opponent_team = None

    gd = conn.query(f"SELECT DISTINCT game_date "
                    f"  FROM schedule "
                    f" WHERE team_id = '{team_id}' "
                    f"   AND opponent = '{opponent_team}';", ttl="10m")

    # My Team's Players
    df = conn.query(f"SELECT jersey_number || ' - ' || full_name as player "
                    f"  FROM roster "
                    f" WHERE team_id = '{team_id}' "
                    f"   AND team = '{my_team}' ;", ttl="10m")

    # Opponent's Team's Players
    df_opp = conn.query(f"SELECT jersey_number || ' - ' || full_name as player "
                        f"  FROM roster "
                        f" WHERE team = '{opponent_team}' "
                        f"   AND active = True "
                        f"   AND team_id = '{team_id}' "
                        f" ORDER BY jersey_number;", ttl="10m")

    with col_c:
        game_date = st.selectbox("Game Date", gd)

    if game_date is None:
        query_str = (f"SELECT schedule_id "
                     f"  FROM schedule "
                     f" WHERE 1=2 ")
    else:
        query_str = (f"SELECT schedule_id "
                     f"  FROM schedule "
                     f" WHERE team_id = '{team_id}' "
                     f"   AND opponent = '{opponent_team}' "
                     f"   AND game_date = '{game_date}' ")

    sid = conn.query(query_str, ttl="10m")

    # if not sid.empty:
    # Extract the 'schedule_id' column
    if game_date is None:
        schedule_id = 0
    else:
        schedule_id = int(sid['schedule_id'].iloc[0])

    my_points = ut.my_points_fn(schedule_id)

    with col_m:
        st.write(f'<span style="color: deepskyblue; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 30px;">{my_points}</span>', unsafe_allow_html=True)

    opponent_points = ut.opponent_points_fn(schedule_id)

    with col_o:
        st.write(f'<span style="color: deepskyblue; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 30px;">{opponent_points}</span>', unsafe_allow_html=True)

    with col_z:
        mp_int = my_points or 0
        op_int = opponent_points or 0
        if mp_int > op_int:
            st.write(f'<span style="color: chartreuse; font-weight: 600; text-align: center; display: block; '
                     f'font-size: 30px;">Win</span>', unsafe_allow_html=True)
        elif mp_int < op_int:
            st.write(f'<span style="color: crimson; font-weight: 600; text-align: center; display: block; '
                     f'font-size: 30px;">Loss</span>', unsafe_allow_html=True)
        else:
            st.write('')

    # Create Streamlit dropdown with the read data for Player 1
    with col4:
        st.write("My Team:")
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)  # Custom height spacer
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
    with tm_elpsd2:
        st.write(f'<span style="color: yellow; text-align: center; display: block; font-size: 18px;">'
                 f'Time Elapsed (hr: mi: ss)</span>', unsafe_allow_html=True)
        # st.write("Time Elapsed (hr: mi: ss)")
        vid_time = st.text_input("(per Hudl min|sec)",
                                 label_visibility=st.session_state.visibility,
                                 disabled=st.session_state.disabled,
                                 value='0:00:00')
        # vid_time = '00:'+vid_time
        if len(vid_time) == 7:
            vid_time = '0' + vid_time

        if len(vid_time) == 5:
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

    # Opponent Player Label and align with Player Headers
    with col3a:
        st.write("Opponent Player:")
        selected_option_opp = st.selectbox("Opponent Player:", df_opp,
                                           label_visibility=st.session_state.visibility,
                                           disabled=st.session_state.disabled)
        # st.write(selected_option_opp)

    # Opponent Scorer Label and align with Player 1
    with col4a:
        st.write("Scored:")
        st.checkbox("Opponent Scored",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="scorer_opp",
                    value=False)

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

    ts = conn.query(f"SELECT player as \"Player\", team as \"Team\", video_time as \"Video Time\", "
                    f"points_scored as \"Points\" "
                    f"  FROM ("
                    f"select player, p1.team, right(to_char(video_time,'HH24:MI:SS'), 7) "
                    f"       as video_time, points_scored"
                    f"  from scoring p1"
                    f"  join schedule s1"
                    f"  	on p1.schedule_id = s1.schedule_id"
                    f"  join team t1"
                    f"      on s1.team_id = t1.team_id"
                    f" where t1.team_name = '{my_team}' "
                    f"   and s1.opponent = '{opponent_team}'"
                    f"   and scorer = true "
                    f"UNION "
                    f"select distinct opponent_player, p2.team, right(to_char(video_time,'HH24:MI:SS'), 7) "
                    f"       as video_time, points_scored"
                    f"  from scoring p2"
                    f"  join schedule s2"
                    f"  	on p2.schedule_id = s2.schedule_id"
                    f"  join team t2"
                    f"      on s2.team_id = t2.team_id"
                    f" where t2.team_name = '{my_team}' "
                    f"   and s2.opponent = '{opponent_team}'"
                    f"   and opponent_player != '') as x"
                    f"  order by video_time desc;", ttl="5")

    st.write("")
    st.write("")
    st.write("Scoring Log")
    st.dataframe(ts)
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
        if (st.session_state.scorer1 or st.session_state.scorer2 or st.session_state.scorer3
                or st.session_state.scorer4 or st.session_state.scorer5 or st.session_state.scorer_opp):
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


if __name__ == "__main__":
    main()
