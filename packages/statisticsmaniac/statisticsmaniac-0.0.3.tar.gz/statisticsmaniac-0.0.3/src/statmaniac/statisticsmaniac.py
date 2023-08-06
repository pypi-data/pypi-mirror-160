import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

def player_stats(player,format):
    #player is a string which is in the format "Virat Kohli"
    #format is 1 for tests , 2 for ODI , 3 for T20s
    # please check the names of the players beforehand on cricinfo website 
    url = "http://search.espncricinfo.com/ci/content/player/search.html?search=" + player.lower().replace(" ","+") + "&x=0&y=0"
    page = requests.get(url)
    format_name = ""
    if format == 1:
        format_name = "Tests"
    elif format == 2:
        format_name = "ODIs"
    else:
        format_name = "T20s"

    soup = BeautifulSoup(page.content, "html.parser")
    player_id = str(soup.find_all(class_='ColumnistSmry')[0]).split('.html')[0].split('/')[-1]
    df = pd.read_html(f'https://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class={format};template=results;type=batting;view=innings')[3]

    return df

#print(player_stats("Virat Kohli", 3))

def save_stats_as_csv(player,format):

    df = player_stats(player,format)
    df.to_csv('stats.csv', header=False, index=False)

#save_stats_as_csv("Virat Kohli", 3)

def player_summary(player,format):
    
    #returns [runs,not outs,average,hundreds]

    df = player_stats(player,format)

    runs = []
    notout = []
    innings = 0
    batting_avg = []
    hundreds = []

    for i in df.Runs:
        if i != 'DNB' and i != 'TDNB' and i != 'sub':
            if '*' not in i:
                innings += 1
                notout.append(False)
            else:
                notout.append(True)
            runs.append(int(i.replace('*','')))
            if innings != 0:
                batting_avg.append(sum(runs)/innings)
            else:
                batting_avg.append(0)
            if len(hundreds) == 0:
                if runs[0] > 100:
                    hundreds.append(1)
                else:
                    hundreds.append(0)

            if runs[len(runs)-1]>=100 and len(hundreds)>0:
                hundreds.append(hundreds[len(hundreds)-1]+1)
            elif len(hundreds)>0:
                hundreds.append(hundreds[len(hundreds)-1])
        else:
            if len(runs) == 0:
                batting_avg.append(0)
                hundreds.append(0)
            else:
                batting_avg.append(batting_avg[len(batting_avg)-1])
                hundreds.append(hundreds[len(hundreds)-1])

    return [sum(runs),notout.count(True),batting_avg[-1],hundreds.count(1)]


#print(player_summary("RG Sharma",3))