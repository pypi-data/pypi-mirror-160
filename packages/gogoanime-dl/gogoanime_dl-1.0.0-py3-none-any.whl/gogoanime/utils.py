"""
@author: AuraMoon55
@contact: garganshul553@gmail.com
@license: MIT License, see LICENSE file
Copyright (C) 2022
"""


import requests
from bs4 import BeautifulSoup

def get_episode_list(url): 
  try:
    soup = (BeautifulSoup(requests.get(url).text, 'html.parser'))
    pid = soup.find_all("input",attrs={"class":"movie_id"})[0].get("value")
    default_ep = soup.find_all("input",attrs={"class":"default_ep"})[0].get("value")
    ep_start = soup.find_all("a",attrs={"class":"active"})[0].get("ep_start")
    ep_end= soup.find_all("a",attrs={"class":"active"})[0].get("ep_end")
    alias = soup.find_all("input",attrs={"class":"alias_anime"})[0].get("value")
    args = {}
    args['ep_start'] = ep_start
    args['ep_end'] = ep_end
    args['id'] = pid
    args['default_ep'] = default_ep
    args['alias'] = alias
    eps = []
    for x in BeautifulSoup(requests.get("https://ajax.gogo-load.com/ajax/load-list-episode", params=args).content, 'html.parser').find_all("li")[::-1]:
      ep = {}
      ep['num'] = x.div.text
      ep['link'] = (f'https://gogoanime.lu{x.a.get("href")}').replace(" ","")
      eps.append(ep)
    return eps
  except requests.exceptions.ConnectionError:
    return "Check the host's network Connection"




def search_anime(query):
  try:
    soup = (BeautifulSoup(requests.get(f"https://gogoanime.lu/search.html?keyword={query.replace(' ','%20')}").text, 'html.parser'))
    results= soup.find_all("ul",attrs={"class":"items"})[0].find_all("p", attrs={"class":"name"})
    res = []
    if len(results) != 0:
      for x in results:
        res.append({'name':x.text.capitalize(), 'url': f"https://gogoanime.lu{x.a.get('href')}"})
    return res
  except requests.exceptions.ConnectionError:
    return "Check the host's network Connection"




def get_embed_url(url):
  try:
    link = (BeautifulSoup(requests.get(url).text, 'html.parser').find_all("div",attrs={"class":"anime_muti_link"})[0]).find_all("a")
    for x in link:
      lin = x.get("data-video")
      if lin.startswith("https://fembed-hd.com"):
        return lin
      else:
        pass
    return None
  except requests.exceptions.ConnectionError:
    return "Check the host's network Connection"
