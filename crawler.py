import re
import requests
from bs4 import BeautifulSoup
from time import sleep

def links_in_html(content, visited, folder, depth=0):
	soup = BeautifulSoup(content, 'lxml')
	links = soup.find_all('a')
	target_base = ' https://example.site.ru/{}'

	for a in links:
		link = a.get('href')
		stash_url = 'https://stash.site.ru{}'.format(link)
		if (
			stash_url not in visited
			and folder in stash_url
			and len(stash_url.split('/')) > depth
		):
			visited.add(stash_url)
			r = requests.get(stash_url, auth=('login', 'pass'))
			target_url = link.split('{}/'.format(folder))[-1]
			if target_url:
				target_link = target_base.format(target_url)
				target = requests.get(target_link)
				print('%s %s' % (target.status_code, target_link))
				# print(target.url, '\n')
				if 'https://www.site.ru' not in target.url and target.status_code != 404:
					print(target.url, target.status_code, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				if r.status_code == 200:
					links_in_html(r.content, visited, folder, depth=depth)
		visited.add(stash_url)


def get_weak_urls(repo_url, folder_name):
	url_parts = repo_url.split('/')
	
	r = requests.get(repo_url, auth=('login', 'pass'))

	if r.status_code != 200:
		print('not')
		return 

	links_in_html(r.content, set(), folder=folder_name, depth=repo_url.count('/'))
	

if __name__ == '__main__':
	repo_url = 'https://stash.com/browse/'
	get_weak_urls(repo_url, repo_url.split('/')[-2])
