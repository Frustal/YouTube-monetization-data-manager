
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
import time

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(sys.path[0], "Modules/Creds/SheetsCreds.json"), scope)

print("Connecting to Google Sheets")
client = gspread.authorize(creds)
print("Done")

def CreatePlayerVideoDict(spread, date):
  playerList = []
  numList = []

  sheets = spread.worksheets()
  for sheet in sheets:
    if sheet.title.__contains__("#"): 
      playerList.append(sheet.title)
  print(playerList)
  sheet1 = spread.worksheet(playerList[0])
  colDict = GetColNums(sheet1)["Номера відео"]
  newPlayerList = []
  for player in playerList:
    time.sleep(1)
    sheet = spread.worksheet(player)
    time.sleep(1)
    dateRow = sheet.find(date).row
    time.sleep(1)
    nums = sheet.cell(dateRow, colDict).value
    try:
      if nums.__contains__(','):
        numList.append(nums.split(", "))
        newPlayerList.append(player)
    except:
      pass
  dictionary = dict(zip(newPlayerList, numList))
  print('dict: ', dictionary)
  return dictionary
  
def PushValues(spreadSheet, colDict, channelName, workSheetName, date, aEstimatedRevenue, aCpm, views, adImpressions):
  sheet = spreadSheet.worksheet(workSheetName)
  time.sleep(3)
  print("Pushing values for ", workSheetName, "for ", date)
  dateRow = sheet.find(date).row
  #update EstimateRevenue
  sheet.update_cell(dateRow, colDict["Загальний дохід"], aEstimatedRevenue)
  #update Cpm
  sheet.update_cell(dateRow, colDict["CPM"], aCpm)
  #update Views
  sheet.update_cell(dateRow, colDict["Перегляди"], views)
  #update AdImpressions
  sheet.update_cell(dateRow, colDict["Покази оголошень"], adImpressions)
  print("Done")

def GetColNums(sheet):
    # get columns
    first_row = sheet.get_all_values()[0]
    colDict = {
      "Загальний дохід" : 0,
      "CPM" : 0,
      "Перегляди" : 0,
      "Покази оголошень" : 0,
      "Номера відео": 0
      }
    for el in colDict:
      row = 1
      for cell in first_row:
        if cell.__contains__(el):
          colDict[el] = row
          break
        row += 1
    return colDict  