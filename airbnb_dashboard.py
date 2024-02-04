# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import utilities.app_functions as app


st.set_page_config(page_title='Airbnb')

# Añado el título
st.title('Airbnb')

# Añado la barra lateral, la cual nos permitirá movernos entre páginas
st.sidebar.header('Menu')

menu = st.sidebar.radio(
    "",
    ("Introducción", "Buscador", "Comparador general", "Comparador particular", "Serie temporal", "Mapa"),
)

# Configo el Menu, para que cuándo se haga click en los distintos botones, estos
# lleven a cada página del dashboard

if menu == 'Introducción':
    app.set_intro()
elif menu == 'Buscador':
    app.set_buscador()
elif menu == 'Comparador general':
    app.set_comparador_general()
elif menu == 'Comparador particular':
    app.set_comparador_particular()
elif menu == 'Serie temporal':
    app.set_serie_temp()
elif menu == 'Mapa':
    app.set_mapa()