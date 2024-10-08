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
    col_blank1, col_mascot, col_blank2 = st.columns(3)

    # My Team
    # mt = conn.query("SELECT DISTINCT team FROM schedule s;", ttl="10m")

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

    tid = conn.query(f"SELECT team_id FROM team WHERE team_name = '{my_team}' "
                     f"   AND team_level = '{my_level}'"
                     f"   AND season = '{my_season}' ;", ttl="10m")

    team_id = int(tid['team_id'].iloc[0])

    mascot = ut.my_mascot_fn(team_id)

    with col_mascot:
        st.write(f'<span style="color: yellow; font-weight: 600; text-align: center; display: block; '
                 f'font-size: 40px;">{mascot}</span>', unsafe_allow_html=True)

    # My Team's Players (don't think this is being used 20240818)
    # df = conn.query(f"SELECT jersey_number || ' - ' || left(full_name, length(right(full_name, "
    #                 f"       POSITION(' ' in full_name))) + 1) as player "
    #                 f"  FROM roster"
    #                 f" WHERE team_id = '{team_id}' ;", ttl="10m")

    # Opponent Team
    ot = conn.query(f"SELECT team "
                    f"  FROM v_opponents_list"
                    f" WHERE team_id = '{team_id}';", ttl="10m")

    st.write("")
    st.write("SUMMARY:&nbsp;&nbsp;&nbsp;Individual Scoring / Plus Minus")

    opponent_checkbox = st.multiselect("Filter Opponent(s)", ot)
    opponent_checkbox.sort(key=lambda x: x[1])
    tchk_result = '|'.join(opponent_checkbox)
    tchk_result_fmt = tchk_result.replace("'", "''").replace("|", "', '")

    ispm_before = (
        f"select pts.player as \"Player\", "
        f"    sum(coalesce(pts_tot.points,0)) as \"Total Points\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(pts_tot.points,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"Points Per Game\", "
        f"	   coalesce(sum(vis.points_for), 0) - "
        f"            coalesce(sum(abs(vis.points_against)), 0) as \"Overall +/-\", "
        f"	   round((coalesce(sum(vis.points_for), 0) - "
        f"            coalesce(sum(abs(vis.points_against)), 0))::numeric/"
        f"            count(distinct pts.schedule_id), 1) as \"+/- Per Game\",  "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(m_fts,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"FTs Per Game\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(m_2s,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"2s Per Game\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(m_3s,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"3s Per Game\", "
        f"	   coalesce(sum(vis.points_for), 0) as \"Team Points For\", "
        f"	   coalesce(sum(abs(vis.points_against)), 0) as \"Team Points Against\", "
        f"	   count(distinct vis.schedule_id) as \"Games Played\", "
        f"	   string_agg(((vis.opponent::text || ' ('::text) || sched.game_date::text) ||"
        f"            ')'::text, ';  '::text) as \"Opponents\" "
        f"  from (select distinct player, schedule_id from public.stat_log) pts "
        f"  join public.schedule sched "
        f"    on pts.schedule_id = sched.schedule_id "
        f"  join (select * from v_individual_scoring order by player, opponent) vis "
        f"   	on pts.player = vis.player "
        f"  	and pts.schedule_id = vis.schedule_id "
        f"  left join public.v_points_individual pts_tot "
        f"   	on pts.player = pts_tot.player "
        f"  	and pts.schedule_id = pts_tot.schedule_id "
        f"  left join v_points_individual_for_summary pos "
        f"   	on pts.player = pos.player "
        f"  left join v_points_individual_against_summary neg "
        f"   	on pts.player = neg.player "
        f" where sched.team_id = '{team_id}' ")

    ispm_after = (
        f" group by pts.player, pos.points_for, abs(neg.points_against), "
        f"        coalesce(pos.teams_played, neg.teams_played) "
        f" order by avg(coalesce(pts_tot.points,0)) desc, "
        f"        left(pts.player, POSITION('-' in pts.player) - 2)::int4 ")

    if len(opponent_checkbox) > 0:
        ispm_conditional = (
            f"   and (SELECT DISTINCT ((sched.opponent::text || ' ('::text) ||"
            f"        sched.game_date::text) || ')'::text) in ('{tchk_result_fmt}') "
        )
    else:
        ispm_conditional = ""

    ispm_query = ispm_before + ispm_conditional + ispm_after

    ispm = conn.query(ispm_query,  ttl="5")

    st.dataframe(ispm)

    st.write("")
    st.write("")
    st.write(f"SUMMARY:&nbsp;&nbsp;&nbsp;Lineup Scoring / Plus Minus")

    lspm_query = (f'SELECT "Lineup", '
                  f'"   +/-",'
                  f'"Team Points", '
                  f'"Free Throws", '
                  f'"   2s",'
                  f'"   3s",'
                  f'"Opponent Points", '
                  f'"Games", '
                  f'"Opponent(s)"'
                  f'  FROM v_lineup_scoring_summary'
                  f' WHERE "Team ID" = {team_id} ;')

    # st.write(lspm_query)

    lspm = conn.query(lspm_query,  ttl="5")

    # st.dataframe(lspm)


    dynamic_filters = ut.DynamicFilters(df=lspm, filters=['Lineup', 'Opponent(s)'], contains_filter=['Lineup'])
    dynamic_filters.display_filters(location='columns', num_columns=1, gap='large')
    dynamic_filters.display_df()


if __name__ == "__main__":
    main()
