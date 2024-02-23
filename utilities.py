import streamlit as st
from sqlalchemy import create_engine, text

# Initialize connection.
conn = st.connection("postgresql", type="sql")


def level_header(schedule_id):
    level = conn.query(f"select team_level from schedule where schedule_id = {schedule_id};", ttl="5")
    team_level_value = level.iloc[0, 0]
    team_level = str(team_level_value)

    # Define the label and value with HTML formatting
    level_label_html = f'<span style="font-size: 15px;">Level</span>'
    level_value_html = f'<span style="color: yellow; font-weight: 600; font-size: 24px;">{team_level}</span>'

    # Combine the label and value HTML
    metric_html = f'<div>{level_label_html}</div><div>{level_value_html}</div>'

    # Display the formatted HTML using st.html
    st.write(metric_html, unsafe_allow_html=True)
    st.write("")


def season_header(schedule_id):
    season = conn.query(f"select season from schedule where schedule_id = {schedule_id};", ttl="5")
    team_season_value = season.iloc[0, 0]
    team_season = str(team_season_value)

    # Define the label and value with HTML formatting
    season_label_html = f'<span style="font-size: 15px;">Season</span>'
    season_value_html = f'<span style="color: yellow; font-weight: 600; font-size: 24px;">{team_season}</span>'

    # Combine the label and value HTML
    metric_html = f'<div>{season_label_html}</div><div>{season_value_html}</div>'

    # Display the formatted HTML using st.html
    st.write(metric_html, unsafe_allow_html=True)
