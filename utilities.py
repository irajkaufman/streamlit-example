import streamlit as st
from streamlit.errors import StreamlitAPIException
import pandas as pd
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


def my_mascot_fn(team_id):
    m = conn.query(f"SELECT mascot as my_mascot FROM team WHERE team_id = {team_id} ;", ttl="10m")

    if not m.empty:
        mascot = m['my_mascot'].iloc[0]
        return mascot
    else:
        return None


def my_points_fn(schedule_id):
    mp = conn.query(f"select sum(points_scored) as my_team_points"
                    f"  from ("
                    f"select distinct p.video_time, p.points_scored"
                    f"  from scoring p"
                    f"  join schedule s"
                    f"    on p.schedule_id = s.schedule_id"
                    f" where points_scored > 0"
                    f"   and p.schedule_id = {schedule_id}) mtp;", ttl="5")

    if not mp.empty:
        my_points = mp['my_team_points'].iloc[0]
        return my_points
    else:
        return None


def opponent_points_fn(schedule_id):
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
        opponent_points = op['opponent_team_points'].iloc[0]
        return opponent_points
    else:
        return None


class DynamicFilters:
    """
    A class to create dynamic multi-select filters in Streamlit.

    ...

    Attributes
    ----------
    df : DataFrame
        The dataframe on which filters are applied.
    filters : dict
        Dictionary with filter names as keys and their selected values as values.

    Methods
    -------
    check_state():
        Initializes the session state with filters if not already set.
    filter_df(except_filter=None):
        Returns the dataframe filtered based on session state excluding the specified filter.
    display():
        Renders the dynamic filters and the filtered dataframe in Streamlit.
    """

    def __init__(self, df, filters, filters_name='filters', contains_filter=None):
        """
        Constructs all the necessary attributes for the DynamicFilters object.

        Parameters
        ----------
            df : DataFrame
                The dataframe on which filters are applied.
            filters : list of filters
                List of columns names in df for which filters are to be created.
            filters_name: str, optional
                Name of the filters object in session state.
        """
        self.df = df
        self.filters_name = filters_name
        self.filters = {filter_name: [] for filter_name in filters}
        self.check_state()
        self.contains_filter = contains_filter

    def check_state(self):
        """Initializes the session state with filters if not already set."""
        # if 'filters' not in st.session_state:
        #     st.session_state.filters = self.filters
        if self.filters_name not in st.session_state:
            st.session_state[self.filters_name] = self.filters

    def filter_df(self, except_filter=None):
        """
        Filters the dataframe based on session state values except for the specified filter.

        Parameters
        ----------
            except_filter : str, optional
                The filter name that should be excluded from the current filtering operation.

        Returns
        -------
            DataFrame
                Filtered dataframe.
        """
        filtered_df = self.df.copy()
        for key, values in st.session_state[self.filters_name].items():
            if key != except_filter and values:
                if key in self.contains_filter:
                    # pattern = "|".join(values)
                    # filtered_df = filtered_df[filtered_df[key].str.contains(pattern, regex=True)]
                    for value in values:
                        filtered_df = filtered_df[filtered_df[key].str.contains(value)]
                else:
                    filtered_df = filtered_df[filtered_df[key].isin(values)]

        return filtered_df

    def display_filters(self, location=None, num_columns=0, gap="small"):
        """
            Renders dynamic multiselect filters for user selection.

            Parameters:
            -----------
            location : str, optional
                The location where the filters are to be displayed. Accepted values are:
                - 'sidebar': Displays filters in the side panel of the application.
                - 'columns': Displays filters in columns format in the main application area.
                - None: Defaults to main application area without columns.
                Default is None.

            num_columns : int, optional
                The number of columns in which filters are to be displayed when location is set to 'columns'.
                Constraints:
                - Must be an integer.
                - Must be less than or equal to 8.
                - Must be less than or equal to the number of filters + 1.
                If location is 'columns', this value must be greater than 0.
                Default is 0.

            gap : str, optional
                Specifies the gap between columns when location is set to 'columns'. Accepted values are:
                - 'small': Minimal gap between columns.
                - 'medium': Moderate gap between columns.
                - 'large': Maximum gap between columns.
                Default is 'small'.

            Behavior:
            ---------
            - The function iterates through session-state filters.
            - For each filter, the function:
                1. Generates available filter options based on the current dataset.
                2. Displays a multiselect box for the user to make selections.
                3. Updates the session state with the user's selection.
            - If any filter value changes, the application triggers an update to adjust other filter options based on the current selection.
            - If a user's previous selection is no longer valid based on the dataset, it's removed.
            - If any filters are updated, the application will rerun for the changes to take effect.

            Exceptions:
            -----------
            Raises StreamlitAPIException if the provided arguments don't meet the required constraints.

            Notes:
            ------
            The function uses Streamlit's session state to maintain user's selections across reruns.
            """
        # error handling
        if location not in ['sidebar', 'columns', None]:
            raise StreamlitAPIException("location must be either 'sidebar' or 'columns'")
        # if num_columns is not integer
        if not isinstance(num_columns, int):
            raise StreamlitAPIException("num_columns must be an integer")
        # if num_columns is greater than 8
        if num_columns > 8:
            raise StreamlitAPIException("num_columns must be less than or equal to 8")
        # if num_columns is greater than the number of filters
        if num_columns > len(st.session_state[self.filters_name]) + 1:
            raise StreamlitAPIException("num_columns must be less than or equal to the number of filters")
        # if location is column and num_columns is 0
        if location == 'columns' and num_columns == 0:
            raise StreamlitAPIException("num_columns must be greater than 0 when location is 'columns'")
        if gap not in ['small', 'medium', 'large']:
            raise StreamlitAPIException("gap must be either 'small', 'medium' or 'large'")

        filters_changed = False

        # initiate counter and max_value for columns
        if location == 'columns' and num_columns > 0:
            counter = 1
            max_value = num_columns
            col_list = st.columns(num_columns, gap=gap)

        for filter_name in st.session_state[self.filters_name].keys():
            filtered_df = self.filter_df(filter_name)
            filtered_df[filter_name] = filtered_df[filter_name].str.split(', ')
            if filter_name in self.contains_filter:
                try:
                    print("What??")
                    # Split the column values on the hyphen ('-')
                    # filtered_df['sort_columns'] = filtered_df[filter_name].str.split(' - ', expand=True)[0]
                    filtered_df = filtered_df.explode(filter_name)
                    filtered_df[['sort_col_num', 'sort_col_name']] = \
                        filtered_df[filter_name].str.split(pat=' - ', expand=True)  # [0].astype(int)

                    print("What 2??")
                    # st.write(filtered_df['sort_columns'], filtered_df[filter_name])

                    # Convert the resulting strings to numeric values
                    filtered_df['sort_col_num'] = pd.to_numeric(filtered_df['sort_col_num'])
                    print("What 3??")

                    filtered_df = filtered_df.sort_values(by=['sort_col_num'])
                    print("What 4??")
                    # st.write(filtered_df)
                except:
                    filtered_df = filtered_df.explode(filter_name).sort_values(by=[filter_name])
            else:
                filtered_df = filtered_df.explode(filter_name).sort_values(by=[filter_name])
            # options = tuple(filtered_df[filter_name].str.split(',')).unique().tolist()
            # st.write(filtered_df)
            options = filtered_df[filter_name].unique().tolist()

            # Remove selected values that are not in options anymore
            valid_selections = [v for v in st.session_state[self.filters_name][filter_name] if v in options]
            if valid_selections != st.session_state[self.filters_name][filter_name]:
                st.session_state[self.filters_name][filter_name] = valid_selections
                filters_changed = True

            if location == 'sidebar':
                with st.sidebar:
                    selected = st.multiselect(f"Filter {filter_name}", options,
                                              default=st.session_state[self.filters_name][filter_name])
            elif location == 'columns' and num_columns > 0:
                with col_list[counter - 1]:
                    selected = st.multiselect(f"Filter {filter_name}", options,
                                              default=st.session_state[self.filters_name][filter_name])

                # increase counter and reset to 1 if max_value is reached
                counter += 1
                counter = counter % (max_value + 1)
                if counter == 0:
                    counter = 1
            else:
                selected = st.multiselect(f"Filter {filter_name}", options,
                                          default=st.session_state[self.filters_name][filter_name])

            if selected != st.session_state[self.filters_name][filter_name]:
                st.session_state[self.filters_name][filter_name] = selected
                filters_changed = True

        if filters_changed:
            st.rerun()

    def display_df(self, **kwargs):
        """Renders the filtered dataframe in the main area."""
        # Display filtered DataFrame
        st.dataframe(self.filter_df(), **kwargs)
