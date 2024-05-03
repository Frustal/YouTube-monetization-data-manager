
import os
import json
import csv
from yt_videos_list2 import ListCreator

def CreateVideoList(channelName, channelURL):
  lc = ListCreator(driver = 'chrome', scroll_pause_time = 0.8, txt = False, md = False, reverse_chronological = False, headless = False)
  lc.create_list_for(url = channelURL, log_silently = True)
  
  String1 = ''
  try:
    lst = channelName.split(" ")
    for el in lst:
      String1 += el
  except:
    String1 = channelName

  with open(String1 + '_chronological_videos_list.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    dictionary = {}
    titles = []
    urls = []
    for line in csv_reader:
      if line[1].__contains__('#'):
          num = ''
          for number in line[1].split("#"):
            if number.isdigit():
              num = '#' + number
          if num != '':
            titles.append(num)
            urls.append(line[3])
    dictionary = dict(zip(titles, urls))
    
  nums = []
  urls = []
  for el in list(dictionary.keys()):
    nums.append(el)
    urls.append(dictionary[el].split('=')[1])
  finalDict = dict(zip(nums, urls))

  #os.path.join(sys.path[0], channelName + '.json')
  with open("VideoURLs/" + String1 + '.json', 'w') as outfile:
    json.dump(finalDict, outfile)
  os.remove(String1 + '_chronological_videos_list.csv')
  os.remove(String1 + '_chronological_videos_list.log')
  print("Done")

