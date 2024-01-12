# importing libraries
import requests
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import openai
import time
import schedule
import os
import random
import shutil
import command 
import pytz
import smtplib, ssl
from email.mime.text import MIMEText
import json
import math
from pytz import timezone
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import logging

load_dotenv()
# SAVEDIRPATH = os.environ['save_dir']
# IMAGESPATH = os.environ['images_dir']
SAVEDIRPATH = "/home/ubuntu/article-automation"
IMAGESPATH = "/home/ubuntu/article-automation"

# Configure logging
logging.basicConfig(filename='cron.logs', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Betpicks:

    def __init__(self):
        article_date = date.today()
        self.DAY = str(article_date.day)
        self.MONTH = str(article_date.month)
        self.YEAR = str(article_date.year)


    def get_data_request(self, URL):
        """
        This function takes a URL as an argument and returns the data in JSON format.
        If the request is not successful, it returns the status code.
        """
        time.sleep(20)
        # sending get request and saving the response as response object
        response = requests.get(url = URL)
        if response.status_code == 200:
            # extracting data in json format
            data = response.json()
            return data
        else:
            print(f"There's a {response.status_code} error with your request")
            return response.status_code

    

    def generate_response(self, statement):
        """
        Takes string as an input and usea OpenAI API to generate responses.
        """
        time.sleep(30)
        openai.api_key = os.environ['openai_key']
        openai.api_key = os.getenv("api_key")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Rewrite the given statement in a catchy and appealing way.\nStatement:" + statement,
            temperature=0.5,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=1
            )
        return response.choices[0].text
    

    def get_games_info(self, URL):
        data = self.get_data_request(URL)
        return data

    def find_and_select_image(self, folder_name, team_name ):
        matching_files = []

        # Iterate through files in the specified folder
        for filename in os.listdir(folder_name):
            # Check if the team name is present in the filename
            if team_name.lower() in filename.lower():
                matching_files.append(os.path.join(folder_name, filename))

        # Check if there are any matching files
        if not matching_files:
            return "No matching files found."

        # Randomly select an image from the matching files
        selected_image_path = random.choice(matching_files)

        return selected_image_path



 

    
    def get_article_thumbnail(self, folder_path, homeTeamName):
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        for folder in folders:
            if homeTeamName in folder:
                files = [f for f in os.listdir(folder_path+'/'+folder) if os.path.isfile(os.path.join(folder_path+'/'+folder, f))]
                random_file = random.choice(files)
                thumbnail = [str(random_file), str(folder_path + '/' + folder + '/' + random_file)]
                return thumbnail
    

class MLB_Article(Betpicks):
    
    def __init__(self):
        article_date = date.today()
        self.DAY = str(article_date.day)
        self.MONTH = str(article_date.month)
        self.YEAR = str(article_date.year)
        self.API_KEY = os.environ['mlb_api_key']
        self.ODDS_API_KEY = os.environ['odds_api_key']


        
        def get_mlb_season_points(self, element):
            if element['statistics'].__contains__("hitting"):
                points = element['statistics']['hitting']['overall']['avg']
                return points
            else:
                return ""



    def generate_html(self, games_data_article):
        for data in games_data_article:
            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            html += Betpicks.generate_response(self, "The " + data["Team 1 (T1)"] + " (" + str(data['Team 1 (T1) win']) + "-" + str(data['Team 1 (T1) loss']) + ") " + " host the " + data["Team 2 (T2)"] + " (" + str(data['Team 2 (T2) win']) + "-" + str(data['Team 2 (T2) loss']) + ") " + " on " + str(data["game_day_name"])  + " at " + str(data["Game Time"]) + " EST." +  str(data["Team 1 (T1) starting pitcher"]) + " will get the start for the " + data["Team 1 (T1)"].split()[-1]  + " vs. " + str(data["Team 2 (T2) starting pitcher"]) + " for the " + data["Team 2 (T2)"].split()[-1]  + " of the day with the first pitch at " + str(data["Game Time"]) + " EST at " + str(data["Arena"]) + ". The " + data["Team 1 (T1)"].split()[-1]  +" are listed as 100 while the" + data["Team 2 (T2)"].split()[-1] + "  have 100 to win." )
            
            
            ######### ODDS DATA #########   

            # SPREAD AND BETTING LINE 
            # html += '\n<table class="table"><caption>' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + '  Spread and Betting Line</caption>'
            # table1_col = ["Favorite", "Favorite Moneyline", "Underdog Moneyline", "Total", "Over Total Odds", "Under Total Odds", "Spread", "Favorite Spread Odds", "Underdog Spread Odds"]
            # table1_cn = '</th>\n<th scope="col">'
            # html += f'\n<thead>\n<tr>\n<th scope="col">{table1_cn.join(table1_col)}</th>\n</tr>\n</thead>'
            # table1_row = [data['favorite_team'],data['spread'],data['favorite_spread_odds'],data['underdog_spread_odds'],data['total_over_under'],data['over_total_odds'],data['under_total_odds']]
            # table1_rn = '</td>\n<td>'
            # html += f'\n<tbody>\n<tr>\n<td>{table1_rn.join(table1_row)}</td>\n</tr>\n</tbody>\n</table>'

            
            # TGMAE INFO
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['game_day_name'] + ", " + data["game_month_name"] + " " + data["game_day_num"] + ", " + data["game_year"]) + "</li>\n<li><strong>Game Time:</strong> " + str(data['Game Time'] + " EST") +    "</li>\n<li><strong>TV Channel:</strong> " + data['game_broadcast'] + "</li>\n<li><strong>Location:</strong> " + data['Location'] + "</li>\n<li><strong>Stadium:</strong> " + data['Arena'] + "</li>\n</ul>"
    
            # PITCHING MATCH UP
            html += "\n<h3>" + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] +  " Pitching Matchup</h3>"
            html += '\n<table class="table">'  
            table2_col = [data['Team 1 (T1)'].split()[-1] , "" , data['Team 2 (T2)'].split()[-1] ]
            table2_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table2_cn.join(table2_col)}</th>\n</tr>\n</thead>'
            table2_row1 = [ str(data['Team 1 (T1) win']) + "-" + str(data['Team 1 (T1) loss']), "W-L",  str(data['Team 2 (T2) win']) + "-" + str(data['Team 2 (T2) loss'])]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row1)}</td>\n<tr>'


            table2_row2 = [ str(data['Team 1 (T1) era']) , "ERA",  str(data['Team 2 (T2) era']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row2)}</td>\n<tr>'

            table2_row3 = [ str(data['Team 1 (T1) ip']) , "IP",  str(data['Team 2 (T2) ip']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row3)}</td>\n<tr>'

            # HAVE A CHECK
            table2_row4 = [ str(data['Team 1 (T1) bb']) , "WALKS",  str(data['Team 2 (T2) bb']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row4)}</td>\n<tr>'

            table2_row5 = [ str(data['Team 1 (T1) gs']) , "GS",  str(data['Team 2 (T2) gs']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row5)}</td>\n</tr>\n</tbody>\n</table>'


            # HOME TEAM Leaders & Batting Stats
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " Leaders & Batting Stats</h2>"

            html += "\n<ul>\n<li>" + data['Player Stats (T1)'][0]['home_top_season_player_name'] + " is leading the " +data['Team 1 (T1)'].split()[-1] + " with " + str(data['Player Stats (T1)'][0]['home_top_season_h']) + " this season while batting " + str(data['Player Stats (T1)'][0]['home_top_season_avg'])+ " with " + str(data['Player Stats (T1)'][0]['home_top_season_rbi']) + " RBIs. He currently has " + str(data['Player Stats (T1)'][0]['home_top_season_hr']) + " home runs and Walks with an " + str(data['Player Stats (T1)'][0]['home_top_season_obp'])  + " OBP this season."  + "</li>\n</ul>"

            html += '\n<table class="table"><caption></caption>'
            table3_col = ["Name", "GP", "AVG", "OBP", "SLG", "HR", "RBI", "H" ]
            table3_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table3_cn.join(table3_col)}</th>\n</tr>\n</thead>'
            
            table3_row1 = ["<strong>" + str(data['Player Stats (T1)'][0]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][0]['home_top_season_GP']), str(data['Player Stats (T1)'][0]['home_top_season_avg']),  str(data['Player Stats (T1)'][0]['home_top_season_obp']), str(data['Player Stats (T1)'][0]['home_top_season_slg']), str(data['Player Stats (T1)'][0]['home_top_season_hr']), str(data['Player Stats (T1)'][0]['home_top_season_rbi']), str(data['Player Stats (T1)'][0]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row1)}</td>\n</tr>'

            table3_row2 = ["<strong>" + str(data['Player Stats (T1)'][1]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][1]['home_top_season_GP']), str(data['Player Stats (T1)'][1]['home_top_season_avg']),  str(data['Player Stats (T1)'][1]['home_top_season_obp']), str(data['Player Stats (T1)'][1]['home_top_season_slg']), str(data['Player Stats (T1)'][1]['home_top_season_hr']), str(data['Player Stats (T1)'][1]['home_top_season_rbi']), str(data['Player Stats (T1)'][1]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row2)}</td>\n</tr>'

            table3_row3 = ["<strong>" + str(data['Player Stats (T1)'][2]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][2]['home_top_season_GP']), str(data['Player Stats (T1)'][2]['home_top_season_avg']),  str(data['Player Stats (T1)'][2]['home_top_season_obp']), str(data['Player Stats (T1)'][2]['home_top_season_slg']), str(data['Player Stats (T1)'][2]['home_top_season_hr']), str(data['Player Stats (T1)'][2]['home_top_season_rbi']), str(data['Player Stats (T1)'][2]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row3)}</td>\n</tr>'

            table3_row4 = ["<strong>" + str(data['Player Stats (T1)'][3]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][3]['home_top_season_GP']), str(data['Player Stats (T1)'][3]['home_top_season_avg']),  str(data['Player Stats (T1)'][3]['home_top_season_obp']), str(data['Player Stats (T1)'][3]['home_top_season_slg']), str(data['Player Stats (T1)'][3]['home_top_season_hr']), str(data['Player Stats (T1)'][3]['home_top_season_rbi']), str(data['Player Stats (T1)'][3]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row4)}</td>\n</tr>'

            table3_row5 = ["<strong>" + str(data['Player Stats (T1)'][4]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][4]['home_top_season_GP']), str(data['Player Stats (T1)'][4]['home_top_season_avg']),  str(data['Player Stats (T1)'][4]['home_top_season_obp']), str(data['Player Stats (T1)'][4]['home_top_season_slg']), str(data['Player Stats (T1)'][4]['home_top_season_hr']), str(data['Player Stats (T1)'][4]['home_top_season_rbi']), str(data['Player Stats (T1)'][4]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row5)}</td>\n</tr>\n</tbody>\n</table>'


            # AWAY TEAM Leaders & Batting Stats
            html += "\n<h2>" + data['Team 2 (T2)'].split()[-1] +  " Leaders & Batting Stats</h2>"
            
            html += "\n<ul>\n<li>" + data['Player Stats (T2)'][0]['home_top_season_player_name'] + " is leading the " +data['Team 2 (T2)'].split()[-1] + " with " + str(data['Player Stats (T2)'][0]['home_top_season_h']) + " this season while batting " + str(data['Player Stats (T2)'][0]['home_top_season_avg'])+ " with " + str(data['Player Stats (T2)'][0]['home_top_season_rbi']) + " RBIs. He currently has " + str(data['Player Stats (T2)'][0]['home_top_season_hr']) + " home runs and Walks with an " + str(data['Player Stats (T2)'][0]['home_top_season_obp'])  + " OBP this season."  + "</li>\n</ul>"

            html += '\n<table class="table"><caption></caption>' 

            table4_col = ["Name", "GP", "AVG", "OBP", "SLG", "HR", "RBI", "H" ]
            table4_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table4_cn.join(table4_col)}</th>\n</tr>\n</thead>'
            
            table4_row1 = ["<strong>" + str(data['Player Stats (T2)'][0]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][0]['home_top_season_GP']), str(data['Player Stats (T2)'][0]['home_top_season_avg']),  str(data['Player Stats (T2)'][0]['home_top_season_obp']), str(data['Player Stats (T2)'][0]['home_top_season_slg']), str(data['Player Stats (T2)'][0]['home_top_season_hr']), str(data['Player Stats (T2)'][0]['home_top_season_rbi']), str(data['Player Stats (T2)'][0]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row1)}</td>\n</tr>'

            table4_row2 = ["<strong>" + str(data['Player Stats (T2)'][1]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][1]['home_top_season_GP']), str(data['Player Stats (T2)'][1]['home_top_season_avg']),  str(data['Player Stats (T2)'][1]['home_top_season_obp']), str(data['Player Stats (T2)'][1]['home_top_season_slg']), str(data['Player Stats (T2)'][1]['home_top_season_hr']), str(data['Player Stats (T2)'][1]['home_top_season_rbi']), str(data['Player Stats (T2)'][1]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row2)}</td>\n</tr>'

            table4_row3 = ["<strong>" + str(data['Player Stats (T2)'][2]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][2]['home_top_season_GP']), str(data['Player Stats (T2)'][2]['home_top_season_avg']),  str(data['Player Stats (T2)'][2]['home_top_season_obp']), str(data['Player Stats (T2)'][2]['home_top_season_slg']), str(data['Player Stats (T2)'][2]['home_top_season_hr']), str(data['Player Stats (T2)'][2]['home_top_season_rbi']), str(data['Player Stats (T2)'][2]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row3)}</td>\n</tr>'

            table4_row4 = ["<strong>" + str(data['Player Stats (T2)'][3]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][3]['home_top_season_GP']), str(data['Player Stats (T2)'][3]['home_top_season_avg']),  str(data['Player Stats (T2)'][3]['home_top_season_obp']), str(data['Player Stats (T2)'][3]['home_top_season_slg']), str(data['Player Stats (T2)'][3]['home_top_season_hr']), str(data['Player Stats (T2)'][3]['home_top_season_rbi']), str(data['Player Stats (T2)'][3]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row4)}</td>\n</tr>'

            table4_row5 = ["<strong>" + str(data['Player Stats (T2)'][4]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][4]['home_top_season_GP']), str(data['Player Stats (T2)'][4]['home_top_season_avg']),  str(data['Player Stats (T2)'][4]['home_top_season_obp']), str(data['Player Stats (T2)'][4]['home_top_season_slg']), str(data['Player Stats (T2)'][4]['home_top_season_hr']), str(data['Player Stats (T2)'][4]['home_top_season_rbi']), str(data['Player Stats (T2)'][4]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row5)}</td>\n</tr>\n</tbody>\n</table>'

            match_teams = data['Match']
            match_teams = match_teams.replace(" ","_")
            filename = match_teams + '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
            filepath_name = os.path.join(SAVEDIRPATH + "/MLB/", filename+".html")

            try:
                text_file = open(filepath_name , "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/MLB_Images"
            thumbnail = Betpicks.get_article_thumbnail(self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/MLB/"
            try:
                shutil.copy(thumbnail[1], current_path)
                os.chdir(SAVEDIRPATH + "/MLB")
                os.rename(thumbnail[0], filename+'.jpg')
            except Exception:
                pass
            print("Article Saved!")

    def offline_html(self, games_data_article):
        for data in games_data_article:

            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            html += Betpicks.generate_response(self, "The " + data["Team 1 (T1)"] + " (" + str(data['Team 1 (T1) win']) + "-" + str(data['Team 1 (T1) loss']) + ") " + " host the " + data["Team 2 (T2)"] + " (" + str(data['Team 2 (T2) win']) + "-" + str(data['Team 2 (T2) loss']) + ") " + " on " + str(data["game_day_name"])  + " at " + str(data["Game Time"]) + " EST." +  str(data["Team 1 (T1) starting pitcher"]) + " will get the start for the " + data["Team 1 (T1)"].split()[-1]  + " vs. " + str(data["Team 2 (T2) starting pitcher"]) + " for the " + data["Team 2 (T2)"].split()[-1]  + " of the day with the first pitch at " + str(data["Game Time"]) + " EST at " + str(data["Arena"]) + ". The " + data["Team 1 (T1)"].split()[-1]  +" are listed as 100 while the" + data["Team 2 (T2)"].split()[-1] + "  have 100 to win." )
            
            
            ######### ODDS DATA #########   

            # SPREAD AND BETTING LINE 
            # html += '\n<table class="table"><caption>' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + '  Spread and Betting Line</caption>'
            # table1_col = ["Favorite", "Favorite Moneyline", "Underdog Moneyline", "Total", "Over Total Odds", "Under Total Odds", "Spread", "Favorite Spread Odds", "Underdog Spread Odds"]
            # table1_cn = '</th>\n<th scope="col">'
            # html += f'\n<thead>\n<tr>\n<th scope="col">{table1_cn.join(table1_col)}</th>\n</tr>\n</thead>'
            # table1_row = [data['favorite_team'],data['spread'],data['favorite_spread_odds'],data['underdog_spread_odds'],data['total_over_under'],data['over_total_odds'],data['under_total_odds']]
            # table1_rn = '</td>\n<td>'
            # html += f'\n<tbody>\n<tr>\n<td>{table1_rn.join(table1_row)}</td>\n</tr>\n</tbody>\n</table>'

            
            # TGMAE INFO
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['game_day_name'] + ", " + data["game_month_name"] + " " + data["game_day_num"] + ", " + data["game_year"]) + "</li>\n<li><strong>Game Time:</strong> " + str(data['Game Time'] + " EST") +    "</li>\n<li><strong>TV Channel:</strong> " + data['game_broadcast'] + "</li>\n<li><strong>Location:</strong> " + data['Location'] + "</li>\n<li><strong>Stadium:</strong> " + data['Arena'] + "</li>\n</ul>"
    
            # PITCHING MATCH UP
            html += "\n<h3>" + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] +  " Pitching Matchup</h3>"
            html += '\n<table class="table">'  
            table2_col = [data['Team 1 (T1)'].split()[-1] , "" , data['Team 2 (T2)'].split()[-1] ]
            table2_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table2_cn.join(table2_col)}</th>\n</tr>\n</thead>'
            table2_row1 = [ str(data['Team 1 (T1) win']) + "-" + str(data['Team 1 (T1) loss']), "W-L",  str(data['Team 2 (T2) win']) + "-" + str(data['Team 2 (T2) loss'])]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row1)}</td>\n<tr>'


            table2_row2 = [ str(data['Team 1 (T1) era']) , "ERA",  str(data['Team 2 (T2) era']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row2)}</td>\n<tr>'

            table2_row3 = [ str(data['Team 1 (T1) ip']) , "IP",  str(data['Team 2 (T2) ip']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row3)}</td>\n<tr>'

            # HAVE A CHECK
            table2_row4 = [ str(data['Team 1 (T1) bb']) , "WALKS",  str(data['Team 2 (T2) bb']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row4)}</td>\n<tr>'

            table2_row5 = [ str(data['Team 1 (T1) gs']) , "GS",  str(data['Team 2 (T2) gs']) ]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row5)}</td>\n</tr>\n</tbody>\n</table>'


            # HOME TEAM Leaders & Batting Stats
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " Leaders & Batting Stats</h2>"

            html += "\n<ul>\n<li>" + data['Player Stats (T1)'][0]['home_top_season_player_name'] + " is leading the " +data['Team 1 (T1)'].split()[-1] + " with " + str(data['Player Stats (T1)'][0]['home_top_season_h']) + " this season while batting " + str(data['Player Stats (T1)'][0]['home_top_season_avg'])+ " with " + str(data['Player Stats (T1)'][0]['home_top_season_rbi']) + " RBIs. He currently has " + str(data['Player Stats (T1)'][0]['home_top_season_hr']) + " home runs and Walks with an " + str(data['Player Stats (T1)'][0]['home_top_season_obp'])  + " OBP this season."  + "</li>\n</ul>"

            html += '\n<table class="table"><caption></caption>'
            table3_col = ["Name", "GP", "AVG", "OBP", "SLG", "HR", "RBI", "H" ]
            table3_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table3_cn.join(table3_col)}</th>\n</tr>\n</thead>'
            
            table3_row1 = ["<strong>" + str(data['Player Stats (T1)'][0]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][0]['home_top_season_GP']), str(data['Player Stats (T1)'][0]['home_top_season_avg']),  str(data['Player Stats (T1)'][0]['home_top_season_obp']), str(data['Player Stats (T1)'][0]['home_top_season_slg']), str(data['Player Stats (T1)'][0]['home_top_season_hr']), str(data['Player Stats (T1)'][0]['home_top_season_rbi']), str(data['Player Stats (T1)'][0]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row1)}</td>\n</tr>'

            table3_row2 = ["<strong>" + str(data['Player Stats (T1)'][1]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][1]['home_top_season_GP']), str(data['Player Stats (T1)'][1]['home_top_season_avg']),  str(data['Player Stats (T1)'][1]['home_top_season_obp']), str(data['Player Stats (T1)'][1]['home_top_season_slg']), str(data['Player Stats (T1)'][1]['home_top_season_hr']), str(data['Player Stats (T1)'][1]['home_top_season_rbi']), str(data['Player Stats (T1)'][1]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row2)}</td>\n</tr>'

            table3_row3 = ["<strong>" + str(data['Player Stats (T1)'][2]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][2]['home_top_season_GP']), str(data['Player Stats (T1)'][2]['home_top_season_avg']),  str(data['Player Stats (T1)'][2]['home_top_season_obp']), str(data['Player Stats (T1)'][2]['home_top_season_slg']), str(data['Player Stats (T1)'][2]['home_top_season_hr']), str(data['Player Stats (T1)'][2]['home_top_season_rbi']), str(data['Player Stats (T1)'][2]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row3)}</td>\n</tr>'

            table3_row4 = ["<strong>" + str(data['Player Stats (T1)'][3]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][3]['home_top_season_GP']), str(data['Player Stats (T1)'][3]['home_top_season_avg']),  str(data['Player Stats (T1)'][3]['home_top_season_obp']), str(data['Player Stats (T1)'][3]['home_top_season_slg']), str(data['Player Stats (T1)'][3]['home_top_season_hr']), str(data['Player Stats (T1)'][3]['home_top_season_rbi']), str(data['Player Stats (T1)'][3]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row4)}</td>\n</tr>'

            table3_row5 = ["<strong>" + str(data['Player Stats (T1)'][4]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T1)'][4]['home_top_season_GP']), str(data['Player Stats (T1)'][4]['home_top_season_avg']),  str(data['Player Stats (T1)'][4]['home_top_season_obp']), str(data['Player Stats (T1)'][4]['home_top_season_slg']), str(data['Player Stats (T1)'][4]['home_top_season_hr']), str(data['Player Stats (T1)'][4]['home_top_season_rbi']), str(data['Player Stats (T1)'][4]['home_top_season_h']) ] 
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row5)}</td>\n</tr>\n</tbody>\n</table>'


            # AWAY TEAM Leaders & Batting Stats
            html += "\n<h2>" + data['Team 2 (T2)'].split()[-1] +  " Leaders & Batting Stats</h2>"
            
            html += "\n<ul>\n<li>" + data['Player Stats (T2)'][0]['home_top_season_player_name'] + " is leading the " +data['Team 2 (T2)'].split()[-1] + " with " + str(data['Player Stats (T2)'][0]['home_top_season_h']) + " this season while batting " + str(data['Player Stats (T2)'][0]['home_top_season_avg'])+ " with " + str(data['Player Stats (T2)'][0]['home_top_season_rbi']) + " RBIs. He currently has " + str(data['Player Stats (T2)'][0]['home_top_season_hr']) + " home runs and Walks with an " + str(data['Player Stats (T2)'][0]['home_top_season_obp'])  + " OBP this season."  + "</li>\n</ul>"

            html += '\n<table class="table"><caption></caption>' 

            table4_col = ["Name", "GP", "AVG", "OBP", "SLG", "HR", "RBI", "H" ]
            table4_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table4_cn.join(table4_col)}</th>\n</tr>\n</thead>'
            
            table4_row1 = ["<strong>" + str(data['Player Stats (T2)'][0]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][0]['home_top_season_GP']), str(data['Player Stats (T2)'][0]['home_top_season_avg']),  str(data['Player Stats (T2)'][0]['home_top_season_obp']), str(data['Player Stats (T2)'][0]['home_top_season_slg']), str(data['Player Stats (T2)'][0]['home_top_season_hr']), str(data['Player Stats (T2)'][0]['home_top_season_rbi']), str(data['Player Stats (T2)'][0]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row1)}</td>\n</tr>'

            table4_row2 = ["<strong>" + str(data['Player Stats (T2)'][1]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][1]['home_top_season_GP']), str(data['Player Stats (T2)'][1]['home_top_season_avg']),  str(data['Player Stats (T2)'][1]['home_top_season_obp']), str(data['Player Stats (T2)'][1]['home_top_season_slg']), str(data['Player Stats (T2)'][1]['home_top_season_hr']), str(data['Player Stats (T2)'][1]['home_top_season_rbi']), str(data['Player Stats (T2)'][1]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row2)}</td>\n</tr>'

            table4_row3 = ["<strong>" + str(data['Player Stats (T2)'][2]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][2]['home_top_season_GP']), str(data['Player Stats (T2)'][2]['home_top_season_avg']),  str(data['Player Stats (T2)'][2]['home_top_season_obp']), str(data['Player Stats (T2)'][2]['home_top_season_slg']), str(data['Player Stats (T2)'][2]['home_top_season_hr']), str(data['Player Stats (T2)'][2]['home_top_season_rbi']), str(data['Player Stats (T2)'][2]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row3)}</td>\n</tr>'

            table4_row4 = ["<strong>" + str(data['Player Stats (T2)'][3]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][3]['home_top_season_GP']), str(data['Player Stats (T2)'][3]['home_top_season_avg']),  str(data['Player Stats (T2)'][3]['home_top_season_obp']), str(data['Player Stats (T2)'][3]['home_top_season_slg']), str(data['Player Stats (T2)'][3]['home_top_season_hr']), str(data['Player Stats (T2)'][3]['home_top_season_rbi']), str(data['Player Stats (T2)'][3]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row4)}</td>\n</tr>'

            table4_row5 = ["<strong>" + str(data['Player Stats (T2)'][4]['home_top_season_player_name']) +"</strong>", str(data['Player Stats (T2)'][4]['home_top_season_GP']), str(data['Player Stats (T2)'][4]['home_top_season_avg']),  str(data['Player Stats (T2)'][4]['home_top_season_obp']), str(data['Player Stats (T2)'][4]['home_top_season_slg']), str(data['Player Stats (T2)'][4]['home_top_season_hr']), str(data['Player Stats (T2)'][4]['home_top_season_rbi']), str(data['Player Stats (T2)'][4]['home_top_season_h']) ] 
            table4_cn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_cn.join(table4_row5)}</td>\n</tr>\n</tbody>\n</table>'

            match_teams = data['Match']
            match_teams = match_teams.replace(" ","_")
            filename = match_teams + '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
            filepath_name = os.path.join(SAVEDIRPATH + "/MLB/", filename+".html")
            # command.run(['sudo', 'chmod', '-R', '777', '/home/ubuntu/article-automation/NBA']) 
            # text_file = open(filepath_name , "w")
            # text_file.write(html)
            # text_file.close()
            try:
                text_file = open(filepath_name , "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/MLB_Images"
            thumbnail = Betpicks.get_article_thumbnail(self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/MLB/"
            try:
                shutil.copy(thumbnail[1], current_path)
                os.chdir(SAVEDIRPATH+"/MLB")
                os.rename(thumbnail[0], filename+'.jpg')
            except Exception:
                pass
            print("Article Saved!")



    def mlb_main(self):

        if os.path.exists('/home/ubuntu/article-automation/MLB'):
            command.run(['sudo', 'chmod', '-R', '777', '/home/ubuntu/article-automation/MLB']) 
            shutil.rmtree(SAVEDIRPATH+"/MLB", ignore_errors=False, onerror=None)
        if os.path.exists(SAVEDIRPATH+"/MLB.zip"):
            os.remove(SAVEDIRPATH+"/MLB.zip")


        URL =  "http://api.sportradar.us/mlb/trial/v7/en/games/" + self.YEAR + "/"+ self.MONTH + "/" + self.DAY + "/schedule.json?api_key=" + self.API_KEY
        # http://api.sportradar.us/mlb/trial/v7/en/games/2023/05/31/schedule.json?api_key=nappjc3prcnjt4d445vuehxq

        
        data = Betpicks.get_games_info(self, URL)
        if data.__contains__('games'):
            games = data['games']
            games_data_article = []
            
            for game in games:
                if game['status'] == 'unnecessary':
                    smtp_server = 'YOUR_SMTP_SERVER'
                    smtp_port = 0
                    smtp_username = 'YOUR_EMAIL_ADDRESS'
                    smtp_password = 'YOUR_PASSWORD'
                    context = ssl.create_default_context()


                    msg = MIMEText('Dear ,\
                    \n\nI hope this email finds you well. I am writing to inform you that unfortunately, we were unable to generate the MLB article you requested for the match between ' + game['home']['name'] + ' and ' + game['away']['name'] + '. This is due to the fact that the game had an unnecessary status, which means that it did not have a match sr_id associated with it. Without a match sr_id, our automated system is unable to fetch the necessary data from the sportsradar API to generate the article.\
                    \n\nWe understand that you were expecting a detailed article for this match, and we apologize that we could not deliver on this occasion. We apologize once again for any inconvenience caused, and we thank you for your understanding. If you have any questions or concerns, please do not hesitate to reach out to us.\
                    \n\nBest regards,\
                    \n\nAutomated Articles Bot\
                    \nBetpicks')
                    msg['Subject'] = 'Match Article Not Generated Due to Unnecessary Status'
                    msg['From'] = 'contact@sportsinformationtraders.com'
                    msg['To'] = 'sportsinformationtraders@gmail.com'
                    sender_email = 'contact@sportsinformationtraders.com'
                    receiver_email = 'sportsinformationtraders@gmail.com'
                    try:
                        server = smtplib.SMTP_SSL(smtp_server,smtp_port,context=context)
                        server.ehlo()
                        server.login(smtp_username, smtp_password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                    except Exception as e:
                        print(e)
                    finally:
                        server.quit() 

                    continue
                
               
                game_id = game['id']
                game_scheduled = game['scheduled']
                
                game_date = datetime.strptime(game_scheduled, '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.timezone('US/Eastern')).date()
                game_time = datetime.strptime(game_scheduled, '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.timezone('US/Eastern')).time()
                game_time = game_time.strftime("%I:%M %p")
            

                game_day_name = game_date.strftime("%A")
                game_month_name = game_date.strftime("%B")
                game_day_num = game_date.strftime("%d")
                game_year = game_date.strftime("%Y")

                game_date = game_date.strftime("%m-%d-%Y")
                # game_time = game_time.strftime("%H:%M")
                game_location = game['venue']['city'] + ', ' + game['venue']['state']
                game_broadcast = game['broadcast']['network']  
                game_arena = game['venue']['name']
                team_home = game['home']['name']
                team_home_id = game['home']['id']
                team_away = game['away']['name']
                team_away_id = game['away']['id']

                

                #########   GAME STATISTICS #########
                URL =  "http://api.sportradar.us/mlb/trial/v7/en/seasons/"+ self.YEAR + "/REG/teams/" + team_home_id + "/statistics.json?api_key=" + self.API_KEY
                home_data = Betpicks.get_data_request(self, URL)

                URL =  "http://api.sportradar.us/mlb/trial/v7/en/seasons/"+ self.YEAR + "/REG/teams/" + team_away_id + "/statistics.json?api_key=" + self.API_KEY
                away_data = Betpicks.get_data_request(self, URL)


                # PITCHING MATCH UP TABLE INFO
                home_win = home_data['statistics']['pitching']['overall']['games']['win'] 
                home_loss =  home_data['statistics']['pitching']['overall']['games']['loss']
                home_gs =  home_data['statistics']['pitching']['overall']['games']['qstart']
                away_win = away_data['statistics']['pitching']['overall']['games']['win'] 
                away_loss =  away_data['statistics']['pitching']['overall']['games']['loss']
                away_gs =  away_data['statistics']['pitching']['overall']['games']['qstart']

                home_era = home_data['statistics']['pitching']['overall']['era']
                away_era = away_data['statistics']['pitching']['overall']['era']
                
                home_ip = home_data['statistics']['pitching']['overall']['pitch_count']
                away_ip = away_data['statistics']['pitching']['overall']['pitch_count']

                home_bb = home_data['statistics']['pitching']['overall']['onbase']['bb']
                away_bb = away_data['statistics']['pitching']['overall']['onbase']['bb']


                URL =  "http://api.sportradar.us/mlb/trial/v7/en/games/"+ game_id + "/summary.json?api_key=" + self.API_KEY
                game_summary = Betpicks.get_data_request(self, URL)
     
                
                # STARTING PITCHER INFO

                home_starting_pitcher_id = game_summary['game']['home']['probable_pitcher']['id']
                home_starting_pitcher_name = game_summary['game']['home']['probable_pitcher']['first_name'] + ' ' + game_summary['game']['home']['probable_pitcher']['last_name']
                away_starting_pitcher_id = game_summary['game']['away']['probable_pitcher']['id']
                away_starting_pitcher_name = game_summary['game']['away']['probable_pitcher']['first_name'] + ' ' + game_summary['game']['away']['probable_pitcher']['last_name']
                                
                
                # HOME LEADERS AND BATTING STATS TABLE DATA
                URL =  "http://api.sportradar.us/mlb/trial/v7/en/seasons/" + self.YEAR + "/REG/teams/" + team_home_id + "/statistics.json?api_key=" + self.API_KEY
                # http://api.sportradar.us/mlb/trial/v7/en/seasons/2023/REG/teams/55714da8-fcaf-4574-8443-59bfb511a524/statistics.json?api_key=nappjc3prcnjt4d445vuehxq

                home_season_stats = Betpicks.get_data_request(self, URL)

                home_player_season_stats = home_season_stats['players']
                home_player_season_stats.sort(key=self.get_mlb_season_points)
                home_player_season_stats.reverse()
                home_player_season_stats = home_player_season_stats[:5]


                """Top Player Stats Home"""


                top_player_stats_home = []
                for players_stats in home_player_season_stats:
                    home_top = {
                        'home_top_season_player_name': players_stats['first_name'] + " " + players_stats['last_name'],
                        'home_top_season_GP': players_stats['statistics']['hitting']['overall']['games']['play'],
                        'home_top_season_avg': players_stats['statistics']['hitting']['overall']['avg'],
                        'home_top_season_obp': players_stats['statistics']['hitting']['overall']['obp'],
                        'home_top_season_slg': players_stats['statistics']['hitting']['overall']['slg'],
                        'home_top_season_rbi': players_stats['statistics']['hitting']['overall']['rbi'],
                        'home_top_season_h': players_stats['statistics']['hitting']['overall']['onbase']['h'],
                        'home_top_season_hr': players_stats['statistics']['hitting']['overall']['onbase']['hr']
                        
                    }
                    top_player_stats_home.append(home_top) #Player Stats (T1)

              
                # HOME LEADERS AND BATTING STATS TABLE DATA
                URL =  "http://api.sportradar.us/mlb/trial/v7/en/seasons/" + self.YEAR + "/REG/teams/" + team_away_id + "/statistics.json?api_key=" + self.API_KEY
                # http://api.sportradar.us/mlb/trial/v7/en/seasons/2023/REG/teams/55714da8-fcaf-4574-8443-59bfb511a524/statistics.json?api_key=nappjc3prcnjt4d445vuehxq

                away_season_stats = Betpicks.get_data_request(self, URL)

                away_player_season_stats = away_season_stats['players']
                away_player_season_stats.sort(key=self.get_mlb_season_points)
                away_player_season_stats.reverse()
                away_player_season_stats = away_player_season_stats[:5]

                """Top Player Stats away"""
                top_player_stats_away = []
                for players_stats in away_player_season_stats:
                    away_top = {
                        'home_top_season_player_name': players_stats['first_name'] + " " + players_stats['last_name'],
                        'home_top_season_GP': players_stats['statistics']['hitting']['overall']['games']['play'],
                        'home_top_season_avg': players_stats['statistics']['hitting']['overall']['avg'],
                        'home_top_season_obp': players_stats['statistics']['hitting']['overall']['obp'],
                        'home_top_season_slg': players_stats['statistics']['hitting']['overall']['slg'],
                        'home_top_season_rbi': players_stats['statistics']['hitting']['overall']['rbi'],
                        'home_top_season_h': players_stats['statistics']['hitting']['overall']['onbase']['h'],
                        'home_top_season_hr': players_stats['statistics']['hitting']['overall']['onbase']['hr']
                        
                    }
                    top_player_stats_away.append(away_top) #Player Stats (T2)



                print("End of the processing")
                
                game_data = {
                    "Match": team_home + ' vs ' + team_away,
                    "Game Day": game_date,
                    "Game Time": game_time,
                    "game_day_name": game_day_name,
                    "game_day_num": game_day_num,
                    "game_month_name": game_month_name,
                    "game_year": game_year,
                    "game_broadcast": game_broadcast,
                    "Location": game_location,
                    "Arena": game_arena,


                    "Team 1 (T1) starting pitcher": home_starting_pitcher_name,
                    "Team 1 (T1)": team_home,
                    "Team 1 (T1) win": home_win,
                    "Team 1 (T1) loss": home_loss,
                    "Team 1 (T1) era": home_era,
                    "Team 1 (T1) ip": home_ip,
                    "Team 1 (T1) gs": home_gs,
                    "Team 1 (T1) bb": home_bb,
                    "Player Stats (T1)": top_player_stats_home,


                    "Team 2 (T2) starting pitcher": away_starting_pitcher_name,
                    "Team 2 (T2)": team_away,
                    "Team 2 (T2) era": away_era,
                    "Team 2 (T2) ip": away_ip,
                    "Team 2 (T2) bb": away_bb,
                    "Team 2 (T2) gs": away_gs,
                    "Team 2 (T2) win": away_win,
                    "Team 2 (T2) loss": away_loss,
                    
                    "Player Stats (T2)": top_player_stats_away,
                }

                games_data_article.append(game_data)
                print("Article Written")

            os.mkdir(SAVEDIRPATH+"/MLB")
            print("MLB Folder Created!")
            try:
                self.generate_html(games_data_article)
                shutil.make_archive(SAVEDIRPATH+"/MLB", 'zip', SAVEDIRPATH+"/MLB")
                print("Success Online!")
            except:
                self.offline_html(games_data_article)            
                shutil.make_archive(SAVEDIRPATH+"/MLB", 'zip', SAVEDIRPATH+"/MLB")
                print("Success Offline!")
        else:
            print("Data not Found")
           

class NBA_Article(Betpicks):

    def __init__(self):
        article_date = date.today()
        self.DAY = str(article_date.day)
        self.MONTH = str(article_date.month)
        self.YEAR = str(article_date.year)
        self.API_KEY = os.environ['nba_api_key']
        self.ODDS_API_KEY = os.environ['odds_api_key']
    

    def get_season_points(self, element):
        return element['average']['points']
    

    def get_season_steals(self, element):
        return element['average']['steals']
    

    def get_season_blocks(self, element):
        return element['average']['blocks']


    def generate_html(self, games_data_article):
        for data in games_data_article:
            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            html += Betpicks.generate_response(self, data['Player Stats (T1)'][0]['home_top_season_player_name'] + " and the " + data['Team 1 (T1)'] + " will look to fend off " + data['Player Stats (T2)'][0]['away_top_season_player_name'] + "s " + data['Team 2 (T2)'] + " on " + data['Game Day'] + ". The " + data['favorite_team'] + " are (" + data['spread'] + ")-point favorite. A point total of (" + data['total_over_under'] + ") is set for the game. Find more below on the " + data['Team 1 (T1)'].split()[-1] + " vs. " + data['Team 2 (T2)'].split()[-1] + " betting line, injury report, head-to-head stats, best bets and more.")
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Spread and Betting Line</h2>"
            html += '\n<table class="table"><caption>' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + ' Betting Information</caption>'
            table1_col = ["Favorite", "Spread", "Favorite Spread Odds", "Underdog Spread Odds", "Total", "Over Total Odds", "Under Total Odds", "Favorite Moneyline", "Underdog Moneyline"]
            table1_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table1_cn.join(table1_col)}</th>\n</tr>\n</thead>'
            table1_row = [data['favorite_team'],data['spread'],data['favorite_spread_odds'],data['underdog_spread_odds'],data['total_over_under'],data['over_total_odds'],data['under_total_odds'],data['favorite_moneyline'],data['underdog_moneyline']]
            table1_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table1_rn.join(table1_row)}</td>\n</tr>\n</tbody>\n</table>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['Game Day']) + "</li>\n<li><strong>Game Time:</strong> " + str(data['Game Time']) + "</li>\n<li><strong>Location:</strong> " + data['Location'] + "</li>\n<li><strong>Arena:</strong> " + data['Arena'] + "</li>\n</ul>"
            html += "\n<h2>Computer Predictions for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += '\n<table class="table"><caption>Computer Picks for ' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + '</caption>'
            table2_col = ["ATS", "Over/Under", "AI Prediction"]
            table2_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table2_cn.join(table2_col)}</th>\n</tr>\n</thead>'
            table2_row = ["+"+data['spread'],data['total_over_under'],data["favorite_team"]+" "+data['spread']+" Over "+data["total_over_under"]]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row)}</td>\n</tr>\n</tbody>\n</table>'
            # html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends = [
            #     Betpicks.generate_response(self, data['Team 1 (T1)'].split()[0] + "'s record against the spread last year was xx-xx-x."), 
            #     Betpicks.generate_response(self, "As "+data['spread']+"-point favorites or more, the " + data['Team 1 (T1)'].split()[-1] + " went xx-xx against the spread last season."), 
            #     Betpicks.generate_response(self, "There were xx " + data['Team 1 (T1)'].split()[0] + " games (out of xx) that went over the total last year.")
            #     ]
            list2_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list2_rn.join(article_betting_trends)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
            article_team1_leader = [
                Betpicks.generate_response(self, data['Player Stats (T1)'][0]['home_top_season_player_name'] + " paced his squad in points (" + str(data['Player Stats (T1)'][0]['home_top_season_points']) + "), rebounds (" + str(data['Player Stats (T1)'][0]['home_top_season_rebounds']) + ") and assists (" + str(data['Player Stats (T1)'][0]['home_top_season_assists']) + ") per contest last season, shooting " + str(round(data['Player Stats (T1)'][0]['home_top_season_field_point'],1)) + "% from the field and " + str(round(data['Player Stats (T1)'][0]['home_top_season_downtownpoint'],1)) + "% from downtown with " + str(data['Player Stats (T1)'][0]['home_top_season_three_points']) + " made 3-pointers per contest. At the other end, he delivered " + str(data['Player Stats (T1)'][0]['home_top_season_steals']) + " steals and " + str(data['Player Stats (T1)'][0]['home_top_season_blocks']) + " blocks."),
                Betpicks.generate_response(self, data['Player Stats (T1)'][1]['home_top_season_player_name'] + " posted " + str(data['Player Stats (T1)'][1]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][1]['home_top_season_assists']) + " assists and " + str(data['Player Stats (T1)'][1]['home_top_season_rebounds']) + " rebounds per contest last year."),
                Betpicks.generate_response(self, data['Player Stats (T1)'][2]['home_top_season_player_name'] + " averaged " + str(data['Player Stats (T1)'][2]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][2]['home_top_season_rebounds']) + " rebounds and " + str(data['Player Stats (T1)'][2]['home_top_season_assists']) + " assists per contest last season. At the other end, he averaged " + str(data['Player Stats (T1)'][2]['home_top_season_steals']) + " steals and " + str(data['Player Stats (T1)'][2]['home_top_season_blocks']) + " blocks."),
                Betpicks.generate_response(self, data['Player Stats (T1)'][3]['home_top_season_player_name'] + " put up " + str(data['Player Stats (T1)'][3]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][3]['home_top_season_rebounds']) + " rebounds and " + str(data['Player Stats (T1)'][3]['home_top_season_assists']) + " assists per contest last year. At the other end, he posted " + str(data['Player Stats (T1)'][3]['home_top_season_steals']) + " steals and " + str(data['Player Stats (T1)'][3]['home_top_season_blocks']) + " blocks."),
                Betpicks.generate_response(self, data['Player Stats (T1)'][4]['home_top_season_player_name'] + " put up " + str(data['Player Stats (T1)'][4]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][4]['home_top_season_rebounds']) + " rebounds and " + str(data['Player Stats (T1)'][4]['home_top_season_assists']) + " assists per game last year, shooting " + str(round(data['Player Stats (T1)'][4]['home_top_season_field_point'],1)) + "% from the floor and " + str(round(data['Player Stats (T1)'][4]['home_top_season_downtownpoint'],1)) + "% from beyond the arc with " + str(data['Player Stats (T1)'][4]['home_top_season_three_points']) + " made 3-pointers per game.")
                ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team1_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Season Stats</h2>"
            html += '\n<table class="table">'
            table3_col = ["", "Stat"]
            table3_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table3_cn.join(table3_col)}</th>\n</tr>\n</thead>'
            table3_row1 = ["<strong>Field Goal %</strong>",str(data['Field Goal (T1)'])]
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row1)}</td>\n</tr>'
            table3_row2 = ["<strong>Opp. Field Goal %</strong>",str(data['Opp. Field Goal (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row2)}</td>\n</tr>'
            table3_row3 = ["<strong>Rebounds Per Game %</strong>",str(data['Rebounds (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row3)}</td>\n</tr>'
            table3_row4 = ["<strong>Opp. Rebounds Per Game %</strong>",str(data['Opp. Rebounds (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row4)}</td>\n</tr>'
            table3_row5 = ["<strong>Turnovers Per Game %</strong>",str(data['Turnovers (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row5)}</td>\n</tr>'
            table3_row6 = ["<strong>Opp. Turnovers Per Game %</strong>",str(data['Opp. Turnovers (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row6)}</td>\n</tr>\n</tbody>\n</table>'
            # html += "\n<h2>" + data['Team 2 (T2)'].split()[-1] + " vs " + data['Team 1 (T1)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends_1 = [
            #     Betpicks.generate_response(self, "Against the spread, " + data['Team 2 (T2)'].split()[0] + " is xx-xx-x this season."), 
            #     Betpicks.generate_response(self, "The " + data['Team 2 (T2)'].split()[-1] + " are xx-xx as "+data['spread']+"-point underdogs or more."), 
            #     Betpicks.generate_response(self, "Out of xx " + data['Team 2 (T2)'].split()[0] + " games so far this season, xx have hit the over.")
            #     ]
            # list3_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list3_rn.join(article_betting_trends_1)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Leaders</h2>"
            article_team2_leader = [
                Betpicks.generate_response(self, data['Player Stats (T2)'][0]['away_top_season_player_name'] + " averages " + str(data['Player Stats (T2)'][0]['away_top_season_points']) + " points and adds " + str(data['Player Stats (T2)'][0]['away_top_season_assists']) + " assists per game, putting him at the top of the " + data['Team 2 (T2)'].split()[-1] + "’ leaderboards in those statistics."),
                Betpicks.generate_response(self, data['Player Stats (T2)'][1]['away_top_season_player_name'] + " is at the top of the " + data['Team 2 (T2)'].split()[0] + " " + data['Team 2 (T2)'].split()[1] + " rebounding leaderboard with " + str(data['Player Stats (T2)'][1]['away_top_season_rebounds']) + " rebounds per game. He also notches " + str(data['Player Stats (T2)'][1]['away_top_season_points']) + " points and adds " + str(data['Player Stats (T2)'][1]['away_top_season_assists']) + " assists per game."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[0] + " " + data['Team 2 (T2)'].split()[1] + " leader in steals is " + data['away_player_best_steals'] + " with " + str(data['away_player_best_steals_avg']) + " per game, and its leader in blocks is " + data['away_player_best_blocks'] + " with " + str(data['away_player_best_blocks_avg']) + " per game.")
                ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team2_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Season Stats</h2>"
            html += '\n<table class="table">'
            table4_col = ["", "Stat"]
            table4_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table4_cn.join(table4_col)}</th>\n</tr>\n</thead>'
            table4_row1 = ["<strong>Field Goal %</strong>",str(data['Field Goal (T2)'])]
            table4_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_rn.join(table4_row1)}</td>\n</tr>'
            table4_row2 = ["<strong>Opp. Field Goal %</strong>",str(data['Opp. Field Goal (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row2)}</td>\n</tr>'
            table4_row3 = ["<strong>Rebounds Per Game %</strong>",str(data['Rebounds (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row3)}</td>\n</tr>'
            table4_row4 = ["<strong>Opp. Rebounds Per Game %</strong>",str(data['Opp. Rebounds (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row4)}</td>\n</tr>'
            table4_row5 = ["<strong>Turnovers Per Game %</strong>",str(data['Turnovers (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row5)}</td>\n</tr>'
            table4_row6 = ["<strong>Opp. Turnovers Per Game %</strong>",str(data['Opp. Turnovers (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row6)}</td>\n</tr>\n</tbody>\n</table>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Injury Report</h2>"
            article_team1_injury = ""
            for injury in data['Injuries (T1)']:
                article_team1_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 1 (T1)'].split()[-1] + ": </strong>" + article_team1_injury
            article_team2_injury = ""
            for injury in data['Injuries (T2)']:
                article_team2_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 2 (T2)'].split()[-1] + ": </strong>" + article_team2_injury
            html += "\n<h2>Betting Tips for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += Betpicks.generate_response(self, "\nWe have the " + data['Team 1 (T1)'].split()[-1] + " ("+data['spread']+") predicted as our best bet in this game. Our computer model has the scoring going over the total of "+data['total_over_under']+" points, finishing with the final outcome of " + data['Team 1 (T1)'] + " " + data['spread']+ "." )

            match_teams = data['Match']
            match_teams = match_teams.replace(" ","_")
            filename = match_teams + '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
            filepath_name = os.path.join(SAVEDIRPATH + "/NBA/", filename+".html")
            try:
                text_file = open(filepath_name , "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/NBA_Images"
            thumbnail = Betpicks.get_article_thumbnail(self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/NBA/"
            try:
                shutil.copy(thumbnail[1], current_path)
                os.chdir(SAVEDIRPATH + "/NBA")
                os.rename(thumbnail[0], filename+'.jpg')
            except Exception:
                pass
            print("Article Saved!")


    def offline_html(self, games_data_article):
        for data in games_data_article:
            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            html += data['Player Stats (T1)'][0]['home_top_season_player_name'] + " and the " + data['Team 1 (T1)'] + " will look to fend off " + data['Player Stats (T2)'][0]['away_top_season_player_name'] + "s " + data['Team 2 (T2)'] + " on " + data['Game Day'] + ". The " + data['favorite_team'] + " are (" + data['spread'] + ")-point favorite. A point total of (" + data['total_over_under'] + ") is set for the game. Find more below on the " + data['Team 1 (T1)'].split()[-1] + " vs. " + data['Team 2 (T2)'].split()[-1] + " betting line, injury report, head-to-head stats, best bets and more."
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Spread and Betting Line</h2>"
            html += '\n<table class="table"><caption>' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + ' Betting Information</caption>'
            table1_col = ["Favorite", "Spread", "Favorite Spread Odds", "Underdog Spread Odds", "Total", "Over Total Odds", "Under Total Odds", "Favorite Moneyline", "Underdog Moneyline"]
            table1_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table1_cn.join(table1_col)}</th>\n</tr>\n</thead>'
            table1_row = [data['favorite_team'],str(data['spread']),str(data['favorite_spread_odds']),str(data['underdog_spread_odds']),str(data['total_over_under']),str(data['over_total_odds']),str(data['under_total_odds']),str(data['favorite_moneyline']),str(data['underdog_moneyline'])]
            table1_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table1_rn.join(table1_row)}</td>\n</tr>\n</tbody>\n</table>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['Game Day']) + "</li>\n<li><strong>Game Time:</strong> " + str(data['Game Time']) + "</li>\n<li><strong>Location:</strong> " + data['Location'] + "</li>\n<li><strong>Arena:</strong> " + data['Arena'] + "</li>\n</ul>"
            html += "\n<h2>Computer Predictions for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += '\n<table class="table"><caption>Computer Picks for ' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + '</caption>'
            table2_col = ["ATS", "Over/Under", "AI Prediction"]
            table2_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table2_cn.join(table2_col)}</th>\n</tr>\n</thead>'
            table2_row = ["+"+data['spread'],data['total_over_under'],data["favorite_team"]+" -"+data['spread']+" Over "+data["total_over_under"]]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row)}</td>\n</tr>\n</tbody>\n</table>'
            # html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends = [
            #     data['Team 1 (T1)'].split()[0] + "'s record against the spread last year was xx-xx-x.", 
            #     "As "+data['spread']+"-point favorites or more, the " + data['Team 1 (T1)'].split()[-1] + " went xx-xx against the spread last season.", 
            #     "There were xx " + data['Team 1 (T1)'].split()[0] + " games (out of xx) that went over the total last year."
            #     ]
            list2_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list2_rn.join(article_betting_trends)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
            article_team1_leader = [
                data['Player Stats (T1)'][0]['home_top_season_player_name'] + " paced his squad in points (" + str(data['Player Stats (T1)'][0]['home_top_season_points']) + "), rebounds (" + str(data['Player Stats (T1)'][0]['home_top_season_rebounds']) + ") and assists (" + str(data['Player Stats (T1)'][0]['home_top_season_assists']) + ") per contest last season, shooting " + str(round(data['Player Stats (T1)'][0]['home_top_season_field_point'],1)) + "% from the field and " + str(round(data['Player Stats (T1)'][0]['home_top_season_downtownpoint'],1)) + "% from downtown with " + str(data['Player Stats (T1)'][0]['home_top_season_three_points']) + " made 3-pointers per contest. At the other end, he delivered " + str(data['Player Stats (T1)'][0]['home_top_season_steals']) + " steals and " + str(data['Player Stats (T1)'][0]['home_top_season_blocks']) + " blocks.",
                data['Player Stats (T1)'][1]['home_top_season_player_name'] + " posted " + str(data['Player Stats (T1)'][1]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][1]['home_top_season_assists']) + " assists and " + str(data['Player Stats (T1)'][1]['home_top_season_rebounds']) + " rebounds per contest last year.",
                data['Player Stats (T1)'][2]['home_top_season_player_name'] + " averaged " + str(data['Player Stats (T1)'][2]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][2]['home_top_season_rebounds']) + " rebounds and " + str(data['Player Stats (T1)'][2]['home_top_season_assists']) + " assists per contest last season. At the other end, he averaged " + str(data['Player Stats (T1)'][2]['home_top_season_steals']) + " steals and " + str(data['Player Stats (T1)'][2]['home_top_season_blocks']) + " blocks.",
                data['Player Stats (T1)'][3]['home_top_season_player_name'] + " put up " + str(data['Player Stats (T1)'][3]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][3]['home_top_season_rebounds']) + " rebounds and " + str(data['Player Stats (T1)'][3]['home_top_season_assists']) + " assists per contest last year. At the other end, he posted " + str(data['Player Stats (T1)'][3]['home_top_season_steals']) + " steals and " + str(data['Player Stats (T1)'][3]['home_top_season_blocks']) + " blocks.",
                data['Player Stats (T1)'][4]['home_top_season_player_name'] + " put up " + str(data['Player Stats (T1)'][4]['home_top_season_points']) + " points, " + str(data['Player Stats (T1)'][4]['home_top_season_rebounds']) + " rebounds and " + str(data['Player Stats (T1)'][4]['home_top_season_assists']) + " assists per game last year, shooting " + str(round(data['Player Stats (T1)'][4]['home_top_season_field_point'],1)) + "% from the floor and " + str(round(data['Player Stats (T1)'][4]['home_top_season_downtownpoint'],1)) + "% from beyond the arc with " + str(data['Player Stats (T1)'][4]['home_top_season_three_points']) + " made 3-pointers per game."
                ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team1_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Season Stats</h2>"
            html += '\n<table class="table">'
            table3_col = ["", "Stat"]
            table3_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table3_cn.join(table3_col)}</th>\n</tr>\n</thead>'
            table3_row1 = ["<strong>Field Goal %</strong>",str(data['Field Goal (T1)'])]
            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row1)}</td>\n</tr>'
            table3_row2 = ["<strong>Opp. Field Goal %</strong>",str(data['Opp. Field Goal (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row2)}</td>\n</tr>'
            table3_row3 = ["<strong>Rebounds Per Game %</strong>",str(data['Rebounds (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row3)}</td>\n</tr>'
            table3_row4 = ["<strong>Opp. Rebounds Per Game %</strong>",str(data['Opp. Rebounds (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row4)}</td>\n</tr>'
            table3_row5 = ["<strong>Turnovers Per Game %</strong>",str(data['Turnovers (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row5)}</td>\n</tr>'
            table3_row6 = ["<strong>Opp. Turnovers Per Game %</strong>",str(data['Opp. Turnovers (T1)'])]
            html += f'\n<tr>\n<td>{table3_rn.join(table3_row6)}</td>\n</tr>\n</tbody>\n</table>'
            # html += "\n<h2>" + data['Team 2 (T2)'].split()[-1] + " vs " + data['Team 1 (T1)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends_1 = [
            #     "Against the spread, " + data['Team 2 (T2)'].split()[0] + " is xx-xx-x this season.", 
            #     "The " + data['Team 2 (T2)'].split()[-1] + " are xx-xx as "+data['spread']+"-point underdogs or more.", 
            #     "Out of xx " + data['Team 2 (T2)'].split()[0] + " games so far this season, xx have hit the over."
            #     ]
            # list3_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list3_rn.join(article_betting_trends_1)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Leaders</h2>"
            article_team2_leader = [
                data['Player Stats (T2)'][0]['away_top_season_player_name'] + " averages " + str(data['Player Stats (T2)'][0]['away_top_season_points']) + " points and adds " + str(data['Player Stats (T2)'][0]['away_top_season_assists']) + " assists per game, putting him at the top of the " + data['Team 2 (T2)'].split()[-1] + "’ leaderboards in those statistics.",
                data['Player Stats (T2)'][1]['away_top_season_player_name'] + " is at the top of the " + data['Team 2 (T2)'].split()[0] + " " + data['Team 2 (T2)'].split()[1] + " rebounding leaderboard with " + str(data['Player Stats (T2)'][1]['away_top_season_rebounds']) + " rebounds per game. He also notches " + str(data['Player Stats (T2)'][1]['away_top_season_points']) + " points and adds " + str(data['Player Stats (T2)'][1]['away_top_season_assists']) + " assists per game.",
                data['Team 2 (T2)'].split()[0] + " " + data['Team 2 (T2)'].split()[1] + " leader in steals is " + data['away_player_best_steals'] + " with " + str(data['away_player_best_steals_avg']) + " per game, and its leader in blocks is " + data['away_player_best_blocks'] + " with " + str(data['away_player_best_blocks_avg']) + " per game."
                ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team2_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Season Stats</h2>"
            html += '\n<table class="table">'
            table4_col = ["", "Stat"]
            table4_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table4_cn.join(table4_col)}</th>\n</tr>\n</thead>'
            table4_row1 = ["<strong>Field Goal %</strong>",str(data['Field Goal (T2)'])]
            table4_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table4_rn.join(table4_row1)}</td>\n</tr>'
            table4_row2 = ["<strong>Opp. Field Goal %</strong>",str(data['Opp. Field Goal (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row2)}</td>\n</tr>'
            table4_row3 = ["<strong>Rebounds Per Game %</strong>",str(data['Rebounds (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row3)}</td>\n</tr>'
            table4_row4 = ["<strong>Opp. Rebounds Per Game %</strong>",str(data['Opp. Rebounds (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row4)}</td>\n</tr>'
            table4_row5 = ["<strong>Turnovers Per Game %</strong>",str(data['Turnovers (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row5)}</td>\n</tr>'
            table4_row6 = ["<strong>Opp. Turnovers Per Game %</strong>",str(data['Opp. Turnovers (T2)'])]
            html += f'\n<tr>\n<td>{table4_rn.join(table4_row6)}</td>\n</tr>\n</tbody>\n</table>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Injury Report</h2>"
            article_team1_injury = ""
            for injury in data['Injuries (T1)']:
                article_team1_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 1 (T1)'].split()[-1] + ": </strong>" + article_team1_injury
            article_team2_injury = ""
            for injury in data['Injuries (T2)']:
                article_team2_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 2 (T2)'].split()[-1] + ": </strong>" + article_team2_injury
            html += "\n<h2>Betting Tips for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html +=  "\nWe have the " + data['Team 1 (T1)'].split()[-1] + " ("+data['spread']+") predicted as our best bet in this game. Our computer model has the scoring going over the total of "+data['total_over_under']+" points, finishing with the final outcome of " + data['Team 1 (T1)'] + " "+data['spread']+ "."

            match_teams = data['Match']
            match_teams = match_teams.replace(" ","_")
            filename = match_teams + '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
            filepath_name = os.path.join(SAVEDIRPATH + "/NBA/", filename+".html")
            # command.run(['sudo', 'chmod', '-R', '777', '/home/ubuntu/article-automation/NBA']) 
            # text_file = open(filepath_name , "w")
            # text_file.write(html)
            # text_file.close()
            try:
                text_file = open(filepath_name , "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/NBA_Images"
            thumbnail = Betpicks.get_article_thumbnail(self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/NBA/"
            try:
                shutil.copy(thumbnail[1], current_path)
                os.chdir(SAVEDIRPATH+"/NBA")
                os.rename(thumbnail[0], filename+'.jpg')
            except Exception:
                pass
            print("Article Saved!")


    def nba_main(self):
        if os.path.exists('/home/ubuntu/article-automation/NBA'):
            command.run(['sudo', 'chmod', '-R', '777', '/home/ubuntu/article-automation/NBA']) 
            shutil.rmtree(SAVEDIRPATH+"/NBA", ignore_errors=False, onerror=None)
        if os.path.exists(SAVEDIRPATH+"/NBA.zip"):
            os.remove(SAVEDIRPATH+"/NBA.zip")
        print("NBA Folder Removed!")
        # api-endpoint
        URL = "http://api.sportradar.us/nba/trial/v7/en/games/" + self.YEAR + "/" + self.MONTH + "/" + self.DAY + "/schedule.json?api_key=" + self.API_KEY
        # Game Info
        data = Betpicks.get_games_info(self, URL)
        if data.__contains__('games'):
            games = data['games']
            games_data_article = []
            for game in games:
                if game['status'] == 'unnecessary':
                    smtp_server = 'YOUR_SMTP_SERVER'
                    smtp_port = 0
                    smtp_username = 'YOUR_EMAIL_USER'
                    smtp_password = 'YOUR_EMAIL_PASSWORD'
                    context = ssl.create_default_context()

                    msg = MIMEText('Dear ,\
                    \n\nI hope this email finds you well. I am writing to inform you that unfortunately, we were unable to generate the NBA article you requested for the match between ' + game['home']['name'] + ' and ' + game['away']['name'] + '. This is due to the fact that the game had an unnecessary status, which means that it did not have a match sr_id associated with it. Without a match sr_id, our automated system is unable to fetch the necessary data from the sportsradar API to generate the article.\
                    \n\nWe understand that you were expecting a detailed article for this match, and we apologize that we could not deliver on this occasion. We apologize once again for any inconvenience caused, and we thank you for your understanding. If you have any questions or concerns, please do not hesitate to reach out to us.\
                    \n\nBest regards,\
                    \n\nAutomated Articles Bot\
                    \nBetpicks')
                    msg['Subject'] = 'Match Article Not Generated Due to Unnecessary Status'
                    msg['From'] = 'contact@sportsinformationtraders.com'
                    msg['To'] = 'sportsinformationtraders@gmail.com'
                    sender_email = 'contact@sportsinformationtraders.com'
                    receiver_email = 'sportsinformationtraders@gmail.com'
                    try:
                        server = smtplib.SMTP_SSL(smtp_server,smtp_port,context=context)
                        server.ehlo()
                        server.login(smtp_username, smtp_password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                    except Exception as e:
                        print(e)
                    finally:
                        server.quit() 

                    continue
                game_id = game['id']
                game_scheduled = game['scheduled']
                game_sr_id = game['sr_id']
                game_date = datetime.strptime(game_scheduled, '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.timezone('US/Eastern')).date()
                game_time = datetime.strptime(game_scheduled, '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.timezone('US/Eastern')).time()
                game_time = game_time.strftime("%I:%M %p")
                game_date = game_date.strftime("%m-%d-%Y")
                # game_time = game_time.strftime("%H:%M")
                game_location = game['venue']['city'] + ', ' + game['venue']['state']
                game_arena = game['venue']['name']
                team_home = game['home']['name']
                team_home_id = game['home']['id']
                team_away = game['away']['name']
                team_away_id = game['away']['id']

                """Home Team Profile"""
                URL = "http://api.sportradar.us/nba/trial/v7/en/teams/" + team_home_id + "/profile.json?api_key=" + self.API_KEY
                home_team_profile = Betpicks.get_data_request(self, URL)
                home_players = home_team_profile['players']
                home_players_names = []
                for players in home_players:
                    home_players_names.append(players['full_name'])

                """Season Stats Home"""
                SEASON_TYPE = "REG"
                YEAR = "2022"
                URL = "http://api.sportradar.us/nba/trial/v7/en/seasons/" + YEAR + "/" + SEASON_TYPE + "/teams/" + team_home_id + "/statistics.json?api_key=" + self.API_KEY
                home_season_stats = Betpicks.get_data_request(self, URL)
                home_field_goal = home_season_stats['own_record']['average']['field_goals_made']
                home_opp_field_goal = home_season_stats['opponents']['average']['field_goals_made']
                home_rebounds = home_season_stats['own_record']['average']['rebounds']
                home_opp_rebounds = home_season_stats['opponents']['average']['rebounds']
                home_turnovers = home_season_stats['own_record']['average']['turnovers']
                home_opp_turnovers = home_season_stats['opponents']['average']['turnovers']

                home_player_season_stats = home_season_stats['players']
                home_player_season_stats.sort(key=self.get_season_points)
                home_player_season_stats.reverse()
                home_player_season_stats = home_player_season_stats[:5]

                """Top Player Stats Home"""
                top_player_stats_home = []
                for players_stats in home_player_season_stats:
                    home_top = {
                        'home_top_season_player_name': players_stats['full_name'],
                        'home_top_season_points': players_stats['average']['points'],
                        'home_top_season_rebounds': players_stats['average']['rebounds'],
                        'home_top_season_assists': players_stats['average']['assists'],
                        'home_top_season_field_point': players_stats['total']['field_goals_pct']*100,
                        'home_top_season_downtownpoint': players_stats['total']['three_points_pct']*100,
                        'home_top_season_three_points': players_stats['average']['three_points_made'],
                        'home_top_season_steals': players_stats['average']['steals'],
                        'home_top_season_blocks': players_stats['average']['blocks']
                    }
                    top_player_stats_home.append(home_top)

                """Away Team Profile"""
                URL = "http://api.sportradar.us/nba/trial/v7/en/teams/" + team_away_id + "/profile.json?api_key=" + self.API_KEY
                away_team_profile = Betpicks.get_data_request(self, URL)
                away_players = away_team_profile['players']
                away_players_names = []
                for players in away_players:
                    away_players_names.append(players['full_name'])

                """Season Stats Away"""
                SEASON_TYPE = "REG"
                YEAR = "2022"
                URL = "http://api.sportradar.us/nba/trial/v7/en/seasons/" + YEAR + "/" + SEASON_TYPE + "/teams/" + team_away_id + "/statistics.json?api_key=" + self.API_KEY
                away_season_stats = Betpicks.get_data_request(self, URL)
                away_field_goal = away_season_stats['own_record']['average']['field_goals_made']
                away_opp_field_goal = away_season_stats['opponents']['average']['field_goals_made']
                away_rebounds = away_season_stats['own_record']['average']['rebounds']
                away_opp_rebounds = away_season_stats['opponents']['average']['rebounds']
                away_turnovers = away_season_stats['own_record']['average']['turnovers']
                away_opp_turnovers = away_season_stats['opponents']['average']['turnovers']

                away_player_season_stats = away_season_stats['players']
                away_player_season_stats.sort(key=self.get_season_steals)
                away_player_season_stats.reverse()
                away_player_best_steals = away_player_season_stats[0]['full_name']
                away_player_best_steals_avg = away_player_season_stats[0]['average']['steals']

                away_player_season_stats.sort(key=self.get_season_blocks)
                away_player_season_stats.reverse()
                away_player_best_blocks = away_player_season_stats[0]['full_name']
                away_player_best_blocks_avg = away_player_season_stats[0]['average']['blocks']

                away_player_season_stats.sort(key=self.get_season_points)
                away_player_season_stats.reverse()
                away_player_season_stats = away_player_season_stats[:3]

                """Top Player Stats Away"""
                top_player_stats_away = []
                for players_stats in away_player_season_stats:
                    away_top = {
                        'away_top_season_player_name': players_stats['full_name'],
                        'away_top_season_points': players_stats['average']['points'],
                        'away_top_season_rebounds': players_stats['average']['rebounds'],
                        'away_top_season_assists': players_stats['average']['assists'],
                        'away_top_season_field_point': players_stats['total']['field_goals_pct']*100,
                        'away_top_season_downtownpoint': players_stats['total']['three_points_pct']*100,
                        'away_top_season_three_points': players_stats['average']['three_points_made'],
                        'away_top_season_steals': players_stats['average']['steals'],
                        'away_top_season_blocks': players_stats['average']['blocks']
                    }
                    top_player_stats_away.append(away_top)

                """Injurys"""
                home_injuries = []
                away_injuries = []
                URL = "http://api.sportradar.us/nba/trial/v7/en/league/injuries.json?api_key=" + self.API_KEY
                season_injury_data = Betpicks.get_data_request(self, URL)
                season_injury_data = season_injury_data['teams']
                for player_injury in season_injury_data:
                    if player_injury['id'] == team_home_id:
                        home_player_injury = player_injury['players']
                        for injury in home_player_injury:
                            injury_data = {
                                'name': injury['full_name'], 
                                'status': injury['injuries'][0]['status'],
                                'desc': injury['injuries'][0]['desc']
                            }
                            home_injuries.append(injury_data)
                    if player_injury['id'] == team_away_id:
                        away_player_injury = player_injury['players']
                        for injury in away_player_injury:
                            injury_data = {
                                'name': injury['full_name'], 
                                'status': injury['injuries'][0]['status'],
                                'desc': injury['injuries'][0]['desc']
                            }
                            away_injuries.append(injury_data)

                """ODDs Data"""
                URL = "https://api.sportradar.us/oddscomparison-ust1/en/eu/sport_events/" + game_sr_id + "/markets.json?api_key=" + self.ODDS_API_KEY
                odds_data = Betpicks.get_data_request(self, URL)
                odds_data = odds_data['sport_event']['consensus']['lines']

                spread = "-"
                home_odds = "-"
                away_odds = "-"
                underdog_spread_odds = "-"
                favorite_spread_odds = "-"
                underdog_moneyline = "-"
                favorite_moneyline = "-"
                favorite_team = "-"
                underdog_team = "-"
                total_over_under = "-"
                over_total_odds = "-"
                under_total_odds = "-"
                home_moneyline = "-"
                away_moneyline = "-"

                for line in odds_data:
                    if line['name'] == 'spread_current':
                        spread = line['spread']
                        home_odds = line['outcomes'][0]['odds']
                        away_odds = line['outcomes'][1]['odds']
                        if float(home_odds) > float(away_odds):
                            favorite_team = "0"
                        else:
                            favorite_team = "1"
                    if line['name'] == 'total_current':
                        total_over_under = line['total']
                        over_total_odds = '-'+str((float(line['outcomes'][0]['odds'])-1)*100)
                        under_total_odds = '-'+str((float(line['outcomes'][1]['odds'])-1)*100)
                    if line['name'] == 'moneyline_current':
                        home_moneyline = str(round((float(line['outcomes'][0]['odds'])-1) * 100,1))
                        away_moneyline = str(round((float(line['outcomes'][1]['odds'])-1) * 100,1))

                if float(away_odds) >= 2.00:
                    away_odds = -100/(float(away_odds) - 1)
                else:
                    away_odds = (float(away_odds) - 1)*100

                if float(home_odds) >= 2.00:
                    home_odds = -100/(float(home_odds) - 1)
                else:
                    home_odds = (float(home_odds) - 1)*100
                
                if away_odds > 0:
                    away_odds = '+'+str(away_odds)
                if home_odds > 0:
                    home_odds = '+'+str(home_odds)

                if favorite_team == "0":
                    favorite_team = team_home
                    underdog_team = team_away
                    underdog_spread_odds = away_odds
                    favorite_spread_odds = home_odds
                    underdog_moneyline = '+'+away_moneyline
                    favorite_moneyline = '-'+home_moneyline
                else:
                    favorite_team = team_away
                    underdog_team = team_home
                    underdog_spread_odds = home_odds
                    favorite_spread_odds = away_odds
                    underdog_moneyline = '+'+home_moneyline
                    favorite_moneyline = '-'+away_moneyline
                    
                game_data = {
                    "Match": team_home + ' vs ' + team_away,
                    "Game Day": game_date,
                    "Game Time": game_time,
                    "Location": game_location,
                    "Arena": game_arena,
                    "Team 1 (T1)": team_home,
                    "Player Stats (T1)": top_player_stats_home,
                    "Field Goal (T1)": home_field_goal,
                    "Opp. Field Goal (T1)": home_opp_field_goal,
                    "Rebounds (T1)": home_rebounds,
                    "Opp. Rebounds (T1)": home_opp_rebounds,
                    "Turnovers (T1)": home_turnovers,
                    "Opp. Turnovers (T1)": home_opp_turnovers,
                    "Injuries (T1)": home_injuries,
                    "Team 2 (T2)": team_away,
                    "Player Stats (T2)": top_player_stats_away,
                    "away_player_best_steals": away_player_best_steals,
                    "away_player_best_steals_avg": away_player_best_steals_avg,
                    "away_player_best_blocks": away_player_best_blocks,
                    "away_player_best_blocks_avg": away_player_best_blocks_avg,
                    "Field Goal (T2)": away_field_goal,
                    "Opp. Field Goal (T2)": away_opp_field_goal,
                    "Rebounds (T2)": away_rebounds,
                    "Opp. Rebounds (T2)": away_opp_rebounds,
                    "Turnovers (T2)": home_turnovers,
                    "Opp. Turnovers (T2)": away_opp_turnovers,
                    "Injuries (T2)": away_injuries,
                    "spread": spread,
                    "underdog_spread_odds": underdog_spread_odds,
                    "favorite_spread_odds": favorite_spread_odds,
                    "favorite_team": favorite_team,
                    "total_over_under": total_over_under,
                    "over_total_odds": over_total_odds,
                    "under_total_odds": under_total_odds,
                    "underdog_moneyline": underdog_moneyline,
                    "favorite_moneyline": favorite_moneyline,
                    "underdog_team": underdog_team
                }
                games_data_article.append(game_data)
                print("Article Written")
            
            os.mkdir(SAVEDIRPATH+"/NBA")
            print("NBA Folder Created!")
            try:
                self.generate_html(games_data_article)
                shutil.make_archive(SAVEDIRPATH+"/NBA", 'zip', SAVEDIRPATH+"/NBA")
                print("Success Online!")
            except:
                self.offline_html(games_data_article)            
                shutil.make_archive(SAVEDIRPATH+"/NBA", 'zip', SAVEDIRPATH+"/NBA")
                print("Success Offline!")
        else:
            print("Data not Found")


class NHL_Article(Betpicks):
    
    def __init__(self):
        article_date = date.today()
        self.DAY = str(article_date.day)
        self.MONTH = str(article_date.month)
        self.YEAR = str(article_date.year)
        self.API_KEY = os.environ['nhl_api_key']
        self.ODDS_API_KEY = os.environ['odds_api_key']
     

    def get_season_goals(self, element):
        return element['statistics']['total']['goals']
    

    def get_season_saves(self, element):
        return element['goaltending']['total']['saves_pct']
    

    def generate_html(self, games_data_article):
        for data in games_data_article:
            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            if data["Game Number"] == 1: 
                html += Betpicks.generate_response(self, "The " + data["Team 1 (T1)"] + " are set for Game 1 on " + str(data["Game Day"]) + " against the " + data["Team 2 (T2)"] + ", beginning at " + str(data["Game Time"]) + " ET. The oddsmakers have made the " + data["favorite_team"] + " solid favorites at " + data["favorite_moneyline"] + " on the moneyline, and the " + data["underdog_team"] + " are at " + data["underdog_moneyline"] + ". Find more below on the " + data["Team 1 (T1)"].split()[-1] + " vs. " + data["Team 2 (T2)"].split()[-1] + " betting line, injury report, head-to-head stats, best bets and more.")
            else:
                if data["Advantage Team"] is None:
                    html += Betpicks.generate_response(self, "On " + str(data["Game Day"]) + " the " + data["Team 1 (T1)"] + " and the " + data["Team 2 (T2)"] + " will face off in Game " + str(data["Game Number"]) + ", beginning at " + str(data["Game Time"]) + " ET. The series is currently tied " + str(data["Home Points"]) + "-" + str(data["Away Points"]) + ". The sportsbooks have made the " + data["Team 1 (T1)"].split()[-1] + " slight favorites at xx on the moneyline, and the " + data["Team 2 (T2)"].split()[-1] + " are at xx. Find more below on the " + data["Match"] + " betting line, injury report, head-to-head stats, best bets and more.")
                elif data["Advantage Team"] == data["Team 1 (T1)"]:
                    html += Betpicks.generate_response(self, "On " + str(data["Game Day"]) + " the " + data["Team 1 (T1)"] + " and the " + data["Team 2 (T2)"] + " will face off in Game " + str(data["Game Number"]) + ", beginning at " + str(data["Game Time"]) + " ET. The " + data["Team 1 (T1)"].split()[-1] + " have a " + str(data["Home Points"]) + "-" + str(data["Away Points"]) + " edge in the series. The sportsbooks have made the " + data["Team 1 (T1)"].split()[-1] + " slight favorites at xx on the moneyline, and the " + data["Team 2 (T2)"].split()[-1] + " are at xx. Find more below on the " + data["Match"] + " betting line, injury report, head-to-head stats, best bets and more.")
                else:
                    html += Betpicks.generate_response(self, "On " + str(data["Game Day"]) + " the " + data["Team 1 (T1)"] + " and the " + data["Team 2 (T2)"] + " will face off in Game " + str(data["Game Number"]) + ", beginning at " + str(data["Game Time"]) + " ET. The " + data["Team 2 (T2)"].split()[-1] + " have a " + str(data["Home Points"]) + "-" + str(data["Away Points"]) + " edge in the series. The sportsbooks have made the " + data["Team 2 (T2)"].split()[-1] + " slight favorites at xx on the moneyline, and the " + data["Team 1 (T1)"].split()[-1] + " are at xx. Find more below on the " + data["Match"] + " betting line, injury report, head-to-head stats, best bets and more.")
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Spread and Betting Line</h2>"
            html += '\n<table class="table"><caption>' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + ' Betting Information</caption>'
            table1_col = ["Favorite", "Moneyline", "Underdog", "Moneyline"]
            table1_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table1_cn.join(table1_col)}</th>\n</tr>\n</thead>'
            table1_row = [data["favorite_team"],data["favorite_moneyline"],data["underdog_team"],data["underdog_moneyline"]]
            table1_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table1_rn.join(table1_row)}</td>\n</tr>\n</tbody>\n</table>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['Game Day']) + "</li>\n<li><strong>Game Time:</strong> " + str(data['Game Time']) + "</li>\n<li><strong>Location:</strong> " + data['Location'] + "</li>\n<li><strong>Arena:</strong> " + data['Arena'] + "</li>\n</ul>"
            html += "\n<h2>Computer Predictions for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += '\n<table class="table"><caption>Computer Picks for ' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + '</caption>'
            table2_col = ["ATS", "Over/Under", "AI Prediction"]
            table2_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table2_cn.join(table2_col)}</th>\n</tr>\n</thead>'
            # table2_row = ["+"+data['spread']+" ("+data["underdog_spread_odds"]+")","+/-"+data["total_over_under"],data["favorite_team"]+" "+data['spread']+" Over "+data["favorite_moneyline"]]
            table2_row = [data['total_over_under'],data["favorite_moneyline"],data["favorite_team"]+" "+data['spread']+" Over "+data["favorite_moneyline"]]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row)}</td>\n</tr>\n</tbody>\n</table>'
            # html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends = [
            #     Betpicks.generate_response(self, "Through xx games as the moneyline favorite this season, " + data["favorite_team"] + " has won xx times."), 
            #     Betpicks.generate_response(self, "The " + data["favorite_team"] + " have won xx of the xx games they have played with moneyline odds shorter than xx."), 
            #     Betpicks.generate_response(self, "There is a " + str(data["win_pct_ml_f"]) + "% chance that " + data["favorite_team"] + " wins this contest, per the moneyline.")
            # ]
            list2_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list2_rn.join(article_betting_trends)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
            article_team1_leader = [
                Betpicks.generate_response(self, data['Player Stats (T1)'][0]['home_top_season_player_name'] + " has been a major player for "+ data['Team 1 (T1)'].split()[-1] + " this season, with " + str(data['Player Stats (T1)'][0]['home_top_season_points']) + " points in " + str(data['Player Stats (T1)'][0]['home_top_season_games_played']) + " games."),
                Betpicks.generate_response(self, "Through " + str(data['Player Stats (T1)'][1]['home_top_season_games_played']) + " games, " + data['Player Stats (T1)'][1]['home_top_season_player_name'] + " has " + str(data['Player Stats (T1)'][1]['home_top_season_goals']) + " goals and " + str(data['Player Stats (T1)'][1]['home_top_season_assists']) + " assists."),
                Betpicks.generate_response(self, data['Player Stats (T1)'][2]['home_top_season_player_name'] + "season total of " + str(data['Player Stats (T1)'][2]['home_top_season_points']) + " points has come from " + str(data['Player Stats (T1)'][2]['home_top_season_goals']) + " goals and " + str(data['Player Stats (T1)'][2]['home_top_season_assists']) + " assists."),
                Betpicks.generate_response(self, data['Player Stats (T1)'][3]['home_top_season_player_name'] + " has a record of " + str(data['Player Stats (T1)'][3]['home_top_season_points']) + " points. He has blocked " + str(data['Player Stats (T1)'][3]['home_top_season_blocks']) + " goals with a " + str(round(data['Player Stats (T1)'][3]['home_top_season_takeaway_pct'],1)) + "% save percentage."),
                Betpicks.generate_response(self, data["Goal Keeper Stats (T1)"]['Name'] + " has a record of " + data["Goal Keeper Stats (T1)"]['Record'] + ". He has conceded " + str(data["Goal Keeper Stats (T1)"]['Conceded Goals']) + " goals (" + str(data["Goal Keeper Stats (T1)"]['Avg Goals']) + " goals against average) and racked up " + str(data["Goal Keeper Stats (T1)"]['Saved Goals']) + " saves with a " + str(data["Goal Keeper Stats (T1)"]['Save Pct']) + " save percentage (xx-best in the league).")
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team1_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Season Stats</h2>"
            article_team1_stats = [
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + "’s " + str(data["Total Goals (T1)"]) + " goals this season make them the one of the best scoring team in the league."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + " are ranked xx in NHL action for the fewest goals against this season, having conceded " + str(data["Opp. Total Goals (T1)"]) + " total goals (" + str(data["Avg goals against (T1)"]) + " per game)."),
                Betpicks.generate_response(self, "With a " + str(data["Goals Diff (T1)"]) + " goal differential, they’re ranked one of the best in the NHL."),
                Betpicks.generate_response(self, "The " + str(data["Powerplay Goals (T1)"]) + " power-play goals" + data['Team 1 (T1)'].split()[-1] + " have put up this season (on " + str(data["Powerplay Shots (T1)"]) + " power-play chances) lead the league."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + "’s " + str(data["Powerplay Conversation (T1)"]) + "% power-play conversion rate ranks amoung the best in the NHL this season."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + "’s offense has scored " + str(data["Shorthanded Goals (T1)"]) + " shorthanded goals this season."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + " have the league’s xxth-ranked penalty-kill percentage at " + str(round(data["Penalty Goals Pct (T1)"],1)) + "%."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + " win " + str(round(data["Faceoffs Pct (T1)"],1)) + "% of their faceoffs (xxth in the league)."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + " have a " + str(round(data["Evenstrength Pct (T1)"],1)) + "% shooting percentage as a squad, ranking xx in the NHL."),
                Betpicks.generate_response(self, data['Team 1 (T1)'].split()[-1] + "’s players are looking for their shutout win this season. As a team, they are averaging " + str(data["Average Hit (T1)"]) + " hits and " + str(data["Average Blocked (T1)"]) + " blocked shots per game.")
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team1_stats)}</li>\n</ul>'
            # html += "\n<h2>" + data['Team 2 (T2)'].split()[-1] + " vs " + data['Team 1 (T1)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends_1 = [
            #     Betpicks.generate_response(self, "The " + data["underdog_team"] + " have claimed an upset victory in xx, or xx%, of the xx games they have played as an underdog this season."), 
            #     Betpicks.generate_response(self, data["favorite_team"] + " has played with moneyline odds of " + data["spread"] + " or longer once this season and lost that game."), 
            #     Betpicks.generate_response(self, "The " + data["underdog_team"] + " have a " + str(round(data["win_pct_total_ud"],1)) + "% chance to win this game (implied from the moneyline).")
            # ]
            # list3_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list3_rn.join(article_betting_trends_1)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Leaders</h2>"
            article_team2_leader = [
                Betpicks.generate_response(self, data['Player Stats (T2)'][0]['away_top_season_player_name'] + " has been a major player for "+ data['Team 2 (T2)'].split()[-1] + " this season, with " + str(data['Player Stats (T2)'][0]['away_top_season_points']) + " points in " + str(data['Player Stats (T2)'][0]['away_top_season_games_played']) + " games."),
                Betpicks.generate_response(self, "Through " + str(data['Player Stats (T2)'][1]['away_top_season_games_played']) + " games, " + data['Player Stats (T2)'][1]['away_top_season_player_name'] + " has " + str(data['Player Stats (T2)'][1]['away_top_season_goals']) + " goals and " + str(data['Player Stats (T2)'][1]['away_top_season_assists']) + " assists."),
                Betpicks.generate_response(self, data['Player Stats (T2)'][2]['away_top_season_player_name'] + "season total of " + str(data['Player Stats (T2)'][2]['away_top_season_points']) + " points has come from " + str(data['Player Stats (T2)'][2]['away_top_season_goals']) + " goals and " + str(data['Player Stats (T2)'][2]['away_top_season_assists']) + " assists."),
                Betpicks.generate_response(self, data['Player Stats (T2)'][3]['away_top_season_player_name'] + " has a record of " + str(data['Player Stats (T2)'][3]['away_top_season_points']) + " points. He has blocked " + str(data['Player Stats (T2)'][3]['away_top_season_blocks']) + " goals with a " + str(round(data['Player Stats (T2)'][3]['away_top_season_takeaway_pct'],1)) + "% save percentage."),
                Betpicks.generate_response(self, data["Goal Keeper Stats (T2)"]['Name'] + " has a record of " + data["Goal Keeper Stats (T2)"]['Record'] + ". He has conceded " + str(data["Goal Keeper Stats (T2)"]['Conceded Goals']) + " goals (" + str(data["Goal Keeper Stats (T2)"]['Avg Goals']) + " goals against average) and racked up " + str(data["Goal Keeper Stats (T2)"]['Saved Goals']) + " saves with a " + str(data["Goal Keeper Stats (T2)"]['Save Pct']) + " save percentage (xx-best in the league).")
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team2_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Season Stats</h2>"
            article_team2_stats = [
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + "’s " + str(data["Total Goals (T2)"]) + " goals this season make them the one of the best scoring team in the league."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + "are ranked xx in NHL action for the fewest goals against this season, having conceded " + str(data["Opp. Total Goals (T2)"]) + " total goals (" + str(data["Avg goals against (T2)"]) + " per game)."),
                Betpicks.generate_response(self, "With a " + str(data["Goals Diff (T2)"]) + " goal differential, they’re ranked one of the best in the NHL."),
                Betpicks.generate_response(self, "The " + str(data["Powerplay Goals (T2)"]) + " power-play goals" + data['Team 2 (T2)'].split()[-1] + " have put up this season (on " + str(data["Powerplay Shots (T2)"]) + " power-play chances) lead the league."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + "’s " + str(data["Powerplay Conversation (T2)"]) + "% power-play conversion rate ranks amoung the best in the NHL this season."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + "’s offense has scored " + str(data["Shorthanded Goals (T2)"]) + " shorthanded goals this season."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + " have the league’s xxth-ranked penalty-kill percentage at " + str(round(data["Penalty Goals Pct (T2)"],1)) + "%."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + " win " + str(data["Faceoffs Pct (T2)"]) + "% of their faceoffs (xxth in the league)."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + " have a " + str(round(data["Evenstrength Pct (T2)"],1)) + "% shooting percentage as a squad, ranking xx in the NHL."),
                Betpicks.generate_response(self, data['Team 2 (T2)'].split()[-1] + "’s players are looking for their shutout win this season. As a team, they are averaging " + str(data["Average Hit (T2)"]) + " hits and " + str(data["Average Blocked (T2)"]) + " blocked shots per game.")
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team2_stats)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Injury Report</h2>"
            article_team1_injury = ""
            for injury in data['Injuries (T1)']:
                article_team1_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 1 (T1)'].split()[-1] + ": </strong>" + article_team1_injury
            article_team2_injury = ""
            for injury in data['Injuries (T2)']:
                article_team2_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 2 (T2)'].split()[-1] + ": </strong>" + article_team2_injury
            html += "\n<h2>Betting Tips for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += Betpicks.generate_response(self, "\nWe have the " + data['favorite_team'] + " (" + str(data['spread']) + ") predicted as our best bet in this game. Our computer model has the scoring going over the total of xx points, with the teams finishing with a final score of " + data['Team 1 (T1)'].split()[-1] + " xx, " + data['Team 2 (T2)'].split()[-1] + " xx when it’s sorted out on the court.")

            match_teams = data['Match']
            match_teams = match_teams.replace(" ","_")
            filename = match_teams + '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
            filepath_name = os.path.join(SAVEDIRPATH + "/NHL/", filename+".html")
            try:
                text_file = open(filepath_name , "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/NHL_Images"
            thumbnail = Betpicks.get_article_thumbnail(self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/NHL/"
            try:
                shutil.copy(thumbnail[1], current_path)
                os.chdir(SAVEDIRPATH + "/NHL")
                os.rename(thumbnail[0], filename+'.jpg')
            except Exception:
                pass
            print("Article Saved!")
            

    def offline_html(self, games_data_article):
        for data in games_data_article:
            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            if data["Game Number"] == 1: 
                html += "The " + data["Team 1 (T1)"] + " are set for Game 1 on " + str(data["Game Day"]) + " against the " + data["Team 2 (T2)"] + ", beginning at " + str(data["Game Time"]) + " ET. The oddsmakers have made the " + data["favorite_team"] + " solid favorites at " + data["favorite_moneyline"] + " on the moneyline, and the " + data["underdog_team"] + " are at " + data["underdog_moneyline"] + ". Find more below on the " + data["Team 1 (T1)"].split()[-1] + " vs. " + data["Team 2 (T2)"].split()[-1] + " betting line, injury report, head-to-head stats, best bets and more."
            else:
                if data["Advantage Team"] is None:
                    html += "On " + str(data["Game Day"]) + " the " + data["Team 1 (T1)"] + " and the " + data["Team 2 (T2)"] + " will face off in Game " + str(data["Game Number"]) + ", beginning at " + str(data["Game Time"]) + " ET. The series is currently tied " + str(data["Home Points"]) + "-" + str(data["Away Points"]) + ". The sportsbooks have made the " + data["Team 1 (T1)"].split()[-1] + " slight favorites at xx on the moneyline, and the " + data["Team 2 (T2)"].split()[-1] + " are at xx. Find more below on the " + data["Match"] + " betting line, injury report, head-to-head stats, best bets and more."
                elif data["Advantage Team"] == data["Team 1 (T1)"]:
                    html += "On " + str(data["Game Day"]) + " the " + data["Team 1 (T1)"] + " and the " + data["Team 2 (T2)"] + " will face off in Game " + str(data["Game Number"]) + ", beginning at " + str(data["Game Time"]) + " ET. The " + data["Team 1 (T1)"].split()[-1] + " have a " + str(data["Home Points"]) + "-" + str(data["Away Points"]) + " edge in the series. The sportsbooks have made the " + data["Team 1 (T1)"].split()[-1] + " slight favorites at xx on the moneyline, and the " + data["Team 2 (T2)"].split()[-1] + " are at xx. Find more below on the " + data["Match"] + " betting line, injury report, head-to-head stats, best bets and more."
                else:
                    html += "On " + str(data["Game Day"]) + " the " + data["Team 1 (T1)"] + " and the " + data["Team 2 (T2)"] + " will face off in Game " + str(data["Game Number"]) + ", beginning at " + str(data["Game Time"]) + " ET. The " + data["Team 2 (T2)"].split()[-1] + " have a " + str(data["Home Points"]) + "-" + str(data["Away Points"]) + " edge in the series. The sportsbooks have made the " + data["Team 2 (T2)"].split()[-1] + " slight favorites at xx on the moneyline, and the " + data["Team 1 (T1)"].split()[-1] + " are at xx. Find more below on the " + data["Match"] + " betting line, injury report, head-to-head stats, best bets and more."
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Spread and Betting Line</h2>"
            html += '\n<table class="table"><caption>' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + ' Betting Information</caption>'
            table1_col = ["Favorite", "Moneyline", "Underdog", "Moneyline"]
            table1_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table1_cn.join(table1_col)}</th>\n</tr>\n</thead>'
            table1_row = [data["favorite_team"],data["favorite_moneyline"],data["underdog_team"],data["underdog_moneyline"]]
            table1_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table1_rn.join(table1_row)}</td>\n</tr>\n</tbody>\n</table>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['Game Day']) + "</li>\n<li><strong>Game Time:</strong> " + str(data['Game Time']) + "</li>\n<li><strong>Location:</strong> " + data['Location'] + "</li>\n<li><strong>Arena:</strong> " + data['Arena'] + "</li>\n</ul>"
            html += "\n<h2>Computer Predictions for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += '\n<table class="table"><caption>Computer Picks for ' + data['Team 1 (T1)'].split()[-1] + ' vs ' + data['Team 2 (T2)'].split()[-1] + '</caption>'
            table2_col = ["ATS", "Over/Under", "AI Prediction"]
            table2_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table2_cn.join(table2_col)}</th>\n</tr>\n</thead>'
            # table2_row = ["+"+data['spread']+" ("+data["underdog_spread_odds"]+")","+/-"+data["total_over_under"],data["favorite_team"]+" "+data['spread']+" Over "+data["favorite_moneyline"]]
            table2_row = [data['total_over_under'],data["favorite_moneyline"],data["favorite_team"]+" "+data['spread']+" Over "+data["favorite_moneyline"]]
            table2_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table2_rn.join(table2_row)}</td>\n</tr>\n</tbody>\n</table>'
            # html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends = [
            #     "Through xx games as the moneyline favorite this season, " + data["favorite_team"] + " has won xx times.", 
            #     "The " + data["favorite_team"] + " have won xx of the xx games they have played with moneyline odds shorter than xx.", 
            #     "There is a " + str(data["win_pct_ml_f"]) + "% chance that " + data["favorite_team"] + " wins this contest, per the moneyline."
            # ]
            list2_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list2_rn.join(article_betting_trends)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
            article_team1_leader = [
                data['Player Stats (T1)'][0]['home_top_season_player_name'] + " has been a major player for "+ data['Team 1 (T1)'].split()[-1] + " this season, with " + str(data['Player Stats (T1)'][0]['home_top_season_points']) + " points in " + str(data['Player Stats (T1)'][0]['home_top_season_games_played']) + " games.",
                "Through " + str(data['Player Stats (T1)'][1]['home_top_season_games_played']) + " games, " + data['Player Stats (T1)'][1]['home_top_season_player_name'] + " has " + str(data['Player Stats (T1)'][1]['home_top_season_goals']) + " goals and " + str(data['Player Stats (T1)'][1]['home_top_season_assists']) + " assists.",
                data['Player Stats (T1)'][2]['home_top_season_player_name'] + "season total of " + str(data['Player Stats (T1)'][2]['home_top_season_points']) + " points has come from " + str(data['Player Stats (T1)'][2]['home_top_season_goals']) + " goals and " + str(data['Player Stats (T1)'][2]['home_top_season_assists']) + " assists.",
                data['Player Stats (T1)'][3]['home_top_season_player_name'] + " has a record of " + str(data['Player Stats (T1)'][3]['home_top_season_points']) + " points. He has blocked " + str(data['Player Stats (T1)'][3]['home_top_season_blocks']) + " goals with a " + str(round(data['Player Stats (T1)'][3]['home_top_season_takeaway_pct'],1)) + "% save percentage.",
                data["Goal Keeper Stats (T1)"]['Name'] + " has a record of " + data["Goal Keeper Stats (T1)"]['Record'] + ". He has conceded " + str(data["Goal Keeper Stats (T1)"]['Conceded Goals']) + " goals (" + str(data["Goal Keeper Stats (T1)"]['Avg Goals']) + " goals against average) and racked up " + str(data["Goal Keeper Stats (T1)"]['Saved Goals']) + " saves with a " + str(data["Goal Keeper Stats (T1)"]['Save Pct']) + " save percentage (xx-best in the league)."
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team1_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'] + " Season Stats</h2>"
            article_team1_stats = [
                data['Team 1 (T1)'].split()[-1] + "’s " + str(data["Total Goals (T1)"]) + " goals this season make them the one of the best scoring team in the league.",
                data['Team 1 (T1)'].split()[-1] + " are ranked xx in NHL action for the fewest goals against this season, having conceded " + str(data["Opp. Total Goals (T1)"]) + " total goals (" + str(data["Avg goals against (T1)"]) + " per game).",
                "With a " + str(data["Goals Diff (T1)"]) + " goal differential, they’re ranked one of the best in the NHL.",
                "The " + str(data["Powerplay Goals (T1)"]) + " power-play goals" + data['Team 1 (T1)'].split()[-1] + " have put up this season (on " + str(data["Powerplay Shots (T1)"]) + " power-play chances) lead the league.",
                data['Team 1 (T1)'].split()[-1] + "’s " + str(data["Powerplay Conversation (T1)"]) + "% power-play conversion rate ranks amoung the best in the NHL this season.",
                data['Team 1 (T1)'].split()[-1] + "’s offense has scored " + str(data["Shorthanded Goals (T1)"]) + " shorthanded goals this season.",
                data['Team 1 (T1)'].split()[-1] + " have the league’s xxth-ranked penalty-kill percentage at " + str(round(data["Penalty Goals Pct (T1)"],1)) + "%.",
                data['Team 1 (T1)'].split()[-1] + " win " + str(round(data["Faceoffs Pct (T1)"],1)) + "% of their faceoffs (xxth in the league).",
                data['Team 1 (T1)'].split()[-1] + " have a " + str(round(data["Evenstrength Pct (T1)"],1)) + "% shooting percentage as a squad, ranking xx in the NHL.",
                data['Team 1 (T1)'].split()[-1] + "’s players are looking for their shutout win this season. As a team, they are averaging " + str(data["Average Hit (T1)"]) + " hits and " + str(data["Average Blocked (T1)"]) + " blocked shots per game."
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team1_stats)}</li>\n</ul>'
            # html += "\n<h2>" + data['Team 2 (T2)'].split()[-1] + " vs " + data['Team 1 (T1)'].split()[-1] + " Betting Trends</h2>"
            # article_betting_trends_1 = [
            #     "The " + data["favorite_team"] + " have claimed an upset victory in xx, or " + str(data["win_pct_total_f"]) + "%, of the xx games they have played as an underdog this season.", 
            #     data["underdog_team"] + " has played with moneyline odds of " + str(data["underdog_spread_odds"]) + " or longer once this season and lost that game.", 
            #     "The " + data["favorite_team"] + " have a " + str(data["win_pct_ml_f"]) + "% chance to win this game (implied from the moneyline)."
            # ]
            # list3_rn = '</li>\n<li>'
            # html += f'\n<ul>\n<li>{list3_rn.join(article_betting_trends_1)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Leaders</h2>"
            article_team2_leader = [
                data['Player Stats (T2)'][0]['away_top_season_player_name'] + " has been a major player for "+ data['Team 2 (T2)'].split()[-1] + " this season, with " + str(data['Player Stats (T2)'][0]['away_top_season_points']) + " points in " + str(data['Player Stats (T2)'][0]['away_top_season_games_played']) + " games.",
                "Through " + str(data['Player Stats (T2)'][1]['away_top_season_games_played']) + " games, " + data['Player Stats (T2)'][1]['away_top_season_player_name'] + " has " + str(data['Player Stats (T2)'][1]['away_top_season_goals']) + " goals and " + str(data['Player Stats (T2)'][1]['away_top_season_assists']) + " assists.",
                data['Player Stats (T2)'][2]['away_top_season_player_name'] + "season total of " + str(data['Player Stats (T2)'][2]['away_top_season_points']) + " points has come from " + str(data['Player Stats (T2)'][2]['away_top_season_goals']) + " goals and " + str(data['Player Stats (T2)'][2]['away_top_season_assists']) + " assists.",
                data['Player Stats (T2)'][3]['away_top_season_player_name'] + " has a record of " + str(data['Player Stats (T2)'][3]['away_top_season_points']) + " points. He has blocked " + str(data['Player Stats (T2)'][3]['away_top_season_blocks']) + " goals with a " + str(round(data['Player Stats (T2)'][3]['away_top_season_takeaway_pct'],1)) + "% save percentage.",
                data["Goal Keeper Stats (T2)"]['Name'] + " has a record of " + data["Goal Keeper Stats (T2)"]['Record'] + ". He has conceded " + str(data["Goal Keeper Stats (T2)"]['Conceded Goals']) + " goals (" + str(data["Goal Keeper Stats (T2)"]['Avg Goals']) + " goals against average) and racked up " + str(data["Goal Keeper Stats (T2)"]['Saved Goals']) + " saves with a " + str(data["Goal Keeper Stats (T2)"]['Save Pct']) + " save percentage (xx-best in the league)."
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team2_leader)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 2 (T2)'] + " Season Stats</h2>"
            article_team2_stats = [
                data['Team 2 (T2)'].split()[-1] + "’s " + str(data["Total Goals (T2)"]) + " goals this season make them the one of the best scoring team in the league.",
                data['Team 2 (T2)'].split()[-1] + "are ranked xx in NHL action for the fewest goals against this season, having conceded " + str(data["Opp. Total Goals (T2)"]) + " total goals (" + str(data["Avg goals against (T2)"]) + " per game).",
                "With a " + str(data["Goals Diff (T2)"]) + " goal differential, they’re ranked one of the best in the NHL.",
                "The " + str(data["Powerplay Goals (T2)"]) + " power-play goals" + data['Team 2 (T2)'].split()[-1] + " have put up this season (on " + str(data["Powerplay Shots (T2)"]) + " power-play chances) lead the league.",
                data['Team 2 (T2)'].split()[-1] + "’s " + str(data["Powerplay Conversation (T2)"]) + "% power-play conversion rate ranks amoung the best in the NHL this season.",
                data['Team 2 (T2)'].split()[-1] + "’s offense has scored " + str(data["Shorthanded Goals (T2)"]) + " shorthanded goals this season.",
                data['Team 2 (T2)'].split()[-1] + " have the league’s xxth-ranked penalty-kill percentage at " + str(round(data["Penalty Goals Pct (T2)"],1)) + "%.",
                data['Team 2 (T2)'].split()[-1] + " win " + str(round(data["Faceoffs Pct (T2)"],1)) + "% of their faceoffs (xxth in the league).",
                data['Team 2 (T2)'].split()[-1] + " have a " + str(round(data["Evenstrength Pct (T2)"],1)) + "% shooting percentage as a squad, ranking xx in the NHL.",
                data['Team 2 (T2)'].split()[-1] + "’s players are looking for their shutout win this season. As a team, they are averaging " + str(data["Average Hit (T2)"]) + " hits and " + str(data["Average Blocked (T2)"]) + " blocked shots per game."
            ]
            html += f'\n<ul>\n<li>{list2_rn.join(article_team2_stats)}</li>\n</ul>'
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + " Injury Report</h2>"
            article_team1_injury = ""
            for injury in data['Injuries (T1)']:
                article_team1_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 1 (T1)'].split()[-1] + ": </strong>" + article_team1_injury
            article_team2_injury = ""
            for injury in data['Injuries (T2)']:
                article_team2_injury += "\n" + injury['name'] + ": " + injury['status'] + " (" + injury['desc'] + ")<br>"
            html += "\n<strong>" + data['Team 2 (T2)'].split()[-1] + ": </strong>" + article_team2_injury
            html += "\n<h2>Betting Tips for " + data['Team 1 (T1)'].split()[-1] + " vs " + data['Team 2 (T2)'].split()[-1] + "</h2>"
            html += "\nWe have the " + data['favorite_team'] + " (" + str(data['spread']) + ") predicted as our best bet in this game. Our computer model has the scoring going over the total of xx points, with the teams finishing with a final score of " + data['Team 1 (T1)'].split()[-1] + " xx, " + data['Team 2 (T2)'].split()[-1] + " xx when it’s sorted out on the court."

            match_teams = data['Match']
            match_teams = match_teams.replace(" ","_")
            filename = match_teams + '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
            filepath_name = os.path.join(SAVEDIRPATH + "/NHL/", filename+".html")
            try:
                text_file = open(filepath_name , "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/NHL_Images"
            thumbnail = Betpicks.get_article_thumbnail(self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/NHL/"
            try:
                shutil.copy(thumbnail[1], current_path)
                os.chdir(SAVEDIRPATH + "/NHL")
                os.rename(thumbnail[0], filename+'.jpg')
            except Exception:
                pass
            print("Article Saved!")


    def nhl_main(self):
        if os.path.exists('/home/ubuntu/article-automation/NHL'):
            command.run(['sudo', 'chmod', '-R', '777', '/home/ubuntu/article-automation/NHL']) 
            shutil.rmtree(SAVEDIRPATH+"/NHL", ignore_errors=False, onerror=None)
        if os.path.exists(SAVEDIRPATH+"/NHL.zip"):
            os.remove(SAVEDIRPATH+"/NHL.zip")
        print("NHL Folder Removed!")
        # api-endpoint
        URL = "http://api.sportradar.us/nhl/trial/v7/en/games/" + self.YEAR + "/" + self.MONTH + "/" + self.DAY + "/schedule.json?api_key=" + self.API_KEY
        # URL = "http://api.sportradar.us/nhl/trial/v7/en/games/2023/06/10/schedule.json?api_key=" + self.API_KEY
        # Game Info
        data = Betpicks.get_games_info(self, URL)
        if data.__contains__('games'):
            games = data['games']
            games_data_article = []
            for game in games:
                if game['status'] == 'unnecessary':
                    smtp_server = 'YOUR_SMTP_SERVER'
                    smtp_port = 0
                    smtp_username = 'YOUR_EMAIL'
                    smtp_password = 'YOUR_PASSWORD'
                    context = ssl.create_default_context()

                    msg = MIMEText('Dear ,\
                    \n\nI hope this email finds you well. I am writing to inform you that unfortunately, we were unable to generate the NHL article you requested for the match between ' + game['home']['name'] + ' and ' + game['away']['name'] + '. This is due to the fact that the game had an unnecessary status, which means that it did not have a match sr_id associated with it. Without a match sr_id, our automated system is unable to fetch the necessary data from the sportsradar API to generate the article.\
                    \n\nWe understand that you were expecting a detailed article for this match, and we apologize that we could not deliver on this occasion. We apologize once again for any inconvenience caused, and we thank you for your understanding. If you have any questions or concerns, please do not hesitate to reach out to us.\
                    \n\nBest regards,\
                    \n\nAutomated Articles Bot\
                    \nBetpicks')
                    msg['Subject'] = 'Match Article Not Generated Due to Unnecessary Status'
                    msg['From'] = 'contact@sportsinformationtraders.com'
                    msg['To'] = 'sportsinformationtraders@gmail.com'
                    sender_email = 'contact@sportsinformationtraders.com'
                    receiver_email = 'sportsinformationtraders@gmail.com'
                    try:
                        server = smtplib.SMTP_SSL(smtp_server,smtp_port,context=context)
                        server.ehlo()
                        server.login(smtp_username, smtp_password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                    except Exception as e:
                        print(e)
                    finally:
                        server.quit() 

                    continue
                game_id = game['id']
                game_sr_id = game['sr_id']
                game_scheduled = game['scheduled']
                game_date = datetime.strptime(game_scheduled, '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.timezone('US/Eastern')).date()
                game_time = datetime.strptime(game_scheduled, '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.timezone('US/Eastern')).time()
                game_time = game_time.strftime("%I:%M %p")
                game_date = game_date.strftime("%m-%d-%Y")
                # game_time = game_time.strftime("%H:%M")
                game_location = game['venue']['city'] + ', ' + game['venue']['state']
                game_arena = game['venue']['name']
                team_home = game['home']['name']
                team_home_id = game['home']['id']
                team_away = game['away']['name']
                team_away_id = game['away']['id']
                if data.__contains__('home_points') and data.__contains__('away_points'):
                    home_game_points = game['home_points']
                    away_game_points = game['away_points']
                    game_number = home_game_points + away_game_points + 1
                    game_advantage = max(home_game_points, away_game_points)
                    if game_advantage > away_game_points:
                        game_advantage_team = team_home
                    elif game_advantage > home_game_points:
                        game_advantage_team = team_away
                    else:
                        game_advantage_team = None
                else:
                    home_game_points = 0
                    away_game_points = 0
                    game_number = 1
                    game_advantage_team = None
                
                """Home Team Profile"""
                URL = "http://api.sportradar.us/nhl/trial/v7/en/teams/" + team_home_id + "/profile.json?api_key=" + self.API_KEY
                home_team_profile = Betpicks.get_data_request(self, URL)
                home_players = home_team_profile['players']
                home_players_names = []
                for players in home_players:
                    home_players_names.append(players['full_name'])
                
                """Season Stats Home"""
                SEASON_TYPE = "REG"
                YEAR = "2022"
                URL = "http://api.sportradar.us/nhl/trial/v7/en/seasons/" + YEAR + "/" + SEASON_TYPE + "/teams/" + team_home_id + "/statistics.json?api_key=" + self.API_KEY
                home_season_stats = Betpicks.get_data_request(self, URL)
                home_total_goals = home_season_stats['own_record']['statistics']['total']['goals']
                home_avg_goals = home_season_stats['own_record']['statistics']['average']['goals']
                home_opp_total_goals = home_season_stats['opponents']['statistics']['total']['goals']
                home_goals_diff = home_total_goals - home_opp_total_goals
                home_pp_goals = home_season_stats['own_record']['statistics']['powerplay']['goals'] 
                home_pp_shots = home_season_stats['own_record']['statistics']['powerplay']['shots'] 
                home_pp_conv_rate = home_season_stats['own_record']['statistics']['powerplay']['percentage'] 
                home_sh_goals = home_season_stats['own_record']['statistics']['shorthanded']['goals'] 
                home_penalty_goals = home_season_stats['own_record']['statistics']['penalty']['goals'] 
                home_penalty_shots = home_season_stats['own_record']['statistics']['penalty']['shots'] 
                if home_penalty_shots > 0:
                    home_penalty_win_percentage = (home_penalty_goals/home_penalty_shots)*100
                else:
                    home_penalty_win_percentage = 0
                home_faceoff_win_percentage = home_season_stats['own_record']['statistics']['evenstrength']['faceoff_win_pct']
                home_es_shots = home_season_stats['own_record']['statistics']['evenstrength']['shots']
                home_es_goals = home_season_stats['own_record']['statistics']['evenstrength']['goals']
                if home_es_shots > 0:
                    home_es_connect_pct = (home_es_goals/home_es_shots)*100
                else:
                    home_es_shots = 0
                home_avg_blocked = home_season_stats['own_record']['statistics']['average']['blocked_shots']
                home_avg_hit = home_season_stats['own_record']['statistics']['average']['hits']
                home_avg_goals_against = home_season_stats['own_record']['goaltending']['average']['goals_against']
                home_player_season_stats = home_season_stats['players']
                
                home_player_season_stats_gk = []
                for goalkeeper in home_player_season_stats:
                    if goalkeeper.__contains__('goaltending'):
                        home_player_season_stats_gk.append(goalkeeper)
                
                home_player_season_stats.sort(key=self.get_season_goals)
                home_player_season_stats.reverse()
                home_player_season_stats = home_player_season_stats[:5]
                
                home_player_season_stats_gk.sort(key=self.get_season_saves)
                home_player_season_stats_gk = home_player_season_stats_gk[-1]
                home_gk_season_stats = {
                    'Record': str(home_player_season_stats_gk['goaltending']['total']['wins']) + "-" + str(home_player_season_stats_gk['goaltending']['total']['losses']) + "-" + str(home_player_season_stats_gk['goaltending']['total']['overtime_losses']),
                    'Name': home_player_season_stats_gk['full_name'],
                    'Save Pct': home_player_season_stats_gk['goaltending']['total']['saves_pct'],
                    'Conceded Goals': home_player_season_stats_gk['goaltending']['total']['goals_against'],
                    'Saved Goals': home_player_season_stats_gk['goaltending']['total']['saves'],
                    'Avg Goals': home_player_season_stats_gk['goaltending']['total']['avg_goals_against']
                }
                
                """Top Player Stats Home"""
                top_player_stats_home = []
                for players_stats in home_player_season_stats:
                    home_top = {
                        'home_top_season_player_name': players_stats['full_name'],
                        'home_top_season_games_played': players_stats['statistics']['total']['games_played'],
                        'home_top_season_goals': players_stats['statistics']['total']['goals'],
                        'home_top_season_points': players_stats['statistics']['total']['points'],
                        'home_top_season_assists': players_stats['statistics']['total']['assists'],
                        'home_top_season_blocks': players_stats['statistics']['total']['blocked_shots'],
                        'home_top_season_takeaway_pct': players_stats['statistics']['average']['takeaways']*100,
                        'home_top_season_giveaway_pct': players_stats['statistics']['average']['giveaways']*100,
                        'home_top_season_giveaway_pct': players_stats['statistics']['average']['goals']
                    }
                    top_player_stats_home.append(home_top)
                
                """Away Team Profile"""
                URL = "http://api.sportradar.us/nhl/trial/v7/en/teams/" + team_away_id + "/profile.json?api_key=" + self.API_KEY
                away_team_profile = Betpicks.get_data_request(self, URL)
                away_players = away_team_profile['players']
                away_players_names = []
                for players in home_players:
                    away_players_names.append(players['full_name'])
                
                """Season Stats Away"""
                SEASON_TYPE = "REG"
                YEAR = "2022"
                URL = "http://api.sportradar.us/nhl/trial/v7/en/seasons/" + YEAR + "/" + SEASON_TYPE + "/teams/" + team_away_id + "/statistics.json?api_key=" + self.API_KEY
                away_season_stats = Betpicks.get_data_request(self, URL)
                away_total_goals = away_season_stats['own_record']['statistics']['total']['goals']
                away_avg_goals = away_season_stats['own_record']['statistics']['average']['goals']
                away_opp_total_goals = away_season_stats['opponents']['statistics']['total']['goals']
                away_goals_diff = away_total_goals - away_opp_total_goals
                away_pp_goals = away_season_stats['own_record']['statistics']['powerplay']['goals'] 
                away_pp_shots = away_season_stats['own_record']['statistics']['powerplay']['shots'] 
                away_pp_conv_rate = away_season_stats['own_record']['statistics']['powerplay']['percentage'] 
                away_sh_goals = away_season_stats['own_record']['statistics']['shorthanded']['goals'] 
                away_penalty_goals = away_season_stats['own_record']['statistics']['penalty']['goals'] 
                away_penalty_shots = away_season_stats['own_record']['statistics']['penalty']['shots'] 
                if away_penalty_shots > 0:
                    away_penalty_win_percentage = (away_penalty_goals/away_penalty_shots)*100
                else:
                    away_penalty_win_percentage = 0
                away_faceoff_win_percentage = away_season_stats['own_record']['statistics']['evenstrength']['faceoff_win_pct']
                away_es_shots = away_season_stats['own_record']['statistics']['evenstrength']['shots']
                away_es_goals = away_season_stats['own_record']['statistics']['evenstrength']['goals']
                if away_es_shots > 0:
                    away_es_connect_pct = (away_es_goals/away_es_shots)*100
                else:
                    away_es_shots = 0
                away_avg_blocked = away_season_stats['own_record']['statistics']['average']['blocked_shots']
                away_avg_hit = away_season_stats['own_record']['statistics']['average']['hits']
                away_avg_goals_against = away_season_stats['own_record']['goaltending']['average']['goals_against']
                away_player_season_stats = away_season_stats['players']
                
                away_player_season_stats_gk = []
                for goalkeeper in away_player_season_stats:
                    if goalkeeper.__contains__('goaltending'):
                        away_player_season_stats_gk.append(goalkeeper)
                
                away_player_season_stats.sort(key=self.get_season_goals)
                away_player_season_stats.reverse()
                away_player_season_stats = away_player_season_stats[:5]
                
                away_player_season_stats_gk.sort(key=self.get_season_saves)
                away_player_season_stats_gk = away_player_season_stats_gk[-1]
                away_gk_season_stats = {
                    'Record': str(away_player_season_stats_gk['goaltending']['total']['wins']) + "-" + str(away_player_season_stats_gk['goaltending']['total']['losses']) + "-" + str(away_player_season_stats_gk['goaltending']['total']['overtime_losses']),
                    'Name': away_player_season_stats_gk['full_name'],
                    'Save Pct': away_player_season_stats_gk['goaltending']['total']['saves_pct'],
                    'Conceded Goals': away_player_season_stats_gk['goaltending']['total']['goals_against'],
                    'Saved Goals': away_player_season_stats_gk['goaltending']['total']['saves'],
                    'Avg Goals': away_player_season_stats_gk['goaltending']['total']['avg_goals_against']
                }
                
                """Top Player Stats away"""
                top_player_stats_away = []
                for players_stats in away_player_season_stats:
                    away_top = {
                        'away_top_season_player_name': players_stats['full_name'],
                        'away_top_season_games_played': players_stats['statistics']['total']['games_played'],
                        'away_top_season_goals': players_stats['statistics']['total']['goals'],
                        'away_top_season_points': players_stats['statistics']['total']['points'],
                        'away_top_season_assists': players_stats['statistics']['total']['assists'],
                        'away_top_season_blocks': players_stats['statistics']['total']['blocked_shots'],
                        'away_top_season_takeaway_pct': players_stats['statistics']['average']['takeaways']*100,
                        'away_top_season_giveaway_pct': players_stats['statistics']['average']['giveaways']*100,
                        'away_top_season_giveaway_pct': players_stats['statistics']['average']['goals']
                    }
                    top_player_stats_away.append(away_top)
                
                """Injurys"""
                home_injuries = []
                away_injuries = []
                URL = "http://api.sportradar.us/nhl/trial/v7/en/league/injuries.json?api_key=" + self.API_KEY
                season_injury_data = Betpicks.get_data_request(self, URL)
                season_injury_data = season_injury_data['teams']
                for player_injury in season_injury_data:
                    if player_injury['id'] == team_home_id:
                        home_player_injury = player_injury['players']
                        for injury in home_player_injury:
                            injury_data = {
                                'name': injury['full_name'], 
                                'status': injury['injuries'][0]['status'],
                                'desc': injury['injuries'][0]['desc']
                            }
                            home_injuries.append(injury_data)
                    if player_injury['id'] == team_away_id:
                        away_player_injury = player_injury['players']
                        for injury in away_player_injury:
                            injury_data = {
                                'name': injury['full_name'], 
                                'status': injury['injuries'][0]['status'],
                                'desc': injury['injuries'][0]['desc']
                            }
                            away_injuries.append(injury_data)
                
                """ODDs Data"""
                URL = "https://api.sportradar.us/oddscomparison-ust1/en/eu/sport_events/" + game_sr_id + "/markets.json?api_key=" + self.ODDS_API_KEY
                odds_data = Betpicks.get_data_request(self, URL)
                odds_data = odds_data['sport_event']['consensus']
                pct_data = []
                if odds_data.__contains__('bet_percentage_outcomes'):
                    pct_data = odds_data['bet_percentage_outcomes']
                odds_data = odds_data['lines']

                spread = "-"
                home_odds = "-"
                away_odds = "-"
                underdog_spread_odds = "-"
                favorite_spread_odds = "-"
                underdog_moneyline = "-"
                favorite_moneyline = "-"
                favorite_team = "-"
                underdog_team = "-"
                total_over_under = "-"
                over_total_odds = "-"
                under_total_odds = "-"
                home_moneyline = "-"
                away_moneyline = "-"
                win_pct_ml_home = "-"
                win_pct_total_home = "-"
                win_pct_ml_away = "-"
                win_pct_total_away = "-"
                win_pct_ml_f = "-"
                win_pct_total_f = "-"
                win_pct_ml_ud = "-"
                win_pct_total_ud = "-"

                for line in odds_data:
                    if line['name'] == 'spread_current':
                        spread = line['spread']
                        home_odds = line['outcomes'][0]['odds']
                        away_odds = line['outcomes'][1]['odds']
                        if float(home_odds) > float(away_odds):
                            favorite_team = "0"
                        else:
                            favorite_team = "1"
                    if line['name'] == 'total_current':
                        total_over_under = '-'+line['total']
                        over_total_odds = '-'+str((float(line['outcomes'][0]['odds'])-1)*100)
                        under_total_odds = '-'+str((float(line['outcomes'][1]['odds'])-1)*100)
                    if line['name'] == 'moneyline_current':
                        home_moneyline = str(round((float(line['outcomes'][0]['odds'])-1) * 100,1))
                        away_moneyline = str(round((float(line['outcomes'][1]['odds'])-1) * 100,1))

                if not pct_data:
                    pass 
                else:
                    for pct in pct_data:
                        if pct['name'] == 'moneyline':
                            win_pct_ml_home = pct['outcomes'][0]['percentage']
                            win_pct_ml_home = round(float(win_pct_ml_home),1)
                            win_pct_ml_away = pct['outcomes'][1]['percentage']
                            win_pct_ml_away = round(float(win_pct_ml_away),1)
                        if pct['name'] == 'total':
                            win_pct_total_home = pct['outcomes'][0]['percentage']
                            win_pct_total_away = pct['outcomes'][1]['percentage']

                if away_odds != '-':                    
                    if float(away_odds) >= 2.00:
                        away_odds = -100/(float(away_odds) - 1)
                    else:
                        away_odds = (float(away_odds) - 1)*100
                    
                    if away_odds > 0:
                        away_odds = '+'+str(away_odds)
                
                if home_odds != '-':
                    if float(home_odds) >= 2.00:
                        home_odds = -100/(float(home_odds) - 1)
                    else:
                        home_odds = (float(home_odds) - 1)*100
                
                    if home_odds > 0:
                        home_odds = '+'+str(home_odds)

                if favorite_team == "0":
                    favorite_team = team_home
                    underdog_team = team_away
                    underdog_spread_odds = away_odds
                    favorite_spread_odds = home_odds
                    underdog_moneyline = '+'+away_moneyline
                    favorite_moneyline = '-'+home_moneyline
                    win_pct_ml_ud = str(win_pct_ml_away)
                    win_pct_total_ud = win_pct_total_away
                    win_pct_total_f = win_pct_total_home
                    win_pct_ml_f = str(win_pct_ml_home)
                else:
                    favorite_team = team_away
                    underdog_team = team_home
                    underdog_spread_odds = home_odds
                    favorite_spread_odds = away_odds
                    underdog_moneyline = '+'+home_moneyline
                    favorite_moneyline = '-'+str(away_moneyline)
                    win_pct_ml_ud = win_pct_ml_home
                    win_pct_total_ud = win_pct_total_home
                    win_pct_total_f = win_pct_total_away
                    win_pct_ml_f = str(win_pct_ml_home)

                game_data = {
                    "Match": team_home + ' vs ' + team_away,
                    "Game Day": game_date,
                    "Game Time": game_time,
                    "Location": game_location,
                    "Arena": game_arena,
                    "Home Points": home_game_points,
                    "Away Points": away_game_points,
                    "Game Number": game_number,
                    "Advantage Team": game_advantage_team,
                    "Team 1 (T1)": team_home,
                    "Player Stats (T1)": top_player_stats_home,
                    "Goal Keeper Stats (T1)": home_gk_season_stats,
                    "Total Goals (T1)": home_total_goals,
                    "Average Goal (T1)": home_avg_goals,
                    "Opp. Total Goals (T1)": home_opp_total_goals,
                    "Avg goals against (T1)": home_avg_goals_against,
                    "Goals Diff (T1)": home_goals_diff,
                    "Powerplay Goals (T1)": home_pp_goals,
                    "Powerplay Shots (T1)": home_pp_shots,
                    "Powerplay Conversation (T1)": home_pp_conv_rate,
                    "Shorthanded Goals (T1)": home_sh_goals,
                    "Penalty Goals Pct (T1)": home_penalty_win_percentage,
                    "Faceoffs Pct (T1)": home_faceoff_win_percentage,
                    "Evenstrength Pct (T1)": home_es_connect_pct,
                    "Average Blocked (T1)": home_avg_blocked,
                    "Average Hit (T1)": home_avg_hit,
                    "Injuries (T1)": home_injuries,
                    "Team 2 (T2)": team_away,
                    "Player Stats (T2)": top_player_stats_away,
                    "Goal Keeper Stats (T2)": away_gk_season_stats,
                    "Total Goals (T2)": away_total_goals,
                    "Average Goal (T2)": away_avg_goals,
                    "Opp. Total Goals (T2)": away_opp_total_goals,
                    "Avg goals against (T2)": away_avg_goals_against,
                    "Goals Diff (T2)": away_goals_diff,
                    "Powerplay Goals (T2)": away_pp_goals,
                    "Powerplay Shots (T2)": away_pp_shots,
                    "Powerplay Conversation (T2)": away_pp_conv_rate,
                    "Shorthanded Goals (T2)": away_sh_goals,
                    "Penalty Goals Pct (T2)": away_penalty_win_percentage,
                    "Faceoffs Pct (T2)": away_faceoff_win_percentage,
                    "Evenstrength Pct (T2)": away_es_connect_pct,
                    "Average Blocked (T2)": away_avg_blocked,
                    "Average Hit (T2)": away_avg_hit,
                    "Injuries (T2)": away_injuries,
                    "spread": spread,
                    "underdog_spread_odds": underdog_spread_odds,
                    "favorite_spread_odds": favorite_spread_odds,
                    "favorite_team": favorite_team,
                    "total_over_under": total_over_under,
                    "over_total_odds": over_total_odds,
                    "under_total_odds": under_total_odds,
                    "underdog_moneyline": underdog_moneyline,
                    "favorite_moneyline": favorite_moneyline,
                    "underdog_team": underdog_team,
                    "win_pct_ml_ud": win_pct_ml_ud,
                    "win_pct_ml_f": win_pct_ml_f,
                    "win_pct_total_ud": win_pct_total_ud,
                    "win_pct_total_f": win_pct_total_ud
                }
                games_data_article.append(game_data)
                print("Article Written")
            
            os.mkdir(SAVEDIRPATH+"/NHL")
            print("NHL Folder Created!")
            try:
                self.generate_html(games_data_article)
                shutil.make_archive(SAVEDIRPATH + "/NHL", 'zip', SAVEDIRPATH+"/NHL")
                print("Success Online!")
            except:
                self.offline_html(games_data_article)            
                shutil.make_archive(SAVEDIRPATH+"/NHL", 'zip', SAVEDIRPATH+"/NHL")
                print("Success Offline!")
        else:
            print("Data not Found")



class NFL_Article(Betpicks):

    def __init__(self):
        print("contructor function")
        article_date = date.today()
        self.DAY = str(article_date.day)
        self.MONTH = str(article_date.month)
        self.YEAR = str(article_date.year)
        self.WEEK_DAY = str(article_date.isocalendar()[1])
        self.ODDS_METABET_API_KEY = "YOUR_API_KEY"

    def decode_time(self, timestamp):
        utc_datetime = datetime.utcfromtimestamp(timestamp/1000)

        # Set the UTC timezone for the datetime object
        utc_timezone = timezone('UTC')
        utc_datetime = utc_timezone.localize(utc_datetime)

        # Convert to Eastern Time (ET)
        eastern_timezone = timezone('US/Eastern')
        eastern_datetime = utc_datetime.astimezone(eastern_timezone)

        game_time = eastern_datetime.strftime("%I:%M %p")
        return eastern_datetime, game_time

    def find_player_with_max_passing_yards(self, player_list):
        if not player_list:
            return None  # Return None if the list is empty

        max_passing_yards_player = max(
            player_list, key=lambda x: x.get('FOOTBALL_PASSING_YARDS', 0))
        return max_passing_yards_player.get('id')

    def find_player_with_max_ruhsing_yards(self, player_list):
        if not player_list:
            return None  # Return None if the list is empty

        max_passing_rushing_player = max(
            player_list, key=lambda x: x.get('FOOTBALL_RUSHING_YARDS', 0))
        return max_passing_rushing_player.get('id')

    def find_player_with_max_recieving_yards(self, player_list):
        if not player_list:
            return None  # Return None if the list is empty

        max_recieving_yard_player = max(
            player_list, key=lambda x: x.get('FOOTBALL_RECEIVING_YARDS', 0))
        return max_recieving_yard_player.get('id')

    def find_player_with_max_defensive_sacks(self, player_list):
        if not player_list:
            return None  # Return None if the list is empty

        max_defensive_sacks_player = max(
            player_list, key=lambda x: x.get('FOOTBALL_DEFENSIVE_SACKS', 0))
        return max_defensive_sacks_player.get('id')

    def find_player_with_max_defensive_tackles(self, player_list):
        if not player_list:
            return None  # Return None if the list is empty

        max_defensive_tackles_player = max(
            player_list, key=lambda x: x.get('FOOTBALL_DEFENSIVE_TACKLES', 0))
        return max_defensive_tackles_player.get('id')

    def find_player_with_max_defensive_interceptions(self, player_list):
        if not player_list:
            return None  # Return None if the list is empty

        max_defensive_interceptions_player = max(
            player_list, key=lambda x: x.get('FOOTBALL_DEFENSIVE_INTERCEPTIONS', 0))
        return max_defensive_interceptions_player.get('id')

    def get_field_value(self, document, field):
        if field in document:
            return document[field]
        else:
            return "0"

    def check_dict_key(self, dictionary, key):
        if key in dictionary:
            return dictionary[key]
        else:
            return 0

    def decimal_to_american_odds(self, decimal_odds):
        if decimal_odds >= 2:
            american_odds = int((decimal_odds - 1) * 100)
        else:
            american_odds = int(-100 / (decimal_odds - 1))
        return american_odds

    def check_start_of_week(self, date_str):
        # Define your week mapping
        week_mapping = {
            "NOV 15": 11,
            "NOV 14": 11,
            "NOV 20": 12,
            "NOV 21": 12,
            "NOV 22": 12,
            "NOV 28": 13,
            "DEC 05": 14,
            "DEC 06": 14,
            "DEC 07": 14,
            "DEC 08": 14,
            "DEC 12": 15,
            "DEC 19": 16,
            "DEC 26": 17,
            "DEC 27": 17,
            "JAN 02": 18,
            "JAN 03": 18,
            "JAN 11": 19
        }

        date_object = datetime.strptime(date_str, "%Y-%m-%d")

        if date_object.weekday() == 2:  # tuesday corresponds to 1

            formatted_date = date_object.strftime("%b %d").upper()
            # Check if the formatted date is in your week_mapping
            if formatted_date in week_mapping:
                return week_mapping[formatted_date]

        return None

    def generate_html(self, data):

        # for data in games_data_article:

        print("in generate_html function")

        print("Intro to game")
        html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
        html += "The " + data['Team 1 (T1)'] + " (" + str(data['Team 1 (T1) wins']) + "-" + str(data['Team 1 (T1) losses']) + ") " + " and the " + data['Team 2 (T2)'] + " (" + str(data['Team 2 (T2) wins']) + "-" + str(data['Team 2 (T2) losses']) + ") " + " play at " + data['Arena'] + " on " + \
            str(data['game_month_name']) + " " + str(data['game_day_num']) + ", " + str(data['game_year']) + ". Find more below on the " + data["Team 1 (T1)"].split(
        )[-1] + " vs. " + data["Team 2 (T2)"].split()[-1] + " betting line, injury report, head-to-head stats, best bets and more."

        print("Intro mini")
        html += "\n" + Betpicks.generate_response(self, "The " + data['favorite_team_name'].split()[-1] + " (" + str(
            data["spread_odd"]) + ") are slight favorites against the " + data["underdog_team_name"].split()[-1] + ". The total is set at " + str(data["overUnder_odds"]))

        # SPREAD AND BETTING LINE TABLE
        print("SPREAD AND BETTING LINE TABLE")
        html += "\n<h2>" + str(data['Team 1 (T1)'].split()[-1]) + " vs " + str(
            data['Team 2 (T2)'].split()[-1]) + " Spread and Betting Line</h2>"

        html += '\n<table class="table"><caption>' + str(data['Team 1 (T1)'].split(
        )[-1]) + ' vs ' + str(data['Team 2 (T2)'].split()[-1]) + ' Betting Information</caption>'

        table5_col = ["Favorite", "Spread", "Favorite spread odds",
                      "Underdog spread odds", "Total", "Over total odds", "Under total odds"]

        table5_cn = '</th>\n<th scope="col">'

        html += f'\n<thead>\n<tr>\n<th scope="col">{table5_cn.join(table5_col)}</th>\n</tr>\n</thead>'

        table5_row = [str(data["favorite_team_name"]), str(data['spread_odd']), str(data['favorite_spread_odds']), str(data['underdog_spread_odds']), str(
            data['overUnder_odds']), str(data['overUnderLineOver_odds']), str(data['overUnderLineUnder_odds'])]

        table5_rn = '</td>\n<td>'
        html += f'\n<tbody>\n<tr>\n<td>{table5_rn.join(table5_row)}</td>\n</tr>\n</tbody>\n</table>'

        print("Game Info")
        html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs. " + \
            data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
        html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['game_day_name']) + ", " + data["game_month_name"] + " " + str(data["game_day_num"]) + ", " + str(data["game_year"]) + "</li>\n<li><strong>Game Time:</strong> " + str(
            data['Game Time'] + " ET") + "</li>\n<li><strong>TV Channel:</strong> " + data["Game broadcast"] + "</li>\n<li><strong>Stadium:</strong> " + data['Arena'] + "</li>\n</ul>"

        print("Prediction and Computer Picks")
        # Table Prediction and Computer Picks
        html += "\n<h2>" + str(data['Team 1 (T1)'].split()[-1]) + " vs " + \
            str(data['Team 2 (T2)'].split()[-1]) + \
            " Prediction and Computer Picks</h2>"

        html += '\n<table class="table"><caption>Prediction for ' + \
            str(data['Team 1 (T1)'].split()[-1]) + ' vs ' + \
            str(data['Team 2 (T2)'].split()[-1]) + '</caption>'

        table3_col = ["Spread Pick", "Total Pick", "Predicted Score"]
        table3_cn = '</th>\n<th scope="col">'

        html += f'\n<thead>\n<tr>\n<th scope="col">{table3_cn.join(table3_col)}</th>\n</tr>\n</thead>'
        table3_row = [str(data["underdog_team_name"]) + " (" + str(data['spread_pick']) + ")", "Over (" + str(math.ceil(data['underdog_predicted_score'] + math.ceil(data["favorite_predicted_score"]))) + ")",
                      str(data["underdog_team_name"]) + " " + str(round(data['underdog_predicted_score'])) + ", " + str(math.floor(data["favorite_team_name"] - 0.5)) + " " + str(math.floor((data["favorite_predicted_score"] - 0.5)))]

        table3_rn = '</td>\n<td>'
        html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row)}</td>\n</tr>\n</tbody>\n</table>'

        print("HOME LEADERS")
        html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
        html += "\n<ul>\n<li>" + Betpicks.generate_response(self, data["Team 1 (T1) passing yard leader"]["name"] + " has thrown for " + str(data["Team 1 (T1) passing yard leader"]["passing_yards"]) + " yards this season on " + str(
            data["Team 1 (T1) passing yard leader"]["passing_attempts"]) + " attempts with " + str(data["Team 1 (T1) passing yard leader"]["passing_touchdowns"]) + " touchdowns and " + str(data["Team 1 (T1) passing yard leader"]["passing_interceptions"]) + " interceptions.")

        html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 1 (T1) rushing yard leader"]["name"] + " is currently leading the team in the rushing with " + str(data["Team 1 (T1) rushing yard leader last year"]["rushing_yard"]) + " yards, a long of " + str(data["Team 1 (T1) rushing yard leader last year"]["rushing_long"]) + " and  " + str(
            data["Team 1 (T1) rushing yard leader last year"]["touchdowns"]) + "touchdowns.")

        html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 1 (T1) receiving yard leader"]["name"] + " is currently leading the team in receiving with " + str(data["Team 1 (T1) receiving yard leader"]["recieving_yard"]) + " yards on  " + str(data["Team 1 (T1) receiving yard leader"]
                                                                                                                                                                                                                                                                  ["receiving_receptions"]) + " receptions and " + str(data["Team 1 (T1) receiving yard leader"]["touchdowns"]) + " touchdowns on the season.")

        html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 1 (T1) defensive sack leader"]["name"] + " leads the team in sacks so far this year with " + str(data["Team 1 (T1) defensive sack leader last year"]["defensive_sacks"]) + " sacks, along with " + str(
            data["Team 1 (T1) defensive sack leader"]["defensive_tackles"]) + " total tackles. ")

        html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 1 (T1) defensive tackles leader"]["name"] + " has been a force on defence this season as he leads the team with  " + str(data["Team 1 (T1) defensive tackles leader last year"]["defensive_tackles"]) + " solo tackles, along with " + str(
            data["Team 1 (T1) defensive tackles leader last year"]["defensive_sacks"]) + " sack, and " + str(data["Team 1 (T1) defensive tackles leader last year"]["tfl"]) + " interceptions.")

        html += "</li>\n</ul>"

        # HOME SEASONAL STATS Team 1 (T1) defensive tackles
        print("HOME SEASONAL STATS TABLE")
        html += "\n<h2>" + str(data['Team 1 (T1)']) + " Season Stats</h2>"
        html += '\n<table class="table">'

        table6_col = ["Stat", "Average (Total)", "Rank"]

        table6_cn = '</th>\n<th scope="col">'
        html += f'\n<thead>\n<tr>\n<th scope="col">{table6_cn.join(table6_col)}</th>\n</tr>\n</thead>'
        table6_row1 = ["<strong>Pass yards</strong>",
                       str(data['Team 1 (T1) passing yard']), "-"]
        table6_rn = '</td>\n<td>'
        html += f'\n<tbody>\n<tr>\n<td>{table6_rn.join(table6_row1)}</td>\n</tr>'
        table6_row2 = ["<strong>Rush yards</strong>",
                       str(data['Team 1 (T1) rushing yard']), "-"]
        html += f'\n<tr>\n<td>{table6_rn.join(table6_row2)}</td>\n</tr>'
        table6_row3 = ["<strong>Points scored</strong>",
                       str(data['Team 1 (T1) receiving yard']), "-"]
        html += f'\n<tr>\n<td>{table6_rn.join(table6_row3)}</td>\n</tr>'
        table6_row5 = ["<strong>Turnovers</strong>",
                       str(data['Team 1 (T1) defensive sacks']), "-"]
        html += f'\n<tr>\n<td>{table6_rn.join(table6_row5)}</td>\n</tr>'
        table6_row6 = ["<strong>Points allowed</strong>",
                       str(data['Team 1 (T1) defensive interceptions']), "-"]
        html += f'\n<tr>\n<td>{table6_rn.join(table6_row6)}</td>\n</tr>\n</tbody>\n</table>'

        print("AWAY LEADERS")

        html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
        html += "\n<ul>\n<li>" + Betpicks.generate_response(self, data["Team 2 (T2) passing yard leader"]["name"] + " has thrown for " + str(data["Team 2 (T2) passing yard leader"]["passing_yards"]) + " yards this season on " + str(
            data["Team 2 (T2) passing yard leader"]["passing_attempts"]) + " attempts with " + str(data["Team 2 (T2) passing yard leader"]["passing_touchdowns"]) + " touchdowns and " + str(data["Team 2 (T2) passing yard leader"]["passing_interceptions"]) + " interceptions.")

        html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 2 (T2) rushing yard leader"]["name"] + " is currently leading the team in the rushing with " + str(data["Team 2 (T2) rushing yard leader"]["rushing_yard"]) + " yards, a long of " + str(data["Team 2 (T2) rushing yard leader"]["rushing_long"]) + " and  " + str(
            data["Team 2 (T2) rushing yard leader"]["rushing_touchdowns"]) + "touchdowns.")

        html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 2 (T2) receiving yard leader"]["name"] + " is currently leading the team in receiving with " + str(data["Team 2 (T2) receiving yard leader"]["recieving_yard"]) + " yards on  " + str(data["Team 2 (T2) receiving yard leader"]
                                                                                                                                                                                                                                                                  ["receiving_receptions"]) + " receptions and " + str(data["Team 2 (T2) receiving yard leader"]["touchdowns"]) + " touchdowns on the season.")

        html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 2 (T2) defensive sack leader"]["name"] + " leads the team in sacks so far this year with " + str(data["Team 2 (T2) defensive sack leader"]["defensive_sacks"]) + " sacks, along with " + str(
            data["Team 2 (T2) defensive sack leader"]["defensive_tackles"]) + " total tackles. ")

        html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 2 (T2) defensive tackles leader"]["name"] + " has been a force on defence this season as he leads the team with  " + str(data["Team 2 (T2) defensive tackles leader"]["defensive_tackles"]) + " solo tackles, along with " + str(
            data["Team 2 (T2) defensive tackles leader"]["defensive_sacks"]) + " sack, and " + str(data["Team 2 (T2) defensive tackles leader"]["defensive_intercption"]) + " interceptions.")

        html += "</li>\n</ul>"

        # AWAY SEASONAL STATS Team 2 (T2) defensive tackles
        print("AWAy SEASONAL STATS TABLE")
        html += "\n<h2>" + data['Team 2 (T2)'] + " Season Stats</h2>"
        html += '\n<table class="table">'
        table7_col = ["Stat", "Average (Total)", "Rank"]
        table7_cn = '</th>\n<th scope="col">'
        html += f'\n<thead>\n<tr>\n<th scope="col">{table7_cn.join(table7_col)}</th>\n</tr>\n</thead>'
        table7_row1 = ["<strong>Pass yards</strong>",
                       str(data['Team 2 (T2) passing yard']), "-"]
        table7_rn = '</td>\n<td>'
        html += f'\n<tbody>\n<tr>\n<td>{table7_rn.join(table7_row1)}</td>\n</tr>'
        table7_row2 = ["<strong>Rush yards</strong>",
                       str(data['Team 2 (T2) rushing yard']), "-"]
        html += f'\n<tr>\n<td>{table7_rn.join(table7_row2)}</td>\n</tr>'
        table7_row3 = ["<strong>Points scored</strong>",
                       str(data['Team 2 (T2) receiving yard']), "-"]
        html += f'\n<tr>\n<td>{table7_rn.join(table7_row3)}</td>\n</tr>'
        table7_row5 = ["<strong>Turnovers</strong>",
                       str(data['Team 2 (T2) defensive sacks']), "-"]
        html += f'\n<tr>\n<td>{table7_rn.join(table7_row5)}</td>\n</tr>'
        table7_row6 = ["<strong>Points allowed</strong>",
                       str(data['Team 2 (T2) defensive interceptions']), "-"]
        html += f'\n<tr>\n<td>{table7_rn.join(table7_row6)}</td>\n</tr>\n</tbody>\n</table>'

        # injuries data for home and away
        print("injuries data for home and away table")
        html += "\n<h2>" + str(data['Team 1 (T1)'].split()[-1]) + " and " + \
                str(data['Team 2 (T2)'].split()[-1]) + \
                " Injury Report</h2>"

        html += '\n<table class="table"><caption>Injury Report for ' + \
                str(data['Team 1 (T1)'].split()[-1]) + ' and ' + \
                str(data['Team 2 (T2)'].split()[-1]) + '</caption>'

        table4_col = ["Player", "Pos.", "Injury", "Status"]
        table4_cn = '</th>\n<th scope="col">'
        html += f'\n<thead>\n<tr>\n<th scope="col">{table4_cn.join(table4_col)}</th>\n</tr>\n</thead>'

        html += f'\n<tbody>'

        print("Home injuries table")
        # Loop through the list of dictionaries and generate table rows
        # for player_data in data['Team 1 (T1) injuries']:
        #     html += f'\n<tr>\n<td>{player_data["name"]}</td>\n<td>{player_data["position"]}</td>\n<td>{player_data["injury"]}</td>\n<td>{player_data["status"]}</td>\n</tr>'

        for player_data in data['Team 1 (T1) injuries']:
            html += f'\n<tr>\n<td>{player_data["name"]}</td>\n<td>{player_data["position"]}</td>\n<td>{player_data["injury"]}</td>\n<td>{player_data["status"]}</td>\n</tr>'
            print("\n")
        # html += f'\n</tbody>\n</table>'
        html += f'\n</tbody>\n</table>'

        match_teams = data['Team 1 (T1)'] + "_" + data['Team 2 (T2)']
        filename = match_teams + \
            '_Betting_Pick_Against_the_Spread_' + str(data['Game Day'])
        filepath_name = os.path.join(
            SAVEDIRPATH + "/NFL/", filename+".html")
        try:
            text_file = open(filepath_name, "w")
            text_file.write(html)
            text_file.close()
        except Exception:
            pass
        images_folder_path = IMAGESPATH + "/NFL_Images"
        thumbnail = Betpicks.get_article_thumbnail(
            self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
        current_path = SAVEDIRPATH + "/NFL/"
        try:
            print("article image saved")
            shutil.copy(thumbnail[1], current_path)
            os.chdir(SAVEDIRPATH + "/NFL")
            os.rename(thumbnail[0], filename+'.jpg')
        except Exception:
            print("article image not saved")
            pass
        print("Article Saved online!")

    def offline_html(self, data):
        # for data in games_data_article:

        print("in generate_html offline function")
        try:
        
            print("Intro to game")
            html = "<head><meta charset='UTF-8'><meta name='keywords' content='HTML, CSS, JavaScript'></head>"
            html += "The " + data['Team 1 (T1)'] + " (" + str(data['Team 1 (T1) wins']) + "-" + str(data['Team 1 (T1) losses']) + ") " + " and the " + data['Team 2 (T2)'] + " (" + str(data['Team 2 (T2) wins']) + "-" + str(data['Team 2 (T2) losses']) + ") " + " play at " + data['Arena'] + " on " + \
                str(data['game_month_name']) + " " + str(data['game_day_num']) + ", " + str(data['game_year']) + ". Find more below on the " + data["Team 1 (T1)"].split(
            )[-1] + " vs. " + data["Team 2 (T2)"].split()[-1] + " betting line, injury report, head-to-head stats, best bets and more."

            print("Intro mini")
            html += "\n" + Betpicks.generate_response(self, "The " + data['favorite_team_name'].split()[-1] + " (" + str(
                data["spread_odd"]) + ") are slight favorites against the " + data["underdog_team_name"].split()[-1] + ". The total is set at " + str(data["overUnder_odds"]))

            # over
            # SPREAD AND BETTING LINE TABLE
            print("SPREAD AND BETTING LINE TABLE")
            html += "\n<h2>" + str(data['Team 1 (T1)'].split()[-1]) + " vs " + str(
                data['Team 2 (T2)'].split()[-1]) + " Spread and Betting Line</h2>"

            html += '\n<table class="table"><caption>' + str(data['Team 1 (T1)'].split(
            )[-1]) + ' vs ' + str(data['Team 2 (T2)'].split()[-1]) + ' Betting Information</caption>'

            table5_col = ["Favorite", "Spread", "Favorite spread odds",
                            "Underdog spread odds", "Total", "Over total odds", "Under total odds"]

            table5_cn = '</th>\n<th scope="col">'

            html += f'\n<thead>\n<tr>\n<th scope="col">{table5_cn.join(table5_col)}</th>\n</tr>\n</thead>'

            table5_row = [str(data["favorite_team_name"]), str(data['spread_odd']), str(data['favorite_spread_odds']), str(data['underdog_spread_odds']), str(
                data['overUnder_odds']), str(data['overUnderLineOver_odds']), str(data['overUnderLineUnder_odds'])]

            table5_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table5_rn.join(table5_row)}</td>\n</tr>\n</tbody>\n</table>'

            print("Game Info")
            html += "\n<h2>" + data['Team 1 (T1)'].split()[-1] + " vs. " + \
                data['Team 2 (T2)'].split()[-1] + " Game Info</h2>"
            html += "\n<ul>\n<li><strong>Game Day:</strong> " + str(data['game_day_name']) + ", " + data["game_month_name"] + " " + str(data["game_day_num"]) + ", " + str(data["game_year"]) + "</li>\n<li><strong>Game Time:</strong> " + str(
                data['Game Time'] + " ET") + "</li>\n<li><strong>TV Channel:</strong> " + data["Game broadcast"] + "</li>\n<li><strong>Stadium:</strong> " + data['Arena'] + "</li>\n</ul>"

            print("Prediction and Computer Picks")
            html += "\n<h2>" + str(data['Team 1 (T1)'].split()[-1]) + " vs " + \
                str(data['Team 2 (T2)'].split()[-1]) + \
                " Prediction and Computer Picks</h2>"

            html += '\n<table class="table"><caption>Prediction for ' + \
                str(data['Team 1 (T1)'].split()[-1]) + ' vs ' + \
                str(data['Team 2 (T2)'].split()[-1]) + '</caption>'

            table3_col = ["Spread Pick", "Total Pick", "Predicted Score"]
            table3_cn = '</th>\n<th scope="col">'
            # underdog_predicted_score
            # favorite_predicted_score

            html += f'\n<thead>\n<tr>\n<th scope="col">{table3_cn.join(table3_col)}</th>\n</tr>\n</thead>'
            table3_row = [str(data["underdog_team_name"]) + " (" + str(data['spread_pick']) + ")", "Under (" + str(math.ceil(data['underdog_predicted_score'] + math.ceil(data["favorite_predicted_score"]))) + ")",
                            str(data["underdog_team_name"]) + " " + str(math.floor((float(data['underdog_predicted_score'] - 0.5)))) + ", " + str(data["favorite_team_name"]) + " " + str(math.floor((float(data["favorite_predicted_score"]) - 0.5)))]

            table3_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table3_rn.join(table3_row)}</td>\n</tr>\n</tbody>\n</table>'

            # defensive_tackles
            print("HOME LEADERS")
            html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
            html += "\n<ul>\n<li>" + Betpicks.generate_response(self, data["Team 1 (T1) passing yard leader"]["name"] + " has thrown for " + str(data["Team 1 (T1) passing yard leader"]["passing_yards"]) + " yards this season on " + str(
                data["Team 1 (T1) passing yard leader"]["passing_attempts"]) + " attempts with " + str(data["Team 1 (T1) passing yard leader"]["passing_touchdowns"]) + " touchdowns and " + str(data["Team 1 (T1) passing yard leader"]["passing_interceptions"]) + " interceptions.")

            html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 1 (T1) rushing yard leader"]["name"] + " is currently leading the team in the rushing with " + str(data["Team 1 (T1) rushing yard leader last year"]["rushing_yard"]) + " yards, a long of " + str(data["Team 1 (T1) rushing yard leader last year"]["rushing_long"]) + " and  " + str(
                data["Team 1 (T1) rushing yard leader last year"]["touchdowns"]) + "touchdowns.")

            html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 1 (T1) receiving yard leader"]["name"] + " is currently leading the team in receiving with " + str(data["Team 1 (T1) receiving yard leader"]["recieving_yard"]) + " yards on  " + str(data["Team 1 (T1) receiving yard leader"]
                                                                                                                                                                                                                                                                        ["receiving_receptions"]) + " receptions and " + str(data["Team 1 (T1) receiving yard leader"]["touchdowns"]) + " touchdowns on the season.")

            html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 1 (T1) defensive sack leader"]["name"] + " leads the team in sacks so far this year with " + str(data["Team 1 (T1) defensive sack leader last year"]["defensive_sacks"]) + " sacks, along with " + str(
                data["Team 1 (T1) defensive sack leader"]["defensive_tackles"]) + " total tackles. ")

            html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 1 (T1) defensive tackles leader"]["name"] + " has been a force on defence this season as he leads the team with  " + str(data["Team 1 (T1) defensive tackles leader last year"]["defensive_tackles"]) + " solo tackles, along with " + str(
                data["Team 1 (T1) defensive tackles leader last year"]["defensive_sacks"]) + " sack, and " + str(data["Team 1 (T1) defensive tackles leader last year"]["tfl"]) + " interceptions.")

            html += "</li>\n</ul>"

            # HOME SEASONAL STATS
            print("HOME SEASONAL STATS TABLE")
            html += "\n<h2>" + \
                str(data['Team 1 (T1)']) + " Season Stats</h2>"
            html += '\n<table class="table">'

            table6_col = ["Stat", "Average (Total)"]

            table6_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table6_cn.join(table6_col)}</th>\n</tr>\n</thead>'
            table6_row1 = ["<strong>Pass yards</strong>",
                            str(data['Team 1 (T1) passing yard'])]
            table6_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table6_rn.join(table6_row1)}</td>\n</tr>'
            table6_row2 = ["<strong>Rush yards</strong>",
                            str(data['Team 1 (T1) rushing yard'])]
            html += f'\n<tr>\n<td>{table6_rn.join(table6_row2)}</td>\n</tr>'
            table6_row3 = ["<strong>Points scored</strong>",
                            str(data['Team 1 (T1) receiving yard'])]
            html += f'\n<tr>\n<td>{table6_rn.join(table6_row3)}</td>\n</tr>'
            table6_row5 = ["<strong>Turnovers</strong>",
                            str(data['Team 1 (T1) defensive sacks'])]
            html += f'\n<tr>\n<td>{table6_rn.join(table6_row5)}</td>\n</tr>'
            table6_row6 = ["<strong>Points allowed</strong>",
                            str(data['Team 1 (T1) defensive interceptions'])]
            html += f'\n<tr>\n<td>{table6_rn.join(table6_row6)}</td>\n</tr>\n</tbody>\n</table>'

            #  rushing_yard
            print("AWAY LEADERS")

            html += "\n<h2>" + data['Team 1 (T1)'] + " Leaders</h2>"
            html += "\n<ul>\n<li>" + Betpicks.generate_response(self, data["Team 2 (T2) passing yard leader"]["name"] + " has thrown for " + str(data["Team 2 (T2) passing yard leader"]["passing_yards"]) + " yards this season on " + str(
                data["Team 2 (T2) passing yard leader"]["passing_attempts"]) + " attempts with " + str(data["Team 2 (T2) passing yard leader"]["passing_touchdowns"]) + " touchdowns and " + str(data["Team 2 (T2) passing yard leader"]["passing_interceptions"]) + " interceptions.")

            html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 2 (T2) rushing yard leader"]["name"] + " is currently leading the team in the rushing with " + str(data["Team 2 (T2) rushing yard leader"]["rushing_yard"]) + " yards, a long of " + str(data["Team 2 (T2) rushing yard leader"]["rushing_long"]) + " and  " + str(
                data["Team 2 (T2) rushing yard leader"]["rushing_touchdowns"]) + "touchdowns.")

            html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 2 (T2) receiving yard leader"]["name"] + " is currently leading the team in receiving with " + str(data["Team 2 (T2) receiving yard leader"]["recieving_yard"]) + " yards on  " + str(data["Team 2 (T2) receiving yard leader"]
                                                                                                                                                                                                                                                                        ["receiving_receptions"]) + " receptions and " + str(data["Team 2 (T2) receiving yard leader"]["touchdowns"]) + " touchdowns on the season.")

            html += "</li>\n<li>" + Betpicks.generate_response(self, data["Team 2 (T2) defensive sack leader"]["name"] + " leads the team in sacks so far this year with " + str(data["Team 2 (T2) defensive sack leader"]["defensive_sacks"]) + " sacks, along with " + str(
                data["Team 2 (T2) defensive sack leader"]["defensive_tackles"]) + " total tackles. ")

            html += "</li>\n<li>" + Betpicks.generate_response(self, "Last season " + data["Team 2 (T2) defensive tackles leader"]["name"] + " has been a force on defence this season as he leads the team with  " + str(data["Team 2 (T2) defensive tackles leader"]["defensive_tackles"]) + " solo tackles, along with " + str(
                data["Team 2 (T2) defensive tackles leader"]["defensive_sacks"]) + " sack, and " + str(data["Team 2 (T2) defensive tackles leader"]["defensive_intercption"]) + " interceptions.")

            html += "</li>\n</ul>"

            # AWAY SEASONAL STATS
            print("AWAy SEASONAL STATS TABLE")
            html += "\n<h2>" + data['Team 2 (T2)'] + " Season Stats</h2>"
            html += '\n<table class="table">'
            table7_col = ["Stat", "Average (Total)"]
            table7_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table7_cn.join(table7_col)}</th>\n</tr>\n</thead>'
            table7_row1 = ["<strong>Pass yards</strong>",
                            str(data['Team 2 (T2) passing yard'])]
            table7_rn = '</td>\n<td>'
            html += f'\n<tbody>\n<tr>\n<td>{table7_rn.join(table7_row1)}</td>\n</tr>'
            table7_row2 = ["<strong>Rush yards</strong>",
                            str(data['Team 2 (T2) rushing yard'])]
            html += f'\n<tr>\n<td>{table7_rn.join(table7_row2)}</td>\n</tr>'
            table7_row3 = ["<strong>Points scored</strong>",
                            str(data['Team 2 (T2) receiving yard'])]
            html += f'\n<tr>\n<td>{table7_rn.join(table7_row3)}</td>\n</tr>'
            table7_row5 = ["<strong>Turnovers</strong>",
                            str(data['Team 2 (T2) defensive sacks'])]
            html += f'\n<tr>\n<td>{table7_rn.join(table7_row5)}</td>\n</tr>'
            table7_row6 = ["<strong>Points allowed</strong>",
                            str(data['Team 2 (T2) defensive interceptions'])]
            html += f'\n<tr>\n<td>{table7_rn.join(table7_row6)}</td>\n</tr>\n</tbody>\n</table>'

            # injuries data for home and away
            print("injuries data for home and away table")
            html += "\n<h2>" + str(data['Team 1 (T1)'].split()[-1]) + " and " + \
                    str(data['Team 2 (T2)'].split()[-1]) + \
                    " Injury Report</h2>"

            html += '\n<table class="table"><caption>Injury Report for ' + \
                    str(data['Team 1 (T1)'].split()[-1]) + ' and ' + \
                    str(data['Team 2 (T2)'].split()[-1]) + '</caption>'

            table4_col = ["Player", "Pos.", "Injury", "Status"]
            table4_cn = '</th>\n<th scope="col">'
            html += f'\n<thead>\n<tr>\n<th scope="col">{table4_cn.join(table4_col)}</th>\n</tr>\n</thead>'

            html += f'\n<tbody>'

            print("Home injuries table")
            for player_data in data['Team 1 (T1) injuries']:
                html += f'\n<tr>\n<td>{player_data["name"]}</td>\n<td>{player_data["position"]}</td>\n<td>{player_data["injury"]}</td>\n<td>{player_data["status"]}</td>\n</tr>'
                print("\n")

            html += f'\n</tbody>\n</table>'

            match_teams = data['Team 1 (T1)'] + "_vs_" + data['Team 2 (T2)']
            filename = match_teams + \
                '_Prediction_Betting_Tips_& _Picks_' + str(data['Game Day'])
            filepath_name = os.path.join(
                SAVEDIRPATH + "/NFL/", filename+".html")
            try:
                text_file = open(filepath_name, "w")
                text_file.write(html)
                text_file.close()
            except Exception:
                pass
            images_folder_path = IMAGESPATH + "/NFL_Images"
            thumbnail = Betpicks.find_and_select_image(
                self, images_folder_path, str(data['Team 1 (T1)'].split()[-1]))
            current_path = SAVEDIRPATH + "/NFL/Images"
            try:
                if thumbnail is not None:
                    print("Copy Copy")
                    shutil.copy(thumbnail, current_path)
                    
                    if filename is not None:
                        os.chdir(SAVEDIRPATH + "/NFL/Images")
                        os.rename(thumbnail, filename+'.jpg')
                    else:
                        print("Filename is not defined.")
                else:
                    print("Thumbnail is None or has fewer than 2 elements.")
            except Exception as e:
                print("Error during copy or rename:")
                print(e)
                pass
            print("Article Saved online!")
        except Exception as e:
            print(e)

    def nfl_main(self):
        if os.path.exists('./NFL'):
            command.run(['sudo', 'chmod', '-R', '777', './NFL'])
            shutil.rmtree(SAVEDIRPATH+"/NFL",
                          ignore_errors=False, onerror=None)
        if os.path.exists(SAVEDIRPATH+"/NFL.zip"):
            os.remove(SAVEDIRPATH+"/NFL.zip")
        print("NFL Folder Removed!")

        
        if not os.path.exists(SAVEDIRPATH+"/NFL"):
            os.makedirs(SAVEDIRPATH+"/NFL")
            os.makedirs(SAVEDIRPATH+"/NFL/Images")
            print("NFL Folder Created!")
        else:
            print("NFL Folder already exists.")

        print("start")

        today_date = datetime.now().strftime("%Y-%m-%d")
        # week = self.check_start_of_week(today_date)
        # week_name = "Week " + str(week)

        data = []
        games = []
        # print(week_name)

        week_name = "AFC Wild Card Playoffs"

        URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/odds.json?sport=nfl&apiKey=" + \
            self.ODDS_METABET_API_KEY

        print(week_name)

        # Game Info
        try:

            data = Betpicks.get_games_info(self, URL)
            for result in data['results']:
                print("rounds")
                # if result['round'] == week_name:
                games.append(result)

        except Exception as error:
            print(error)

        print(len(games))

        if games:

            print("Start Gathering data")

            games_data_article = []
            for game in games:

                try:

                    game_id = game['gameID']
                    # game_scheduled = game['scheduled']
                    date_unix = game['date']

                    game_date, game_time = self.decode_time(date_unix)

                    game_day_name = game_date.strftime("%A")
                    game_month_name = game_date.strftime("%B")
                    game_day_num = game_date.strftime("%d")
                    game_year = game_date.strftime("%Y")

                    game_date = game_date.strftime("%m-%d-%Y")

                    print("Game Airing data")
                    """Game Airing"""
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/airings.json?providerID=IL63451|X&" + \
                        "&apiKey=" + self.ODDS_METABET_API_KEY
                    game_airing = Betpicks.get_data_request(self, URL)
                    game_broadcast = ""
                    for result in game_airing['results']:
                        if result['gameID'] == game_id:
                            game_broadcast = result['callSign']

                    # game_location = game['location']
                    # game_broadcast = game['broadcast']['network']
                    game_arena = game['location']
                    team_home = game['team1Name']
                    team_home_id = game['team1ID']
                    team_away = game['team2Name']
                    team_away_id = game['team2ID']

                    print("Home Team Profile")
                    """Home Team Profile"""
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/players.json?teamID=" + \
                        str(team_home_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY

                    home_team_profile = Betpicks.get_data_request(self, URL)
                    home_players = home_team_profile['results']
                    home_players_names = []
                    for players in home_players:
                        home_players_names.append(
                            players['firstName'] + " " + players['lastName'])

                    print("Home/Away losses and wins")
                    """Home/Away losses and wins"""
                    # HOME TEAM
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/teams.json?teamID=" + \
                        str(team_home_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_stats = Betpicks.get_data_request(self, URL)

                    home_wins = home_stats['results'][0]['wins']
                    home_losses = home_stats['results'][0]['losses']
                    home_ties = home_stats['results'][0]['ties']
                    home_total_games = home_wins + home_losses + home_ties

                    # AWAY TEAM
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/teams.json?teamID=" + \
                        str(team_away_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_stats = Betpicks.get_data_request(self, URL)

                    away_wins = away_stats['results'][0]['wins']
                    away_losses = away_stats['results'][0]['losses']
                    away_ties = away_stats['results'][0]['ties']
                    away_total_games = away_wins + away_losses + away_ties

                    print("Away Team Profile")
                    """Away Team Profile"""
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/players.json?teamID=" + \
                        str(team_away_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_team_profile = Betpicks.get_data_request(self, URL)
                    away_players = away_team_profile['results']
                    away_players_names = []
                    for players in away_players:
                        away_players_names.append(
                            players['firstName'] + " " + players['lastName'])

                    home_spread_odd = 0
                    away_spread_odd = 0

                    home_moneyLine1 = 0
                    home_moneyLine2 = 0
                    home_spreadLine1 = 0
                    home_spreadLine2 = 0

                    away_moneyLine1 = 0
                    away_moneyLine2 = 0
                    away_spreadLine1 = 0
                    away_spreadLine2 = 0

                    home_over_under = 0
                    away_over_under = 0
                    home_over_underLineOver = 0
                    away_over_underLineOver = 0
                    home_over_underLineUnder = 0
                    away_over_underLineUnder = 0

                    print("odds data")
                    # ODDS Data HOME
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/odds.json?teamID=" + \
                        str(team_home_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY

                    home_odds_results = Betpicks.get_data_request(self, URL)

                    for result in home_odds_results['results']:
                        if result['gameID'] == game_id:
                            for odd in result["odds"]:

                                if odd["provider"] == "BET_365":

                                    home_moneyLine1 = odd['moneyLine1']
                                    home_moneyLine2 = odd['moneyLine2']
                                    home_spread_odd = odd['spread']
                                    home_spreadLine1 = odd['spreadLine1']
                                    home_spreadLine2 = odd['spreadLine2']

                                    home_spreadLine1 = self.decimal_to_american_odds(
                                        home_spreadLine1)
                                    home_spreadLine2 = self.decimal_to_american_odds(
                                        home_spreadLine2)

                                    home_over_under = odd['overUnder']
                                    home_over_underLineOver = odd['overUnderLineOver']
                                    home_over_underLineUnder = odd['overUnderLineUnder']

                                    home_over_underLineOver = self.decimal_to_american_odds(
                                        home_over_underLineOver)
                                    home_over_underLineUnder = self.decimal_to_american_odds(
                                        home_over_underLineUnder)

                    print("ODDS Data away")
                    # ODDS Data away
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/odds.json?teamID=" + \
                        str(team_away_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_odds_results = Betpicks.get_data_request(self, URL)
                    print(game_id)
                    for result in away_odds_results['results']:

                        if result['gameID'] == game_id:
                            for odd in result["odds"]:

                                if odd["provider"] == "BET_365":

                                    away_moneyLine1 = odd['moneyLine1']
                                    away_moneyLine2 = odd['moneyLine2']
                                    away_spread_odd = odd['spread']
                                    away_spreadLine1 = odd['spreadLine1']
                                    away_spreadLine2 = odd['spreadLine2']

                                    away_spreadLine1 = self.decimal_to_american_odds(
                                        away_spreadLine1)
                                    away_spreadLine2 = self.decimal_to_american_odds(
                                        away_spreadLine2)

                                    away_over_under = round(odd['overUnder'])
                                    away_over_underLineOver = odd['overUnderLineOver']
                                    away_over_underLineUnder = odd['overUnderLineUnder']

                                    away_over_underLineOver = self.decimal_to_american_odds(
                                        away_over_underLineOver)
                                    away_over_underLineUnder = self.decimal_to_american_odds(
                                        away_over_underLineUnder)

                    print("favorite team id")
                    favorite_team_id = 0
                    favorite_team_name = ""  # entry 1
                    underdog_team_name = ""  # entry 1
                    spread_odd = 0  # entry 2
                    favorite_spread_odds = 0  # entry 3
                    underdog_spread_odds = 0  # entry 4
                    overUnder_odds = 0  # entry 5
                    overUnderLineOver_odds = 0  # entry 6
                    overUnderLineUnder_odds = 0  # entry 7
                    if home_moneyLine1 < away_moneyLine1 or home_moneyLine2 < away_moneyLine2:
                        print("############ FAV ONE #############")
                        favorite_team_id = team_home_id
                        favorite_team_name = team_home
                        underdog_team_name = team_away
                        spread_odd = round(home_spread_odd, 1)
                        overUnder_odds = round(home_over_under, 1)
                        overUnderLineOver_odds = home_over_underLineOver
                        overUnderLineUnder_odds = home_over_underLineUnder
                        if home_spreadLine1 < home_spreadLine2:
                            favorite_spread_odds = home_spreadLine1
                            underdog_spread_odds = home_spreadLine2
                        else:
                            favorite_spread_odds = home_spreadLine2
                            underdog_spread_odds = home_spreadLine1
                    else:
                        print("############ FAV Two #############")
                        favorite_team_id = team_away_id
                        favorite_team_name = team_away
                        underdog_team_name = team_home
                        spread_odd = round(away_spread_odd, 1)
                        overUnder_odds = round(away_over_under)
                        overUnderLineOver_odds = away_over_underLineOver
                        overUnderLineUnder_odds = away_over_underLineUnder
                        if away_spreadLine1 < away_spreadLine2:
                            favorite_spread_odds = away_spreadLine1
                            underdog_spread_odds = away_spreadLine2
                        else:
                            favorite_spread_odds = away_spreadLine2
                            underdog_spread_odds = away_spreadLine1

                    print("------------ PRINT --------------------")
                    print("home_moneyLine1: ", home_moneyLine1)
                    print("home_moneyLine2: ", home_moneyLine2)
                    print("away_moneyLine2: ", away_moneyLine2)
                    print("away_moneyLine1: ", away_moneyLine1)
                    print("Favorite Team ID: ", favorite_team_id)
                    print("spread_odd: ", spread_odd)
                    print("favorite_spread_odds: ", favorite_spread_odds)
                    print("underdog_spread_odds: ", underdog_spread_odds)
                    print("overUnder_odds: ", overUnder_odds)
                    print("overUnderLineOver_odds: ", overUnderLineOver_odds)
                    print("overUnderLineUnder_odds: ", overUnderLineUnder_odds)

                    print("HOME TEAM PLAYER LEADERS")
                    # HOME TEAM PLAYER LEADERS
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?teamID=" + \
                        str(team_home_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_leaders_data = self.get_data_request(URL)

                    home_player_passing_yard = []
                    home_player_rushing_yard = []
                    home_player_recieving_yard = []
                    home_player_defensive_sacks = []
                    home_player_defensive_tackles = []
                    home_player_defensive_interceptions = []

                    for leader in home_leaders_data['results']:
                        if leader["statistics"].__contains__('FOOTBALL_PASSING_YARDS'):
                            passing = {
                                "id": leader['playerID'],
                                "FOOTBALL_PASSING_YARDS": leader['statistics']['FOOTBALL_PASSING_YARDS']
                            }
                            home_player_passing_yard.append(passing)
                        if leader["statistics"].__contains__('FOOTBALL_RUSHING_YARDS'):
                            rush = {
                                "id": leader['playerID'],
                                "FOOTBALL_RUSHING_YARDS": leader['statistics']['FOOTBALL_RUSHING_YARDS']
                            }
                            home_player_rushing_yard.append(rush)
                        if leader["statistics"].__contains__('FOOTBALL_RECEIVING_YARDS'):
                            recieve = {
                                "id": leader['playerID'],
                                "FOOTBALL_RECEIVING_YARDS": leader['statistics']['FOOTBALL_RECEIVING_YARDS']
                            }
                            home_player_recieving_yard.append(recieve)
                        if leader["statistics"].__contains__('FOOTBALL_DEFENSIVE_SACKS'):
                            sacks = {
                                "id": leader['playerID'],
                                "FOOTBALL_DEFENSIVE_SACKS": leader['statistics']['FOOTBALL_DEFENSIVE_SACKS']
                            }
                            home_player_defensive_sacks.append(sacks)
                        if leader["statistics"].__contains__('FOOTBALL_DEFENSIVE_TACKLES'):
                            tackles = {
                                "id": leader['playerID'],
                                "FOOTBALL_DEFENSIVE_TACKLES": leader['statistics']['FOOTBALL_DEFENSIVE_TACKLES']
                            }
                            home_player_defensive_tackles.append(tackles)
                        if leader["statistics"].__contains__('FOOTBALL_DEFENSIVE_INTERCEPTIONS'):
                            interceptions = {
                                "id": leader['playerID'],
                                "FOOTBALL_DEFENSIVE_INTERCEPTIONS": leader['statistics']['FOOTBALL_DEFENSIVE_INTERCEPTIONS']
                            }
                            home_player_defensive_interceptions.append(
                                interceptions)

                    print("getting IDs of leaders HOME TEAM")
                    # Getting IDs of leaders HOME TEAM
                    home_passing_yard_leader_id = self.find_player_with_max_passing_yards(
                        home_player_passing_yard)
                    home_rushing_yard_leader_id = self.find_player_with_max_ruhsing_yards(
                        home_player_rushing_yard)
                    home_recieving_yard_leader_id = self.find_player_with_max_recieving_yards(
                        home_player_recieving_yard)
                    home_defensive_sacks_leader_id = self.find_player_with_max_defensive_sacks(
                        home_player_defensive_sacks)
                    home_defensive_tackles_leader_id = self.find_player_with_max_defensive_tackles(
                        home_player_defensive_tackles)
                    home_defensive_interceptions_leader_id = self.find_player_with_max_defensive_interceptions(
                        home_player_defensive_interceptions)

                    print("Data for passing yard leader home 1")
                    # Data for passing yard leader home
                    # 1
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_passing_yard_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY

                    home_passing_yard_leader_data = self.get_data_request(URL)

                    if home_passing_yard_leader_data != 404:

                        home_passing_yard_leader_data = home_passing_yard_leader_data["results"][0]

                        home_passing_yard_leader_info = {
                            "name": str(home_passing_yard_leader_data["firstName"] + " " + home_passing_yard_leader_data["lastName"]),
                            "position": home_passing_yard_leader_data["position"],
                            "passing_yards": self.get_field_value(home_passing_yard_leader_data["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "passing_touchdowns": self.get_field_value(home_passing_yard_leader_data["statistics"],  "FOOTBALL_PASSING_TOUCHDOWNS"),
                            "passing_attempts": int(self.get_field_value(home_passing_yard_leader_data["statistics"], "FOOTBALL_PASSING_ATTEMPTS")),
                            "passing_interceptions": int(self.get_field_value(home_passing_yard_leader_data["statistics"], "FOOTBALL_PASSING_INTERCEPTIONS")),

                        }
                    else:
                        home_passing_yard_leader_data = []

                        home_passing_yard_leader_info = {
                            "name": "0.0",
                            "position": "0.0",
                            "passing_yards": "0.0",
                            "passing_touchdowns": "0.0",
                            "passing_attempts": "0.0",
                            "passing_interceptions": "0.0",
                        }

                    SEASON = 2023

                    print("Data for passing yard leader home 1 2023 stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_passing_yard_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_passing_yard_leader_data_last_year = self.get_data_request(
                        URL)

                    if home_passing_yard_leader_data_last_year == 404:

                        home_passing_yard_leader_data_last_year = home_passing_yard_leader_data_last_year[
                            "results"][0]

                        home_passing_yard_leader_info_last_year = {
                            "passing_yards": self.get_field_value(home_passing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "completion_rate": str(((self.get_field_value(home_passing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_COMPLETIONS") / self.get_field_value(home_passing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_ATTEMPTS")) * 100)),
                            "passing_touchdowns": self.get_field_value(home_passing_yard_leader_data_last_year["statistics"],  "FOOTBALL_PASSING_TOUCHDOWNS"),
                            "passing_interceptions": self.get_field_value(home_passing_yard_leader_data_last_year["statistics"],  "FOOTBALL_PASSING_INTERCEPTIONS"),
                            "passing_attempts": self.get_field_value(home_passing_yard_leader_data_last_year["statistics"],  "FOOTBALL_PASSING_ATTEMPTS"),

                        }
                    else:
                        home_passing_yard_leader_data_last_year = []

                        home_passing_yard_leader_info_last_year = {
                            "passing_yards": "0.0",
                            "completion_rate": "0.0",
                            "passing_touchdowns": "0.0",
                            "passing_interceptions": "0.0",
                            "passing_attempts": "0.0",

                        }

                    print("Data for rushing yard leader home 2")
                    # 2
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_rushing_yard_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY

                    home_rushing_yard_leader_data = self.get_data_request(URL)

                    touchdowns = 0

                    if home_rushing_yard_leader_data != 404:

                        home_rushing_yard_leader_data = home_rushing_yard_leader_data["results"][0]

                        rushing = int(self.get_field_value(
                            home_rushing_yard_leader_data["statistics"], "FOOTBALL_RUSHING_TOUCHDOWNS"))
                        recieving = int(self.get_field_value(
                            home_rushing_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"))
                        touchdowns = rushing + touchdowns

                        home_rushing_yard_leader_info = {
                            "name": str(home_rushing_yard_leader_data["firstName"] + " " + home_rushing_yard_leader_data["lastName"]),
                            "position": home_rushing_yard_leader_data["position"],
                            "passing_yards": self.get_field_value(home_rushing_yard_leader_data["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "rushing_touchdowns": str(touchdowns),
                            "recieving_yard":  self.get_field_value(home_rushing_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_YARDS"),
                            "rushing_yard":  self.get_field_value(home_rushing_yard_leader_data["statistics"], "FOOTBALL_RUSHING_YARDS"),
                            "rushing_long":  self.get_field_value(home_rushing_yard_leader_data["statistics"], "FOOTBALL_RUSHING_LONG"),
                        }
                    else:

                        home_rushing_yard_leader_data = []

                        home_rushing_yard_leader_info = {
                            "name": "0.0",
                            "position": "0.0",
                            "passing_yards": "0.0",
                            "rushing_touchdowns": "0.0",
                            "recieving_yard":  "0.0",
                            "rushing_yard":  "0.0",
                            "rushing_long":  "0.0",
                        }

                    print("Data for rushing yard leader home 3 this year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_rushing_yard_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_rushing_yard_leader_data_last_year = self.get_data_request(
                        URL)

                    if home_rushing_yard_leader_data_last_year != 404:

                        home_rushing_yard_leader_data_last_year = home_rushing_yard_leader_data_last_year[
                            "results"][0]

                        passing_completions = float(self.get_field_value(
                            home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_COMPLETIONS"))
                        passing_attempts = float(self.get_field_value(
                            home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_ATTEMPTS"))

                        if passing_attempts != 0:
                            completion_rate = str(
                                (passing_completions / passing_attempts) * 100)
                        else:
                            completion_rate = "N/A"

                        touchdowns = 0
                        rushing = int(self.get_field_value(
                            home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RUSHING_TOUCHDOWNS"))
                        recieving = int(self.get_field_value(
                            home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"))
                        touchdowns = rushing + touchdowns

                        home_rushing_yard_leader_info_last_year = {
                            "rushing_yard": self.get_field_value(home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RUSHING_YARDS"),
                            "completion_rate": str(completion_rate),
                            "touchdowns": str(touchdowns),
                            "passing_interceptions": self.get_field_value(home_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_PASSING_INTERCEPTIONS"),
                            "receiving_receptions": self.get_field_value(home_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_RECEPTIONS"),
                            "receiving_yards": self.get_field_value(home_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_YARDS"),
                            "receiving_touchdowns": self.get_field_value(home_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_TOUCHDOWNS"),
                            "rushing_long":  self.get_field_value(home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RUSHING_LONG"),

                        }
                    else:
                        home_rushing_yard_leader_data_last_year = []

                        home_rushing_yard_leader_info_last_year = {
                            "rushing_yard": "0.0",
                            "completion_rate": "0.0",
                            "touchdowns": "0.0",
                            "passing_interceptions": "0.0",
                            "receiving_receptions": "0.0",
                            "receiving_yards": "0.0",
                            "receiving_touchdowns": "0.0",
                            "rushing_long": "0.0",

                        }

                    print("Data for recieving yard leader home 3")
                    # 3
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_recieving_yard_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_recieving_yard_leader_data = self.get_data_request(
                        URL)

                    if home_recieving_yard_leader_data != 404:

                        home_recieving_yard_leader_data = home_recieving_yard_leader_data[
                            "results"][0]

                        rushing = int(self.get_field_value(
                            home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RUSHING_TOUCHDOWNS"))
                        recieving = int(self.get_field_value(
                            home_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"))
                        touchdowns = rushing + touchdowns

                        home_recieving_yard_leader_info = {
                            "name": str(home_recieving_yard_leader_data["firstName"] + " " + home_recieving_yard_leader_data["lastName"]),
                            "position": home_recieving_yard_leader_data["position"],
                            "touchdowns": str(touchdowns),
                            "passing_yards": self.get_field_value(home_recieving_yard_leader_data["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "passing_touchdowns": self.get_field_value(home_recieving_yard_leader_data["statistics"], "FOOTBALL_PASSING_TOUCHDOWNS"),
                            "recieving_yard":  self.get_field_value(home_recieving_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_YARDS"),
                            "receiving_receptions": self.get_field_value(home_recieving_yard_leader_data["statistics"],  "FOOTBALL_RECEIVING_RECEPTIONS"),

                        }
                    else:
                        home_recieving_yard_leader_data = []

                        home_recieving_yard_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "touchdowns": "0.0",
                            "passing_yards": "0.0",
                            "passing_touchdowns": "0.0",
                            "recieving_yard":  "0.0",
                            "receiving_receptions":  "0.0",

                        }

                    print("Data for receiving yard leader home 3 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_recieving_yard_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_receiving_yard_leader_data_last_year = self.get_data_request(
                        URL)

                    home_receiving_yard_leader_data_last_year = home_receiving_yard_leader_data_last_year[
                        "results"][0]

                    touchdowns = 0

                    if home_receiving_yard_leader_data_last_year != 404:

                        rushing = int(self.get_field_value(
                            home_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RUSHING_TOUCHDOWNS"))
                        recieving = int(self.get_field_value(
                            home_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"))
                        touchdowns = rushing + touchdowns

                        home_receiving_yard_leader_info_last_year = {
                            "name": str(home_receiving_yard_leader_data_last_year["firstName"] + " " + home_receiving_yard_leader_data_last_year["lastName"]),
                            "position": home_receiving_yard_leader_data_last_year["position"],
                            "touchdowns": str(touchdowns),
                            "passing_yards": self.get_field_value(home_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "passing_touchdowns": self.get_field_value(home_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_TOUCHDOWNS"),
                            "recieving_yard":  self.get_field_value(home_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_YARDS"),
                            "receiving_receptions": self.get_field_value(home_receiving_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_RECEPTIONS"),

                        }

                    else:

                        home_receiving_yard_leader_data_last_year = []

                        home_receiving_yard_leader_info_last_year = {
                            "receiving_receptions": "0.0",
                            "receiving_yard": "0.0",
                            "touchdowns": "0.0",
                            "receiving_touchdowns": "0.0",
                            "receiving_targets": "0.0",
                        }

                    print("Data for defensive sacks leader home 4")
                    # 4
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_defensive_sacks_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_defensive_sacks_leader_data = self.get_data_request(
                        URL)

                    if home_defensive_sacks_leader_data != 404:

                        home_defensive_sacks_leader_data = home_defensive_sacks_leader_data[
                            "results"][0]

                        home_defensive_sacks_leader_info = {
                            "name": str(home_defensive_sacks_leader_data["firstName"] + " " + home_defensive_sacks_leader_data["lastName"]),
                            "position": home_defensive_sacks_leader_data["position"],
                            "defensive_intercption": self.get_field_value(home_defensive_sacks_leader_data["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "defensive_sacks": self.get_field_value(home_defensive_sacks_leader_data["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "defensive_tackles": self.get_field_value(home_defensive_sacks_leader_data["statistics"], "FOOTBALL_DEFENSIVE_TACKLES")
                        }
                    else:
                        home_defensive_sacks_leader_data = []

                        home_defensive_sacks_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "defensive_intercption": "0.0",
                            "defensive_sacks": "0.0",
                            "defensive_tackles": "0.0"
                        }

                    print("Data for defensive sack leader home 4 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_defensive_sacks_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_defensive_sacks_leader_data_last_year = self.get_data_request(
                        URL)

                    if home_defensive_sacks_leader_data_last_year != 404:

                        home_defensive_sacks_leader_data_last_year = home_defensive_sacks_leader_data_last_year[
                            "results"][0]

                        home_defensive_sacks_leader_info_last_year = {
                            "defensive_sacks": self.get_field_value(home_defensive_sacks_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "tfl": self.get_field_value(home_defensive_sacks_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "defensive_interceptions": self.get_field_value(home_defensive_sacks_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),

                        }
                    else:
                        home_defensive_sacks_leader_data_last_year = []

                        home_defensive_sacks_leader_info_last_year = {
                            "defensive_sacks": "0.0",
                            "tfl": "0.0",
                            "defensive_interceptions": "0.0",

                        }

                    print("Data for defensive tackles yard leader home 5")
                    # 4
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_defensive_tackles_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_defensive_tackles_leader_data = self.get_data_request(
                        URL)

                    if home_defensive_tackles_leader_data != 404:

                        home_defensive_tackles_leader_data = home_defensive_tackles_leader_data[
                            "results"][0]

                        home_defensive_tackles_leader_info = {
                            "name": str(home_defensive_tackles_leader_data["firstName"] + " " + home_defensive_tackles_leader_data["lastName"]),
                            "position": home_defensive_tackles_leader_data["position"],
                            "defensive_intercption": self.get_field_value(home_defensive_tackles_leader_data["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "defensive_sacks": self.get_field_value(home_defensive_tackles_leader_data["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "defensive_tackles": self.get_field_value(home_defensive_tackles_leader_data["statistics"], "FOOTBALL_DEFENSIVE_TACKLES")
                        }
                    else:
                        home_defensive_tackles_leader_data = []

                        home_defensive_tackles_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "defensive_intercption": "0.0",
                            "defensive_sacks": "0.0",
                            "defensive_tackles": "0.0"
                        }

                    print("Data for defensive tackles leader home 5 last year stats")
                    # 5
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_defensive_tackles_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_defensive_tackles_leader_data_last_year = self.get_data_request(
                        URL)

                    if home_defensive_tackles_leader_data_last_year != 404:

                        home_defensive_tackles_leader_data_last_year = home_defensive_tackles_leader_data_last_year[
                            "results"][0]

                        home_defensive_tackles_leader_info_last_year = {
                            "defensive_tackles": self.get_field_value(home_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "tfl": self.get_field_value(home_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "defensive_sacks": self.get_field_value(home_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),

                        }
                    else:
                        home_defensive_tackles_leader_data_last_year = []

                        home_defensive_tackles_leader_info_last_year = {
                            "defensive_tackles": "0.0",
                            "tfl": "0.0",
                            "defensive_sacks": "0.0",

                        }

                    print("Data for defensive interceptions yard leader home 6")
                    # 6
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_defensive_interceptions_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_defensive_interception_leader_data = self.get_data_request(
                        URL)

                    if home_defensive_interception_leader_data != 404:

                        home_defensive_interception_leader_data = home_defensive_interception_leader_data[
                            "results"][0]

                        home_defensive_interceptions_leader_info_last_year = {
                            "name": str(home_defensive_interception_leader_data["firstName"] + " " + home_defensive_interception_leader_data["lastName"]),
                            "position": home_defensive_interception_leader_data["position"],
                            "defensive_intercption": self.get_field_value(home_defensive_interception_leader_data["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "defensive_sacks": self.get_field_value(home_defensive_interception_leader_data["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "defensive_tackles": self.get_field_value(home_defensive_interception_leader_data["statistics"], "FOOTBALL_DEFENSIVE_TACKLES")
                        }
                    else:
                        home_defensive_interception_leader_data = []

                        home_defensive_interceptions_leader_info_last_year = {
                            "name": "N/A",
                            "position": "N/A",
                            "defensive_intercption": "0.0",
                            "defensive_sacks": "0.0",
                            "defensive_tackles": "0.0"
                        }

                    print(
                        "Data for defensive interceptions leader home 6 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(home_defensive_interceptions_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_defensive_interceptions_leader_data_last_year = self.get_data_request(
                        URL)

                    if home_defensive_interceptions_leader_data_last_year != 404:

                        home_defensive_interceptions_leader_data_last_year = home_defensive_interceptions_leader_data_last_year[
                            "results"][0]

                        home_defensive_interceptions_leader_info_last_year = {
                            "defensive_interceptions": self.get_field_value(home_defensive_interceptions_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "tfl": self.get_field_value(home_defensive_interceptions_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "total_tackles": self.get_field_value(home_defensive_interceptions_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),

                        }
                    else:

                        home_defensive_interceptions_leader_data_last_year = []

                        home_defensive_interceptions_leader_info_last_year = {
                            "defensive_interceptions": "0.0",
                            "tfl": "0.0",
                            "total_tackles": "0.0",

                        }

                    print("Calculating total data")
                    total_passing_yard = 0
                    for passing_yard in home_player_passing_yard:
                        total_passing_yard += self.check_dict_key(
                            passing_yard, "FOOTBALL_PASSING_YARDS")

                    total_rushing_yard = 0
                    for rushing_yard in home_player_rushing_yard:
                        total_rushing_yard += self.check_dict_key(
                            rushing_yard, "FOOTBALL_RUSHING_YARDS")

                    print("Calculating total data 1")

                    home_player_passing_yard_avg_total = str(
                        str(str(round(total_passing_yard / home_total_games))) + "(" + str(total_passing_yard) + ")")
                    home_player_rushing_yard_avg_total = str(
                        str(str(round(total_rushing_yard/home_total_games))) + "(" + str(total_rushing_yard) + ")")

                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/standings.json?sport=nfl&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_points_scored_standing_data = self.get_data_request(
                        URL)

                    home_points_scored_avg = 0
                    home_points_scored_total = 0
                    home_turnovers_avg = 0
                    home_turnovers_total = 0
                    home_points_allowed_avg = 0
                    home_points_allowed_total = 0

                    print("Calculating total data 2")

                    if home_points_scored_standing_data != 404:

                        for division in home_points_scored_standing_data["results"]:
                            for team in division["teams"]:
                                if team["teamID"] == team_home_id:
                                    total_played = team["played"]
                                    home_points_scored_total = team["for"]
                                    home_points_scored_avg = round(
                                        home_points_scored_total/total_played)
                                    home_points_allowed_total = team["against"]
                                    home_points_allowed_avg = round(
                                        home_points_allowed_total/total_played)

                                    break
                            else:
                                continue
                            break
                    else:
                        home_points_scored_total = 0.0

                    print("Calculating total data 3")

                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?teamID=" + \
                        str(team_home_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_turovers_data = self.get_data_request(URL)

                    if home_turovers_data != 404:
                        for team in home_turovers_data["results"]:
                            if team["teamID"] == team_home_id:
                                home_turnovers_total += int(self.check_dict_key(team["statistics"], "FOOTBALL_RUSHING_FUMBLES_LOST")) + int(
                                    self.check_dict_key(team["statistics"], "FOOTBALL_PASSING_INTERCEPTIONS")) + int(self.check_dict_key(team["statistics"], "FOOTBALL_RECEIVING_FUMBLES_LOST"))
                                home_turnovers_avg = round(home_turnovers_total/total_played)

                    home_points_scored_final = str(
                        str(home_points_scored_avg) + "(" + str(home_points_scored_total) + ")")
                    home_turnovers_final = str(
                        str(home_turnovers_avg) + "(" + str(home_turnovers_total) + ")")
                    home_points_allowed_final = str(
                        str(home_points_allowed_avg) + "(" + str(home_points_allowed_total) + ")")

                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/standings.json?sport=nfl&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_points_scored_standing_data = self.get_data_request(
                        URL)

                    away_points_scored_avg = 0
                    away_points_scored_total = 0
                    away_turnovers_avg = 0
                    away_turnovers_total = 0
                    away_points_allowed_avg = 0
                    away_points_allowed_total = 0

                    if away_points_scored_standing_data != 404:

                        for division in away_points_scored_standing_data["results"]:
                            for team in division["teams"]:
                                if team["teamID"] == team_away_id:
                                    total_played = team["played"]
                                    away_points_scored_total = team["for"]
                                    away_points_scored_avg = round(
                                        away_points_scored_total/total_played)
                                    away_points_allowed_total = team["against"]
                                    away_points_allowed_avg = round(
                                        away_points_allowed_total/total_played)

                                    break
                            else:
                                continue
                            break
                    else:
                        away_points_scored_total = 0.0

                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?teamID=" + \
                        str(team_away_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_turovers_data = self.get_data_request(URL)

                    if away_turovers_data != 404:
                        for team in away_turovers_data["results"]:
                            if team["teamID"] == team_away_id:
                                away_turnovers_total += int(self.check_dict_key(team["statistics"], "FOOTBALL_RUSHING_FUMBLES_LOST")) + int(
                                    self.check_dict_key(team["statistics"], "FOOTBALL_PASSING_INTERCEPTIONS"))  + int(self.check_dict_key(team["statistics"], "FOOTBALL_RECEIVING_FUMBLES_LOST"))
                                away_turnovers_avg = round(
                                    away_turnovers_total/total_played)

                    away_points_scored_final = str(
                        str(away_points_scored_avg) + "(" + str(away_points_scored_total) + ")")
                    away_turnovers_final = str(
                        str(away_turnovers_avg) + "(" + str(away_turnovers_total) + ")")
                    away_points_allowed_final = str(
                        str(away_points_allowed_avg) + "(" + str(away_points_allowed_total) + ")")

                    print("AWAY TEAM PLAYER LEADERS")
                    # AWAY TEAM PLAYER LEADERS
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?teamID=" + \
                        str(team_away_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_leaders_data = self.get_data_request(URL)

                    away_player_passing_yard = []
                    away_player_rushing_yard = []
                    away_player_recieving_yard = []
                    away_player_defensive_sacks = []
                    away_player_defensive_tackles = []
                    away_player_defensive_interceptions = []

                    for leader in away_leaders_data['results']:
                        if leader["statistics"].__contains__('FOOTBALL_PASSING_YARDS'):
                            passing = {
                                "id": leader['playerID'],
                                "FOOTBALL_PASSING_YARDS": leader['statistics']['FOOTBALL_PASSING_YARDS']
                            }
                            away_player_passing_yard.append(passing)
                        if leader["statistics"].__contains__('FOOTBALL_RUSHING_YARDS'):
                            rush = {
                                "id": leader['playerID'],
                                "FOOTBALL_RUSHING_YARDS": leader['statistics']['FOOTBALL_RUSHING_YARDS']
                            }
                            away_player_rushing_yard.append(rush)
                        if leader["statistics"].__contains__('FOOTBALL_RECEIVING_YARDS'):
                            recieve = {
                                "id": leader['playerID'],
                                "FOOTBALL_RECEIVING_YARDS": leader['statistics']['FOOTBALL_RECEIVING_YARDS']
                            }
                            away_player_recieving_yard.append(recieve)
                        if leader["statistics"].__contains__('FOOTBALL_DEFENSIVE_SACKS'):
                            sacks = {
                                "id": leader['playerID'],
                                "FOOTBALL_DEFENSIVE_SACKS": leader['statistics']['FOOTBALL_DEFENSIVE_SACKS']
                            }
                            away_player_defensive_sacks.append(sacks)
                        if leader["statistics"].__contains__('FOOTBALL_DEFENSIVE_TACKLES'):
                            tackles = {
                                "id": leader['playerID'],
                                "FOOTBALL_DEFENSIVE_TACKLES": leader['statistics']['FOOTBALL_DEFENSIVE_TACKLES']
                            }
                            away_player_defensive_tackles.append(tackles)
                        if leader["statistics"].__contains__('FOOTBALL_DEFENSIVE_INTERCEPTIONS'):
                            interceptions = {
                                "id": leader['playerID'],
                                "FOOTBALL_DEFENSIVE_INTERCEPTIONS": leader['statistics']['FOOTBALL_DEFENSIVE_INTERCEPTIONS']
                            }
                            away_player_defensive_interceptions.append(
                                interceptions)

                    print("total for away team")
                    total_passing_yard = 0
                    for passing_yard in away_player_passing_yard:
                        total_passing_yard += self.check_dict_key(
                            passing_yard, "FOOTBALL_PASSING_YARDS")

                    total_rushing_yard = 0
                    for rushing_yard in away_player_rushing_yard:
                        total_rushing_yard += self.check_dict_key(
                            rushing_yard, "FOOTBALL_RUSHING_YARDS")

                    total_recieving_yard = 0
                    for recieving in away_player_recieving_yard:
                        total_recieving_yard += self.check_dict_key(
                            recieving, "FOOTBALL_RECEIVING_YARDS")

                    away_player_passing_yard_avg_total = str(
                        str(round(total_passing_yard/away_total_games, 1)) + "(" + str(total_passing_yard) + ")")
                    away_player_rushing_yard_avg_total = str(
                        str(round(total_rushing_yard/away_total_games, 1)) + "(" + str(total_rushing_yard) + ")")

                    print("Getting IDs of leaders away TEAM")
                    # Getting IDs of leaders away TEAM
                    away_passing_yard_leader_id = self.find_player_with_max_passing_yards(
                        away_player_passing_yard)
                    away_rushing_yard_leader_id = self.find_player_with_max_ruhsing_yards(
                        away_player_rushing_yard)
                    away_recieving_yard_leader_id = self.find_player_with_max_recieving_yards(
                        away_player_recieving_yard)
                    away_defensive_sacks_leader_id = self.find_player_with_max_defensive_sacks(
                        away_player_defensive_sacks)
                    away_defensive_tackles_leader_id = self.find_player_with_max_defensive_tackles(
                        away_player_defensive_tackles)
                    away_defensive_interceptions_leader_id = self.find_player_with_max_defensive_interceptions(
                        away_player_defensive_interceptions)

                    print("Data for passing yard leader away 1")
                    # Data for passing yard leader away
                    # 1
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_passing_yard_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_passing_yard_leader_data = self.get_data_request(URL)
                    away_passing_yard_leader_data = away_passing_yard_leader_data["results"][0]

                    print(away_passing_yard_leader_id)

                    if away_passing_yard_leader_data != 404:
                        away_passing_yard_leader_info = {
                            "name": str(away_passing_yard_leader_data["firstName"] + " " + away_passing_yard_leader_data["lastName"]),
                            "position": away_passing_yard_leader_data["position"],
                            "passing_yards": self.get_field_value(away_passing_yard_leader_data["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "passing_touchdowns": self.get_field_value(away_passing_yard_leader_data["statistics"],  "FOOTBALL_PASSING_TOUCHDOWNS"),
                            "passing_attempts": int(self.get_field_value(away_passing_yard_leader_data["statistics"], "FOOTBALL_PASSING_ATTEMPTS")),
                            "passing_interceptions": int(self.get_field_value(away_passing_yard_leader_data["statistics"], "FOOTBALL_PASSING_INTERCEPTIONS")),

                        }

                    else:
                        away_passing_yard_leader_data = []

                        away_passing_yard_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "passing_yards": "0.0",
                            "passing_touchdowns": "0.0",
                            "passing_attempts": "0.0",
                            "passing_interceptions": "0.0",
                        }

                    print("Data for passing yard leader away 1 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_passing_yard_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_passing_yard_leader_data_last_year = self.get_data_request(
                        URL)

                    if away_passing_yard_leader_data_last_year != 404:

                        away_passing_yard_leader_data_last_year = []

                        away_passing_yard_leader_info_last_year = {
                            "passing_yards": "0.0",
                            "completion_rate": "0.0",
                            "passing_touchdowns": "0.0",

                        }

                    print("Data for passing yard leader away 2")
                    # 2
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_rushing_yard_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_rushing_yard_leader_data = self.get_data_request(URL)

                    if away_rushing_yard_leader_data != 404:

                        away_rushing_yard_leader_data = away_rushing_yard_leader_data["results"][0]

                        rushing = int(self.get_field_value(
                            away_rushing_yard_leader_data["statistics"], "FOOTBALL_RUSHING_TOUCHDOWNS"))
                        recieving = int(self.get_field_value(
                            away_rushing_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"))
                        touchdowns = rushing + touchdowns

                        away_rushing_yard_leader_info = {
                            "name": str(away_rushing_yard_leader_data["firstName"] + " " + away_rushing_yard_leader_data["lastName"]),
                            "position": away_rushing_yard_leader_data["position"],
                            "passing_yards": self.get_field_value(away_rushing_yard_leader_data["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "rushing_touchdowns": str(touchdowns),
                            "recieving_yard":  self.get_field_value(away_rushing_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_YARDS"),
                            "rushing_yard":  self.get_field_value(away_rushing_yard_leader_data["statistics"], "FOOTBALL_RUSHING_YARDS"),
                            "rushing_long":  self.get_field_value(away_rushing_yard_leader_data["statistics"], "FOOTBALL_RUSHING_LONG"),
                        }
                    else:
                        away_rushing_yard_leader_data = []

                        away_rushing_yard_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "passing_yards": "0.0",
                            "rushing_touchdowns": "0.0",
                            "recieving_yard":  "0.0",
                            "rushing_yard":  "0.0",
                            "rushing_long":  "0.0",
                        }

                    print("Data for rushing yard leader away 2 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_rushing_yard_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_rushing_yard_leader_data_last_year = self.get_data_request(
                        URL)

                    if away_rushing_yard_leader_data_last_year != 404:

                        away_rushing_yard_leader_data_last_year = away_rushing_yard_leader_data_last_year[
                            "results"][0]

                        passing_completions = float(self.get_field_value(
                            away_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_COMPLETIONS"))
                        passing_attempts = float(self.get_field_value(
                            away_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_PASSING_ATTEMPTS"))

                        if passing_attempts != 0:
                            completion_rate = str(
                                (passing_completions / passing_attempts) * 100)
                        else:
                            completion_rate = "0.0"

                        away_rushing_yard_leader_info_last_year = {
                            "rushing_yards": self.get_field_value(away_rushing_yard_leader_data_last_year["statistics"], "FOOTBALL_RUSHING_YARDS"),
                            "completion_rate": str(completion_rate),
                            "rushing_touchdowns": self.get_field_value(away_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RUSHING_TOUCHDOWNS"),
                            "passing_interceptions": self.get_field_value(away_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_PASSING_INTERCEPTIONS"),
                            "rushing_receptions": self.get_field_value(away_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_RECEPTIONS"),
                            "receiving_yards": self.get_field_value(away_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_YARDS"),
                            "receiving_touchdowns": self.get_field_value(away_rushing_yard_leader_data_last_year["statistics"],  "FOOTBALL_RECEIVING_TOUCHDOWNS"),

                        }
                    else:
                        away_rushing_yard_leader_data_last_year = []

                        away_rushing_yard_leader_info_last_year = {
                            "rushing_yards": "0.0",
                            "completion_rate": "0.0",
                            "rushing_touchdowns": "0.0",
                            "passing_interceptions": "0.0",
                            "rushing_receptions": '0.0',
                            "receiving_yards": "0.0",
                            "receiving_touchdowns": "0.0",

                        }

                    print("Data for passing yard leader away 3")
                    # 3
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_recieving_yard_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_recieving_yard_leader_data = self.get_data_request(
                        URL)

                    if away_recieving_yard_leader_data != 404:

                        away_recieving_yard_leader_data = away_recieving_yard_leader_data[
                            "results"][0]

                        rushing = int(self.get_field_value(
                            away_recieving_yard_leader_data["statistics"], "FOOTBALL_RUSHING_TOUCHDOWNS"))
                        recieving = int(self.get_field_value(
                            away_recieving_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"))
                        touchdowns = rushing + touchdowns

                        away_recieving_yard_leader_info = {

                            "name": str(away_recieving_yard_leader_data["firstName"] + " " + away_recieving_yard_leader_data["lastName"]),
                            "position": away_recieving_yard_leader_data["position"],
                            "touchdowns": str(touchdowns),
                            "passing_yards": self.get_field_value(away_recieving_yard_leader_data["statistics"], "FOOTBALL_PASSING_YARDS"),
                            "passing_touchdowns": self.get_field_value(away_recieving_yard_leader_data["statistics"], "FOOTBALL_PASSING_TOUCHDOWNS"),
                            "recieving_yard":  self.get_field_value(away_recieving_yard_leader_data["statistics"], "FOOTBALL_RECEIVING_YARDS"),
                            "receiving_receptions": self.get_field_value(away_recieving_yard_leader_data["statistics"],  "FOOTBALL_RECEIVING_RECEPTIONS"),
                        }
                    else:
                        away_recieving_yard_leader_data = []

                        away_recieving_yard_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "passing_yards": "0.0",
                            "passing_touchdowns": "0.0",
                            "recieving_yard":  "0.0"
                        }

                    print("Data for receiving yard leader away 3 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_recieving_yard_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_receiving_yard_leader_data_last_year = self.get_data_request(
                        URL)

                    if away_receiving_yard_leader_data_last_year != 404:

                        away_receiving_yard_leader_data_last_year = away_receiving_yard_leader_data_last_year[
                            "results"][0]

                        away_receiving_yard_leader_info_last_year = {
                            "receiving_receptions": self.get_field_value(away_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_RECEPTIONS"),
                            "receiving_yards": self.get_field_value(away_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_YARDS"),
                            "receiving_touchdowns": self.get_field_value(away_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_TOUCHDOWNS"),
                            "receiving_targets": self.get_field_value(away_receiving_yard_leader_data_last_year["statistics"], "FOOTBALL_RECEIVING_TARGETS"),

                        }
                    else:
                        away_receiving_yard_leader_data_last_year = []

                        away_receiving_yard_leader_info_last_year = {
                            "receiving_receptions": "0.0",
                            "receiving_yards": "0.0",
                            "receiving_touchdowns": "0.0",
                            "receiving_targets": "0.0",

                        }

                    print("Data for passing yard leader away 4")
                    # 4
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_defensive_sacks_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_defensive_sacks_leader_data = self.get_data_request(
                        URL)

                    if away_defensive_sacks_leader_data != 404:

                        away_defensive_sacks_leader_data = away_defensive_sacks_leader_data[
                            "results"][0]

                        away_defensive_sacks_leader_info = {
                            "name": str(away_defensive_sacks_leader_data["firstName"] + " " + away_defensive_sacks_leader_data["lastName"]),
                            "position": away_defensive_sacks_leader_data["position"],
                            "defensive_intercption": self.get_field_value(away_defensive_sacks_leader_data["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "defensive_sacks": self.get_field_value(away_defensive_sacks_leader_data["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "defensive_tackles": self.get_field_value(away_defensive_sacks_leader_data["statistics"], "FOOTBALL_DEFENSIVE_TACKLES")
                        }
                    else:

                        away_defensive_sacks_leader_data = []

                        away_defensive_sacks_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "defensive_intercption": "0.0",
                            "defensive_sacks": "0.0",
                            "defensive_tackles": "0.0"
                        }

                    print("Data for defensive sacks leader away 4 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_defensive_sacks_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_defensive_sacks_leader_data_last_year = self.get_data_request(
                        URL)

                    if away_defensive_sacks_leader_data_last_year != 404:

                        away_defensive_sacks_leader_data_last_year = away_defensive_sacks_leader_data_last_year[
                            "results"][0]

                        away_defensive_sacks_leader_info_last_year = {
                            "defensive_sacks": self.get_field_value(away_defensive_sacks_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "tfl": self.get_field_value(away_defensive_sacks_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "defensive_tackles": self.get_field_value(away_defensive_sacks_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),

                        }
                    else:
                        away_defensive_sacks_leader_data_last_year = []

                        away_defensive_sacks_leader_info_last_year = {
                            "defensive_sacks": "0.0",
                            "tfl": "0.0",
                            "defensive_tackles": "0.0",

                        }

                    print("Data for defensive tackles  leader away 5")
                    # 5
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_defensive_tackles_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_defensive_tackles_leader_data = self.get_data_request(
                        URL)

                    if away_defensive_tackles_leader_data != 404:

                        away_defensive_tackles_leader_data = away_defensive_tackles_leader_data[
                            "results"][0]

                        away_defensive_tackles_leader_info = {
                            "name": str(away_defensive_tackles_leader_data["firstName"] + " " + away_defensive_tackles_leader_data["lastName"]),
                            "position": away_defensive_tackles_leader_data["position"],
                            "defensive_intercption": self.get_field_value(away_defensive_tackles_leader_data["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "defensive_sacks": away_defensive_tackles_leader_data["statistics"]["FOOTBALL_DEFENSIVE_SACKS"],
                            "defensive_tackles": self.get_field_value(away_defensive_tackles_leader_data["statistics"], "FOOTBALL_DEFENSIVE_TACKLES")
                        }
                    else:
                        away_defensive_tackles_leader_data = []

                        away_defensive_tackles_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "defensive_intercption": "0.0",
                            "defensive_sacks": "0.0",
                            "defensive_tackles": "0.0"
                        }

                    print("Data for defensive tackles leader away 5 last year stats")
                    print(away_defensive_tackles_leader_id)
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_defensive_tackles_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_defensive_tackles_leader_data_last_year = self.get_data_request(
                        URL)

                    if away_defensive_tackles_leader_data_last_year != 404:
                        away_defensive_tackles_leader_data_last_year = away_defensive_tackles_leader_data_last_year[
                            "results"][0]

                        away_defensive_tackles_leader_info_last_year = {
                            "defensive_tackles": self.get_field_value(away_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "tfl": self.get_field_value(away_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),
                            "defensive_sacks": self.get_field_value(away_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "defensive_interceptions": self.get_field_value(away_defensive_tackles_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),

                        }
                    else:
                        away_defensive_tackles_leader_data_last_year = []
                        away_defensive_tackles_leader_info_last_year = {
                            "defensive_tackles": str("0.0"),
                            "tfl": str("0.0"),
                            "defensive_sacks": str("0.0"),
                            "defensive_interceptions": str("0.0"),

                        }

                    print("Data for defensive interceptions yard leader away 6")
                    # 6
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_defensive_interceptions_leader_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_defensive_interception_leader_data = self.get_data_request(
                        URL)

                    if away_defensive_interception_leader_data != 404:

                        away_defensive_interception_leader_data = away_defensive_interception_leader_data[
                            "results"][0]

                        away_defensive_interceptions_leader_info = {
                            "name": str(away_defensive_interception_leader_data["firstName"] + " " + away_defensive_interception_leader_data["lastName"]),
                            "position": away_defensive_interception_leader_data["position"],
                            "defensive_intercption": self.get_field_value(away_defensive_interception_leader_data["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "defensive_sacks": self.get_field_value(away_defensive_interception_leader_data["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "defensive_tackles": self.get_field_value(away_defensive_interception_leader_data["statistics"], "FOOTBALL_DEFENSIVE_TACKLES")
                        }
                    else:
                        away_defensive_interception_leader_data = []

                        away_defensive_interceptions_leader_info = {
                            "name": "N/A",
                            "position": "N/A",
                            "defensive_intercption": "0.0",
                            "defensive_sacks": "0.0",
                            "defensive_tackles": "0.0"
                        }

                    print(
                        "Data for defensive interceptions leader away 6 last year stats")
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/statistics.json?playerID=" + \
                        str(away_defensive_interceptions_leader_id) + "&season=" + str(SEASON) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_defensive_interceptions_leader_data_last_year = self.get_data_request(
                        URL)

                    if away_defensive_interceptions_leader_data_last_year != 404:

                        away_defensive_interceptions_leader_data_last_year = away_defensive_interceptions_leader_data_last_year[
                            "results"][0]

                        away_defensive_interceptions_leader_info_last_year = {
                            "defensive_interceptions": self.get_field_value(away_defensive_interceptions_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_INTERCEPTIONS"),
                            "passes": self.get_field_value(away_defensive_interceptions_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_SACKS"),
                            "total_tackles": self.get_field_value(away_defensive_interceptions_leader_data_last_year["statistics"], "FOOTBALL_DEFENSIVE_TACKLES"),

                        }

                    else:
                        away_defensive_interceptions_leader_data_last_year = []
                        away_defensive_interceptions_leader_info_last_year = {
                            "defensive_interceptions": "0.0",
                            "passes": "0.0",
                            "total_tackles": "0.0",

                        }

                    print("injuries data")
                    injuries_data_home = []

                    # injuries data home players
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/injuries.json?teamID=" + \
                        str(team_home_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    home_injuries_data = self.get_data_request(URL)

                    for injury in home_injuries_data['results']:
                        if injury["injury"].__contains__('location'):
                            data = {
                                "name": str(injury["firstName"] + " " + injury["lastName"]),
                                "position": injury["position"],
                                "status": injury["injury"]["status"],
                                "injury": injury["injury"]["location"],
                            }

                            injuries_data_home.append(data)
                        else:
                            data = {
                                "name": str(injury["firstName"] + " " + injury["lastName"]),
                                "position": injury["position"],
                                "status": injury["injury"]["status"],
                                "injury": "-",
                            }

                            injuries_data_home.append(data)

                    injuries_data_away = []

                    print("injuries data 1")

                    print("injuries data home players")
                    # injuries data home players
                    URL = "https://sportsinformationtraders.api.areyouwatchingthis.com/api/injuries.json?teamID=" + \
                        str(team_away_id) + "&apiKey=" + \
                        self.ODDS_METABET_API_KEY
                    away_injuries_data = self.get_data_request(URL)

                    for injury in away_injuries_data['results']:

                        if injury["injury"].__contains__('location'):
                            data = {
                                "name": str(injury["firstName"] + " " + injury["lastName"]),
                                "position": injury["position"],
                                "status": injury["injury"]["status"],
                                "injury": injury["injury"]["location"],
                            }
                            injuries_data_away.append(data)
                        else:
                            data = {
                                "name": str(injury["firstName"] + " " + injury["lastName"]),
                                "position": injury["position"],
                                "status": injury["injury"]["status"],
                                "injury": "-",
                            }
                            injuries_data_away.append(data)

                    # Calculating predicted score
                    print("Calculating predicted score")
                    favorite_predicted_score = (
                        overUnder_odds / 2) + spread_odd
                    underdog_predicted_score = overUnder_odds - favorite_predicted_score

                    print("FINAL game data dictionary")
                    #

                    underdog_spread_odds_value = ""
                    if underdog_spread_odds > 0:
                        underdog_spread_odds_value = "+" + \
                            str(underdog_spread_odds)
                    else:
                        underdog_spread_odds_value = "-" + \
                            str(abs(underdog_spread_odds))

                    spread_odds_value = ""
                    if spread_odd > 0:
                        spread_odds_value = "+" + \
                            str(spread_odd)
                    else:
                        spread_odds_value = "-" + str(abs(spread_odd))

                    spread_pick_value = ""
                    spread_pick = -1 * spread_odd
                    if spread_pick > 0:
                        spread_pick_value = "+" + str(spread_pick)
                    else:
                        spread_pick_value = "-" + str(abs(spread_pick))

                    game_data = {
                        "Match": team_home + ' vs ' + team_away,
                        "Game Day": game_date,
                        "Game Time": game_time,
                        "Game broadcast": game_broadcast,
                        "game_day_name": game_day_name,
                        "game_day_num": game_day_num,
                        "game_month_name": game_month_name,
                        "game_year": game_year,
                        "Arena": game_arena,
                        "Team 1 (T1)": team_home,

                        "favorite_team_name": favorite_team_name,
                        "underdog_team_name": underdog_team_name,
                        "spread_odd": spread_odds_value,
                        "spread_pick": spread_pick_value,
                        "favorite_spread_odds": favorite_spread_odds,
                        "underdog_spread_odds": underdog_spread_odds_value,
                        "overUnder_odds": overUnder_odds,
                        "overUnderLineOver_odds": overUnderLineOver_odds,
                        "overUnderLineUnder_odds": overUnderLineUnder_odds,

                        "favorite_predicted_score": favorite_predicted_score,
                        "underdog_predicted_score": underdog_predicted_score,

                        "Team 1 (T1) passing yard leader": home_passing_yard_leader_info,
                        "Team 1 (T1) rushing yard leader": home_rushing_yard_leader_info,
                        "Team 1 (T1) receiving yard leader": home_recieving_yard_leader_info,
                        "Team 1 (T1) defensive sack leader": home_defensive_sacks_leader_info,
                        "Team 1 (T1) defensive tackles leader": home_defensive_tackles_leader_info,

                        "Team 1 (T1) passing yard leader last year": home_passing_yard_leader_info_last_year,
                        "Team 1 (T1) rushing yard leader last year": home_rushing_yard_leader_info_last_year,
                        "Team 1 (T1) receiving yard leader last year": home_receiving_yard_leader_info_last_year,
                        "Team 1 (T1) defensive sack leader last year": home_defensive_sacks_leader_info_last_year,
                        "Team 1 (T1) defensive tackles leader last year": home_defensive_tackles_leader_info_last_year,
                        "Team 1 (T1) defensive interceptions leader last year": home_defensive_interceptions_leader_info_last_year,

                        "Team 2 (T2) passing yard leader last year": away_passing_yard_leader_info_last_year,
                        "Team 2 (T2) rushing yard leader last year": away_rushing_yard_leader_info_last_year,
                        "Team 2 (T2) receiving yard leader last year": away_receiving_yard_leader_info_last_year,
                        "Team 2 (T2) defensive sack leader last year": away_defensive_sacks_leader_info_last_year,
                        "Team 2 (T2) defensive tackles leader last year": away_defensive_tackles_leader_info_last_year,
                        "Team 2 (T2) defensive interceptions leader last year": away_defensive_interceptions_leader_info_last_year,

                        "Team 2 (T2) passing yard leader": away_passing_yard_leader_info,
                        "Team 2 (T2) rushing yard leader": away_rushing_yard_leader_info,
                        "Team 2 (T2) receiving yard leader": away_recieving_yard_leader_info,
                        "Team 2 (T2) defensive sack leader": away_defensive_sacks_leader_info,
                        "Team 2 (T2) defensive tackles leader": away_defensive_tackles_leader_info,
                        "Team 2 (T2) defensive interception leader": away_defensive_interceptions_leader_info,

                        "Team 1 (T1) injuries": injuries_data_home,
                        "Team 1 (T1) wins": home_wins,
                        "Team 1 (T1) losses": home_losses,
                        "Team 1 (T1) ties": home_ties,
                        "Team 2 (T2)": team_away,

                        "Team 1 (T1) passing yard": home_player_passing_yard_avg_total,
                        "Team 1 (T1) rushing yard": home_player_rushing_yard_avg_total,
                        "Team 1 (T1) receiving yard": home_points_scored_final,
                        "Team 1 (T1) defensive sacks": home_turnovers_final,
                        "Team 1 (T1) defensive interceptions": home_points_allowed_final,

                        "Team 2 (T2) passing yard": away_player_passing_yard_avg_total,
                        "Team 2 (T2) rushing yard": away_player_rushing_yard_avg_total,
                        "Team 2 (T2) receiving yard": away_points_scored_final,
                        "Team 2 (T2) defensive sacks": away_turnovers_final,
                        "Team 2 (T2) defensive interceptions": away_points_allowed_final,

                        "Team 2 (T2) wins": away_wins,
                        "Team 2 (T2) losses": away_losses,
                        "Team 2 (T2) ties": away_ties,

                        "Team 2 (T2) injuries": injuries_data_away,

                    }

                    games_data_article.append(game_data)
                    self.offline_html(game_data)
                    print("Article Written  one \n\n")

                except Exception as E:
                    print("Error: ", E)
                    
                    continue

            print("Article Written \n\n")

        try:
            shutil.make_archive(SAVEDIRPATH+"/NFL", 'zip', SAVEDIRPATH+"/NFL")
            print("Success Online!")
        except:
            shutil.make_archive(SAVEDIRPATH+"/NFL",'zip', SAVEDIRPATH+"/NFL")
            print("Success Offline!")


def generate_articles_html():
    print("Job is running at:", datetime.now(pakistan_timezone))
    logging.info('Job executed: generate_articles_html')
    betpick = Betpicks()

    nfl = NFL_Article()

    try:
        nfl.nfl_main()
    except Exception:
        print("***** EXCEPTION IN NFL *****")
        pass



if __name__ == '__main__':
    betpick = Betpicks()

    scheduler = BackgroundScheduler()
    pakistan_timezone = pytz.timezone('Asia/Karachi')

    # Print the current time before starting the scheduler
    print("Current time in 'Asia/Karachi' timezone:", datetime.now(pakistan_timezone))
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    print("Current time in 'UTC' timezone:", utc_now)

    scheduler.add_job(
        generate_articles_html,
        trigger=CronTrigger(day_of_week=3, hour=10, minute=42),
        timezone=pakistan_timezone
    )

    # Start the scheduler
    scheduler.start()

    print("scheduler started")

    # Keep the program running
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # Shut down the scheduler gracefully when the program is terminated
        logging.info('Program terminated. Shutting down scheduler.')
        scheduler.shutdown()

   