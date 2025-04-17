# 🌐 Sentimento Global Pós-Tarifas: Uma Análise Geopolítica do "Liberation Day"

Este projeto propõe a construção de uma análise de sentimentos baseada em notícias internacionais relacionadas às tarifas promovidas pelo presidente Donald Trump no chamado “Liberation Day”. O objetivo é entender como diferentes países foram afetados e retratados na mídia, cruzando os resultados com a intensidade das tarifas impostas e visualizando os dados por meio de mapas interativos.

---

## 📅 O que foi o Liberation Day?

O "Liberation Day" (Dia da Libertação), celebrado em 2 de abril de 2025, foi uma data proclamada pelo então presidente dos Estados Unidos, Donald Trump, para anunciar uma nova política comercial baseada na imposição de tarifas significativas sobre importações de diversos países.

Durante um discurso no Jardim das Rosas da Casa Branca, Trump declarou que esse dia marcaria a "renascença da indústria americana" e a "recuperação do destino dos EUA", promovendo uma "independência econômica" do país. As medidas incluíram tarifas de até 54% sobre produtos de origem chinesa, além de novas taxas sobre bens de países europeus, latino-americanos e asiáticos.

---

## 🤖 O que é Análise de Sentimentos?

A análise de sentimentos é uma técnica que utiliza **inteligência artificial**, especialmente **processamento de linguagem natural (NLP)**, para identificar automaticamente se um texto expressa uma emoção **positiva**, **negativa** ou **neutra**.

### 🧠 Intuição Simples:
O algoritmo “lê” uma frase e tenta capturar a emoção subjacente:

- "O produto é excelente!" → **positivo**
- "O atendimento foi péssimo." → **negativo**
- "A entrega foi realizada ontem." → **neutro**

### 🔧 Como funciona (resumo):
1. **Pré-processa o texto** (remove pontuação, acentos, palavras irrelevantes);
2. **Tokeniza** o conteúdo (quebra em palavras ou frases);
3. **Aplica dicionários de sentimentos** ou **modelos treinados** para cada item;
4. **Calcula um score agregado**, geralmente de –1 (negativo) a +1 (positivo).

---

## 🎯 Objetivos do Projeto

1. Medir o sentimento das notícias relacionadas a **cada um dos países afetados pelas tarifas**.
2. Criar um **mapa geográfico** colorindo os países:
   - de acordo com o nível de tarifa imposta;
   - de acordo com o sentimento médio das notícias relacionadas a esse país.
3. Gerar **insights interpretativos** sobre as reações da mídia internacional.

---

## 🌍 Países Alvo para Análise (sujeitos a ajustes)
- China  
- Alemanha  
- Brasil  
- México  
- Índia  
- Japão  
- Coreia do Sul  
- França  
- Reino Unido  

Esses países foram escolhidos com base em sua relevância comercial com os EUA e na repercussão esperada das tarifas.

---

## 🔧 Etapas do Projeto

### 1. Web Scraping de Notícias + Armazenamento em SQL  
📅 *Prazo: até 23/04*

**Objetivo**: Coletar notícias relacionadas ao Liberation Day e às tarifas, oriundas de veículos como CNN, G1, entre outros.

**Ferramentas e Competências**:
- Bibliotecas: `BeautifulSoup`, `newspaper3k`, `Selenium`, `Playwright`
- Técnicas: tratamento de HTML, paginação, extração de texto limpo
- Armazenamento em banco SQL: SQLite ou PostgreSQL.

---

### 2. Análise de Sentimentos com Python  
📅 *Prazo: até 27/04*

**Objetivo**: Quantificar o tom emocional das notícias associadas a cada país.

**Técnicas envolvidas**:
- Data Science
- Inteligencia artificial
- Pre processamento de dados
- Aprendizado não supervisionado

**Métricas geradas**:
- Score de polaridade (–1 a +1)
- Classificação: negativo / neutro / positivo
- Subjectividade (opcional)

---

### 3. Visualização com GeoPandas  
📅 *Prazo: até 27/04*

**Objetivo**: Criar mapas mundiais para visualização das tarifas e do sentimento agregado por país.

**Visualizações previstas**:
- Coloração dos países por **sentimento médio**.
- Contornos mais espessos ou hachurados para países com tarifas elevadas.
- Uso de `GeoPandas`, `Folium` e `Matplotlib` para gerar os mapas.

---

### 4. Integração com IA para Análise Descritiva  
📅 *Prazo: até 27/04*

**Objetivo**: Utilizar um modelo de linguagem (LLM) para gerar **resumos automáticos** da situação de cada país, com base nas notícias e no sentimento extraído.

**Exemplo de saída esperada**:  
> *“A China foi o país com maior intensidade tarifária (54%). As notícias coletadas demonstram forte reação negativa, com termos como ‘retaliação’, ‘guerra comercial’ e ‘boicote’. O sentimento médio foi –0.82.”*

**Ferramentas possíveis**:  
- `transformers` com modelos como `flan-t5`, `bart-large-cnn`  
- ou APIs de LLMs com prompts estruturados

---

### 5. Apresentação Final  
📅 *Prazo: até 30/04*

**Objetivo**: Produzir uma apresentação clara, visual e impactante sobre o projeto, incluindo:
- Introdução e contexto
- Metodologia aplicada
- Resultados e visualizações
- Conclusões e possíveis extensões

---

## 🔗 Links Úteis (adicionar mais posteriormente)

- [📘 Python Sentiment Analysis Tutorial – DataCamp](https://www.datacamp.com/tutorial/simplifying-sentiment-analysis-python)
- [📽 Financial Text Sentiment Analysis in Python – YouTube](https://youtu.be/EeoCcjPuJwE)
- [Como extrair notícias da internet com Python?](https://www.youtube.com/watch?v=XEGa6wVh8Sk)
- [Projeto do membro Igor Pires](https://github.com/Igor0Pires/status-certificacao-trilha-dev)
---

*Este projeto une dados geopolíticos, inteligência artificial e visualização espacial para explorar os impactos emocionais e comerciais de uma das mais controversas medidas econômicas recentes nos EUA.*
