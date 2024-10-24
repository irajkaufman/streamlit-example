-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.ent_att_val_eav_id_seq;

CREATE SEQUENCE public.ent_att_val_eav_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;
-- DROP SEQUENCE public.schedule_new_sched_pk_seq;

CREATE SEQUENCE public.schedule_new_sched_pk_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;
-- DROP SEQUENCE public.scoring_new_scoring_id_seq;

CREATE SEQUENCE public.scoring_new_scoring_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;
-- DROP SEQUENCE public.stat_log_stat_log_id_seq;

CREATE SEQUENCE public.stat_log_stat_log_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;
-- DROP SEQUENCE public.team_team_id_seq;

CREATE SEQUENCE public.team_team_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;-- public.ent_att_val definition

-- Drop table

-- DROP TABLE public.ent_att_val;

CREATE TABLE public.ent_att_val (
    eav_id serial4 NOT NULL,
    eav_attribute text NULL,
    eav_value text NULL,
    eav_comments text NULL,
    cr_dt timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
    mod_dt timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL
);


-- public.roster_team_bkup definition

-- Drop table

-- DROP TABLE public.roster_team_bkup;

CREATE TABLE public.roster_team_bkup (
    jersey_number int4 NOT NULL,
    full_name varchar NOT NULL,
    team varchar NOT NULL
);


-- public.team definition

-- Drop table

-- DROP TABLE public.team;

CREATE TABLE public.team (
    team_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
    team_name varchar NULL,
    mascot varchar NULL,
    team_level varchar NULL,
    season varchar NULL,
    CONSTRAINT team_pkey PRIMARY KEY (team_id)
);


-- public.roster definition

-- Drop table

-- DROP TABLE public.roster;

CREATE TABLE public.roster (
    jersey_number int4 NOT NULL,
    full_name varchar NOT NULL,
    positions varchar NULL,
    active bool NULL,
    created_on timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    team_id int4 NULL,
    team varchar NULL,
    CONSTRAINT fk_roster_team_id FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.schedule definition

-- Drop table

-- DROP TABLE public.schedule;

CREATE TABLE public.schedule (
    schedule_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
    game_num int4 NOT NULL,
    opponent varchar NOT NULL,
    game_date date NOT NULL,
    day_of_week varchar NULL,
    game_time time NULL,
    tournament varchar NULL,
    game_location varchar NULL,
    team_score int4 NULL,
    opp_score int4 NULL,
    win_loss bool NULL,
    league_game bool NULL,
    season varchar NULL,
    team_level varchar NULL,
    team_win bool NULL,
    team_id int4 NULL,
    CONSTRAINT schedule_pk PRIMARY KEY (schedule_id),
    CONSTRAINT fk_schedule_team_id FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.scoring definition

-- Drop table

-- DROP TABLE public.scoring;

CREATE TABLE public.scoring (
    scoring_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
    player varchar NULL,
    points_scored int4 NULL,
    team varchar NULL,
    scorer bool NULL,
    video_time time NULL,
    created_date timestamp DEFAULT CURRENT_TIMESTAMP NULL,
    opponent_player varchar NULL,
    schedule_id int4 NULL,
    CONSTRAINT scoring_pkey PRIMARY KEY (scoring_id),
    CONSTRAINT fk_scoring_schedule_id FOREIGN KEY (schedule_id) REFERENCES public.schedule(schedule_id)
);


-- public.stat_log definition

-- Drop table

-- DROP TABLE public.stat_log;

CREATE TABLE public.stat_log (
    stat_log_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
    stat_name varchar NULL, -- "Free Throw", "2 points", "3 points", "Rebound", "Block", "Steal", "Turnover"
    team varchar NULL, -- same as in scoring table
    player varchar NULL, -- same as in scoring table
    contributor bool NULL, -- replaces scorer in scoring table
    stat_value int4 NULL, -- replaces points_scored in scoring table
    assist bool NULL, -- new field
    success bpchar(4) DEFAULT 'Make'::bpchar NULL, -- new field
    offense varchar DEFAULT 'Half Court'::character varying NULL, -- new field
    shot varchar DEFAULT 'Jumper'::character varying NULL, -- new field
    contested bool NULL, -- new field
    rebound varchar DEFAULT 'Defensive'::character varying NULL, -- new field
    opponent_player varchar NULL, -- same as in scoring table
    schedule_id int4 NULL, -- same as in scoring table
    video_time time NULL, -- same as in scoring table
    created_date timestamp DEFAULT CURRENT_TIMESTAMP NULL,
    CONSTRAINT stat_log_pkey PRIMARY KEY (stat_log_id),
    CONSTRAINT fk_stat_log_schedule_id FOREIGN KEY (schedule_id) REFERENCES public.schedule(schedule_id)
);

-- Column comments

COMMENT ON COLUMN public.stat_log.stat_name IS '"Free Throw", "2 points", "3 points", "Rebound", "Block", "Steal", "Turnover"';
COMMENT ON COLUMN public.stat_log.team IS 'same as in scoring table';
COMMENT ON COLUMN public.stat_log.player IS 'same as in scoring table';
COMMENT ON COLUMN public.stat_log.contributor IS 'replaces scorer in scoring table';
COMMENT ON COLUMN public.stat_log.stat_value IS 'replaces points_scored in scoring table';
COMMENT ON COLUMN public.stat_log.assist IS 'new field';
COMMENT ON COLUMN public.stat_log.success IS 'new field';
COMMENT ON COLUMN public.stat_log.offense IS 'new field';
COMMENT ON COLUMN public.stat_log.shot IS 'new field';
COMMENT ON COLUMN public.stat_log.contested IS 'new field';
COMMENT ON COLUMN public.stat_log.rebound IS 'new field';
COMMENT ON COLUMN public.stat_log.opponent_player IS 'same as in scoring table';
COMMENT ON COLUMN public.stat_log.schedule_id IS 'same as in scoring table';
COMMENT ON COLUMN public.stat_log.video_time IS 'same as in scoring table';


-- public.v_individual_scoring source

CREATE OR REPLACE VIEW public.v_individual_scoring
AS SELECT pts.player,
    COALESCE(pts_tot.points, 0::bigint) AS points_scored,
    COALESCE(pts_tot.m_fts, 0::bigint) AS made_fts,
    COALESCE(pts_tot.m_2s, 0::bigint) AS made_2s,
    COALESCE(pts_tot.m_3s, 0::bigint) AS made_3s,
    sum(pts.stat_value) AS plus_minus,
    COALESCE(lin_tot.points_for, 0::bigint) AS points_for,
    COALESCE(lin_tot.points_against, 0::bigint) AS points_against,
    sched.opponent,
    pts.schedule_id
   FROM stat_log pts
     JOIN schedule sched ON pts.schedule_id = sched.schedule_id
     LEFT JOIN v_points_individual pts_tot ON pts.player::text = pts_tot.player::text AND pts.schedule_id = pts_tot.schedule_id
     LEFT JOIN v_points_lineup lin_tot ON pts.player::text = lin_tot.player::text AND pts.schedule_id = lin_tot.schedule_id
  GROUP BY pts.player, (COALESCE(pts_tot.points, 0::bigint)), (COALESCE(pts_tot.m_fts, 0::bigint)), (COALESCE(pts_tot.m_2s, 0::bigint)), (COALESCE(pts_tot.m_3s, 0::bigint)), lin_tot.points_for, lin_tot.points_against, sched.opponent, pts.schedule_id
  ORDER BY sched.opponent, (sum(pts.stat_value)) DESC, ("left"(pts.player::text, "position"(pts.player::text, '-'::text) - 2)::integer);


-- public.v_lineup_scoring source

CREATE OR REPLACE VIEW public.v_lineup_scoring
AS SELECT team.on_floor AS "Lineup",
    sum(team.stat_value) AS "   +/-",
    COALESCE(sum(team.stat_value) FILTER (WHERE team.stat_value > 0), 0::bigint) AS "Team Points",
    count(*) FILTER (WHERE team.stat_value = 1) AS "Free Throws",
    count(*) FILTER (WHERE team.stat_value = 2) AS "   2s",
    count(*) FILTER (WHERE team.stat_value = 3) AS "   3s",
    COALESCE(sum(team.stat_value) FILTER (WHERE team.stat_value < 0) * '-1'::integer, 0::bigint) AS "Opponent Points",
    team.opponent AS "Opponent",
    team.team_id AS "Team ID"
   FROM ( SELECT DISTINCT pts.video_time,
            string_agg(pts.player, ', '::text) AS on_floor,
            pts.stat_value,
            ((sched.opponent::text || ' ('::text) || sched.game_date::text) || ')'::text AS opponent,
            sched.team_id
           FROM ( SELECT DISTINCT s.video_time,
                    "left"(s.player::text, length(array_to_string((string_to_array(s.player::text, ' '::text))[1:3], ' '::text)) + 2) AS player,
                    "left"(s.player::text, "position"(s.player::text, '-'::text) - 2)::integer AS jersey_number,
                    s.stat_value,
                    s.schedule_id,
                    sc.team_id
                   FROM stat_log s
                     JOIN schedule sc ON s.schedule_id = sc.schedule_id
                  WHERE (s.stat_name::text = ANY (ARRAY['Basket'::character varying::text, 'Free Throw'::character varying::text])) AND s.success = 'Make'::bpchar
                  ORDER BY sc.team_id, s.schedule_id, s.video_time, ("left"(s.player::text, "position"(s.player::text, '-'::text) - 2)::integer)) pts
             JOIN schedule sched ON pts.schedule_id = sched.schedule_id
          GROUP BY pts.video_time, pts.stat_value, (((sched.opponent::text || ' ('::text) || sched.game_date::text) || ')'::text), sched.team_id
          ORDER BY (((sched.opponent::text || ' ('::text) || sched.game_date::text) || ')'::text), pts.video_time) team
  GROUP BY team.on_floor, team.opponent, team.team_id
  ORDER BY team.opponent, (COALESCE(sum(team.stat_value) FILTER (WHERE team.stat_value > 0), 0::bigint)) DESC;


-- public.v_lineup_scoring_summary source

CREATE OR REPLACE VIEW public.v_lineup_scoring_summary
AS SELECT v_lineup_scoring."Lineup",
    sum(v_lineup_scoring."   +/-") AS "   +/-",
    sum(v_lineup_scoring."Team Points") AS "Team Points",
    sum(v_lineup_scoring."Free Throws") AS "Free Throws",
    sum(v_lineup_scoring."   2s") AS "   2s",
    sum(v_lineup_scoring."   3s") AS "   3s",
    sum(v_lineup_scoring."Opponent Points") AS "Opponent Points",
    count(DISTINCT v_lineup_scoring."Opponent") AS "Games",
    string_agg(v_lineup_scoring."Opponent", ';  '::text) AS "Opponent(s)",
    v_lineup_scoring."Team ID"
   FROM v_lineup_scoring
  GROUP BY v_lineup_scoring."Lineup", v_lineup_scoring."Team ID"
  ORDER BY (sum(v_lineup_scoring."   +/-")) DESC, (sum(v_lineup_scoring."Team Points")) DESC, (sum(v_lineup_scoring."   3s")) DESC, (sum(v_lineup_scoring."   2s")) DESC, (sum(v_lineup_scoring."Free Throws")) DESC, (string_agg(v_lineup_scoring."Opponent", ', '::text));


-- public.v_opponents_list source

CREATE OR REPLACE VIEW public.v_opponents_list
AS SELECT DISTINCT ((sch.opponent::text || ' ('::text) || sch.game_date::text) || ')'::text AS team,
    sch.team_id
   FROM schedule sch
  WHERE (EXISTS ( SELECT 1
           FROM scoring sco
          WHERE sch.schedule_id = sco.schedule_id))
  ORDER BY (((sch.opponent::text || ' ('::text) || sch.game_date::text) || ')'::text);


-- public.v_points_individual source

CREATE OR REPLACE VIEW public.v_points_individual
AS SELECT pts.player,
    sum(pts.stat_value) AS points,
    count(*) FILTER (WHERE pts.stat_value = 1) AS m_fts,
    count(*) FILTER (WHERE pts.stat_value = 2) AS m_2s,
    count(*) FILTER (WHERE pts.stat_value = 3) AS m_3s,
    sched.schedule_id,
    sched.opponent
   FROM stat_log pts
     JOIN schedule sched ON pts.schedule_id = sched.schedule_id
  WHERE pts.contributor = true AND (pts.stat_name::text = ANY (ARRAY['Basket'::character varying::text, 'Free Throw'::character varying::text])) AND pts.success = 'Make'::bpchar
  GROUP BY pts.player, sched.schedule_id, sched.opponent;


-- public.v_points_individual_against source

CREATE OR REPLACE VIEW public.v_points_individual_against
AS SELECT pts_neg.player,
    sum(pts_neg.stat_value) AS points_against,
    sched_neg.schedule_id,
    sched_neg.opponent
   FROM stat_log pts_neg
     JOIN schedule sched_neg ON pts_neg.schedule_id = sched_neg.schedule_id
  WHERE pts_neg.stat_value < 0 AND (pts_neg.stat_name::text = ANY (ARRAY['Basket'::character varying, 'Free Throw'::character varying]::text[])) AND pts_neg.success = 'Make'::bpchar
  GROUP BY pts_neg.player, sched_neg.schedule_id, sched_neg.opponent;


-- public.v_points_individual_against_summary source

CREATE OR REPLACE VIEW public.v_points_individual_against_summary
AS SELECT va.player,
    sum(va.points_against) AS points_against,
    string_agg(((sc.opponent::text || ' ('::text) || sc.game_date::text) || ')'::text, ';  '::text) AS teams_played
   FROM ( SELECT v_points_individual_against.player,
            v_points_individual_against.points_against,
            v_points_individual_against.schedule_id,
            v_points_individual_against.opponent
           FROM v_points_individual_against
          ORDER BY v_points_individual_against.player, v_points_individual_against.opponent) va
     JOIN schedule sc ON va.schedule_id = sc.schedule_id
  GROUP BY va.player;


-- public.v_points_individual_for source

CREATE OR REPLACE VIEW public.v_points_individual_for
AS SELECT pts_pos.player,
    sum(pts_pos.stat_value) AS points_for,
    sched_pos.schedule_id,
    sched_pos.opponent
   FROM stat_log pts_pos
     JOIN schedule sched_pos ON pts_pos.schedule_id = sched_pos.schedule_id
  WHERE pts_pos.stat_value > 0 AND (pts_pos.stat_name::text = ANY (ARRAY['Basket'::character varying, 'Free Throw'::character varying]::text[])) AND pts_pos.success = 'Make'::bpchar
  GROUP BY pts_pos.player, sched_pos.schedule_id, sched_pos.opponent;


-- public.v_points_individual_for_summary source

CREATE OR REPLACE VIEW public.v_points_individual_for_summary
AS SELECT vf.player,
    sum(vf.points_for) AS points_for,
    string_agg(((sc.opponent::text || ' ('::text) || sc.game_date::text) || ')'::text, ';  '::text) AS teams_played
   FROM ( SELECT v_points_individual_for.player,
            v_points_individual_for.points_for,
            v_points_individual_for.schedule_id,
            v_points_individual_for.opponent
           FROM v_points_individual_for
          ORDER BY v_points_individual_for.player, v_points_individual_for.opponent) vf
     JOIN schedule sc ON vf.schedule_id = sc.schedule_id
  GROUP BY vf.player;


-- public.v_points_individual_summary source

CREATE OR REPLACE VIEW public.v_points_individual_summary
AS SELECT vf.player,
    sum(vf.points_for) AS points_for,
    sum(vf.points_against) AS points_against,
    string_agg(((sc.opponent::text || ' ('::text) || sc.game_date::text) || ')'::text, ';  '::text) AS teams_played
   FROM ( SELECT vpl.player,
            vpl.points_for,
            vpl.points_against,
            vpl.schedule_id,
            vpl.opponent
           FROM v_points_lineup vpl
          ORDER BY vpl.player, vpl.opponent) vf
     JOIN schedule sc ON vf.schedule_id = sc.schedule_id
  GROUP BY vf.player;


-- public.v_points_lineup source

CREATE OR REPLACE VIEW public.v_points_lineup
AS SELECT pts.player,
    COALESCE(sum(pts.stat_value) FILTER (WHERE COALESCE(pts.stat_value, 0) >= 0), 0::bigint) AS points_for,
    COALESCE(sum(abs(pts.stat_value)) FILTER (WHERE COALESCE(pts.stat_value, 0) <= 0), 0::bigint) AS points_against,
    sched.schedule_id,
    sched.opponent
   FROM stat_log pts
     JOIN schedule sched ON pts.schedule_id = sched.schedule_id
  WHERE (pts.stat_name::text = ANY (ARRAY['Basket'::character varying::text, 'Free Throw'::character varying::text])) AND pts.success = 'Make'::bpchar
  GROUP BY pts.player, sched.schedule_id, sched.opponent;


-- public.v_rebounds_individual source

CREATE OR REPLACE VIEW public.v_rebounds_individual
AS SELECT pts_tot.player,
    sum(pts_tot.stat_value) AS total_rebounds,
    count(*) FILTER (WHERE pts_tot.rebound::text = 'Defensive'::text) AS defensive_rebounds,
    count(*) FILTER (WHERE pts_tot.rebound::text = 'Offensive'::text) AS offensive_rebounds,
    sched_tot.schedule_id,
    sched_tot.opponent
   FROM stat_log pts_tot
     JOIN schedule sched_tot ON pts_tot.schedule_id = sched_tot.schedule_id
  WHERE pts_tot.contributor = true AND pts_tot.stat_name::text = 'Rebound'::text
  GROUP BY pts_tot.player, sched_tot.schedule_id, sched_tot.opponent;