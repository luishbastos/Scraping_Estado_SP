# Web Scraping em Python da Arrecadação do Estado de São Paulo
Código de Web Scrapping para extrair arquivos ODS, fornecido pelo Governo Brasileiro, coletando os dados referentes ao estado de São Paulo

O código foi criado para estudos relacionados a Scrapping em Python, por conta dos diferentes estilos de arquivos, o código foi adaptado para procurar o período (data referente ao dado),
realizei uma análise prêvia pelos arquivos e vi as diferentes posições que o estado de São Paulo poderia assumir (foco do código), os diferentes nomes da planilha, então as funções
presentes são otimizadas para realizar a busca do que procuramos e no final gerar um relatório gráfico, tanto em imagens como em PDF.

### Instalações necessárias

* pip install ezodf
* pip install lxml
* pip install pyexcel
* pip install odfpy
* pip install pyexcel-ods3
* pip install fpdf

A partir destas bibliotecas podemos fazer funcionar o código.

Devemos baixar os novos arquivos através do link a seguir:
<a href="https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/receitadata/arrecadacao/arrecadacao-por-estado"><strong>Acesse a fonte de dados</strong></a>
