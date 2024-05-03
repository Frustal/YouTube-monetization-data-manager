from Modules import Sheets1
from Modules import Stats 
from Modules import VideoListCreator
from Modules import DaysInMonth
#from Modules import SendMessage
import time
import datetime
import json

def PushToSheets(timeToSleep, spreadSheet, colDict, channelName, Player, date, a, b, c, d):
    try:
      Sheets1.PushValues(spreadSheet, colDict, channelName, Player, date, a, b, c, d)
    except:
      msg = "error pushing values on " + channelName + " for " + Player + "trying again..."
      SendMessage.Send_Message(msg)
      print(msg)
      time.sleep(timeToSleep)
      PushToSheets(timeToSleep+30, spreadSheet, colDict, channelName, Player, date, a, b, c, d)
      
def UpdateAnalytics(channelName, date, playerVideoDict, spreadSheet):
    if playerVideoDict == {}:
      pass
    else:
      #getting metrics
      urls = []
      playerIdDict = {}
      String = ""
      videoUrlsDict = {}
  
      String1 = ''
      try:
          lst = channelName.split(" ")
          for el in lst:
              String1 += el
          print(String1)
      except:
          String1 = channelName
  
      with open("VideoURLs/" + String1 + ".json", 'r') as file:
          videoUrlsDict = json.load(file)
      for player in playerVideoDict:
          lst = []
          for videoNum in playerVideoDict[player]:
              for el in videoUrlsDict:
                  if videoNum == el:
                      urls.append(videoUrlsDict[el])
                      lst.append(videoUrlsDict[el])
          playerIdDict[player] = lst
      i = 0
      while i < len(urls):
          if i + 1 != len(urls):
              String += urls[i] + ','
          else:
              String += urls[i]
          i += 1
      MetricsList = Stats.GetVideoMetrics(String, date[1], date[1], channelName)
      #push values
      statsDict = {}
      j = 0
      while j < len(playerIdDict):
          lst = []
          EstimatedRevenue = 0
          CPM = 0
          views = 0
          adImpressions = 0
          num = 0
          for video in list(playerIdDict.values())[j]:
              for el in MetricsList:
                  if video == el[0]:
                      if el[1] != 0:
                          EstimatedRevenue += el[1]
                          CPM += el[2]
                          views += el[3]
                          adImpressions += el[4]
                          num += 1
          if num != 0:
              lst.append(EstimatedRevenue)
              lst.append(CPM / num)
              lst.append(views)
              lst.append(adImpressions)
          elif num == 0:
              for i in range(4):
                  lst.append(0)
          statsDict[list(playerIdDict.keys())[j]] = lst
          j += 1
  
      print(statsDict)
  
      sheet = spreadSheet.worksheet(list(statsDict.keys())[0])
      colDict = Sheets1.GetColNums(sheet)
      for a in range(len(statsDict)):
          Player = list(statsDict.keys())[a]
          ValueList = list(statsDict.values())[a]
          print(Player)
          print(ValueList)
          PushToSheets(60, spreadSheet, colDict, channelName, Player, date[0],
                             ValueList[0], ValueList[1], ValueList[2],
                             ValueList[3])
  
      print("Pushed succesfully")
def UpdateAnalyticsMonth():
    print("Your current channels: ")
    data = {}
    try:
        with open("ChannelList/Channels.json", 'r') as file:
            data = json.load(file)
    except:
        print("No channels found")
        return

    if len(data) != 0:
        i = 1
        for el in data:
            print(str(i) + ' - ' + el)
            i += 1
    else:
        print("No channels found")

    year = datetime.date.today().year
    day = datetime.date.today().day - 4
    monthStr = input("Введіть місяць (e.g. 06): ")
    days = DaysInMonth.DaysInMonthF(int(monthStr), year)
    dates = {
          "01": "січня",
          "02": "лютого",
          "03": "березня",
          "04": "квітня",
          "05": "травня",
          "06": "червня",
          "07": "липня",
          "08": "серпня",
          "09": "вересня",
          "10": "жовтня",
          "11": "листопада",
          "12": "грудня"
          }
    SendMessage.Send_Message("Started bot for " + dates[monthStr])
    print("Started bot for " + dates[monthStr])
    for channel in data:
        SendMessage.Send_Message("Started pushing for " + channel)
        print("Started pushing for " + channel)
        VideoListCreator.CreateVideoList(channel, data[channel])
        print(channel)
        client = Sheets1.client
        spreadSheet = client.open("Аналітика " + channel)
        for iDay in range(days):
          day = iDay + 1
          dayStr = str(day)
          if 1<=day<=9:
              dayStr = '0' + str(day)
          dateStr = str(year) + '-' + monthStr + '-' + dayStr
          dateSheets = str(day) + ' ' + dates[monthStr]
          currentDate = []
          currentDate.append(dateSheets)
          currentDate.append(dateStr)
          print(currentDate)
          playerVideoDict = Sheets1.CreatePlayerVideoDict(spreadSheet, currentDate[0])
          UpdateAnalytics(channel, currentDate, playerVideoDict, spreadSheet)
    SendMessage.Send_Message("Finished bot for " + dates[monthStr])
    print("Finished bot for " + dates[monthStr])
  
def UpdateAnalyticsDay():
    print("Your current channels: ")
    data = {}
    try:
        with open("ChannelList/Channels.json", 'r') as file:
            data = json.load(file)
    except:
        print("No channels found")

    if len(data) != 0:
        i = 1
        for el in data:
            print(str(i) + ' - ' + el)
            i += 1
    else:
        print("No channels found")

    print()
    channelNum = int(input("Enter channel num(e.g. 1): "))
    channelName = ''
    m = 1
    for el in data:
        if m == channelNum:
            channelName = el
            print(channelName)
            break
        else:
            m += 1

    dateStr = input("Введіть дату(e.g 2021-12-06): ")
    dateList = dateStr.split("-")
    dateSheets = str(int(dateList[2]))
    dates = {
        "01": "січня",
        "02": "лютого",
        "03": "березня",
        "04": "квітня",
        "05": "травня",
        "06": "червня",
        "07": "липня",
        "08": "серпня",
        "09": "вересня",
        "10": "жовтня",
        "11": "листопада",
        "12": "грудня"
    }
    for el in dates:
        if el == dateList[1]:
            dateSheets += ' ' + dates[el]
    currentDate = []
    currentDate.append(dateSheets)
    currentDate.append(dateStr)
    print(currentDate)
    client = Sheets1.client
    spreadSheet = client.open("Аналітика " + channelName)
    playerVideoDict = Sheets1.CreatePlayerVideoDict(spreadSheet, currentDate[0])
    UpdateAnalytics(channelName, currentDate, playerVideoDict, spreadSheet)


def UpdateVideoList():
    print("Your current channels: ")
    data = {}
    try:
        with open("ChannelList/Channels.json", 'r') as file:
            data = json.load(file)
    except:
        print("No channels found")

    if len(data) != 0:
        i = 1
        for el in data:
            print(str(i) + ' - ' + el)
            i += 1
    else:
        print("No channels found")

    print()
    channelNum = int(input("Enter channel num(e.g. 1): "))
    channelName = ''
    m = 1
    for el in data:
        if m == channelNum:
            channelName = el
            break
        else:
            m += 1
    VideoListCreator.CreateVideoList(channelName, data[channelName])


def AddDeleteChannel():
    print("Your current channels: ")
    data = {}
    try:
        with open("ChannelList/Channels.json", 'r') as file:
            data = json.load(file)
    except:
        print("No channels found")

    if len(data) != 0:
        i = 1
        for el in data:
            print(str(i) + ' - ' + el)
            i += 1
    else:
        print("No channels found")

    print()
    print("1 - Add channel")
    print("2 - Delete channel")
    playerInput = int(input("Choose your options(e.g. 1): "))

    if playerInput == 1:
        channelName = input("Enter channel name: ")
        channelUrl = input("Enter channel URL: ")
        data[channelName] = channelUrl
        with open("ChannelList/Channels.json", 'w') as outfile:
            json.dump(data, outfile)
    elif playerInput == 2:
        channelNum = int(input("Enter channel num(e.g. 1): "))
        channelName = ''
        m = 1
        for el in data:
            if m == channelNum:
                channelName = el
                break
            else:
                m += 1
        if channelName in data:
            del data[channelName]
        with open("ChannelList/Channels.json", 'w') as outfile:
            json.dump(data, outfile)


def Main():
    while (True):
        print()
        print("Welcome back!")
        print("--YT bot Menu--")
        print("1 - Update analytics for a day")
        print("2 - Update analytics for a month")
        print("3 - Add or delete channel")
        print("4 - Update video list")
        print("5 - exit")
        print("--------------------------")
        playerInput = int(input("Choose your options(e.g. 1): "))

        if playerInput == 1:
            UpdateAnalyticsDay()
        elif playerInput == 2:
            UpdateAnalyticsMonth()
        elif playerInput == 3:
            AddDeleteChannel()
        elif playerInput == 4:
            UpdateVideoList()
        elif playerInput == 5:
            break
          
Main()