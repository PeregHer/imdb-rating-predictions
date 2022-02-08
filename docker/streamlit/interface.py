import itertools
import subprocess
from datetime import date, timedelta

import streamlit as st
import pandas as pd
from itertools import cycle


today = date.today()
end_date = st.sidebar.date_input(label='Choissisez une date de fin', 
              value= today + timedelta(days=30),
              min_value=today,
              max_value=today + timedelta(days=365))


button = st.sidebar.button('Récupérer les données')

if button:
    start = f'{today:%Y-%m-%d}'
    end = f'{end_date:%Y-%m-%d}'
    
    with st.sidebar.spinner('Scraping in progress...'):
        subprocess.call(f'python src/spider_upcoming.py --start {start} --end {end}', shell=True)


df = pd.read_csv('data/upcoming.csv')
i=0

for _ in range(3):
    with st.container():
        cols = st.columns(3)
        for col in cols:
            film = df.iloc[i]
            with st.container():
                col.markdown(f'**{film["title"]}**')
                col.image(film['image'], width=150)
            i += 1