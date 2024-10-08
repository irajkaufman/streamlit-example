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
    if 'score' not in st.session_state:
        st.session_state.score = 0

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "collapsed"
        st.session_state.disabled = False

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
    ot = conn.query(f"SELECT distinct sched.opponent "
                    f"  FROM public.stat_log sl "
                    f"  JOIN public.schedule sched "
                    f"    ON sl.schedule_id = sched.schedule_id"
                    f" WHERE team_id = '{team_id}' ;", ttl="10m")  # UPDATE per My Team's Team ID

    with col_a:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 40px;">{mascot}</span>', unsafe_allow_html=True)

    with col_b:
        # opponent_team = st.selectbox("Opponent Team", ot)
        opp_team = st.selectbox("Opponent Team", ot)
        if opp_team is not None:
            opponent_team = opp_team.replace("'", "''")
        else:
            opponent_team = None

    # My Team's Players
    df = conn.query(f"SELECT jersey_number || ' - ' || left(full_name, length(right(full_name, "
                    # f"POSITION(' ' in full_name))) + 1) as player FROM roster where team = '{my_team}';", ttl="10m")
                    f"POSITION(' ' in full_name))) + 1) as player FROM roster where team_id = '{team_id}' ;", ttl="10m")

    gd = conn.query(f"SELECT DISTINCT game_date "
                    f"  FROM schedule "
                    f" WHERE team_id = '{team_id}' "
                    f"   AND opponent = '{opponent_team}';", ttl="10m")

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

    # mp_query = (f"select sum(points_scored) as my_team_points"
    #             f"  from ("
    #             f"select distinct p.video_time, p.points_scored"
    #             f"  from scoring p"
    #             f"  join schedule s"
    #             f"    on p.schedule_id = s.schedule_id"
    #             f" where points_scored > 0"
    #             f"   and s.schedule_id = '{schedule_id}') m;")
    #
    # mp = conn.query(mp_query, ttl="5")
    #
    # if not mp.empty:
    #     with col_m:
    #         my_points = mp['my_team_points'].iloc[0]
    #         st.write('### ', my_points)
    # else:
    #     st.write('###')
    #
    # op_query = (f"select sum(points_scored)*-1 as opponent_team_points"
    #             f"  from ("
    #             f"select distinct p.video_time, p.points_scored"
    #             f"  from scoring p"
    #             f"  join schedule s"
    #             f"    on p.schedule_id = s.schedule_id"
    #             f" where points_scored < 0"
    #             f"   and s.schedule_id = '{schedule_id}') m;")
    #
    # op = conn.query(op_query, ttl="5")
    #
    # if not op.empty:
    #     with col_o:
    #         opponent_points = op['opponent_team_points'].iloc[0]
    #         st.write('### ', opponent_points)
    # else:
    #     st.write('###')

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

    ispm = conn.query(f"SELECT left(player,length(array_to_string((string_to_array(player, ' '))[1:3], ' ')) + 2)"
                      f"       as \"   Player\", points_scored as \"Points\", "
                      f"       plus_minus as \"   +/-\", made_fts as \"Free Throws\", "
                      f"       made_2s as \"   2s\", made_3s as \"   3s\", "
                      f"       points_for as \"Team Points\", points_against as \"Opponent Points\" "
                      f"  FROM v_individual_scoring"
                      f" WHERE schedule_id = '{schedule_id}' "
                      f" ORDER BY points_scored desc, plus_minus desc", ttl="5")

    st.write("")
    st.write("Individual Scoring / Plus Minus")
    st.dataframe(ispm)

    st.write("")
    st.write("")
    st.write("Lineup Scoring / Plus Minus")

    fop = conn.query(f"SELECT left(player,length(array_to_string((string_to_array(player, ' '))[1:3], ' ')) + 2)"
                     f"       as \"   Player\" "
                     f"  FROM v_individual_scoring"
                     f" WHERE schedule_id = '{schedule_id}' "
                     f" ORDER BY left(player::text, POSITION(('-'::text) IN (player)) - 2)::integer", ttl="5")

    player_checkbox = st.multiselect("Filter on Player(s)", fop)
    player_checkbox.sort(key=lambda x: int(x.split(" -")[0]))

    # Define the common part of the query
    common_query = (
        f"SELECT \"Lineup\", \"   +/-\", \"Team Points\", \"Free Throws\", \"   2s\", "
        f"\"   3s\", \"Opponent Points\" "
        f"FROM v_lineup_scoring "
        f"WHERE \"Opponent\" = '{opponent_team}' || ' (' || '{game_date}' || ')'"
    )

    # Conditionally add the extra AND statement
    if len(player_checkbox) > 0:
        chk_result = '%' + '%'.join(player_checkbox) + '%'
        query = common_query + f" AND \"Lineup\" LIKE '{chk_result}'"
    else:
        query = common_query

    # Execute the query
    lspm = conn.query(query, ttl="5")

    # Display the result
    st.dataframe(lspm)


if __name__ == "__main__":
    main()
