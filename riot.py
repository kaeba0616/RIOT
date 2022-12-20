# 모듈 적용
import requests
import json
import time
import pprint
import sys
import pandas as pd
import os

from tqdm import tqdm

pp = pprint.PrettyPrinter(indent=3)

api_key = 'RGAPI-a90c1f9f-2d25-4fd8-93a0-1b363cd34ab5'

url = 'https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=' + api_key

summonerId = {}

r = requests.get(url)
r = r.json()["entries"]
file= open("GrandMaster.csv", "w", encoding = 'utf-8-sig')
file.write("summonerName,summonerId\n")
num =0
# 마스터리그 소환사 ID수집
for i in r:
  # print(i)
  # print(i['summonerId'], i['summonerName'])
  summonerId[i['summonerName']] = i['summonerId']
  file.write(f"{i['summonerName']},{i['summonerId']}\n")
  num+=1

file.close()
print(num)
print(summonerId)


# 계정 ID 추출
accountId = {}
puuid = {}
numId =0

file = open("GM_Id.csv", "w", encoding = 'utf-8-sig')
file.write("name,id,puuid,accountId\n")
for i,j in zip(tqdm(summonerId.values()), summonerId.keys()):
  if numId >10:
    break
  
  url2 = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/'+ i + '?api_key=' +api_key
  r = requests.get(url2)
  if r.status_code == 200:
    numId +=1 
    pass
  
  elif r.status_code == 429:
    print('api cost full : inflinite loop start')
    print('loop location : ', i)
    start_time = time.time()
    
    while True: # 429error가 끝날 때까지 무한 루프
      if r.status_code == 429:
        print('try 10 second wait time')
        time.sleep(10)
        
        r = requests.get(url2)
        print(r.status_code)
  
      elif r.status_code == 200:
        print('total wait time : ', time.time() - start_time)
        print('recovery api cost')
        break
  
  r = r.json()
  # print(r)
  accountId[j] =r['accountId']
  puuid[j] = r['puuid']
  file.write(f"{r['name']},{r['id']},{r['puuid']},{r['accountId']}\n")  
# print(accountId)  
# print(puuid)
file.close()  


  
# Match ID 추출
matchId={}
# url3 = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/ETutSSS7Olaa2Fik5YvmBmXwAlLP03ZCNI-UVkkHTKfJlN4OafDoy_BBqpYGxpKLTmVVYJ4IT9NV6A/ids?start=0&count=20&api_key=RGAPI-a90c1f9f-2d25-4fd8-93a0-1b363cd34ab5'  
file = open('GM_MatchID.csv', "w", encoding='utf-8-sig')
file.write("name,matchId\n")

for i,j in zip(tqdm(puuid.values()),puuid.keys()):
  url3 = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ i +'/ids?start=0&count=5&api_key=' + api_key
  r = requests.get(url3)
  if r.status_code == 200:
    pass
  
  elif r.status_code == 429:
    print('api cost full : inflinite loop start')
    print('loop location : ', i)
    start_time = time.time()
    
    while True: # 429error가 끝날 때까지 무한 루프
      if r.status_code == 429:
        print('try 10 second wait time')
        time.sleep(10)
        
        r = requests.get(url2)
        print(r.status_code)
  
      elif r.status_code == 200:
        print('total wait time : ', time.time() - start_time)
        print('recovery api cost')
        break
      
  r = r.json()
  print(r)
  matchId[j] = r
  file.write(f"{j},{matchId[j]}\n")
file.close()  

# Match Info 추출
matchInfo={}

# url4 = "https://asia.api.riotgames.com/lol/match/v5/matches/KR_6235159171?api_key=RGAPI-a90c1f9f-2d25-4fd8-93a0-1b363cd34ab5" 

for i, j in zip(tqdm(matchId.values()),matchId.keys()):
  matchNum=1
  os.mkdir(f"RIOT/matchdataset/{j}")
  for match in i:    
    url4 = 'https://asia.api.riotgames.com/lol/match/v5/matches/' +match+ '?api_key=' +api_key
    r = requests.get(url4)
    if r.status_code == 200:
        pass
      
    elif r.status_code == 429:
        print('api cost full : inflinite loop start')
        print('loop location : ', i)
        start_time = time.time()
        
        while True: # 429error가 끝날 때까지 무한 루프
          if r.status_code == 429:
            print('try 10 second wait time')
            time.sleep(10)
            
            r = requests.get(url2)
            print(r.status_code)
      
          elif r.status_code == 200:
            print('total wait time : ', time.time() - start_time)
            print('recovery api cost')
            break    
          
    r = r.json()
    # file = open(f"RIOT/matchdataset/{j}/{matchNum}.csv", 'w', encoding='utf-8-sig')
    # file.write(f"{r}")
    matchNum +=1
    print(r)
    

#게임 ID 추출     
  
# gameId =[]
# url3 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/hqMv8JiT0hjKc96iqUz9ucXFPgsENmbI_5OHPmlyVOCZxwE?queue=420&api_key=RGAPI-e456f533-671c-4947-b960-98443960695b'

# for i in tqdm(accountId.values()):
#   url3 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/'+ i + '?queue=420&api_key=' + api_key
#   r= requests.get(url3)
  
#   if r.status_code ==200:
#     pass
  
#   elif r.status_code ==429:
#     print('api cost full : infinite loop start')
#     print('loop location : ', i)
#     start_time = time.time()
#     while True:
#       if r.status_code ==429:
        
#         print('try 10 second wait time')
#         time.sleep(10)
        
#         r = requests.get(url2)
#         print(r.status_code)
      
#       elif r.status_code ==200:
#         print('total wait time : ', time.time() - start_time)
#         print('recovery api cost')
#         break
#   try:
#     r= r.json()['matches']
    
#     for j in r:
#       j = j['gameId']
#       gameId.append(j)
#   except:
#     print(i)
#     print(r.text)
#     print("matches 오류 확인불가")



# #중복게임 제거

# print(len(gameId))
# set_gameId = set(gameId)
# set_gameId = list(set(gameId))



# # Pandas를 활용해 데이터 수집

# match_grandmaster = pd.DataFrame(columns = ['teamId','win','firstBlood','firstTower','firstInhibitor','firstBaron','firstDragon','firstRiftHerald','towerKills','inhibitorKills','baronKills','dragonKills','riftHeraldKills','gameId'])

# wait_num = []

# for i in range(len(set_gameId)):
#   if i % 30 == 0:
#     wait_num.append(i)
    
#     num = 0
    
#     for i in tqdm(set_gameId[9991:]):
#       num += 1
#       if num % 30 == 0:
#         print("Wait_time")
#         time.sleep(60)
      
#       url4 = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + str(i) +'?api_key=' + api_key 
#       r = requests.get(url4)
      
#       if r.status_code ==200:
#         pass
      
#       elif r.status_code == 429:
#         print('api cost full : infinite loop start')
#         print('loop location : ', i) 
#         start_num = time.time()
        
#         while True:
#           if r.status_code ==429:
            
#             print('try 10 second wait time')
#             time.sleep(10)
            
#             r = requests.get(url2)
#             print(r.status_code)
          
#           elif r.status_code ==200:
#             print('total wait time : ', time.time() - start_time)
#             print('recovery api cost')
#             break
          
#       try:
#         r = r.json()['teams']
#         r = r[0]
        
#         input_data = {
#             'teamId':r['teamId'],
#             'win':r['win'],
#             'firstBlood':r['firstBlood'],
#             'firstTower':r['firstTower'],
#             'firstInhibitor':r['firstInhibitor'],
#             'firstBaron':r['firstBaron'],
#             'firstDragon':r['firstDragon'],
#             'firstRiftHerald':r['firstRiftHerald'],
#             'towerKills':r['towerKills'],
#             'inhibitorKills':r['inhibitorKills'],
#             'baronKills':r['baronKills'],
#             'dragonKills':r['dragonKills'],
#             'riftHeraldKills':r['riftHeraldKills'],
#             'gameId': i
#         }
        
#         match_grandmaster = match_grandmaster.append(input_data, ignore_index = True)
        
#       except:
#         print("403에러!?")
#   match_grandmaster.to_csv("new_match_grandmaster2.csv", header=False, index = False)
  
# # 데이터 저장  
# print(match_grandmaster[:45719])
# match_grandmaster[:45720].to_csv("new_match_grandmater2.csv", header =False, index = False)
   
