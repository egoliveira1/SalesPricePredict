# SalesPricePredict - Ongoing
Predicting the **selling price** of pants for a new venture in the fashion business.

## 1. Problema de negócio:

Eduardo e Marcelo são dois brasileiros, amigos e sócios de um empreendimento. Depois de vários negócios bem sucedidos, eles estão planejando entrar no mercado de moda dos USA como um modelo de negócio tipo E-commerce, chamado **Star Jeans**.

A ideia inicial é entrar no mercado com **apenas um produto e para um público específico**, no caso o produto será **calças jeans para o público masculino**. O objetivo é manter o custo de operação baixo e escalar a medida que forem conseguindo clientes.

Porém, mesmo com o produto de entrada e a audiência definidos, os dois sócios não tem experiência nesse mercado de moda e portanto não sabem **definir** coisas básicas como **preço**, o **modelo** da calça e o **material** para fabricação de cada peça.

Assim, os dois sócios contrataram uma consultoria de Ciência de Dados para responder as seguintes perguntas:

    **1. Qual o melhor preço de vendas para as calças?**
    **2. Quantos tipos de calças e suas cores para o produto inicial?**
    **3. Quais as matérias-primas necessárias para confeccionar as calças?**

As principais **concorrentes** da Start Jeans são as americanas **H&M** e **Macy’s**.

### Questão do Negócio: Qual o melhor preço de venda do produto?

## 2. Planejamento da solução:

    - Saídas: (Produto Final)
        1. Questão do Negócio: Qual o melhor preço de venda do produto?
            - Mediana dos preços dos concorrentes.
            
        2. Formato da entrega
            - Tabela ou gráfico - elaborar protótipo
            
        3. local de entrega
            - App Streamlit
            
    - Processo: (Ações)
        1. Resposta: Realizar o cálculo da mediana
        2. Formato: 
            - Gráfico de barras com a mediana dos preços por tipo e cor nos últimos 30 dias
            - Tabela com as seguintes features: 
                id | product_name | product_type | product_color | product_price
            - Definir schema: Colunas e seus tipos
            - Definir a infraestrutura de armazenamento (SQLITE3)
            - Design do ETL (Scripts de Extração, Transformação e Carga dos dados)
            - Planejamento do agendamento dos scripts (dependências entre os scrips)
            - Fazer as visualizações
            - Entrega do produto final
        3. Local de entrega:
            - App com Streamlit

    - Entradas: (Fontes de dados)
        1. Fontes de dados
            - Site da H&M: https://www2.hm.com/en_us/men/products/jeans.html
            - Site da Macy's: https://www.macys.com/shop/mens-clothing/mens-jeans
        2. Ferramentas
            - Python 3.8.0
            - Bibliotecas de Webscrapping (BS4, Selenium)
            - JupyterLab (Análise, prototipagem e códigos)
            - Crontjog, Airflow
            - Streamlit
            
         