import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google import genai
import psycopg2
import folium
from streamlit.components.v1 import html
import sqlite3
import requests
import geopandas

# insert your API key here
API_KEY = open(r"").read()

@st.cache_data
# Function to import the database from SQLite
def import_database(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM noticias"
    df = pd.read_sql_query(query, conn).set_index('id')
    conn.close()
    return df

st.set_page_config(page_title="Análise de notícias", layout="wide")
st.title("Análise de notícias com Gemini!")

st.markdown("""
Nosso projeto consiste em analisar notícias relacionadas às tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".

Neste projeto, nós buscamos implementar conceitos que se relacionem com as certificações que estamos estudando,
envolvendo coleta de dados brutos por scraping, engenharia de dados com SQL e o uso de Inteligência Artificial via a API do Gemini.
""")
# Insert the head of the dataframe here
st.subheader("Dados utilizados")
st.write("O dataframe abaixo contém as notícias que serão utilizadas. Elas foram geradas via Scraping e estão armazenadas em um banco de dados SQL.")

df = import_database("noticias_database.db")
st.dataframe(df.head(5))

def generate_response(prompt):
    client = genai.Client(api_key='AIzaSyCK01vW2n-DzBs_ajmXC78BevtyhzFW9UM')
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

# ANÁLISE GERAL ==================================================================================================
st.subheader("Análise geral")
st.write("Clique no botão abaixo para gerar uma análise geral sobre o impacto das tarifas no comércio internacional e na economia global.")

prompt_general = f"""
Você é um economista e está analisando notícias relacionadas as tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".
Forneça uma breve descrição do que são essas tarifas.
Por favor, responda em português.
Foque em aspectos gerais da situação, sem se preocupar com o impacto em um país específico.
Destaque a relevância do evento e como ele pode afetar o comércio internacional. Acrescente a relevância na história econômica global e como ela se relaciona com políticas econômicas anteriores.
Você não deve responder como se estivesse em uma conversa, mas sim como se estivesse escrevendo um artigo ou um blog.

Os dados que você deve considerar são os seguintes:
{df['conteudo'].to_string(index=False)}
Há algumas notícias que não falam sobre tarifas, mas sim sobre outros assuntos. Você deve ignorar essas notícias e focar apenas nas que falam sobre tarifas do "Liberation Day".
"""
if st.button("Gerar análise geral"):
    with st.spinner("Gerando resposta..."):
        response = generate_response(prompt_general)
        st.write(response)

# ANALISE POR PAIS ==================================================================================================
st.subheader("Análise por país")
st.write("Selecione um país na lista baixo para gerar uma análise detalhada sobre o impacto das tarifas nesse país.")
country = st.selectbox("País", ['Brasil', 'Estados Unidos', 'China', 'Canadá'])

prompt_country = f"""
Você é um economista e está analisando notícias relacionadas as tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".
Por favor, responda em português.
Foque em como as notícias estão reportando os possíveis impactos no país {country}.
Atribua um score de sentimento geral entre -1 e 1, onde -1 é negativo, 0 é neutro e 1 é positivo relacionado aos impactos para o país {country}.
Destaque de forma breve quais motivos te levaram a atribuir esse score.
Aponte também quais setores da economia podem ser mais afetados e como isso pode impactar a economia do país {country} a curto e longo prazo.
Você não deve responder como se estivesse em uma conversa, mas sim como se estivesse escrevendo um artigo ou um blog.

Os dados que você deve considerar são os seguintes. Foque apenas nesses dados. Os jornais utilizados são Agencia Brasil, Brasil de Fato e BCB do Canadá.:
{df['conteudo'].to_string(index=False)}
Há algumas notícias que não falam sobre tarifas, mas sim sobre outros assuntos. Você deve ignorar essas notícias e focar apenas nas que falam sobre tarifas do "Liberation Day".
"""
st.subheader(f"Análise para o {country}")
if st.button(f"Gerar análise para o {country}"):
    with st.spinner("Gerando resposta..."):
        response = generate_response(prompt_country)
        st.write(response)

## ANALISE POR JORNAL ==================================================================================================
st.subheader("Análise por jornal")
st.write("Clique no botão abaixo para entender como cada jornal está reportando o evento.")

prompt_journal = f"""
Você é um economista e está analisando notícias relacionadas as tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".
Por favor, responda em português.
Foque em como cada jornal está reportando os possíveis impactos no comércio internacional e na economia global.
Destaque as diferenças entre os jornais e tente fazer uma análise comparativa entre eles.
Se possível, identifique possíveis vieses ou tendências nas reportagens de cada jornal. Mas por favor, não invente nada.
Você não deve responder como se estivesse em uma conversa, mas sim como se estivesse escrevendo um artigo ou um blog.

Os dados que você deve considerar são os seguintes:
{df[['url', 'titulo']].to_string(index=False)}
"""

if st.button("Gerar análise por jornal"):
    with st.spinner("Gerando resposta..."):
        response = generate_response(prompt_journal)
        st.write(response)

# MAPA INTERATIVO ==================================================================================================
st.subheader("Mapa interativo")
st.write("Nesta seção, criamos um mapa interativo utilizando a biblioteca Folium. O mapa mostra os países afetados pelas tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de 'Liberation Day'.")
st.write("O mapa é interativo e permite que você visualize os países afetados de forma dinâmica. Você pode dar zoom e explorar diferentes regiões do mundo.")

# Criação do mapa com Folium
# importando os dados de tarifas por país que esta na pasta auxiliares
tarifa_por_pais = pd.read_excel("tarifas_por_pais.xlsx")
m = folium.Map(
location=[-50, 20],
zoom_start=2.4,
tiles="cartodb positron",
max_bounds=True,
max_bounds_style={"color": "black", "weight": 2, "fillOpacity": 0.5},

prefer_canvas=True,
dragging=True)

folium.Choropleth(
    geo_data=requests.get('https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json').json(),
    data=tarifa_por_pais,
    columns=['Country', 'Tarifa'],
    nan_fill_color="black",
nan_fill_opacity=0.1,
key_on="feature.properties.name",
fill_color="RdBu_r",
legend_name="Tarifa (%)").add_to(m)

        
# Renderiza como HTML e mostra no Streamlit
map_html = m._repr_html_()
html(map_html, height=800)


# Perguntas frequentes
st.subheader("Perguntas frequentes")
st.markdown("""
Nesta seção, utilizamos a API do Gemini para responder explicar alguns conceitos ou tecnologias que utilizamos no projeto.
Aproveite para aprender sobre como funciona alguma biblioteca ou alguma ferramenta utilizada no projeto.

Selecione um tópico na lista abaixo e clique no botão para gerar uma resposta.
""")

topico = st.selectbox("Tópico", ['Web Scraping', 'Streamlit', 'Folium', 'SQL', 'Gemini', 'API', 'Pandas', 'Python', 'Github', 'Análise de Sentimentos'])

prompt_questions = f"""
Pense que você está escrevendo um texto sobre o tópico {topico}.
Você deseja informar ao leitor oque é esse tópico.
Sua tarefa é informar o que é esse tópico.
Responda em português.
Inicialmente, dê uma resposta intuitiva sobre o que é o tópico.
Posteriormente, dê uma resposta mais técnica e formalizada.
Tente ser breve na resposta, mas sem omitir informações importantes.
Você não deve responder como se estivesse em uma conversa, mas sim como se estivesse escrevendo um artigo ou um blog.
"""

if st.button(f"Gerar resposta para o tópico {topico}"):
    with st.spinner("Gerando resposta..."):
        response = generate_response(prompt_questions)
        st.write(response)