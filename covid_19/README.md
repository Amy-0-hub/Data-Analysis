# COVID-19 in the U.S.: Exploratory Data Analysis & Visualization

This project analyzes the spread and control of COVID-19 in the United States using public datasets([Johns Hopkins CSSE COVID-19 Data]**https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data**). Spcifically, the project addresses the following research questions:


### Research Questions
1. **Trend Analysis:** How did the confirmed COVID-19 cases and death trends change over time in different states?
2. **Stage-wise Distribution:** What is the distribution of confirmed cases across different states during the early, middle, and late stages of an epidemic? 
3. **Testing and Case Detection:** Does increased COVID-19 testing lead to more confirmed cases?


## Dataset

The dataset is sourced from the **CSSEGISandData** repository maintained by Johns Hopkins Univeristy. Specifically, the `csse_covid_19_daily_reports_us` folder provides daily reports for each U.S. state. Sample dataset columns:
- Province_State: The name of the State within the USA
- Confirmed: Cumulative number of confirmed cases
- Deaths: Cumulative number of deaths
- Date: Date of the report

> The dataset includes many other columns. Only the most relevant ones for this project are listed above.


## Stage Definition

To analyze state-wise case distributions over time, the dataset is dividedd into three pandemic stages based on the timeline:

- **Early Stage:** First 1/3 of the time period
- **Mid Stage:** Second 1/3 of the time period
- **Late Stage:** Last 1/3 of the time period

This division allows comparison of how the pandemic evolved geographical in different time frames.



## Processing Steps

1. **Data clean and data preprocessing**
    - Handle missing values
    - Drop unnecessary columns
    - Convert and sort datetime columns

2. **Explore Data Analysis (EDA)**
    - Understand trends and distributions
    - Examine correlations between testing and cases

3. **Interactive Dashboard Development**
    Built with Streamlit, featuring:
    - Line chart for case & death trends (Q1)
    - Choropleth map for stage-wise confirmed case distribution (Q2)
    - Scatter plot for testing vs. confirmed cases (Q3)


## Built with
1. pandas
2. matplotlib
3. plotly
4. seaborn
5. streamlit


## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py