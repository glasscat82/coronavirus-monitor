# parsing coronavirus-monitor.info/country/russia/ Russian statistics
import sys
import requests, fake_useragent  # pip install requests
import json
from datetime import datetime
from prettytable import PrettyTable
# from multiprocessing import Pool
from bs4 import BeautifulSoup

def p(text, *args):
	print(text, *args, sep=' / ', end='\n')

def write_json(data, filename='monitor.json'):
	with open(filename, 'w', encoding='utf8') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filename='monitor.json'):
	with open(filename, 'r', encoding='utf-8') as f:
		return json.load(f)
	return {}  

def get_html(url):
	# Random User-Agent
	ua = fake_useragent.UserAgent() 
	user = ua.random
	header = {'User-Agent':str(user)}
	try:
		page = requests.get(url, headers = header, timeout = 10)
		return page.text
	except Exception as e:
		print(sys.exc_info()[1])
		return False

def get_all_links(html):
	soup = BeautifulSoup(html, 'lxml')
	teg_ = soup.find('body').find('div', id='russia_stats')
	h1_ = soup.find('body').find('section', id="content").find('div', class_='col-xs-12 col-sm-12 col-md-9 col-lg-9').find('h1').text.strip()
	# p(h1_)
	# dell headers from tables
	if teg_.find('div', class_='flex-table header'):
		for div_ in teg_.find_all('div', class_='flex-table header'):
			div_.extract()
	links = []
	for row_ in teg_.find_all('div', class_='flex-table'):		
		sity_ = row_.find('div', class_='flex-row first').find('a')
		name_ = sity_.text.strip()
		a_ = sity_.get('href')
		# add row from tables
		row = []
		row.append(a_)
		# row.append(name_)
		#----		
		for num_ in row_.find_all('div', {'class':'flex-row'}):
			row.append(num_.text.strip())
		links.append(row)
	return {"links":links, "h1":h1_}

def sfp(now):
	if now.find('+'):
		return now.replace('+', ' +')
	return now

def main():
	start = datetime.now()
	js_path = 'monitor.json'
	url = 'https://coronavirus-monitor.info/country/russia/'
	teg = get_all_links(get_html(url))
	# the table
	x = PrettyTable()
	x.field_names = ["№", "Регион", "Заражено", "Вылечено", "Погибло", "% Смертей"]
	x.align["Регион"] = "l"
	for index, r_ in enumerate(teg['links'], 1):
		x.add_row([index, r_[1], sfp(r_[2]), sfp(r_[3]), sfp(r_[4]), r_[5]])
	# x.sortby = "Active"
	# x.reversesort = True
	print(x.get_string(title=teg['h1']))
	
	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()