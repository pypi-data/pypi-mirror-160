"""
@author: AuraMoon55
@contact: garganshul553@gmail.com
@license: MIT License, see LICENSE file
Copyright (C) 2022
"""



from .utils import get_episode_list, search_anime, get_embed_url
import os
from .downloaders import get_chromedriver, dlfiles

class GoGo:
  """
  Parameters:
      - download_path : path of folder in which files will be downloaded By default it is downloads
  """
  
  def __init__(self, download_path="downloads"):
    download_path = os.path.join("./", download_path)
    if os.path.exists(download_path):
      self.path = download_path
    else:
      os.mkdir(download_path)
      self.path = download_path
  
  def search(self, query):
    res = search_anime(query)
    if not isinstance(res, list):
      return print("Exiting... Because" + f"{res}")
    if len(res) <1:
      return print("No Results Found")
    ques = "{}. {}"
    q = "\n".join(ques.format(res.index(x), x["name"]) for x in res)
    ques = f"Following are search results for {query} Please Choose and send the number of your choice: \n\n{q}\nSend cancel to cancel the process\n"
    option = input(ques)
    try:
      option= int(option)
    except ValueError:
      return print("Process Cancelled")
    try:
      choice = res[option]
    except IndexError:
      return print("Please search again as process is cancelled due to input of wrong option")
    print(f"Please Wait Fetching Episodes of {choice['name']}\n")
    episodes= get_episode_list(choice['url'])
    if not isinstance(episodes, list):
      return print("Exiting..." + f"{episodes}")
    if len(episodes) < 1:
      return print("No Episodes Found")
    q = "{}.{}"
    ques = "Following Episodes Were Found, please send the number of selected episode and send cancel if you want to stop:\n\n"
    for ep in episodes:
      ques += q.format(episodes.index(ep), ep['num'])
      ques += "\n"
    ques += "\n"
    epi = input(ques)
    try:
      epi = int(epi)
    except ValueError:
      return print("Process Cancelled")
    try:
      epi = episodes[epi]
    except IndexError:
      return print("Please search again as process is cancelled due to input of wrong option")
    print("Please Wait Getting Download Links")
    file = os.path.join(self.path, f"{choice['name']} - {epi['num']}")
    embds = get_embed_url(epi['link'])
    if not embds:
      return print("No Links Found")
    if embds.startswith("Check"):
      return print("Exiting...bcoz ->", embds)
    return dlfiles(file, embds)
