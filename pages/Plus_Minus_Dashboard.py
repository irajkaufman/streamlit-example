import streamlit as st
from sqlalchemy import create_engine, text

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

    col_a, col_b, col_c = st.columns(3)
    col_m, col_o, col_z = st.columns(3)

    # My Team
    mt = conn.query("SELECT DISTINCT team FROM schedule s;", ttl="10m")

    # Opponent Team
    ot = conn.query(f"select distinct sched.opponent "
                    f"  from public.scoring pts "
                    f"  join public.schedule sched "
                    f"    on pts.schedule_id = sched.schedule_id;", ttl="10m")

    with col_a:
        my_team = st.selectbox("My Team", mt)

    with col_b:
        # opponent_team = st.selectbox("Opponent Team", ot)
        opp_team = st.selectbox("Opponent Team", ot)
        opponent_team = opp_team.replace("'", "''")

    # My Team's Players
    df = conn.query(f"SELECT jersey_number || ' - ' || left(full_name, length(right(full_name, "
                    f"POSITION(' ' in full_name))) + 1) as player FROM roster where team = '{my_team}';", ttl="10m")

    gd = conn.query(f"SELECT DISTINCT game_date FROM schedule where team = '{my_team}' "
                    f"and opponent = '{opponent_team}';", ttl="10m")

    # Opponent's Team's Players
    df_opp = conn.query(f"SELECT jersey_number || ' - ' || full_name as player "
                        f"FROM roster "
                        f"where team = '{opponent_team}' "
                        f"and active = True "
                        f"order by jersey_number;", ttl="10m")

    with col_c:
        game_date = st.selectbox("Game Date", gd)

    sid = conn.query(f"SELECT schedule_id FROM schedule WHERE team = '{my_team}' "
                     f"and opponent = '{opponent_team}' and game_date = '{game_date}';", ttl="10m")

    # if not sid.empty:
    # Extract the 'schedule_id' column
    schedule_id = int(sid['schedule_id'].iloc[0])

    # Display the extracted values
    # st.write(f"Captured schedule_ids: {schedule_id}")

    mp_query = (f"select sum(points_scored) as my_team_points"
                f"  from ("
                f"select distinct p.video_time, p.points_scored"
                f"  from scoring p"
                f"  join schedule s"
                f"    on p.schedule_id = s.schedule_id"
                f" where points_scored > 0"
                f"   and s.schedule_id = '{schedule_id}') m;")

    mp = conn.query(mp_query, ttl="5")

    if not mp.empty:
        with col_m:
            my_points = mp['my_team_points'].iloc[0]
            st.write('### ', my_points)
    else:
        st.write('###')

    op_query = (f"select sum(points_scored)*-1 as opponent_team_points"
                f"  from ("
                f"select distinct p.video_time, p.points_scored"
                f"  from scoring p"
                f"  join schedule s"
                f"    on p.schedule_id = s.schedule_id"
                f" where points_scored < 0"
                f"   and s.schedule_id = '{schedule_id}') m;")

    op = conn.query(op_query, ttl="5")

    if not op.empty:
        with col_o:
            opponent_points = op['opponent_team_points'].iloc[0]
            st.write('### ', opponent_points)
    else:
        st.write('###')

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
