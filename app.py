import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google import genai
import psycopg2
import folium
from streamlit.components.v1 import html

API_KEY = open("gemini_api_key.txt").read()

def get_data_from_db(query):
    conn = psycopg2.connect( 
        host="localhost",
        database="news_api",
        user="postgres",
        password="2025",
    )

    cursor = conn.cursor()
    cursor.execute(query)
    df = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(df, columns=columns).set_index("id")
    cursor.close()
    conn.close()
    return df

st.set_page_config(page_title="Análise de notícias", layout="wide")
st.title("Análise de notícias com Gemini!")

st.markdown("""
Nosso projeto consiste em analisar notícias relacionadas às tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".

Neste projeto, nós buscamos implementar conceitos que se relacionem com as certificações que estamos estudando,
envolvendo coleta de dados brutos por scraping, engenharia de dados com SQL e o uso de Inteligência Artificial via a API do Gemini.
""")

st.markdown("""
## Etapas do projeto

### Web Scraping
Na etapa de Web Scraping, buscamos coletar dados de notícias relacionadas às tarifas aplicadas pelo presidente Donald Trump em alguns jornais selecionados.
Aqui, tivemos a oportunidade de aplicar conceitos de coleta de dados brutos utilizando Python e algumas bibliotecas como BeautifulSoup, Requests, Scrapy, entre outras.
Para alimentar o modelo do Gemini, buscamos coletar as principais informações de uma notícia de forma que a IA pudesse ter informações úteis para fazer uma análise dos dados.
Os dados que coletamos foram:
1. Título da notícia
2. URL da notícia
3. Data de publicação
4. Conteúdo da notícia

### SQL
Para armazenar os dados coletados, utilizamos a biblioteca Sqlite3 para criarmos um database utilizando SQL.
Essa escolha se deu pela praticidade e leveza que o SQLite oferece, permitindo a criação de um banco de dados relacional local, de fácil integração com as demais etapas do projeto, sem a necessidade de configuração de servidores externos. 

Assim, garantimos maior agilidade no armazenamento, consulta e atualização das informações de maneira eficiente e organizada.

### Inteligência Artificial
Na etapa de inteligência artificial do projeto, incorporamos o uso da API do Gemini para realizar a análise avançada das notícias coletadas. 
Através dessa integração, buscamos extrair insights qualificados sobre os impactos econômicos gerados pelos eventos noticiados, tanto em âmbito global quanto em análises específicas por país. 
Além disso, a aplicação da IA possibilitou a avaliação da repercussão das notícias em diferentes veículos de comunicação, permitindo a identificação de padrões editoriais, variações na narrativa e possíveis vieses na cobertura jornalística. 
Com isso, foi possível comparar o tratamento dado aos mesmos fatos por distintos jornais, enriquecendo a interpretação dos dados e oferecendo uma perspectiva crítica sobre a formação de opinião pública e seus efeitos econômicos.

Ademais, utilizamos a API do Gemini para realizar uma análise de sentimentos, atribuindo scores que variam de -1 a 1, onde -1 representa uma percepção negativa, 0 uma percepção neutra e 1 uma percepção positiva.
Essa análise nos permitiu compreender como as notícias foram recebidas e interpretadas, tanto em termos de impacto econômico quanto de percepção pública, fornecendo uma visão abrangente sobre a reação do mercado e da sociedade em relação às tarifas impostas.

### Folium
Para a visualização geográfica dos dados, utilizamos a biblioteca folium, que nos permitiu criar um mapa-múndi interativo e intuitivo.
No mapa, cada país foi colorido de acordo com as tarifas aplicadas, adotando uma escala de intensidade: quanto maior a tarifa incidente, mais forte era a tonalidade atribuída ao território correspondente. 

Essa abordagem visual facilitou a compreensão imediata dos impactos econômicos globais, destacando de forma clara as regiões mais afetadas pelas medidas tarifárias e permitindo uma análise espacial precisa dos dados coletados.

### Streamlit
Para tornar o projeto acessível e interativo, desenvolvemos uma interface utilizando o streamlit. Através dessa plataforma, o usuário pode solicitar que a inteligência artificial realize todas as análises descritas anteriormente, como a avaliação dos impactos econômicos por país, a comparação de repercussões entre jornais e a identificação de possíveis vieses na cobertura das notícias. Além disso, incorporamos ao aplicativo o mapa construído com o folium, permitindo que o usuário visualize de maneira dinâmica as tarifas aplicadas em cada região do mundo. 

Complementarmente, criamos uma seção dedicada para esclarecimento de dúvidas, em que o usuário pode consultar a IA sobre aspectos específicos do projeto, como o funcionamento das bibliotecas empregadas, os aplicativos utilizados ou o próprio processo de análise de dados. Dessa forma, o projeto oferece uma experiência completa, intuitiva e educativa, reunindo análise de dados, inteligência artificial, visualização geográfica e suporte interativo em um único ambiente integrado.
"""
)
# Insert the head of the dataframe here
st.subheader("Dados utilizados")
st.write("O dataframe abaixo contém as notícias que serão utilizadas. Elas foram geradas via Scraping e estão armazenadas em um banco de dados SQL.")

query = """
SELECT * FROM news
"""
df = get_data_from_db(query)

st.dataframe(df.head(5))

def generate_response(prompt):
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

prompt_general = f"""
Você é um economista e está analisando notícias relacionadas as tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".
Forneça uma breve descrição do que são essas tarifas.
Por favor, responda em português.
Foque em aspectos gerais da situação, sem se preocupar com o impacto em um país específico.
Destauqe a relevância do evento e como ele pode afetar o comércio internacional. Acrescente a relevância na história econômica global e como ela se relaciona com políticas econômicas anteriores.
Você não deve responder como se estivesse em uma conversa, mas sim como se estivesse escrevendo um artigo ou um blog.

Os dados que você deve considerar são os seguintes:
{df.to_string(index=False)}
"""
st.subheader("Análise geral")
st.write("Clique no botão abaixo para gerar uma análise geral sobre o impacto das tarifas no comércio internacional e na economia global.")
if st.button("Gerar análise geral"):
    with st.spinner("Gerando resposta..."):
        response = generate_response(prompt_general)
        st.write(response)


st.subheader("Análise por país")
st.write("Selecione um país na lista baixo para gerar uma análise detalhada sobre o impacto das tarifas nesse país.")
country = st.selectbox("País", ['Brasil', 'Estados Unidos', 'China'])

prompt_country = f"""
Você é um economista e está analisando notícias relacionadas as tarifas aplicadas pelo presidente Donald Trump no dia chamado por ele de "Liberation Day".
Por favor, responda em português.
Foque em como as notícias estão reportando os possíveis impactos no país {country}.
Atribua um score de sentimento geral entre -1 e 1, onde -1 é negativo, 0 é neutro e 1 é positivo relacionado aos impactos para o país {country}.
Destaque de forma breve quais motivos te levaram a atribuir esse score.
Aponte também quais setores da economia podem ser mais afetados e como isso pode impactar a economia do país {country} a curto e longo prazo.
Você não deve responder como se estivesse em uma conversa, mas sim como se estivesse escrevendo um artigo ou um blog.

Os dados que você deve considerar são os seguintes:
{df.to_string(index=False)}
"""

st.subheader(f"Análise para o {country}")
if st.button(f"Gerar análise para o {country}"):
    with st.spinner("Gerando resposta..."):
        response = generate_response(prompt_country)
        st.write(response)

## ANALISE POR JORNAL ==================================================================================================


# Adicionando um mapa interativo com Folium
# Criação do mapa com Folium
m = folium.Map(location=[-23.55052, -46.633308], zoom_start=12)  # São Paulo

# # Adiciona um marcador
# folium.Marker(
#     [-23.55052, -46.633308],
#     popup='Centro de SP',
#     tooltip='Clique para ver'
# ).add_to(m)

# Renderiza como HTML e mostra no Streamlit
map_html = m._repr_html_()
st.markdown("### Mapa interativo com Folium")
html(map_html, height=500)


# Perguntas frequentes
st.subheader("Perguntas frequentes")
st.write("Selecionamos alguns tópicos que são importantes para entender o nosso projeto. Selecione uma opção da lista abaixo para entender melhor algum tópico que ficar em dúvida.")

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