#from ig import igdb
#from igdb_api_python import igdb
from igdb_api_python.igdb import igdb as igdb
from datetime import datetime
import time, os
import sqlite3
import requests
import json
import sys
import secrets
import math
import plotly.plotly as py
import plotly.graph_objs as go

def get_datetime():
    now = time.strftime("%a %b %d %H:%M:%S %Y")
    time.sleep(5)
    soon = time.strftime("%a %b %d %H:%M:%S %Y")
    tdelta = datetime.strptime(now, '%a %b %d %H:%M:%S %Y') - datetime.strptime(soon, '%a %b %d %H:%M:%S %Y')
    print(tdelta.total_seconds())
    # timestamp2 = "Jan 27 11:52:02 2014"
    #
    # t1 = datetime.strptime(timestamp1, "%b %d %H:%M:%S %Y")
    # t2 = datetime.strptime(timestamp2, "%b %d %H:%M:%S %Y")
    #
    # difference = t1 - t2
    #
    # print(difference.days) # 380, in this case
    #
    # latest = max((t1, t2)) # t1, in this case



#ENTER YOUR KEY HERE

API_KEY = secrets.API_KEY

igdb = igdb(API_KEY)

#DB starts
DBNAME = 'game.db'
#CACHE_FNAME
games_cache_2013 = '2013games.json'
games_cache_2014 = '2014games.json'
games_cache_2015 = '2015games.json'
games_cache_2016 = '2016games.json'
games_cache_2017 = '2017games.json'
genre_cache = 'genre.json'
platform_cache = 'platform.json'
CACHE_FNAME = "cache.json"


### Set up CACHE
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()


# if there was no file, no worries. There will be soon!
except Exception as e:

    CACHE_DICTION = {}


######### API Functions #########

### Calls API For games by release year


#### note: This API free to use, with 3k regular requests a month
#### This Function uses "expander" calls which free users only get 100 per month, use sparingly!
def get_games_by_releaseYear(releaseYear):
    print("getting game data...")

    result = igdb.release_dates({
        'filters' :{
            "[y][eq]"    : releaseYear,

        },
        'expand': ["game", "platform"],
        'order':"date:desc",
        'fields': ["game.name", "game.genres", "game.esrb", "platform.name", "m"],
        'scroll':1,
        'limit':50
    })

    list_of_games = []
    xcount = result.headers["X-Count"]
    timestoscroll = (math.ceil((int(xcount)) / 50)) - 1
    for x in range(timestoscroll):
        for y in result.body:
            empty_dict = {}
            game = y["game"]
            platform = y["platform"]
            try:
                empty_dict["id"] = game["id"]
            except:
                empty_dict["id"] = ""
            try:
                empty_dict["name"] = game["name"]
            except:
                empty_dict["name"] = ""
            try:
                empty_dict["genres"] = game["genres"]
            except:
                empty_dict["genres"] =""
            try:
                esrb = game["esrb"]
                empty_dict["rating"] = esrb["rating"]
            except:
                empty_dict["rating"] = ""
            try:
                empty_dict["platform"] = platform["name"]
            except:
                empty_dict["platform"] = ""
            try:
                empty_dict["releaseMonth"] = y["m"]
            except:
                empty_dict["releaseMonth"] = ""
            empty_dict["releaseYear"] = releaseYear
            list_of_games.append(empty_dict)
        result = igdb.scroll(result)

    # loaded_json = json.loads(newresult.text)
    dumped_json = json.dumps(list_of_games, indent = 4)
    games_cache = str(releaseYear) + "games.json"
    fw = open(games_cache,"a")
    fw.write(dumped_json)
    fw.close()
    CACHE_DICTION["game_released_in_" + str(releaseYear)] = time.strftime("%a %b %d %H:%M:%S %Y")
    dumped_json = json.dumps(CACHE_DICTION, indent = 4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json)
    fw.close()


#### Genre API function
def get_genres():
    print("getting genre data...")
    result = igdb.genres({ #there are only 20 genres

        'fields': "name",
        'limit':20
    })

    list_of_genres = []
    # xcount = result.headers["X-Count"]
    # print(xcount)
    # timestoscroll = (math.ceil((int(xcount)) / 20)) - 1
    # print(timestoscroll)
    for x in result.body:
        empty_dict = {}
        try:

            empty_dict["id"] = x["id"]
        except:
            empty_dict["id"] = ""
        try:
            empty_dict["name"] = x["name"]
        except:
            empty_dict["name"] = ""
        list_of_genres.append(empty_dict)


    # loaded_json = json.loads(newresult.text)
    dumped_json = json.dumps(list_of_genres, indent = 4)
    fw = open(genre_cache,"w")
    fw.write(dumped_json)
    fw.close()
    CACHE_DICTION["genre"] = time.strftime("%a %b %d %H:%M:%S %Y")
    dumped_json = json.dumps(CACHE_DICTION, indent = 4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json)
    fw.close()

#### Platform API Function
def get_platform_info():
    print("Getting Platform Data...")

    result = igdb.platforms({
        'fields':["name", "id", "summary", "alternative_name", "generation"],
        'scroll':1,
        'limit':50
    })
    list_of_platforms = []
    xcount = result.headers["X-Count"]
    timestoscroll = (math.ceil((int(xcount)) / 50)) - 1
    for x in range(timestoscroll):
        for y in result.body:
            empty_dict = {}
            try:
                empty_dict["id"] = y["id"]
            except:
                empty_dict["id"] = ""
            try:
                empty_dict["name"] = y["name"]
            except:
                empty_dict["name"] = ""
            try:
                empty_dict["alternative_name"] = y["alternative_name"]
            except:
                empty_dict["alternative_name"] = ""
            try:
                empty_dict["generation"] = y["generation"]
            except:
                empty_dict["generation"] = ""
            try:
                empty_dict["summary"] = y["summary"]
            except:
                empty_dict["summary"] = ""
            list_of_platforms.append(empty_dict)
        result = igdb.scroll(result)
    # loaded_json = json.loads(newresult.text)
    dumped_json = json.dumps(list_of_platforms, indent = 4)
    fw = open(platform_cache,"w")
    fw.write(dumped_json)
    fw.close()
    CACHE_DICTION["platform_time"] = time.strftime("%a %b %d %H:%M:%S %Y")
    dumped_json = json.dumps(CACHE_DICTION, indent = 4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json)
    fw.close()

#if platform cache time stamp is older than 6 months, return True value to get data again
def is_platform_cache_old():
    print("checking cache...")
    now = time.strftime("%a %b %d %H:%M:%S %Y")
    tdelta = datetime.strptime(now, '%a %b %d %H:%M:%S %Y') - datetime.strptime(CACHE_DICTION["platform_time"], '%a %b %d %H:%M:%S %Y')
    if tdelta.total_seconds > 15552000:
        return True
    else:
        return False



###### Database creation functions ######

### Create Database with necessary Tables
def init_db():
    #code to create a new database goes here
    #handle exception if connection fails by printing the error

    try:
        conn = sqlite3.connect("game.db")
        cur = conn.cursor()
    except Exception as e:
        print(e)



    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'Platforms';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        DROP TABLE IF EXISTS 'ESRB';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        DROP TABLE IF EXISTS 'Genres';
    '''
    cur.execute(statement)
    conn.commit()

    statement = ' CREATE TABLE `Games` ( '
    statement += '   `Id`        INTEGER UNIQUE PRIMARY KEY,'
    statement += '   `Name`  TEXT,'
    statement += '  `Genre1`    TEXT,'
    statement += '  `Genre2`    TEXT,'
    statement += '  `Genre3`    TEXT,'
    statement += '  `ReleaseMonth`  Integer ,'
    statement += '  `ReleaseYear`  TEXT ,'
    statement += '  `Platform`  TEXT ,'
    statement += '  `Rating`    Text );'



    try:
        cur.execute(statement)
        conn.commit()
    except:
        # print('Table Exists. Delete? y/n')
        # while True:
        #     decision = input()
        #
        #     if decision == "y":
        #         dropstatement = ' DROP TABLE `Tweets` '
        #         cur.execute(dropstatement)
        #         cur.execute(statement)
        #         conn.commit()
        #         break
        #     elif decision == 'n':
        #         break
        #     else:
        #         pass
        pass


    statement = ' CREATE TABLE `Platforms` ( '
    statement += '   `Id`        INTEGER UNIQUE PRIMARY KEY,'
    statement += '   `Name`  TEXT,'
    statement += '  `AlternativeName`    TEXT,'
    statement += '  `ConsoleGeneration`  TEXT ,'
    statement += '  `Summary`    TEXT );'
    try:
        cur.execute(statement)
        conn.commit()
    except:
        pass

    statement = ' CREATE TABLE `Genre` ( '
    statement += '   `Id`        INTEGER UNIQUE PRIMARY KEY,'
    statement += '   `Name`  TEXT);'

    try:
        cur.execute(statement)
        conn.commit()
    except:
        pass

    statement = ' CREATE TABLE `ESRB` ( '
    statement += '   `Id`        INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,'
    statement += '   `Rating`  TEXT);'
    try:
        cur.execute(statement)
        conn.commit()
    except:
        pass


    #close database connection
    conn.close()

### Adds ESRB Data to DB
def add_esrb_ratings():
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()

    esrb_ratings = ["RP", "EC", "E", "E10+", "T", "M", "AO"]
    for x in range(7):
        try:
            cur.execute(' INSERT INTO `ESRB` (Rating) VALUES ("{}")'.format(esrb_ratings[x]))
        except Exception as ex:
            print(ex)
            pass #bandaid for repeat Tweets
    conn.commit()
    conn.close()

### Adds Genre Data to DB
def add_genre_data():
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()

    with open(genre_cache) as json_data:
        g = json.load(json_data)

        for genre in g:
            params = (genre["id"], genre["name"])

            try:
                cur.execute(" INSERT INTO `Genre` (Id, Name) VALUES (?, ?)", params)

            except Exception as ex:

                pass #bandaid for repeat Tweets
        conn.commit()
    conn.close()

### Adds Game Data to DB
def add_games_data():
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()


    ### Add countries data first
    for x in ['2013games.json', '2014games.json', '2015games.json', '2016games.json', '2017games.json' ]:

        with open(x) as json_data:
            g = json.load(json_data)


        for game in g:
            list_of_genres = []
            for x in range(3):
                try:
                    list_of_genres.append(game["genres"][x])
                except:
                    list_of_genres.append("")

            #Add code to insert each of these data of interest to the games table
            params= (game["id"], game["name"], list_of_genres[0], list_of_genres[1], list_of_genres[2], game["releaseMonth"], game["releaseYear"], game["platform"], game["rating"] )
            try:
                cur.execute(" INSERT INTO `Games` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

            except Exception as ex:

                pass #bandaid for repeat Tweets
        conn.commit()
    conn.close()

### Adds Platform Data to DB
def add_platform_data():
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()


    ### Add countries data first
    with open(platform_cache) as json_data:
        g = json.load(json_data)


    for console in g:


        #Add code to insert each of these data of interest to the games table
        params= (console["id"], console["name"], console["alternative_name"], console["generation"], console["summary"] )
        try:
            cur.execute(" INSERT INTO `Platforms` VALUES (?, ?, ?, ?, ?)", params)

        except:
            pass
             #bandaid for repeat Tweets
    conn.commit()
    conn.close()
#### Updates Games Table for Genre names
def update_genres():

    conn = sqlite3.connect('game.db')
    cur = conn.cursor()

    statement = " UPDATE `Games` SET `Genre1` = (SELECT Genre.Name From Genre where Genre.Id = Games.Genre1) "
    cur.execute(statement)
    statement = " UPDATE `Games` SET `Genre2` = (SELECT Genre.Name From Genre where Genre.Id = Games.Genre2) "
    cur.execute(statement)
    statement = " UPDATE `Games` SET `Genre3` = (SELECT Genre.Name From Genre where Genre.Id = Games.Genre3) "
    cur.execute(statement)
    conn.commit()
    conn.close()
### Update Games Table for Ratings
def update_ratings():
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()

    statement = " UPDATE `Games` SET `Rating` = (SELECT ESRB.Rating From ESRB where ESRB.Id = Games.Rating) "
    cur.execute(statement)
    conn.commit()


##### SQL Query Functions ######


###### Counts Releases by Rating
def query_ratingCounts(releaseYear = None):
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()
    rating_list =[]
    rating_list_count = []

    if releaseYear is None:
        statement = "Select Rating, Count(*) From Games "
        statement += " GROUP BY Rating "
        statement += " Having Count(*) > 30 AND Rating NOT Null"
        cur.execute(statement)
        for x in cur:
            rating_list.append(x[0])
            rating_list_count.append(x[1])
    else:
        statement = "Select Rating, Count(*) From Games "
        statement += " GROUP BY Rating, ReleaseYear "
        statement += " Having ReleaseYear = {} AND Count(*) > 30  AND Rating Not Null".format(releaseYear)
        cur.execute(statement)
        for x in cur:
            rating_list.append(x[0])
            rating_list_count.append(x[1])
    combined_list = [rating_list, rating_list_count]

    return combined_list

##### Counts Releases by Platform
def query_platformCounts(releaseYear = None):
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()
    platform_list =[]
    platform_list_count = []

    if releaseYear is None:
        statement = "Select Platform, Count(Platform) From Games "
        statement += " GROUP BY Platform "
        statement += " Having Count(Platform) > 30 Order by Count(Platform) DESC"
        cur.execute(statement)
        for x in cur:
            platform_list.append(x[0])
            platform_list_count.append(x[1])
    else:
        statement = "Select Platform, Count(Platform) From Games "
        statement += " GROUP BY Platform, ReleaseYear "
        statement += " Having ReleaseYear = {} AND Count(Platform) > 30 Order by Count(Platform) DESC".format(releaseYear)
        cur.execute(statement)
        for x in cur:
            platform_list.append(x[0])
            platform_list_count.append(x[1])
    combined_list = [platform_list, platform_list_count]
    return combined_list

##### Counts Releases by Genre
def query_genreCounts(releaseYear = None):
    # Connect to choc database
    conn = sqlite3.connect('game.db')
    cur = conn.cursor()
    genre_dictionary = {}

    if releaseYear is None:
        statement = "Select Count(Games.Genre1), Genre.Name "
        statement += " From Genre Join Games on Genre.Name = Games.Genre1 "
        statement += " Group By Genre.Name Order By Genre.Name Desc"
        cur.execute(statement)
        for x in cur:
            genre = x[0]
            count = x[1]
            genre_dictionary[genre] = count

        statement = "Select Count(Games.Genre2), Genre.Name "
        statement += " From Genre Join Games on Genre.Name = Games.Genre2 "
        statement += " Group By Genre.Name Order By Genre.Name Desc"
        cur.execute(statement)
        for x in cur:
            if x[1] not in genre_dictionary:
                genre_dictionary[x[1]] = x[0]
                continue
            genre = x[1]
            count = x[0] + genre_dictionary[genre]
            genre_dictionary[genre] = count
        statement = "Select Count(Games.Genre3), Genre.Name "
        statement += " From Genre Join Games on Genre.Name = Games.Genre3 "
        statement += " Group By Genre.Name Order By Genre.Name Desc"
        cur.execute(statement)
        for x in cur:
            if x[1] not in genre_dictionary:
                genre_dictionary[x[1]] = x[0]
                continue
            genre = x[1]
            count = x[0] + genre_dictionary[genre]
            genre_dictionary[genre] = count
    else:

        statement = "Select Count(Games.Genre1), Genre.Name "
        statement += " From Genre Join Games on Genre.Name = Games.Genre1 "
        statement += " Group By Genre.Name, Games.ReleaseYear Having Games.ReleaseYear = {} Order By Genre.Name Desc".format(releaseYear)
        cur.execute(statement)
        for x in cur:
            genre = x[0]
            count = x[1]
            genre_dictionary[genre] = count

        statement = "Select Count(Games.Genre2), Genre.Name "
        statement += " From Genre Join Games on Genre.Name = Games.Genre2 "
        statement += " Group By Genre.Name, Games.ReleaseYear Having Games.ReleaseYear = {} Order By Genre.Name Desc".format(releaseYear)
        cur.execute(statement)
        for x in cur:
            if x[1] not in genre_dictionary:
                genre_dictionary[x[1]] = x[0]
                continue
            genre = x[1]
            count = x[0] + genre_dictionary[genre]
            genre_dictionary[genre] = count
        statement = "Select Count(Games.Genre3), Genre.Name "
        statement += " From Genre Join Games on Genre.Name = Games.Genre3 "
        statement += " Group By Genre.Name, Games.ReleaseYear Having Games.ReleaseYear = {} Order By Genre.Name Desc".format(releaseYear)
        cur.execute(statement)
        for x in cur:
            if x[1] not in genre_dictionary:
                genre_dictionary[x[1]] = x[0]
                continue
            genre = x[1]
            count = x[0] + genre_dictionary[genre]
            genre_dictionary[genre] = count


    list_names =[]
    list_vals = []
    for k,v in genre_dictionary.items():
        list_names.append(k)
        list_vals.append(v)
    combined_list = [list_names, list_vals]


    return combined_list

##### Counts Releases in General
def query_releaseCounts(releaseYear = None, platform = False):
        conn = sqlite3.connect('game.db')
        cur = conn.cursor()
        list_of_monthly_releases = []

        if not platform: #if we're not doing a query by platform
            if releaseYear is None:
                for x in range(12):

                    statement = "Select Count(Name) From Games Where ReleaseMonth = {}".format(str(x + 1))
                    cur.execute(statement)
                    for x in cur:
                        list_of_monthly_releases.append(x[0])
            else:
                for x in range(12):

                    statement = "Select Count(Name) From Games Where ReleaseYear = {} and ReleaseMonth = {}".format(releaseYear, str(x + 1))
                    cur.execute(statement)
                    for x in cur:
                        list_of_monthly_releases.append(x[0])


        else: # if we're doing a query by platform
            if releaseYear is None:
                for x in range(12):

                    statement = "SELECT Platform, ReleaseMonth, Count(*) From Games "
                    statement += " Group By Platform, ReleaseYear, ReleaseMonth "
                    statement += " Having ReleaseYear = {} and Count(*) >3 and ReleaseMonth = {}".format(releaseYear, str(x + 1))
                    cur.execute(statement)
                    for x in cur:
                        list_of_monthly_releases.append(x[0])
            else:

                for x in range(12):

                    statement = "SELECT Platform, ReleaseMonth, Count(*) From Games "
                    statement += " Group By Platform, ReleaseYear, ReleaseMonth "
                    statement += " Having ReleaseYear = {} and Count(*) >3 and ReleaseMonth = {}".format(releaseYear, str(x + 1))
                    cur.execute(statement)
                    for x in cur:
                        list_of_monthly_releases.append(x[0])



        return list_of_monthly_releases



######## Plotly Functions #########

#### Plots pie chart data
def plot_pie_chart(pie_data):

    platform_names = pie_data[0]
    platform_counts = pie_data[1]
    data = [ dict(
            type = 'pie',

            values = platform_counts,
            labels = platform_names,
            textinfo = "percent",
            textposition = "outside",

            hoverlabel = {
                        "namelength": 15,
                        "font": {
                                "family" : "Arial",
                                "size": 13
                        }
            },


            opacity = 1,
    )]
    layout = [ dict(

            title = '2017 Releases by Platform',
            titlefont = {
                        "family": "Open Sans",
                        "size": 17,
                        "color": "#000000"
            },
            calendar = "gregorian",

            margin = {
                    "l": 80,
                    "r": 80,
                    "t": 100,
                    "b": 80,
                    "pad": 0,
                    "autoexpand": "true"

            },
            autosize = "true",
            hoverlabel = {
                        "namelength": 15,
                        "font": {
                                "family" : "Arial",
                                "size": 13
                        }
            },

    )]
    fig = dict( data=data, layout=layout )
    py.plot( fig, validate=False, filename='2017 Releases' )

#### plots line chart data
def plot_line_data(list_of_monthly_releases):

    data = [ dict(
            type = 'scatter',

            mode = 'lines',
            x = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            y = list_of_monthly_releases,
            xcalender = "gregorian",
            ycalender = "gregorian",
            hoverlabel = {
                        "namelength": 15,
                        "font": {
                                "family" : "Arial",
                                "size": 13
                        }
            },
            hoveron = 'points',
            hoverinfo = "x+y+z+text",
            opacity = 1,
    )]
    layout = [ dict(
            font = {
                    "family": "Verdana",
                    "size": 12,
                    "color": "#444",
            },
            title = '2017 Releases by Month',
            titlefont = {
                        "family": "Open Sans",
                        "size": 17,
                        "color": "#000000"
            },
            calendar = "gregorian",
            hoverdistance = 20,
            spikedistance = 20,
            width = 1000,
            height = 570,
            margin = {
                    "l": 80,
                    "r": 80,
                    "t": 100,
                    "b": 80,
                    "pad": 0,
                    "autoexpand": "true"

            },
            xaxis = {
                    "type": "category",
                    "visible": "true",
                    "autorange": "true",
                    "rangemode": "normal",
                    "range": [0,11],
                    "categoryorder": "trace",
                    "color": "#444",
                    "tickmode": "auto",
                    "nticks": 0,
                    "showticklabels": "true",
                    "tickangle": "true",
                    "gridwidth": 1,
                    "showgrid": "false",
                    "anchor": "y",
                    "side": "bottom",
                    "domain": [0,1],
                    "constrain": "range",
                    "constraintoward": "center",
                    "tick0": 0,
                    "dtick": 1
            },
            yaxis = {
                    "type": "linear",
                    "title": "# of Releases",
                    "visible": "true",
                    "autorange": "true",
                    "rangemode": "normal",
                    "color": "#444",
                    "tickmode": "auto",
                    "nticks": 0,
                    "showticklabels": "true",
                    "tickangle": "true",
                    "gridwidth": 1,
                    "showgrid": "false",
                    "anchor": "x",
                    "side": "left",
                    "domain": [0,1],
                    "constrain": "range",
                    "constraintoward": "center",
                    "tick0": 0,
                    "dtick": 20
            },
            autosize = "true",
            hoverlabel = {
                        "namelength": 15,
                        "font": {
                                "family" : "Arial",
                                "size": 13
                        }
            },

    )]

    fig = dict( data=data, layout=layout )
    py.plot( fig, validate=False, filename='2017 Releases' )




### Classes for Plotly Output ######

##### Class for Line Chart
class LineChart():
    def __init__(self, releaseYear = None):
        self.releaseYear = releaseYear
        if self.releaseYear == "allyears":
            list_of_monthly_releases = query_releaseCounts()

            plot_line_data(list_of_monthly_releases)
        else:
            list_of_monthly_releases = query_releaseCounts(self.releaseYear)

            plot_line_data(list_of_monthly_releases)

###Class for Platform Line Charts
class PlatformChart(LineChart):
    def __init__(self, platform = True, releaseYear = None):
        self.platform = platform

        self.releaseYear = releaseYear
        if self.releaseYear == "allyears":
            list_of_monthly_releases = query_releaseCounts()
            plot_line_data(list_of_monthly_releases)
        else:
            list_of_monthly_releases = query_releaseCounts(self.platform)
            plot_line_data(list_of_monthly_releases)

#### Class for Pie Charts
class PieChart():
        def __init__(self, releaseYear = None):
            self.releaseYear = releaseYear
            if self.releaseYear == "allyears":
                list_of_releases = query_platformCounts()

                plot_pie_chart(list_of_releases)
            else:
                list_of_releases = query_platformCounts(self.releaseYear)
                plot_pie_chart(list_of_releases)

##### Class for Genre Plotly Chart
class GenreChart(PieChart):
    def __init__(self, releaseYear = None):

        self.releaseYear = releaseYear
        if self.releaseYear == "allyears":
            list_of_genre_releases = query_genreCounts()
            plot_pie_chart(list_of_genre_releases)
        else:
            list_of_genre_releases = query_genreCounts(self.releaseYear)
            plot_pie_chart(list_of_genre_releases)

##### Class for Rating Plotly chart
class RatingChart(PieChart):
    def __init__(self, releaseYear = None):

        self.releaseYear = releaseYear
        if self.releaseYear == "allyears":
            list_of_rating_releases = query_ratingCounts()
            plot_pie_chart(list_of_rating_releases)
        else:
            list_of_rating_releases = query_ratingCounts(self.releaseYear)
            plot_pie_chart(list_of_rating_releases)





####### interactive_prompt helper functions #######

#### Cleans up database
def clean_db():

    init_db()
    add_games_data()
    add_genre_data()
    add_platform_data()
    add_esrb_ratings()
    update_genres()
    update_ratings()

### Runs at program start, checks if database is bad or old
def data_checking():
    try:
        if "platform_time" in CACHE_DICTION:  #does the cache entry for platform exist?
            pass
            # if is_platform_cache_old(): # is the cache entry old?
            #     # get_platform_info()
            #     pass
            # else:
            #     print("but here")
            #     pass
        else:
            print("WOW")
            # get_platform_info()
    except Exception as e:
        print(e)
        # get_platform_info()

    try:
        if os.path.isfile("game.db"):
            try:
                conn = sqlite3.connect("game.db")
                cur = conn.cursor()
                statement = 'Select Name From Games Where Genre1 = "Shooter"'

                cur.execute(statement)
                statement = 'Select Rating From ESRB Where Rating = "M"'

                cur.execute(statement)
                statement = 'Select Name From Genre Where Name = "Shooter"'

                cur.execute(statement)
                statement = 'Select Name From Platforms Where Name = "Nintendo Switch"'

                cur.execute(statement)
                print("Database seems fine, continuing with boot")

            except Exception as e:
                # print(e)
                print("Something wrong with your DB, spinning up new one to be safe")
                clean_db()

        else:
            print("Revving up new DB")
            clean_db()

    except Exception as e:
        print(e)



 # Close the open file

### Displays help, interactive_prompt function
def displayHelp():

    print('`linechart`')
    print('     get a line plot of how many game releases by month through various years ')
    print('     ')

    print('`piechart`')
    print('     get a pie chart of game releases by different categories')

    print('`exit`')
    print('     quit the program')
    print('`help`')
    print('     display this menu')

### For Demo Testing to show relational keys
def test_foreign_keys():
    init_db()
    add_games_data()
    add_genre_data()
    add_esrb_ratings()
    add_platform_data()


def interactive_prompt():
    print("Booting Program...")

    data_checking()

    while True:
        userInput = input('\nInput a command. at any time in this program. type `help` for assistance, or `exit` to quit\n')
        if userInput == "cleanup":
            print("Revving up clean DB")
            clean_db()
        if userInput == "exit":
            sys.exit(0)
        if userInput == "help":

            displayHelp()
        if userInput == "foreign":
            test_foreign_keys()

        if userInput == "linechart":
            print("Enter the year you want to display")
            print("You can pick a single year from 2013-2017, or type `allyears` to check the entire DB")
            while True:
                yearInput = input("\nEnter a Year, or type `back` to go pick another chart\nAdd on `-p`to get a chart by platform\n")
                if yearInput == "exit":
                    sys.exit(0)
                if yearInput == "help":

                    displayHelp()
                if yearInput == "back":
                    break
                if len(yearInput.split()) == 1:
                    if yearInput not in ["2013", "2014", "2015", "2016", "2017", "allyears"]:
                        print("\nAre you sure that is a year?")
                        pass
                    else:
                        print("\ngetting that chart for you")
                        LineChart(releaseYear = yearInput)
                        print("\nType another year or type `back` to try another graph")
                elif len(yearInput.split()) == 2:
                    if yearInput.split()[0] not in ["2013", "2014", "2015", "2016", "2017", "allyears"]:
                        print("\nAre you sure that is a year?")
                        pass
                    elif "-p" not in yearInput.split()[1]:
                        print("\nAre you sure you entered things correctly?")
                        pass
                    else:
                        print("\ngetting that chart for you, with a dash of platform")
                        #PlatformChart(releaseYear = yearInput)
                        print("\nType another year or type `back` to try another graph")

        if userInput == "piechart":
            print("Enter the year you want to display a piechart. The default category is by Platform")
            print("You can pick a single year from 2013-2017, or type `allyears` to check the entire DB")
            acceptable_hooks = ["-g", "-r"]
            while True:
                yearInput = input("\nEnter a Year, or type `back` to go pick another chart\nadd on ` -r` to get a chart of ratings or ` -g` for genre\n")
                if yearInput == "exit":
                    sys.exit(0)
                if yearInput == "help":
                    print("help")
                    displayHelp()
                if yearInput == "back":
                    break
                if len(yearInput.split()) == 1:
                    if yearInput.split()[0] not in ["2013", "2014", "2015", "2016", "2017", "allyears"]:
                        print("\nAre you sure that is a year?")
                        pass
                    else:
                        print("\ngetting that chart for you")
                        PieChart(releaseYear = yearInput)
                        print("\nType another year or type `back` to try another graph")
                elif len(yearInput.split()) == 2:
                    if yearInput.split()[1] not in acceptable_hooks:
                        print("\nAre you sure you entered things correctly?")
                        pass
                    else:
                        if "-g" in yearInput.split()[1]:
                            print("getting that chart for you, with a dash of genre")
                            GenreChart(releaseYear = yearInput.split()[0])
                            print("Type another year or type `back` to try another graph")
                        elif "-r" in yearInput.split()[1]:
                            print("getting that chart for you, with a dash of rating")
                            RatingChart(releaseYear = yearInput.split()[0])
                            print("Type another year or type `back` to try another graph") ###Interactive CLI

if __name__ == "__main__":
    interactive_prompt()
