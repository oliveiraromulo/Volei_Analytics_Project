from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup

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
	return links_tratados

game_links = get_all_games_links()

# print('Links Tratados: ', game_links)

def get_data_from_game(url_list):
	for url in range(10):
		print('URL: ', url_list[url])
		browser.get(url_list[url])
		# data_jogo = browser.find_element_by_xpath('//*[@id="Content_Main_LB_DateTime"]')
		time_casa = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_HomeTeam"]')
		placar_casa = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_WonSetHome"]')
		time_visita = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_GuestTeam"]')
		placar_visita = browser.find_element_by_xpath('//*[@id="Content_Main_LBL_WonSetGuest"]')
		print('Nome do arquivo CSV: ', time_casa.text.replace(' ', '_').strip() ,'_', placar_casa.text.strip(),
			' x ',
			placar_visita.text.strip(), '_', time_visita.text.replace(' ', '_').strip())
		# conj_sets = ['SET1', 'SET2', 'SET3', 'SET4', 'SET5']
		# conj_sets = browser.find_element_by_xpath('//div[@id=ctl00_Content_Main_RTS_PlayByPlay]')
		# for sets in conj_sets:
		# 	print(sets.text)
		# try:
		
		html_source = browser.page_source
		if "Jogador por Jogador" not in html_source:
			raise Exception('Jogo nao foi computado.')
		elif "Dados não disponíveis" in html_source:
		    raise Exception('Jogo nao contem dados.')
		else:
			jog_por_jog_button = browser.find_element_by_xpath('//*[@id="RTS_MatchInfo"]/div/ul/li[3]/a/span/span/span')
			action = ActionChains(browser)
			action.click(jog_por_jog_button)
			action.perform()
			tabela_jogadas = browser.find_elements_by_class_name('Row_WinnerHome')
			# jogadas = tabela_jogadas.find_element_by_tag_name('div')
			jogadas = [j.text for j in tabela_jogadas if j is not None]
			print(jogadas)
				
		continue


games = get_data_from_game(game_links)

	# def get_play_by_play(url_game):
	# 	jog_por_jog_button = browser.find_element_by_xpath('//*[@id="RTS_MatchInfo"]/div/ul/li[3]/a/span/span/span')
	# 	action = ActionChains(browser)
	# 	action.click(jog_por_jog_button)
	# 	action.perform()
	# 	# conj_sets = ['SET1', 'SET2', 'SET3', 'SET4', 'SET5']
	# 	# conj_sets = browser.find_element_by_xpath('//div[@id=ctl00_Content_Main_RTS_PlayByPlay]')
	# 	# for sets in conj_sets:
	# 	# 	print(sets.text)
	# 	tabela_jogadas = browser.find_elements_by_css_selector('#Content_Main_ctl15_RLC_MainColumn > div')
	# 	print(tabela_jogadas)

"""

for a in browser.find_elements_by_css_selector('p.Calendar_p_TextRow'):
    print('Pré Formatação: ', a.get_attribute('onclick'))
    on_click_links.append(a.get_attribute('onclick'))

print('Tamanho lista: ', len(on_click_links))

#Retira as strings repetidas. 
new_list = list(set(on_click_links))


print('Tamanho nova lista: ', len(new_list))

links_tratados = []

"""