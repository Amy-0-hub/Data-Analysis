# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import os

# load data
def load_data():
    covid_19_folder_path = 'csse_covid_19_daily_reports_us'
    all_covid_19_files = []
    for files_name in os.listdir(covid_19_folder_path):
        if files_name.endswith('.csv'):
            files_path = os.path.join(covid_19_folder_path, files_name)
            df_files = pd.read_csv(files_path)
            all_covid_19_files.append(df_files)
    # all files are stored in all_covid_19_files, to make it more concise, let's combine all files and assign an index to identify each file's origin
    combined_df = pd.concat(all_covid_19_files, ignore_index = True)
    return combined_df

# Step 1: data clean and data preprocessing
def drop_columns(df):
    ## drop the unnecessary columns from dataframe
    columns_to_drop = ['Country_Region', 'Last_Update', 'Hospitalization_Rate', 'Case_Fatality_Ratio', 'UID', 'ISO3']
    df = df.drop(columns = columns_to_drop, errors = 'ignore')
    # handle missing values
    df = df.dropna(inplace = False)
    return df

def convert_cols(df):
    ## column ‘Date’ is converted to datetime and sort it
    df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
    df = df.sort_values(by = 'Date')
    return df

# step 2: explore and analyze the data
def add_columns(df):
    #add 'Stage' column
    stage_labels = []
    for stages, group in df.groupby('Province_State'):
        group = group.sort_values('Date')
        n = len(group)
        stages = ['Early Stage'] * (n // 3) + ['Mid Stage'] * (n // 3) + ['Last Stage'] * (n - 2 * (n // 3))
        stage_labels.extend(stages)
    df = df.sort_values(['Province_State', 'Date']).reset_index(drop = True)
    df['Stage'] = stage_labels
    # state abbreviation is to plot a map add 'state_abbr' column： State abbreviation for plotting a map based on states
    state_abbr = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
    df['State_Abbr'] = df['Province_State'].map(state_abbr)

    df_test_confirm = df[['Date', 'Total_Test_Results', 'Confirmed', 'Province_State']]
    df_test_confirm = df_test_confirm.dropna()
    return df, df_test_confirm

# step 3: build an interactive dashboard
def build_a_dashboard(df, df_test_confirm):
    # dashboard title
    st.title('COVID-19 in the U.S.: Data Analysis & Visualization')
    st.markdown('Explore the spread and control of COVID-19 in the United States.')
    ## sidebar filters
    st.sidebar.title('Filter Options:')
    choose_state = st.sidebar.selectbox('Select a state:', df['Province_State'].unique())
    choose_stage = st.sidebar.selectbox('Select a stage:', ['Early Stage', 'Mid Stage', 'Last Stage'])
    ## filter by state
    state_options = df[df['Province_State'] == choose_state]
    stage_options = df[df['Stage'] == choose_stage]
    df_test_confirm_state_option = df_test_confirm[df_test_confirm['Province_State'] == choose_state]
    ## key insights
    tab1, tab2, tab3 = st.tabs(['Trend over Time', 'State Summary', 'Test vs. Confirmed'])
    return choose_state, choose_stage, state_options, stage_options, df_test_confirm_state_option, tab1, tab2, tab3

## question 1: create a line chart to visualize the trend of confirmed COVID-19 cases and deaths over time for different states.
## the x-axis represents the datetime, and the y-axis shows the number of people (confirmed and deaths).
def create_tab1(tab1, choose_state, state_options):
    with tab1:
        st.header(f'Trend of COVID-19 Cases and Deaths in {choose_state}')
        fig1, ax1 = plt.subplots()
        plt.xticks(rotation=90)

        color1 = 'tab:red'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Number of confirmed COVID-19 cases', color = color1)
        line1 = ax1.plot(state_options['Date'], state_options['Confirmed'].fillna(0), label = 'confirmed cases', color = color1)
        ax1.tick_params(axis = 'y', labelcolor = color1)

        ax2 =ax1.twinx()

        color2 = 'tab:blue'
        ax2.set_ylabel('Number of deaths', color = color2)
        line2 = ax2.plot(state_options['Date'], state_options['Deaths'].fillna(0), label = 'deaths', color = color2)
        ax2.tick_params(axis = 'y', labelcolor = color2)

        line_1, label_1 = ax1.get_legend_handles_labels()
        line_2, label_2 = ax2.get_legend_handles_labels()
        combined = dict(zip(line_1 + line_2, label_1 + label_2))
        ax1.legend(combined.keys(), combined.values(), loc = 'upper left')
        st.pyplot(fig1)

## question 2: analyzing the distribution of confirmed cases across different states during three stages
def create_tab2(tab2, choose_stage,stage_options):
    with tab2:
        st.header(f'The Distribution of Confirmed Cases across different states in the {choose_stage}')
        fig2 = px.choropleth(
            stage_options,
            locations='State_Abbr',
            locationmode='USA-states',           
            color='Confirmed',         
            scope='usa',               
            color_continuous_scale='Viridis')
        st.plotly_chart(fig2, use_container_width=True)

## question 3: Does increased COVID-19 testing lead to more confirmed cases?
def create_tab3(tab3, choose_state, df_test_confirm_state_option):
    with tab3:
        st.header(f'Testing vs. Confirmed Cases in {choose_state}')
        fig3, ax = plt.subplots()
        sns.scatterplot(data = df_test_confirm_state_option,
                        x = 'Total_Test_Results',
                        y = 'Confirmed', 
                        ax = ax )
        ax.set_xlabel('Number of test')
        ax.set_ylabel('Number of confirmed Cases')
        ax.set_title('Does increased COVID-19 testing lead to more confirmed cases?')
        st.pyplot(fig3)

if __name__ == "__main__":
    combined_df = load_data()
    df1 = drop_columns(combined_df)
    df2 = convert_cols(df1)
    df3, df_test_confirm1 = add_columns(df2)
    choose_state1, choose_stage1, state_options1, stage_options1, df_test_confirm_state_option1, tab11, tab21, tab31= build_a_dashboard(df3, df_test_confirm1)
    create_tab1(tab11, choose_state1, state_options1)
    create_tab2(tab21, choose_stage1, stage_options1)
    create_tab3(tab31, choose_state1, df_test_confirm_state_option1)