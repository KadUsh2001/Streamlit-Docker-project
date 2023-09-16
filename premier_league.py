import streamlit as st
import pandas as pd
import numpy as np
import os

path = os.getcwd() + "/" + "premier_league.csv"

st.title('Premier league team results')

data = pd.read_csv(path)

def type_of_analysis():
    type_of_an = st.radio("What type of analysis would you like?", ("Season only", "Team only", "Season and team"))
    return type_of_an
