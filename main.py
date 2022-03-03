#Bibliotecas que precisamos instalar usando o PIP
#pip install ezodf
#pip install lxml
#pip install pyexcel
#pip install odfpy
#pip install pyexcel-ods3
#pip install fpdf

#Imports
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import pyexcel_ods3 as pods
from fpdf import FPDF

receitas = ['IMPOSTO SOBRE IMPORTAÇÃO', 'IMPOSTO SOBRE EXPORTAÇÃO', 'IPI - TOTAL', 'IPI - FUMO', 'IPI - BEBIDAS', 'IPI - AUTOMÓVEIS', 'IPI - VINCULADO À IMPORTACAO', 'IPI - OUTROS', 'IMPOSTO SOBRE A RENDA - TOTAL','IRPF', 'IRPJ', 'ENTIDADES FINANCEIRAS', 'DEMAIS EMPRESAS', 'IMPOSTO S/ RENDA RETIDO NA FONTE', 'IRRF - RENDIMENTOS DO TRABALHO', 'IRRF - RENDIMENTOS DO CAPITAL', 'IRRF - REMESSAS P/ EXTERIOR', 'IRRF - OUTROS RENDIMENTOS', 'IMPOSTO S/ OPERAÇÕES FINANCEIRAS', 'IMPOSTO TERRITORIAL RURAL', 'COFINS', 'FINANCEIRAS', 'DEMAIS', 'CONTRIBUIÇÃO PARA O PIS/PASEP', 'FINANCEIRAS', 'DEMAIS', 'CSLL','FINANCEIRAS', 'DEMAIS', 'CIDE-COMBUSTÍVEIS', 'CPSSS - Contrib. p/ o Plano de Segurid. Social Serv. Público', 'OUTRAS RECEITAS ADMINISTRADAS']

def normaliza_periodo(periodo):
  periodo = periodo.replace('Dezembro - ', '01/12/').replace('Novembro - ', '01/11/').replace('Outubro - ', '01/10/').replace('Janeiro - ','01/01/').replace('Fevereiro - ', '01/02/').replace('Março - ','01/03/').replace('Abril - ','01/04/').replace('Maio - ', '01/05/').replace('Junho - ','01/06/').replace('Julho - ','01/07/').replace('Agosto - ', '01/08/').replace('Setembro - ', '01/09/')
  periodo = periodo.replace('Dezembro-', '01/12/').replace('Novembro-', '01/11/').replace('Outubro-', '01/10/').replace('Janeiro-','01/01/').replace('Fevereiro-', '01/02/').replace('Março-','01/03/').replace('Abril-','01/04/').replace('Maio-', '01/05/').replace('Junho-','01/06/').replace('Julho-','01/07/').replace('Agosto-', '01/08/').replace('Setembro-', '01/09/')
  return periodo

def extrator(data):
  valores = []
  lista_nome_planilha = str(list(data.keys())[0])
  nome_planilha = ''
  for i in range(len(lista_nome_planilha)):
    nome_planilha += lista_nome_planilha[i]
  pos_periodo = procura_periodo(nome_planilha)
  pos_sp = procura_sp(nome_planilha) + 1
  periodo = (str(data[nome_planilha][pos_periodo]).replace('Período: ', '').replace("['", '').replace("']", ''))
  periodo = normaliza_periodo(periodo)
  for i in range(len(receitas)):
    valores.append(data[nome_planilha][pos_sp + i][26])
  receita_valor = dict(zip(receitas, valores))
  return receita_valor, periodo

def cria_df(Tabela, receita_valor, periodo):
  df = pd.DataFrame(list(receita_valor.items()), columns = ['Receita', 'Valor'])
  df['Periodo'] = pd.to_datetime(periodo, format="%d/%m/%Y")
  Tabela = Tabela.append(df, ignore_index=True)
  return Tabela

def procura_sp(nome_planilha):
  UF = ['SP']
  for i in range(len(data[nome_planilha])-1):
    for j in range(len(data[nome_planilha][i])):
     if any(item in UF for item in data[nome_planilha][i]) == True:
       return i

def procura_periodo(nome_planilha):
  meses = ['Janeiro - ', 'Fevereiro - ', 'Março - ', 'Abril - ', 'Maio - ', 'Junho - ', 'Julho - ', 'Agosto - ','Setembro - ','Outubro - ','Novembro - ', 'Dezembro - ', 'Janeiro-', 'Fevereiro-', 'Março-', 'Abril-', 'Maio-', 'Junho-', 'Julho-', 'Agosto-','Setembro-','Outubro-','Novembro-', 'Dezembro-', ]
  datas = []
  for ano in range(datetime.datetime.now().year, 2008, -1):
    for i in range(len(meses)):
      if i < 12:
        data_final = 'Período: ' + meses[i]+ str(ano)
        datas.append(data_final)
        for i in range(len(data[nome_planilha])-1):
          if any(item in datas for item in data[nome_planilha][i]) == True:
              return i
      else:
        data_final = 'Período: ' + meses[i] + str(ano)
        datas.append(data_final)
        for i in range(len(data[nome_planilha])-1):
          if any(item in datas for item in data[nome_planilha][i]) == True:
              return i

def cria_DF_filtrado(receita):
  receita_observada = [receita]
  DF_Filtrado = Dataframe[Dataframe['Receita'].isin(receita_observada)]
  DF_Filtrado.sort_values(by=['Periodo'], inplace=True)
  return DF_Filtrado

def Resultados_PDF(diretorio_imagem):
  pdf = FPDF(orientation='L')
  for filename in os.listdir(diretorio_imagem):
    if filename.endswith('.png'):
      pdf.add_page()
      pdf.image(diretorio_imagem + '/' + filename, 0,0,0,0)
  pdf.output("PDF/Gráficos.pdf","F")


def gerar_grafico_Imposto_Importacao():
  DF_Imposto_Importacao = cria_DF_filtrado('IMPOSTO SOBRE IMPORTAÇÃO')
  #Valor do Imposto sobre Importação pelo Mês
  fig = plt.figure(figsize=(10,5))
  ax = fig.add_axes([0,0,1,1])
  ax.plot(DF_Imposto_Importacao['Periodo'],DF_Imposto_Importacao['Valor'], color='cornflowerblue')
  ax.set_title('Valor do Imposto sobre Importação X Tempo', fontsize=16)
  ax.set_xlabel('Data da coleta',fontsize=16)
  ax.set_ylabel('Valor do Imposto',fontsize=16)
  ax.legend(['Valor do Imposto sobre Importação'], loc='lower right', fontsize=10)
  fig.savefig('Imagens/ImpostoImportacaoXTempo.png', bbox_inches='tight')

def gerar_grafico_Imposto_Exportacao():
  DF_Imposto_Exportacao = cria_DF_filtrado('IMPOSTO SOBRE EXPORTAÇÃO')
  #Valor do Imposto sobre Exportação pelo Mês
  fig = plt.figure(figsize=(10,5))
  ax = fig.add_axes([0,0,1,1])
  ax.plot(DF_Imposto_Exportacao['Periodo'],DF_Imposto_Exportacao['Valor'], color='orangered')
  ax.set_title('Valor do Imposto sobre Exportação X Tempo', fontsize=16)
  ax.set_xlabel('Data da coleta',fontsize=16)
  ax.set_ylabel('Valor do Imposto',fontsize=16)
  ax.legend(['Valor do Imposto sobre Exportação'], loc='upper right', fontsize=10)
  fig.savefig('Imagens/ImpostoExportacaoXTempo.png', bbox_inches='tight')

def gerar_grafico_Imposto_Renda():
  DF_Imposto_Renda_Total = cria_DF_filtrado('IMPOSTO SOBRE A RENDA - TOTAL') #Configurando o dataframe relacionado a receita desejada
  #Valor do Imposto sobre a renda total pelo Mês
  fig = plt.figure(figsize=(10,5))
  ax = fig.add_axes([0,0,1,1])
  ax.plot(DF_Imposto_Renda_Total['Periodo'],DF_Imposto_Renda_Total['Valor'], color='crimson')
  ax.set_title('Valor do Imposto sobre a renda total X Tempo', fontsize=16)
  ax.set_xlabel('Data da coleta',fontsize=16)
  ax.set_ylabel('Valor do Imposto de renda',fontsize=16)
  ax.legend(['Valor do Imposto de renda'], loc='upper right', fontsize=10)
  fig.savefig('Imagens/ImpostoRendaTotalXTempo.png', bbox_inches='tight')


def gerar_grafico_Contribuicao_PIS_PASEP():
  DF_Contribuicao_PIS_PASEP = cria_DF_filtrado('CONTRIBUIÇÃO PARA O PIS/PASEP')
  #Valor da contribuição para o PIS/PASEP
  fig = plt.figure(figsize=(10,5))
  ax = fig.add_axes([0,0,1,1])
  ax.plot(DF_Contribuicao_PIS_PASEP['Periodo'],DF_Contribuicao_PIS_PASEP['Valor'], color='purple')
  ax.set_title('Valor da contribuição para o PIS/PASEP X Tempo', fontsize=16)
  ax.set_xlabel('Data da coleta',fontsize=16)
  ax.set_ylabel('Valor da contribuição',fontsize=16)
  ax.legend(['Valor da contribuição'], loc='upper right', fontsize=10)
  fig.savefig('Imagens/ContribuicaoPISPASEPXTempo.png', bbox_inches='tight')

def gerar_grafico_seguridade():
  DF_Contribuicao_Seguridade = cria_DF_filtrado('CPSSS - Contrib. p/ o Plano de Segurid. Social Serv. Público')
  #Valor da Contribuição para o Plano de Seguridade Social do Servidor Público
  fig = plt.figure(figsize=(10,5))
  ax = fig.add_axes([0,0,1,1])
  ax.plot(DF_Contribuicao_Seguridade['Periodo'],DF_Contribuicao_Seguridade['Valor'], color='firebrick')
  ax.set_title('Contrib. p/ o Plano de Segurid. Social Serv. Público X Tempo', fontsize=16)
  ax.set_xlabel('Data da coleta',fontsize=16)
  ax.set_ylabel('Valor da contribuição',fontsize=16)
  ax.legend(['Valor da contribuição'], loc='upper right', fontsize=10)
  fig.savefig('Imagens/SeguridadeSocialXTempo.png', bbox_inches='tight')

def gerar_grafico_Imposto_Importacao_Exportacao():
  DF_Imposto_Importacao = cria_DF_filtrado('IMPOSTO SOBRE IMPORTAÇÃO')
  #Valor do Imposto sobre Importação pelo Mês
  fig = plt.figure(figsize=(10,5))
  ax = fig.add_axes([0,0,1,1])
  ax.plot(DF_Imposto_Importacao['Periodo'],DF_Imposto_Importacao['Valor'], color='cornflowerblue')
  ax.set_title('Valor do Imposto sobre Importação X Tempo', fontsize=16)
  ax.set_xlabel('Data da coleta',fontsize=16)
  ax.set_ylabel('Valor do Imposto',fontsize=16)
  ax.legend(['Valor do Imposto sobre Importação'], loc='lower right', fontsize=10)
  
  
  DF_Imposto_Exportacao = cria_DF_filtrado('IMPOSTO SOBRE EXPORTAÇÃO')
  #Valor do Imposto sobre Exportação pelo Mês
  ay = fig.add_axes([0.09,0.65,0.3,0.29])
  ay.plot(DF_Imposto_Exportacao['Periodo'],DF_Imposto_Exportacao['Valor'], color='orangered')
  ay.set_title('Imposto sobre Exportação X Tempo', fontsize=10)
  ay.set_xlabel('Data da coleta',fontsize=10)
  ay.set_ylabel('Valor do Imposto',fontsize=10)
  ay.legend(['Imposto sobre Exportação'], loc='upper right', fontsize=10)
  
  fig.savefig('Imagens/ImpostoImportacaoExportacao.png', bbox_inches='tight')



#Main do código, necessário apenas os arquivos no diretório Arrecadacao, talvez seja necessário realizar a troca dos diretórios.
#Fonte utilizada: https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/receitadata/arrecadacao/arrecadacao-por-estado
diretorio = 'Arrecadacao/'
diretorio_Imagem = 'Imagens/'
Dataframe = pd.DataFrame()
for filename in os.listdir(diretorio):
  if filename.endswith('.ods'):
      data = pods.get_data(diretorio + filename)
      receita_valor, periodo = extrator(data)
      Dataframe = cria_df(Dataframe, receita_valor, periodo)

# #Gera resultados tanto gráficos como um PDF contendo todos eles.
gerar_grafico_Imposto_Importacao()
gerar_grafico_Imposto_Exportacao()
gerar_grafico_Imposto_Renda()
gerar_grafico_Contribuicao_PIS_PASEP()
gerar_grafico_seguridade()
gerar_grafico_Imposto_Importacao_Exportacao()
Resultados_PDF(diretorio_Imagem)