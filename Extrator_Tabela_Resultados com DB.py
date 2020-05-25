from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import psycopg2 as pg
#from datetime import datetime as dt

#Parametros de inicialização do navegador
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-exensions")
browser = webdriver.Chrome('chromedriver', options = options)
browser.get('http://superliga.cbv.com.br/resultados-feminino')
frame_link = browser.find_element(By.XPATH, '//*[@id="wrappers"]/div[3]/div/section/iframe').get_attribute('src')
print(frame_link)

def extraiNumeroRodada():
	browser.get(frame_link)
	#time.sleep(1)
	print('Titulo da Pagina: ', browser.title) 
	headings = []
	fases_selector = browser.find_elements_by_css_selector('span.rtsTxt')
	#print('QTD:', qtd_fases_selector)

	for fases in fases_selector:
		print(fases.text)
		headings.append(fases.text)
	return headings
rounds = extraiNumeroRodada()
print('Fases: ', rounds)

def extraiResultadosPorRodada():
	browser.get(frame_link)
	games = browser.find_elements_by_css_selector('div.t-row.t-hidden-xs.t-hidden-sm')
	#links = games.find_element_by_css_selector('p.Calendar_p_TextRow')
	games_list = []
	games_list_2 = []
	for game in games:
		# print('Game: ', game)
		# date = game.find_element_by_css_selector('p.Calendar_p_TextRow.Calendar_p_TextRow_Italic').get_attribute('span')
		# print('Date: ', date)
		# print('Game: ', game.text)
		games_list.append(game.text)
		games_list_2 = [tupla for tupla in games_list if tupla != []]
	# print('Jogo: ', games_list[1].split('\n'))

	result_list = []
	list_length = len(games_list_2)
	print('Tamanho Lista: ',list_length)

	for ind_game in range(len(games_list_2)):
		# print('Games: ',len(games_list))
		#print(games_list[ind_game].split('\n'))

		# print('Após split de espaço: ', games_list_2[ind_game].split('\n'))
		# games_list_2 = games_list_2[ind_game].split('\n')
		# print('Após o split do placar: ', games_list_2[ind_game][3])
		# print('Após split do placar: ', games_list_2[ind_game][3].strip().split('-'))
		if games_list_2[ind_game].split('\n') == ['']:
			games_list_2[ind_game].split('\n').remove('')
			print('Eliminado')
		else:
			result_list.append(games_list_2[ind_game].split('\n'))
	return result_list

result_list_csv = extraiResultadosPorRodada()

# print(final_list[1][2])


def insere_dados(dt_jogo, nm_local, tm_casa, tm_fora, 
	nr_pt_casa, nr_pt_fora):
	
	conn = None

	sql = """INSERT INTO TB_RESULT_JOGOS_RODADA(DT_JOGO,
												NM_LOCAL,
												NM_EQUIPE_CASA,
												NM_EQUIPE_VISITANTE,
												NR_PONTO_CASA,
												NR_PONTO_FORA)
				VALUES (%s, %s, %s, %s, %s, %s)"""

	try:
		#Conectando no banco
		conn = pg.connect("dbname=############ user=########## password=##########")

		#Criando um novo cursor
		cur = conn.cursor()

		#Executando o insert
		cur.execute(sql, (dt_jogo, nm_local, tm_casa, tm_fora, 
	nr_pt_casa, nr_pt_fora))

		cur.commit()

		cur.close
	except (Exception, pg.DatabaseError) as error:
		print("Ops! Algo deu errado. Verifique o seguinte erro: ", error)
	finally:
		if conn is not None:
			conn.close()


for result in range(len(result_list_csv)):
	data_db = result_list_csv[result][0].split("-")
	data_jg = str(data_db[0])
	local_jg =  str(result_list_csv[result][1])
	tm_cs = str(result_list_csv[result][2])
	placar_db = str(result_list_csv[result][3]).split("-")
	pt_cs = str(placar_db[0])
	pt_fr = str(placar_db[1])
	tm_fr = str(result_list_csv[result][4])

	insere_dados(data_jg, local_jg, tm_cs, tm_fr, pt_cs, pt_fr)


# import csv

# separator = ';'
# breakline = '\n'

# csvFile = open('superliga_feminino_classificatoria_18_19.csv', 'w')

# # csv_writer = csv.writer(csvFile)
# # csv_headings = ['DATA', 'LOCAL', 'TIME CASA', 'PLACAR', 'TIME VISITANTE']
# csvFile.write(
# 	'DATA'+separator+
# 	'LOCAL'+separator+
# 	'TIME CASA'+separator+
# 	'PLACAR'+separator+
# 	'TIME VISITANTE'+breakline)

# for result in range(len(result_list_csv)):
# 	csvFile.write(
# 		result_list_csv[result][0]+separator+
# 		result_list_csv[result][1]+separator+
# 		result_list_csv[result][2]+separator+
# 		str(result_list_csv[result][3])+separator+
# 		result_list_csv[result][4]+breakline)

# csvFile.close()

# # for result in range(len(result_list_csv)):
# # 	print('Data: ', result_list_csv[result][0])
# # 	print('Local: ', result_list_csv[result][1])
# # 	print('Casa: ', result_list_csv[result][2])
# # 	print('Placar: ', result_list_csv[result][3])
# # 	print('Fora: ', result_list_csv[result][4])
