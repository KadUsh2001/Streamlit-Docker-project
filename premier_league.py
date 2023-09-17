import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(layout="wide")
path = os.getcwd() + "/" + "premier_league.csv"

st.title('Premier league team results')

data = pd.read_csv(path)
data['Season'] = ["20" + x[-2:] for x in data['Season']]
data.rename(columns={'Qualification or relegation': 'Notes'}, inplace=True)
data["CL"] =  data.Notes.str.contains('Champions League',na=False)
data["EL"] = data.Notes.str.contains("Europa League", na=False)
data["UEFA"] = data.Notes.str.contains("UEFA", na=False)
data["Relegation"] = data.Notes.str.contains("Relegation", na=False)
data["CL"] = [1 if x else 0 for x in data["CL"]]
data["EL"] = [1 if x else 0 for x in data["EL"]]
data["UEFA"] = [1 if x else 0 for x in data["UEFA"]]
data["Relegation"] = [1 if x else 0 for x in data["Relegation"]]
data["EL"] = data[["EL", "UEFA"]].max(axis=1)
data.drop("UEFA",axis=1, inplace=True)

type_of_an = st.radio("What type of analysis would you like?", ("Season only", "Team only", "Season and team"))

if type_of_an == "Season only":
    season = st.slider('Which season?',min_value = 2001,max_value = 2022,step = 1)

    if st.checkbox("Start analysis"):
        col1, col2 = st.columns(2)
        season_string = str(season)
        season_df = data[data['Season'] == season_string]
        league_table = season_df[["Pos", "Team", "Pts"]]
        with col1:
            st.header("League table")
            st.dataframe(league_table, hide_index=True)


        with col2:
            teams_selected = st.multiselect("Which teams's points do you want to see", np.sort(np.array(season_df["Team"]), ))
            if len(teams_selected) > 0:
                teams_selected_data = season_df[season_df["Team"].isin(teams_selected)]
                teams_selected_data = teams_selected_data[["Team", "Pts"]]
                fig = plt.figure(figsize=(10,5))
                sns.barplot(data = teams_selected_data, x ="Team", y="Pts", alpha=0.8)
                plt.title('Number of points in the season plot')
                plt.ylabel('Number of points', fontsize=12)
                plt.xlabel('Teams', fontsize=12)
                st.pyplot(fig)

        col3, col4, col5 = st.columns(3)
        with col3:
            CL_df = season_df[season_df["CL"] == 1]
            CL_df = CL_df[["Team"]]
            st.header("Qualified for the Champions league")
            st.dataframe(CL_df, hide_index=True)
        with col4:
            EL_df = season_df[season_df["EL"] == 1]
            EL_df = EL_df[["Team"]]
            st.header("Qualified for the Europa league")
            st.dataframe(EL_df, hide_index=True)
        with col5:
            relegated_df = season_df[season_df["Relegation"] == 1]
            relegated_df = relegated_df[["Team"]]
            st.header("Relegated from the Premier League")
            st.dataframe(relegated_df, hide_index=True)




if type_of_an == "Team only":
    team = st.selectbox("Which team?", ("Arsenal", "Aston Villa", "Birmingham City", "Blackburn Rovers",
                                         "Bolton Wanderers", "Bournemouth", "Bradford City", "Brentford City",
                                           "Brighton & Hove Albion", "Burnley", "Cardiff City", "Charlton Athletic",
                                           "Chelsea", "Coventry City", "Crystal Palace", "Derby County", "Everton",
                                           "Fulham", "Huddersfield Town", "Hull City", "Ipswich Town", "Leeds United",
                                           "Leicester City", "Liverpool", "Manchester City", "Manchester United",
                                           "Middlesbrough", "Newcastle United", "Norwich City", "Portsmouth",
                                           "Queens Park Rangers", "Reading", "Sheffield United", "Southampton",
                                           "Stoke City", "Sunderland", "Swansea City", "Tottenham Hotspur", "Watford",
                                           "West Bromwich Albion", "West Ham United", "Wigan Athletic",
                                             "Wolverhampton Wanderers"))
    if st.checkbox("Start analysis"):
        team_string = str(team)
        team_df = data[data['Team'] == team_string]
        seasons_selected = st.multiselect("Which seasons do you want to see", np.sort(np.array(team_df["Season"]), ))
        col6, col7, col8 = st.columns(3)
        with col6:
            if len(seasons_selected) > 0:
                seasons_selected_data = team_df[team_df["Season"].isin(seasons_selected)]
                pos_df = seasons_selected_data[["Season", "Pos"]]

                st.dataframe(pos_df, hide_index=True,
                              column_config={
                                "Season": st.column_config.NumberColumn(
                                    "Season",
                                    help="Premier League season",
                                    format="%d",),
                                "Pos": st.column_config.NumberColumn(
                                    "Position",
                                    help="Premier League table position",
                                    format= "%d ⚽",)
                                })





        with col7:
            if len(seasons_selected) > 0:
                seasons_selected_data = team_df[team_df["Season"].isin(seasons_selected)]
                CL_quals = seasons_selected_data["CL"].sum()
                EL_quals = seasons_selected_data["EL"].sum()
                Relegs = seasons_selected_data["Relegation"].sum()
                vic_data = seasons_selected_data[seasons_selected_data["Pos"] == 1]
                vic = len(vic_data)
                df_values = [[vic, CL_quals, EL_quals, Relegs]]
                final_team_df = pd.DataFrame(df_values, columns=["Victories", "CL qualifications", "EL qualifications",
                                                                "Relegations"])
                st.dataframe(final_team_df, hide_index=True,
                            column_config={
                                "Victories": st.column_config.NumberColumn(
                                    "Victories",
                                    help="BPL victories",
                                    format="%d 👑",),
                                    "CL qualifications": st.column_config.NumberColumn(
                                    "CL qualifications",
                                    help="Champions League qualifications",
                                    format="%d 🏆",),
                                    "EL qualifications": st.column_config.NumberColumn(
                                    "EL qualifications",
                                    help="Europa League qualifications",
                                    format="%d 🏆",),
                                    "Relegations": st.column_config.NumberColumn(
                                    "Relegations",
                                    help="Premier League relegations",
                                    format="%d 📉",)
                            })
        with col8:
            if len(seasons_selected) > 0:
                seasons_selected_data = team_df[team_df["Season"].isin(seasons_selected)]
                wdl_df = seasons_selected_data[["Season", "W", "D", "L"]]
                total_wins = wdl_df["W"].sum()
                total_draws = wdl_df["D"].sum()
                total_losses = wdl_df["L"].sum()
                plot_df = pd.DataFrame([["Victories", total_wins], ["Draws", total_draws], ["Losses", total_losses]],
                                       columns=["Labels", "Values"])
                fig = plt.figure(figsize=(10,5))
                sns.barplot(data = plot_df, x ="Labels", y="Values", palette = ["green", "gray", "red"], alpha=0.8)
                plt.title('Wins,draws and losses plot')
                plt.ylabel('Count', fontsize=12)
                plt.xlabel('Result', fontsize=12)
                st.pyplot(fig)




if type_of_an == "Season and team":
    season = st.slider('Which season?',min_value = 2001,max_value = 2022,step = 1)
    season_string = str(season)
    season_df = data[data['Season'] == season_string]
    team = st.selectbox("Which team?", np.sort(np.array(season_df["Team"])))
    team_string = str(team)
    if st.checkbox("Start analysis"):
        season_team_df = season_df[season_df["Team"] == team_string]
        col9, col10, col11 = st.columns(3)
        with col9:
            goals_df = season_team_df[["GF", "GA"]]
            goals_for = goals_df["GF"].sum()
            goals_against = goals_df["GA"].sum()
            plot_df = pd.DataFrame([["Goals made", goals_for], ["Goals against", goals_against]],
                                       columns=["Labels", "Values"])
            fig = plt.figure(figsize=(10,5))
            sns.barplot(data = plot_df, x ="Labels", y="Values", palette = ["green", "red"], alpha=0.8)
            plt.title('Goals for and against plot')
            plt.ylabel('Count', fontsize=12)
            plt.xlabel('Type of goal', fontsize=12)
            st.pyplot(fig)
        with col10:
            season_team_df = season_df[season_df["Team"] == team_string]
            CL_quals = season_team_df["CL"].sum()
            EL_quals = season_team_df["EL"].sum()
            Relegs = season_team_df["Relegation"].sum()
            vic_data = season_team_df[season_team_df["Pos"] == 1]
            vic = len(vic_data)
            pos = season_team_df["Pos"].sum()
            df_values = [[pos, vic, CL_quals, EL_quals, Relegs]]
            final_team_df = pd.DataFrame(df_values, columns=["Position", "Victory", "CL qualification", "EL qualification",
                                                            "Relegation"])
            st.dataframe(final_team_df, hide_index=True,
                        column_config={
                            "Position": st.column_config.NumberColumn(
                                "Position",
                                help="BPL position",
                                format="%d 🏅",),
                            "Victory": st.column_config.NumberColumn(
                                "Victory",
                                help="BPL victory",
                                format="%d 👑",),
                                "CL qualification": st.column_config.NumberColumn(
                                "CL qualification",
                                help="Champions League qualification",
                                format="%d 🏆",),
                                "EL qualification": st.column_config.NumberColumn(
                                "EL qualification",
                                help="Europa League qualification",
                                format="%d 🏆",),
                                "Relegation": st.column_config.NumberColumn(
                                "Relegation",
                                help="Premier League relegation",
                                format="%d 📉",)
                        })
        with col11:
            season_team_data = season_df[season_df["Team"] == team_string]
            wdl_df = season_team_data[["Season", "W", "D", "L"]]
            total_wins = wdl_df["W"].sum()
            total_draws = wdl_df["D"].sum()
            total_losses = wdl_df["L"].sum()
            plot_df = pd.DataFrame([["Victories", total_wins], ["Draws", total_draws], ["Losses", total_losses]],
                                    columns=["Labels", "Values"])
            fig = plt.figure(figsize=(10,5))
            sns.barplot(data = plot_df, x ="Labels", y="Values", palette = ["green", "gray", "red"], alpha=0.8)
            plt.title('Wins,draws and losses plot')
            plt.ylabel('Count', fontsize=12)
            plt.xlabel('Result', fontsize=12)
            st.pyplot(fig)












