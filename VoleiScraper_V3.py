from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup
import csv


options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-exensions")
browser = webdriver.Chrome('chromedriver', options = options)
browser.get('http://superliga.cbv.com.br/resultados-feminino')

frame_link = browser.find_element(By.XPATH, '//*[@id="wrappers"]/div[3]/div/section/iframe').get_attribute('src')
print('Pagina para realizar o scrape: ', frame_link)

browser.get(frame_link)

on_click_links = []
on_click_links_list = [] 

def get_all_games_links():
	for a in browser.find_elements_by_css_selector('p.Calendar_p_TextRow'):
	    # print('Pré Formatação: ', a.get_attribute('onclick'))
	    on_click_links.append(a.get_attribute('onclick'))

	print('Tamanho lista: ', len(on_click_links))

	#Retira as strings repetidas. 
	new_list = list(set(on_click_links))

	new_list_2 = [x for x in new_list if x is not None]
	# print('Tamanho nova lista: ', len(new_list_2))

	links_tratados = []
	for link in range(len(new_list_2)):
		if new_list_2[link] == ['']:
			new_list_2[link].remove('')
		else:
			name_link = new_list_2[link].strip().replace("javascript:window.location='", 'http://cbv-web.dataproject.com/').replace("';", '')
			# print('Pós Formatação: ', name_link)
			links_tratados.append(name_link)
	links_tratados.remove('javascript:window.location=')
	return links_tratados

game_links = get_all_games_links()

# print('Links Tratados: ', game_links)

def get_data_from_game(url_list):
	for url in range(len(url_list)):
		print('URL: ', url_list[url])
		browser.get(url_list[url])
		# data_jogo = browser.find_element_by_xpath('//*[@id="Content_Main_LB_DateTime"]')
		time_casa = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_HomeTeam"]')
		placar_casa = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_WonSetHome"]')
		time_visita = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_GuestTeam"]')
		placar_visita = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_WonSetGuest"]')
		# print('Nome do arquivo CSV: ', time_casa.text.replace(' ', '_').strip() ,'_', placar_casa.text.strip(),
		# 	'x',
		# 	placar_visita.text.strip(), '_', time_visita.text.replace(' ', '_').strip())
		csvNome = str(url) + ' - ' + time_casa.text.replace(' ', '_').replace('/', '_').strip() + '_' + placar_casa.text.strip() + 'x' + placar_visita.text.strip() + '_' + time_visita.text.replace(' ', '_').replace('/', '_').strip() + '.csv'
		print('Nome CSV: ', csvNome)
		# conj_sets = ['SET1', 'SET2', 'SET3', 'SET4', 'SET5']
		# conj_sets = browser.find_element_by_xpath('//div[@id=ctl00_Content_Main_RTS_PlayByPlay]')
		# for sets in conj_sets:
		# 	print(sets.text)
		# try:
		dataset = []
		data = []
		html_source = browser.page_source
		if "Jogador por Jogador" not in html_source:
			#raise Exception('Jogo nao foi computado.')
			print('Jogo nao foi computado')
		elif "Dados não disponíveis" in html_source:
		    #raise Exception('Jogo nao contem dados.')
		    print('Jogo nao contem dados')
		else:
			jog_por_jog_button = browser.find_element_by_xpath('//*[@id="RTS_MatchInfo"]/div/ul/li[3]/a/span/span/span')
			action = ActionChains(browser)
			action.click(jog_por_jog_button)
			action.perform()
			# sets = browser.find_elements_by_css_selector('#ctl00_Content_Main_RTS_PlayByPlay > div > ul > li.rtsLI > a > span > span > span')
			sets = browser.find_elements_by_partial_link_text('SET')
			print(sets)
			for s in range(len(sets)):
				elem = sets[s].text
				print(elem)
				sets2 = browser.find_element_by_link_text(elem)
				sets2.click()
				tabela_jogadas = browser.find_elements_by_class_name('Row_WinnerHome')
				for tj in range(len(tabela_jogadas)):
					team_home = tabela_jogadas[tj].find_element_by_class_name('LYC_SkillPlayer_Home')
					points = tabela_jogadas[tj].find_elements_by_tag_name('div')
					#p_away = tabela_jogadas[tj].find_element_by_xpath('//*[@id="Home_Table"]/table/tbody/tr')
					team_away = tabela_jogadas[tj].find_element_by_class_name('LYC_SkillPlayer_Guest')
				# jogadas = [j.text for j in tabela_jogadas if j is not None]
					print('Casa: ', team_home.text)
					print('Ponto: ', points[3].text)
					print('Fora: ', team_away.text)
					#dataset.append([team_home.text, points[3].text, team_away.text])
					if team_home.text == '' and team_away.text == '':
						# print('Entrou no if')
						data.append([points[3].text.replace('\n', '').replace('-', 'x'), 'Não Declarado', 'Não Declarado'])
					elif team_away.text == '':
						# print('Entrou no elif')
						palavra = team_home.text.split('\n')
						data.append([points[3].text.replace('\n', '').replace('-', 'x'), palavra[0], palavra[1]])
					else:
						# print('Entrou no else')
						palavra = team_away.text.split('\n')
						data.append([points[3].text.replace('\n', '').replace('-', 'x'), palavra[0], palavra[1]])
				print(data)
				separator = ';'
				breakline = '\n'
				csvFile = open(csvNome, 'w')
				csvFile.write(
					'PONTOS'+separator+
					'JOGADOR'+separator+
					'AÇÃO'+ breakline)

				for cont in range(len(data)):
					csvFile.write(
						str(data[cont][0])+separator+
						str(data[cont][1])+separator+
						str(data[cont][2])+breakline)

				csvFile.close()
			pass
		continue
	return data

games = get_data_from_game(game_links)

print('Tamanho dataset: ', len(games))

def cria_csv(nome_csv, dados):
	print('Criando Dataset em CSV')
	print(dataset)
	separator = ';'
	breakline = '\n'
	csvFile = open(csvNome, 'w')
	csvFile.write(
		'PONTOS'+separator+
		'JOGADOR'+separator+
		'AÇÃO'+ breakline)

	for cont in range(len(dataset)):
		csvFile.write(
			dataset[cont]+separator+
			data[cont]+separator+
			dataset[cont]+breakline)

	csvFile.close()