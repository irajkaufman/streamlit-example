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

    # My Team
    mt = conn.query("SELECT DISTINCT team FROM schedule s;", ttl="10m")

    # Opponent Team
    ot = conn.query(f"select team "
                    f"  from v_opponents_list;", ttl="10m")

    with col_a:
        my_team = st.selectbox("My Team", mt)

    # My Team's Players
    df = conn.query(f"SELECT jersey_number || ' - ' || left(full_name, length(right(full_name, "
                    f"POSITION(' ' in full_name))) + 1) as player FROM roster where team = '{my_team}';", ttl="10m")

    st.write("")
    st.write("Individual Scoring Summary")

    opponent_checkbox = st.multiselect("Filter on Opponent(s)", ot)
    opponent_checkbox.sort(key=lambda x: x[1])
    tchk_result = '|'.join(opponent_checkbox)
    tchk_result_fmt = tchk_result.replace("'", "''").replace("|", "', '")

    ispm_before = (
        f"select pts.player as \"Player\", "
        f"    sum(coalesce(pts_tot.points,0)) as \"Total Points\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(pts_tot.points,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"Points Per Game\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(m_fts,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"FTs Per Game\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(m_2s,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"2s Per Game\", "
        f"	case when sum(coalesce(pts_tot.points,0)) = 0 then 0 "
        f"	   else round(sum(coalesce(m_3s,0))::numeric/"
        f"            count(distinct vis.schedule_id), 1) end as \"3s Per Game\", "
        f"	   coalesce(sum(vis.points_for), 0) - "
        f"            coalesce(sum(abs(vis.points_against)), 0) as \"Overall +/-\", "
        f"	   round((coalesce(sum(vis.points_for), 0) - "
        f"            coalesce(sum(abs(vis.points_against)), 0))::numeric/"
        f"            count(distinct pts.schedule_id), 1) as \"+/- Per Game\",  "
        f"	   coalesce(sum(vis.points_for), 0) as \"Team Points For\", "
        f"	   coalesce(sum(abs(vis.points_against)), 0) as \"Team Points Against\", "
        f"	   count(distinct vis.schedule_id) as \"Games Played\", "
        f"	   string_agg(((vis.opponent::text || ' ('::text) || sched.game_date::text) ||"
        f"            ')'::text, ';  '::text) as \"Opponents\" "
        f"  from (select distinct player, schedule_id from public.scoring) pts "
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
        f"   	on pts.player = neg.player ")

    ispm_after = (
        f" group by pts.player, pos.points_for, abs(neg.points_against), "
        f"        coalesce(pos.teams_played, neg.teams_played) "
        f" order by avg(coalesce(pts_tot.points,0)) desc, "
        f"        left(pts.player, POSITION('-' in pts.player) - 2)::int4 ")

    if len(opponent_checkbox) > 0:
        ispm_conditional = (
            f" where (SELECT DISTINCT ((sched.opponent::text || ' ('::text) ||"
            f"        sched.game_date::text) || ')'::text) in ('{tchk_result_fmt}') "
        )
    else:
        ispm_conditional = ""

    ispm_query = ispm_before + ispm_conditional + ispm_after

    ispm = conn.query(ispm_query,  ttl="5")

    st.dataframe(ispm)

    st.write("")
    st.write("")
    st.write("Lineup Scoring / Plus Minus")

    col_d, col_e = st.columns(2)

    # Opponent Team for Lineup Summary
    ots = conn.query(f"select team "
                     f"  from v_opponents_list;", ttl="10m")

    with col_d:
        player_checkbox = st.multiselect("Filter on Player(s)", df)
        player_checkbox.sort(key=lambda x: int(x.split(" -")[0]))

    with col_e:
        opp_sum_checkbox = st.multiselect("Opponent(s)", ots)
        opp_sum_checkbox.sort(key=lambda x: x[1])
        tchk_sum_result = '|'.join(opp_sum_checkbox)
        tchk_sum_result_fmt = tchk_sum_result.replace("'", "''").replace("|", "', '")

    if len(opp_sum_checkbox) > 0:
        ispm_conditional2 = (
            f" where \"Opponent(s)\" in ('{tchk_sum_result_fmt}') "
        )
    else:
        ispm_conditional2 = ""

    lspm_before = (f"SELECT * "
                   f"  FROM v_lineup_scoring_summary")

    if len(player_checkbox) > 0:
        pchk_result = '%' + '%'.join(player_checkbox) + '%'
        lspm_conditional = f" WHERE \"Lineup\" like '{pchk_result}' "
        if len(opp_sum_checkbox) > 0:
            ispm_conditional2 = (
                f" and \"Opponent(s)\" in ('{tchk_sum_result_fmt}') "
            )
        else:
            ispm_conditional2 = ""
    else:
        lspm_conditional = ""

    lspm_query = lspm_before + lspm_conditional + ispm_conditional2

    lspm = conn.query(lspm_query,  ttl="5")

    st.dataframe(lspm)


if __name__ == "__main__":
    main()
