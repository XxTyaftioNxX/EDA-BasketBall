import streamlit as st
import pandas as pd
import base64
import re

st.title('NBA Player Stats')
st.markdown("""
This app performs simple webscraping of NBA player stats 
* **Made using Python and Streamlit**
* **Data Taken From [Basketball-reference.com](https://www.basketball-reference.com/) **
* **Lets user download csv file of the selected stats**
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))

#Performing WebScraping
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk', 'FG%', '3P%', '2P%', 'eFG%', 'FT%', 'GS', 'TOV', 
                            '2PA', '3PA', 'FTA', 'FGA', 'ORB', 'DRB' ], axis=1)
    return playerstats, df

playerstats, df = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos)

#SideBar - Stat selection
different_stats = ['Games Started(GS)', 'Turnover Percentage(TOV)', 'Effective Field Goal Percentage(eFG%)', 
                    '2-Point Attempts(2PA)', '3-Point Attempts(3PA)', 'Free Throw Attempts (FTA)', 'Field Goal Attempts (FGA)',
                    'Offensive Rebounds (ORB)', 'Defensive Rebounds (DRB)']
additional_stats = st.sidebar.multiselect('Additional Stats', different_stats)

#Extraction of column name in DF
pattern = r'\((.*?)\)'
stat_names = []

for stat in additional_stats:
    stat_name = re.findall(pattern, stat)
    stat_names.append(stat_name[0])

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Player Stats of Selected Team(s)')
st.write('Number of Players found: ' + str(df_selected_team.shape[0]))

if len(stat_names) > 0:
    for stat in stat_names:
        df_selected_team[stat] = df[stat]

if df_selected_team.shape[0] > 0:
    st.dataframe(df_selected_team.set_index('Player').sort_values(by=['Player']))
else:
    st.header('No Team and Position Selected!')


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)



