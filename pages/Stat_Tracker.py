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
    def log_shot_then_clear_selection(current_stat, current_stat_value, success_fn, offense_fn, shot_type_fn,
                                      rebound_end_fn, button_clicked):
        st.cache_data.clear()
        dup_check = conn.query(f"SELECT count(*) "
                               f"  FROM public.stat_log"
                               f" WHERE schedule_id = '{schedule_id}' "
                               f"   AND video_time = '{vid_time}';", ttl="10m")
        # st.rerun
        dup_check_list = dup_check.values.tolist()
        print("dup_check_list[0][0] = ", dup_check_list[0][0])
        print("dup_check_list = ", dup_check_list)
        print("schedule_id = ", schedule_id)
        print("vid_time = ", vid_time)
        if dup_check_list[0][0] > 0:
            st.warning('Whoa Nellie! Please update the "Time Elapsed", and RE-submit the previous stat.',
                       icon="✋🏻")
            return
        if current_stat != "Free Throw" and current_stat != "Basket":
            success_fn = ""
        if current_stat != "Basket":
            offense_fn = ""
            shot_type_fn = ""
            for key in st.session_state.keys():
                if key.startswith("provider") or key == "contested":
                    st.session_state[key] = False
        if current_stat != "Rebound":
            rebound_end_fn = ""
        log_shot(current_stat,
                 current_stat_value,
                 my_team,
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
                 success_fn,
                 offense_fn,
                 shot_type_fn,
                 rebound_end_fn,
                 schedule_id,
                 vid_time,
                 button_clicked)
        print("Re-setting checkboxes, BEFORE")
        for key in st.session_state.keys():
            if key.startswith("contributor") or key.startswith("provider") or key == "contested":
                # print("key = ", key)
                # print("st.session_state[key] =", st.session_state[key])
                st.session_state[key] = False
                # st.rerun
            # print("suc_list[0][0] = ", suc_list[0][0])
            # print("off_list[0][0] = ", suc_list[0][0])
            # print("shot_list[0][0] = ", suc_list[0][0])
            # print("reb_list[0][0] = ", suc_list[0][0])
            if st.session_state['suc_stat'] != suc_list[0][0]:
                st.session_state['suc_stat'] = suc_list[0][0]
            if st.session_state['off_stat'] != off_list[0][0]:
                st.session_state['off_stat'] = off_list[0][0]
            if st.session_state['shot_stat'] != shot_list[0][0]:
                st.session_state['shot_stat'] = shot_list[0][0]
            if st.session_state['reb_stat'] != reb_list[0][0]:
                st.session_state['reb_stat'] = reb_list[0][0]
        print("Re-setting checkboxes, AFTER")

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

    # Initialize session states
    if 'score' not in st.session_state:
        st.session_state.score = 0

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "collapsed"
        st.session_state.disabled = False

    if 'clicked_button' not in st.session_state:
        st.session_state.clicked_button = False
        st.session_state.contributor1 = False
        st.session_state.contributor2 = False
        st.session_state.contributor3 = False
        st.session_state.contributor4 = False
        st.session_state.contributor5 = False
        st.session_state.contributor_opp = False
        st.session_state.provider1 = False
        st.session_state.provider2 = False
        st.session_state.provider3 = False
        st.session_state.provider4 = False
        st.session_state.provider5 = False
        st.session_state.provider_opp = False
        st.session_state.contested = False

    # Initialize global variables (inside main function)
    free_throw = 1
    jumper = 2
    triple = 3
    rebound = 1
    block = 1
    steal = 1
    turnover = 1
    rebound_end = ""
    # team = 'Campolindo'
    # button_clicked = False

    # Initialize stat queries (dropdowns)
    suc = conn.query(f"SELECT eav_value "
                     f"  FROM ent_att_val "
                     f" WHERE eav_attribute = 'success' "
                     f" ORDER BY eav_id ;", ttl="10m")
    suc_list = suc.values.tolist()

    off = conn.query(f"SELECT eav_value "
                     f"  FROM ent_att_val "
                     f" WHERE eav_attribute = 'offense' "
                     f" ORDER BY eav_id ;", ttl="10m")
    off_list = off.values.tolist()

    shot = conn.query(f"SELECT eav_value "
                      f"  FROM ent_att_val "
                      f" WHERE eav_attribute = 'shot' "
                      f" ORDER BY eav_id ;", ttl="10m")
    shot_list = shot.values.tolist()

    reb = conn.query(f"SELECT eav_value "
                     f"  FROM ent_att_val "
                     f" WHERE eav_attribute = 'rebound' "
                     f" ORDER BY eav_id ;", ttl="10m")
    reb_list = reb.values.tolist()

    # *************************************************
    # ****** Top Headers: My Team, Level, Season ******
    # *************************************************
    col_team, col_level, col_season = st.columns(3)
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

    # *****************************************************
    # ****** 2nd Header Line: mascot, opponent, date ******
    # *****************************************************
    col_a, col_b, col_c = st.columns(3)
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
                        f" UNION "
                        f" SELECT '0 - UNKNOWN' as player "
                        f" ORDER BY player;", ttl="10m")

    with col_c:
        game_date = st.selectbox("Game Date", gd)

    # **************************************************************
    # ****** my team's score, opponent team's score, Win/Loss ******
    # **************************************************************
    col_m, col_o, col_z = st.columns(3)
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

    # ****************************************************
    # ****** HTML and CSS to draw a horizontal line ******
    # ****************************************************
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

    # *****************************************
    # ****** (Non-)Scoring Stats Headers ******
    # *****************************************
    col_scoring, col_non_scoring = st.columns(2)
    with col_scoring:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 29px;">Scoring Stats</span>', unsafe_allow_html=True)

    with col_non_scoring:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 29px;">Non-Scoring Stats</span>', unsafe_allow_html=True)

    # ***************************************************
    # ****** Stat Buttons, Drop-downs, & 1 Boolean ******
    # ***************************************************
    col_scoring_1, col_scoring_2, col_scoring_3, col_scoring_4 = st.columns(4)
    with col_scoring_2:
        success = st.selectbox("Success Drop-down", suc, key="suc_stat",
                               label_visibility=st.session_state.visibility,
                               disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        offense = st.selectbox("Offense Drop-down", off, key="off_stat",
                               label_visibility=st.session_state.visibility,
                               disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        shot_type = st.selectbox("Shot Drop-down", shot, key="shot_stat",
                                 label_visibility=st.session_state.visibility,
                                 disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        st.checkbox("Contested?",
                    key="contested",
                    value=False)

    with col_scoring_1:
        if st.button("Free Throw", key='ft', on_click=log_shot_then_clear_selection,
                     args=["Free Throw", free_throw, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("2 points", key='jmp', on_click=log_shot_then_clear_selection,
                     args=["Basket", jumper, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("3 points", key='tri', on_click=log_shot_then_clear_selection,
                     args=["Basket", triple, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass

    with col_scoring_4:
        rebound_end = st.selectbox("Drop-down 4", reb, key="reb_stat",
                                   label_visibility=st.session_state.visibility,
                                   disabled=st.session_state.disabled, )
        st.markdown("<div style='height: 106px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("Turnover", key='to', on_click=log_shot_then_clear_selection,
                     args=["Turnover", turnover, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass

    with col_scoring_3:
        if st.button("Rebound", key='reb', on_click=log_shot_then_clear_selection,
                     args=["Rebound", rebound, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("Block", key='blk', on_click=log_shot_then_clear_selection,
                     args=["Block", block, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass
        st.markdown("<div style='height: 17px;'></div>", unsafe_allow_html=True)  # Custom height spacer
        if st.button("Steal", key='stl', on_click=log_shot_then_clear_selection,
                     args=["Steal", steal, success, offense, shot_type, rebound_end, True],
                     use_container_width=True):
            pass

    # *****************************************
    # ****** Time Elapsed Text Box Input ******
    # *****************************************
    tm_elapsed1, tm_elapsed2, tm_elapsed3 = st.columns(3)
    with tm_elapsed2:
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


    # *********************************************
    # ****** Player 1 / Opponent Contributor ******
    # *********************************************
    col4, col5, asst1, col3a, col4a = st.columns(5)
    with col4:
        st.write("My Team:")
        selected_option1 = st.selectbox("Player 1:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled,)

    with col5:
        st.write("Contributed:")
        st.checkbox("Scored 1",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="contributor1",
                    value=False)

    with asst1:
        st.write("Assisted:")
        st.checkbox("Assisted 1",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="provider1",
                    value=False)

    # Opponent Player Label and align with Player Headers
    with col3a:
        st.write("Opponent Player:")
        selected_option_opp = st.selectbox("Opponent Player:", df_opp,
                                           label_visibility=st.session_state.visibility,
                                           disabled=st.session_state.disabled)
        # st.write(selected_option_opp)

    # Opponent Contributor Label and align with Player 1
    with col4a:
        st.write("Contributed:")
        st.checkbox("Opponent Contributed",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="contributor_opp",
                    value=False)

    # ****************************************************
    # ****** Player 2 / Opponent Facilitator Labels ******
    # ****************************************************
    col6, col7, asst2, col3b, col4b = st.columns(5)
    with col6:
        selected_option2 = st.selectbox("Player 2:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col7:
        st.checkbox("Scored 2",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="contributor2",
                    value=False)

    with asst2:
        st.checkbox("Assisted 2",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="provider2",
                    value=False)

    with col3b:
        st.write("Opponent Player:")

    # Opponent Facilitator Label and align with Player 2
    with col4b:
        st.write("Assisted:")

    # *********************************************
    # ****** Player 3 / Opponent Facilitator ******
    # *********************************************
    col8, col9, asst3, col3c, col4c = st.columns(5)
    with col8:
        selected_option3 = st.selectbox("Player 3:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col9:
        st.checkbox("Scored 3",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="contributor3",
                    value=False)

    with asst3:
        st.checkbox("Assisted 3",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="provider3",
                    value=False)

    # Opponent Player Label and align with Player 2
    with col3c:
        # st.write("Opponent Player:")
        selected_option_opp = st.selectbox("Opponent Facilitator:", df_opp,
                                           label_visibility=st.session_state.visibility,
                                           disabled=st.session_state.disabled)
        # st.write(selected_option_opp)

    # Opponent Facilitator Label and align with Player 2
    with col4c:
        # st.write("Assisted:")
        st.checkbox("Opponent Assisted",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="provider_opp",
                    value=False)

    # **********************
    # ****** Player 4 ******
    # **********************
    col10, col11, asst4, col3d, col4d = st.columns(5)
    with col10:
        selected_option4 = st.selectbox("Player 4:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col11:
        st.checkbox("Scored 4",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="contributor4",
                    value=False)

    with asst4:
        st.checkbox("Assisted 4",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="provider4",
                    value=False)

    # **********************
    # ****** Player 5 ******
    # **********************
    col12, col13, asst5, col3e, col4e = st.columns(5)
    with col12:
        selected_option5 = st.selectbox("Player 5:", df,
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
    with col13:
        st.checkbox("Scored 5",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="contributor5",
                    value=False)

    with asst5:
        st.checkbox("Assisted 5",
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    key="provider5",
                    value=False)

    # st.write("")
    # st.write("NOTE: 'Time Elapsed' and 'Opponent' are required fields")
    # UPDATE "scoring" TABLE THROUGHOUT FILE, and MODIFY INSERT QUERIES, BELOW:
    insert_query1 = text(f"INSERT INTO stat_log (stat_name, team, player, contributor, "
                         f"stat_value, assist, success, offense, shot, contested, rebound, "
                         f"opponent_player, schedule_id, video_time) VALUES ( "
                         f":current_stat, :team, :selected_option1, :contributor1, "
                         f":current_stat_value, :provider1, :success, :offense, :shot_type, :contested, :rebound_end, "
                         f":selected_option_opp, :schedule_id, :vid_time);")
    insert_query2 = text(f"INSERT INTO stat_log (stat_name, team, player, contributor, "
                         f"stat_value, assist, success, offense, shot, contested, rebound, "
                         f"opponent_player, schedule_id, video_time) VALUES ( "
                         f":current_stat, :team, :selected_option2, :contributor2, "
                         f":current_stat_value, :provider2, :success, :offense, :shot_type, :contested, :rebound_end, "
                         f":selected_option_opp, :schedule_id, :vid_time);")
    insert_query3 = text(f"INSERT INTO stat_log (stat_name, team, player, contributor, "
                         f"stat_value, assist, success, offense, shot, contested, rebound, "
                         f"opponent_player, schedule_id, video_time) VALUES ( "
                         f":current_stat, :team, :selected_option3, :contributor3, "
                         f":current_stat_value, :provider3, :success, :offense, :shot_type, :contested, :rebound_end, "
                         f":selected_option_opp, :schedule_id, :vid_time);")
    insert_query4 = text(f"INSERT INTO stat_log (stat_name, team, player, contributor, "
                         f"stat_value, assist, success, offense, shot, contested, rebound, "
                         f"opponent_player, schedule_id, video_time) VALUES ( "
                         f":current_stat, :team, :selected_option4, :contributor4, "
                         f":current_stat_value, :provider4, :success, :offense, :shot_type, :contested, :rebound_end, "
                         f":selected_option_opp, :schedule_id, :vid_time);")
    insert_query5 = text(f"INSERT INTO stat_log (stat_name, team, player, contributor, "
                         f"stat_value, assist, success, offense, shot, contested, rebound, "
                         f"opponent_player, schedule_id, video_time) VALUES ( "
                         f":current_stat, :team, :selected_option5, :contributor5, "
                         f":current_stat_value, :provider5, :success, :offense, :shot_type, :contested, :rebound_end, "
                         f":selected_option_opp, :schedule_id, :vid_time);")

    # Scoring Log Query:
    ts = conn.query(
        f"SELECT video_time as \"Video Time\", "
        f"       player as \"Player\", "
        f"       team as \"Team\", "
        f"       stat_name as \"Stat\", "
        f"       success as \"Shot Success?\", "
        f"       offense as \"Offense Scenario\", "
        f"       shot as \"Shot Type\", "
        f"       contested as \"Shot Contested?\", "
        f"       rebound as \"Rebound End\", "
        f"       stat_value as \"Stat Value\" "
        f"  FROM ( "
        f"                select player, p1.team, "
        f"                stat_name, success, offense, shot, contested, rebound, "
        f"                right(to_char(video_time,'HH24:MI:SS'), 7) as video_time, stat_value "
        f"                  from stat_log p1 "
        f"                  join schedule s1 "
        f"                      on p1.schedule_id = s1.schedule_id "
        f"                  join team t1 "
        f"                      on s1.team_id = t1.team_id "
        f"                 where t1.team_name = '{my_team}' "
        f"                   and s1.opponent = '{opponent_team}' "
        f"                   and contributor = true"
        f"                UNION "
        f"                select distinct opponent_player, p2.team, "
        f"                stat_name, success, offense, shot, contested, rebound, "
        f"                right(to_char(video_time,'HH24:MI:SS'), 7) "
        f"                       as video_time, stat_value "
        f"                  from stat_log p2 "
        f"                  join schedule s2 "
        f"                      on p2.schedule_id = s2.schedule_id "
        f"                  join team t2 "
        f"                      on s2.team_id = t2.team_id "
        f"                 where t2.team_name = '{my_team}' "
        f"                   and s2.opponent = '{opponent_team}' "
        f"                   and opponent_player != '' "
        f"        ) as x "
        f" ORDER BY video_time desc; ", ttl="5")

    st.write("")
    st.write("")
    st.write("Scoring Log")
    st.dataframe(ts)
    # st.write(st.session_state)


def log_shot(current_stat,
             current_stat_value,
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
             success,
             offense,
             shot_type,
             rebound_end,
             schedule_id,
             vid_time,
             button_clicked):
    print(f"In the callback function {current_stat_value}")
    if button_clicked:
        print(f"In the button_clicked condition {current_stat_value}")
        if not st.session_state.contributor_opp:
            selected_option_opp = ""
            st.session_state.score += current_stat_value
        if st.session_state.contributor_opp:
            current_stat_value = current_stat_value * -1
            team = opponent_team
            st.session_state.score -= current_stat_value
        if (st.session_state.contributor1 or st.session_state.contributor2 or st.session_state.contributor3
                or st.session_state.contributor4 or st.session_state.contributor5 or st.session_state.contributor_opp):
            with conn.session as session:
                # import ipdb
                # ipdb.set_trace()
                session.execute(insert_query1, {"current_stat": current_stat, "team": team,
                                                "selected_option1": selected_option1, "contributor1":
                                                st.session_state.contributor1, "current_stat_value": current_stat_value,
                                                "provider1": st.session_state.provider1, "success": success, "offense":
                                                offense, "shot_type": shot_type, "contested":
                                                st.session_state.contested, "rebound_end": rebound_end,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id,
                                                "vid_time": vid_time})
                session.execute(insert_query2, {"current_stat": current_stat, "team": team,
                                                "selected_option2": selected_option2, "contributor2":
                                                st.session_state.contributor2, "current_stat_value": current_stat_value,
                                                "provider2": st.session_state.provider2, "success": success, "offense":
                                                offense, "shot_type": shot_type, "contested":
                                                st.session_state.contested, "rebound_end": rebound_end,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id,
                                                "vid_time": vid_time})
                session.execute(insert_query3, {"current_stat": current_stat, "team": team,
                                                "selected_option3": selected_option3, "contributor3":
                                                st.session_state.contributor3, "current_stat_value": current_stat_value,
                                                "provider3": st.session_state.provider3, "success": success, "offense":
                                                offense, "shot_type": shot_type, "contested":
                                                st.session_state.contested, "rebound_end": rebound_end,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id,
                                                "vid_time": vid_time})
                session.execute(insert_query4, {"current_stat": current_stat, "team": team,
                                                "selected_option4": selected_option4, "contributor4":
                                                st.session_state.contributor4, "current_stat_value": current_stat_value,
                                                "provider4": st.session_state.provider4, "success": success, "offense":
                                                offense, "shot_type": shot_type, "contested":
                                                st.session_state.contested, "rebound_end": rebound_end,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id,
                                                "vid_time": vid_time})
                session.execute(insert_query5, {"current_stat": current_stat, "team": team,
                                                "selected_option5": selected_option5, "contributor5":
                                                st.session_state.contributor5, "current_stat_value": current_stat_value,
                                                "provider5": st.session_state.provider5, "success": success, "offense":
                                                offense, "shot_type": shot_type, "contested":
                                                st.session_state.contested, "rebound_end": rebound_end,
                                                "selected_option_opp": selected_option_opp, "schedule_id": schedule_id,
                                                "vid_time": vid_time})
                session.commit()


if __name__ == "__main__":
    main()
    st.write(st.session_state)
