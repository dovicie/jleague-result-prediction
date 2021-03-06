import csv
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def write_data():
    
    clubs_and_ids = []    
    for num in range(1,79):
        if not num in [35,37,38,39,40,41,42,43,44,45,48]:
            url = 'https://data.j-league.or.jp/SFMS01/search?team_ids={}'.format(num) 
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            records = soup.find_all('tr')
            club = records[-7].find('td').text
            if club != '(指定なし)':
                row = [num, records[-7].find('td').text]
                clubs_and_ids.append(row)
                
            time.sleep(1)

    with open(f'./club_and_id.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(clubs_and_ids)
        
def preprocess_data():
    
    df =  pd.read_csv("./club_and_id.csv", names=["club_id", "club_ja"])
    
    clubs = ['kashima-antlers','jef-united','urawa-red-diamonds','tokyo-verdy','yokohama-fa-marinos','yokohama-flugels','shimizu-s-pulse','nagoya-grampus-eight','gamba-osaka','sanfrecce-hiroshima','kashiwa-reysol','shonan-bellmare','jubilo-iwata','consadole-sapporo','vissel-kobe','cerezo-osaka','kawasaki-frontale','fc-tokyo','avispa-fukuoka','kyoto-sanga','omiya-ardija','ventforet-kofu','montedio-yamagata','oita-trinita','sagan-tosu','yokohama-fc','tokushima-vortis','matsumoto-yamaga','v-varen-nagasaki','vegalta-sendai','albirex-niigata']
    
    df.insert(1,"club",clubs)
    
    df = df.append(
        [
            {'club_id': 5, 'club': 'yokohama-fa-marinos', 'club_ja': '横浜Ｍ' },
            {'club_id': 21, 'club': 'kawasaki-frontale', 'club_ja': '川崎' },
            {'club_id': 22, 'club': 'fc-tokyo', 'club_ja': 'Ｆ東京' },
            {'club_id': 34, 'club': 'yokohama-fc', 'club_ja': '横浜Ｃ' },
        ],
        ignore_index=True)
    
    club_abbies = ["kasm","chib","uraw","tk-v","y-fm","y-fg","shim","nago","g-os","hiro","kasw","shon","iwat","sapp","kobe","c-os","ka-f","fctk","fuku","kyot","omiy","kofu","yama","oita","tosu","y-fc","toku","mats","ngsk","send","niig","y-fm","ka-f","fctk","y-fc"]
    df.insert(2,"club_abbr",club_abbies)
    
    df.to_csv(f'./club_and_id.csv',index=False)
    
def main():
    write_data()
    preprocess_data()
    
if __name__ == '__main__':
    main()
        

    
    


        

        
