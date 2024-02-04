# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import numpy as np
import plotnine as p9
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as plotlyex

# Primero leemos los datos scrapeados
airbnb = pd.read_csv('airbnb.csv', sep=';')

# Primera página: Introducción

def set_intro():
    st.header('Introducción')
    
    st.write("""En este Dashboard podrá encontrar gráficos e información de más en 50.000 alojamientos para 6 personas en toda España.
             Estos datos han sido scrapeados de la web de airbnb (https://www.airbnb.es/).
             Más concretamente podrá ajustar destino, fechas y rango de precios para encontrar su alojamiento ideal, además podrá visualizar gráficos como la variación el precio del alojamiento a lo largo del año, el precio medio por Comunidad Autónoma, mapas y mucho más.
             Aproveche para decidir sus próximas vacaciones!""")
    
    # Añado una foto para hacer más bonito el dashboard
    st.image('image_airbnb.jpg', caption='Imágen extraída de https://static.hosteltur.com/', use_column_width=True)



# Segunda página: Buscador

def set_buscador():
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    st.header('Buscador')
    
    st.write("""Introduzca el destino, la fecha y el rango de euros que está
             dispuesto a gastarse y le mostraremos los 20 alojamientos con
             mejor valoración para que usted pueda elegir sus vacaciones ideales.""")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        ccaa_buscador = st.selectbox('Seleccione una Comunidad Autónoma', ['Andalucía',
                                                                           'Aragón',
                                                                           'Asturias',
                                                                           'Cantabria',
                                                                           'Castilla-La Mancha',
                                                                           'Castilla y León',
                                                                           'Cataluña',
                                                                           'Extremadura',
                                                                           'Galicia',
                                                                           'Islas Baleares',
                                                                           'Canarias',
                                                                           'La Rioja',
                                                                           'Comunidad de Madrid',
                                                                           'Región de Murcia',
                                                                           'Navarra',
                                                                           'País Vasco',
                                                                           'Comunidad Valenciana'])
    
    with col2:
        mes_buscador = st.selectbox('Seleccione un mes', ['Febrero',
                                                          'Marzo',
                                                          'Abril',
                                                          'Mayo',
                                                          'Junio',
                                                          'Julio',
                                                          'Agosto',
                                                          'Septiembre',
                                                          'Octubre',
                                                          'Noviembre',
                                                          'Diciembre',
                                                          'Enero'])
        
    with col3:
        precio_min, precio_max = st.slider('Seleccione un rango de precios', 0.0, 1500.0, (200.0, 500.0))
            
    # Filtro el DataFrame
    output_data = airbnb.loc[(airbnb['Destino'] == ccaa_buscador) & (airbnb['Mes'] == mes_buscador) &
                             (airbnb['precio_noche'] <= precio_max) &
                             (airbnb['precio_noche'] >= precio_min)].sort_values(by=['Valoración', 'Nº Reseñas'], ascending=False)
    
    # Muestro las columnas bonitas
    output_data = output_data[['Alojamiento', 'Precio (€/noche)',
                               'Descuento', 'Valoración', 'Nº Reseñas']]
    
    if output_data.shape[0] == 0:
        st.write('Lo sentimos, no hay alojamientos para sus requisitos.')
    else:
        st.write('Aquí tiene el top-20 de los mejores alojamientos para sus requisitos:')
        st.write(f'Destino: {ccaa_buscador}')
        st.write(f'Mes: {mes_buscador}')
        st.dataframe(output_data.head(20), hide_index=True)
        
    st.write(f'''A continuación, por si no le ha gustado ninguna de las 20 opciones que le hemos propuesto, 
             le mostraremos un gráfico donde podrá consultar todos los alojamientos disponibles en {ccaa_buscador} en {mes_buscador}. 
             Pase el ratón por encima de los puntos para ver de que alojamiento se trata, además podrá consultar el precio y la valoración.''')
    grafico_data = airbnb.loc[(airbnb['Destino'] == ccaa_buscador) & (airbnb['Mes'] == mes_buscador)]
    
    fig = plotlyex.scatter(grafico_data, x='Valoración', y='precio_noche', title=f'Valoración Vs Precio para {ccaa_buscador} en {mes_buscador}',
                     labels={'Valoración': 'Valoración', 'precio_noche': 'Precio (€/noche)'},
                     color_discrete_sequence=['#8091DE'], opacity=0.5, hover_name='Alojamiento')

    fig.update_xaxes(title="Valoración", tickvals=np.arange(2.5, 5.1, 0.25), ticktext=[str(x)+'★' for x in np.arange(2.5, 5.1, 0.25)])
    fig.update_yaxes(title="Precio (€/noche)", tickvals=list(range(0,1500,100)), ticktext=[str(x)+'€' for x in range(0,1500,100)])

    st.plotly_chart(fig)
     


# Tercera página: Comparador general

def set_comparador_general():
    
    st.header('Comparador de precios general')
    
    st.write('''Si no tiene claro donde ni cuándo viajar esta es su página, 
             aquí encontrará dos gráficos que le ayudarán a comparar precios por Comunidad Autónoma y Mes. 
             Aproveche y viaje barato!''')

        
    data_ccaa_precio = airbnb[['Destino', 'precio_noche']].groupby('Destino').mean('precio_noche').sort_values(by='precio_noche', ascending=False).reset_index()
    
    fig_ccaa = plotlyex.bar(data_ccaa_precio, x='Destino', y='precio_noche', color='Destino',
                 title='Precio medio de alojamiento por Comunidad Autónoma',
                 category_orders={"Destino": data_ccaa_precio['Destino']},
                 labels={'precio_noche': 'Precio medio (€/noche)', 'Destino': 'Comunidad Autónoma'},
                 range_y=[150, 250],
                 color_discrete_sequence=plotlyex.colors.qualitative.Pastel)

    fig_ccaa.update_layout(xaxis=dict(tickangle=315, tickvals=list(range(len(data_ccaa_precio['Destino']))),
                                  ticktext=data_ccaa_precio['Destino'], tickmode='array'),
                      xaxis_title='Comunidad Autónoma')

    st.plotly_chart(fig_ccaa)
             
    
    data_mes_precio = airbnb[['Mes', 'precio_noche']].groupby('Mes').mean('precio_noche').reset_index()
    ordered_months = ['Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'Enero']
    data_mes_precio['Mes'] = pd.Categorical(data_mes_precio['Mes'], categories=ordered_months, ordered=True)
    data_mes_precio = data_mes_precio.sort_values('Mes')
    
    fig_meses = plotlyex.bar(data_mes_precio, x='Mes', y='precio_noche', color='Mes',
                 title='Precio medio de alojamiento por mes',
                 category_orders={"Mes": data_mes_precio['Mes']},
                 labels={'precio_noche': 'Precio medio (€/noche)', 'Mes': 'Mes'},
                 range_y=[150, 250],
                 color_discrete_sequence=plotlyex.colors.qualitative.Pastel)

    fig_meses.update_layout(xaxis=dict(tickangle=315, tickvals=list(range(len(data_mes_precio['Mes']))),
                                  ticktext=data_mes_precio['Mes'], tickmode='array'),
                      xaxis_title='Meses')


    st.plotly_chart(fig_meses)
    
    
    
# Cuarta página: Comparador particular

def set_comparador_particular():
    st.header('Comparador de precios particular')
    
    st.write('''Si no tiene claro donde ni cuándo viajar, está a punto de descubrirlo.''')
    
    st.write('''Primero, elija los meses en los que se plantea hacer su viaje y le mostraremos un gráfico con el que podrá tomar la decisión más económica.''')
    
    meses_elegir_mes = st.multiselect('Seleccione los meses', ['Febrero',
                                                               'Marzo',
                                                               'Abril',
                                                               'Mayo',
                                                               'Junio',
                                                               'Julio',
                                                               'Agosto',
                                                               'Septiembre',
                                                               'Octubre',
                                                               'Noviembre',
                                                               'Diciembre',
                                                               'Enero'])
    
    boton_elegir_mes = st.button('Mostrar gráficos por meses')
    
    if boton_elegir_mes and len(meses_elegir_mes) > 0:
        data_elegir_mes = airbnb[['Mes', 'precio_noche']].loc[airbnb.Mes.isin(meses_elegir_mes)]
        
        grafico_elegir_mes = (
                                p9.ggplot(data_elegir_mes, p9.aes(x='precio_noche', fill='Mes', color='Mes'))
                                    + p9.geom_density(alpha=0.2, show_legend=False)
                                    + p9.scale_x_continuous(name="Precio (€/noche)",
                                                         breaks=range(0,1500,100),
                                                         labels=[str(x)+'€' for x in range(0,1500,100)])
                                    + p9.scale_y_continuous(name="Distribución")
                                    + p9.theme(axis_ticks_major_y = p9.element_blank(),
                                               axis_text_y = p9.element_blank())
                                    + p9.labs(title="Distribución del precio por mes")
                                    + p9.facet_wrap('Mes', ncol=1)
                                )
       
        st.pyplot(grafico_elegir_mes.draw())
    
    st.write('''Segundo, una vez haya elegido el mes, elija las Comunidades Autónomas a las que se plantea viajar y le mostraremos un gráfico con el que podrá tomar la decisión más económica.''')
    
    mes_elegir_ccaa = st.selectbox('Seleccione un mes', ['Febrero',
                                                         'Marzo',
                                                         'Abril',
                                                         'Mayo',
                                                         'Junio',
                                                         'Julio',
                                                         'Agosto',
                                                         'Septiembre',
                                                         'Octubre',
                                                         'Noviembre',
                                                         'Diciembre',
                                                         'Enero'])
    
    ccaa_elegir_ccaa = st.multiselect('Seleccione las Comunidades Autónomas', ['Andalucía',
                                                                               'Aragón',
                                                                               'Asturias',
                                                                               'Cantabria',
                                                                               'Castilla-La Mancha',
                                                                               'Castilla y León',
                                                                               'Cataluña',
                                                                               'Extremadura',
                                                                               'Galicia',
                                                                               'Islas Baleares',
                                                                               'Canarias',
                                                                               'La Rioja',
                                                                               'Comunidad de Madrid',
                                                                               'Región de Murcia',
                                                                               'Navarra',
                                                                               'País Vasco',
                                                                               'Comunidad Valenciana'])
    

    boton_elegir_ccaa = st.button('Mostrar gráficos por CCAA')
    
    if boton_elegir_ccaa and len(ccaa_elegir_ccaa) > 0:
        data_elegir_ccaa = airbnb[['Destino', 'Mes', 'precio_noche']].loc[(airbnb.Mes == mes_elegir_ccaa) & (airbnb.Destino.isin(ccaa_elegir_ccaa))]
        
        grafico_elegir_ccaa = (
                                p9.ggplot(data_elegir_ccaa, p9.aes(x='precio_noche', fill='Destino', color='Destino'))
                                    + p9.geom_density(alpha=0.2, show_legend=False)
                                    + p9.scale_x_continuous(name="Precio (€/noche)",
                                                         breaks=range(0,1500,100),
                                                         labels=[str(x)+'€' for x in range(0,1500,100)])
                                    + p9.scale_y_continuous(name="Distribución")
                                    + p9.theme(axis_ticks_major_y = p9.element_blank(),
                                               axis_text_y = p9.element_blank())
                                    + p9.labs(title=f"Distribución del precio por CCAA para {mes_elegir_ccaa}")
                                    + p9.facet_wrap('Destino', ncol=1)
                                )
        
        st.pyplot(grafico_elegir_ccaa.draw())
    
 

# Quinta página: Serie temporal

def set_serie_temp():
    
    st.header('Serie temporal')
    
    st.write('''Introduzca varias Comunidades Autónomas y le mostraremos el precio medio
             del alojamiento en cada mes del año para las Comunidades Autónomas seleccionadas,
             así usted podrá comparar precios y elegir el mejor destino.''')
    
    ccaa_serie = st.multiselect('Seleccione las Comunidades Autónomas', ['Andalucía',
                                                                         'Aragón',
                                                                         'Asturias',
                                                                         'Cantabria',
                                                                         'Castilla-La Mancha',
                                                                         'Castilla y León',
                                                                         'Cataluña',
                                                                         'Extremadura',
                                                                         'Galicia',
                                                                         'Islas Baleares',
                                                                         'Canarias',
                                                                         'La Rioja',
                                                                         'Comunidad de Madrid',
                                                                         'Región de Murcia',
                                                                         'Navarra',
                                                                         'País Vasco',
                                                                         'Comunidad Valenciana'])
    
    boton_serie = st.button('Mostrar gráfico')
        
    if boton_serie and len(ccaa_serie) > 0:
        data_serie_temp = airbnb[['Mes','Destino','precio_noche']].loc[(airbnb.Destino.isin(ccaa_serie))].groupby(['Mes', 'Destino']).mean('precio_noche').reset_index()
        
        grafico_serie_temp = (p9.ggplot(data_serie_temp, p9.aes(x='Mes', y='precio_noche', color='Destino'))
                              + p9.geom_line()
                              + p9.aes(group='Destino')
                              + p9.ggtitle('Precio medio de los alojamientos por mes.')
                              + p9.scale_x_discrete(name="Meses",
                                                 limits=['Febrero',
                                                         'Marzo',
                                                         'Abril',
                                                         'Mayo',
                                                         'Junio',
                                                         'Julio',
                                                         'Agosto',
                                                         'Septiembre',
                                                         'Octubre',
                                                         'Noviembre',
                                                         'Diciembre',
                                                         'Enero'])
                              + p9.scale_y_continuous(name="Precio medio (€/noche)",
                                                   breaks=range(110,350,20),
                                                   labels=[str(x)+'€' for x in range(110,350,20)])
                              + p9.theme(axis_text_x=p9.element_text(angle=45, hjust=1)))
        st.pyplot(grafico_serie_temp.draw())



# Sexta página: Mapa

def set_mapa():

    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    st.header('Mapa')
    
    st.write('''Seleccione un mes y le mostraremos un mapa que representará el
             precio medio del alojamiento en cada Comunidad Autónoma.''')
    
    mes_mapa = st.selectbox('Seleccione un mes', ['Febrero',
                                                  'Marzo',
                                                  'Abril',
                                                  'Mayo',
                                                  'Junio',
                                                  'Julio',
                                                  'Agosto',
                                                  'Septiembre',
                                                  'Octubre',
                                                  'Noviembre',
                                                  'Diciembre',
                                                  'Enero'])
    
    boton_mapa = st.button(f'Mostrar mapa para {mes_mapa}')
        
    if boton_mapa:
    
        archivo_shapefile = 'Comunidades_Autonomas_ETRS89_30N.shp'
        comunidades_autonomas = gpd.read_file(archivo_shapefile)
        comunidades_autonomas = comunidades_autonomas.iloc[range(17)]
        comunidades_autonomas = comunidades_autonomas[['Texto','geometry']]
        comunidades_autonomas.rename(columns={'Texto':'Destino'}, inplace=True)
        comunidades_autonomas.loc[comunidades_autonomas.Destino == 'Principado de Asturias', 'Destino'] = 'Asturias'
        comunidades_autonomas.loc[comunidades_autonomas.Destino == 'Castilla - La Mancha', 'Destino'] = 'Castilla-La Mancha'
        comunidades_autonomas.loc[comunidades_autonomas.Destino == 'Comunidad Foral de Navarra', 'Destino'] = 'Navarra'

        data_mapa = airbnb.loc[airbnb.Mes == mes_mapa][['Destino', 'precio_noche']].groupby('Destino').mean().reset_index()

        comunidades_autonomas = comunidades_autonomas.merge(data_mapa, how='inner', on='Destino')

        fig, ax = plt.subplots(figsize=(8, 8))

        comunidades_autonomas.plot(ax=ax, column='precio_noche', legend=True,
                                    legend_kwds={'label': "Precio medio (€/noche)",
                                                 'orientation': "horizontal"})

        ax.set_title(f'Precio medio por Comunidad Autónoma para {mes_mapa}')
        ax.axis('off')

        st.pyplot(plt)
        

# Creamos el dashboard
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
    set_intro()
elif menu == 'Buscador':
    set_buscador()
elif menu == 'Comparador general':
    set_comparador_general()
elif menu == 'Comparador particular':
    set_comparador_particular()
elif menu == 'Serie temporal':
    set_serie_temp()
elif menu == 'Mapa':
    set_mapa()