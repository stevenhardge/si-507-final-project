#from ig import igdb
#from igdb_api_python import igdb
from igdb_api_python.igdb import igdb as igdb
from datetime import datetime
import time, os
import sqlite3
import requests
import json
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
DBNAME = 'test.db'
#CACHE_FNAME
games_cache_2013 = '2013games.json'
games_cache_2014 = '2014games.json'
games_cache_2015 = '2015games.json'
games_cache_2016 = '2016games.json'
games_cache_2017 = '2017games.json'
genre_cache = 'genre.json'
platform_cache = 'platform.json'
CACHE_FNAME = "cache.json"
CACHE_DICTION = {}


try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def get_games_by_releaseYear(releaseYear):

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

def get_genres():
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


def is_platform_cache_old(): #if cache time stamp is older than 6 months, return True value to get data again
    now = time.strftime("%a %b %d %H:%M:%S %Y")
    tdelta = datetime.strptime(now, '%a %b %d %H:%M:%S %Y') - datetime.strptime(CACHE_DICTION["platform_time"], '%a %b %d %H:%M:%S %Y')
    if tdelta.total_seconds > 1340000:
        return True
    else:
        return False


def get_platform_info():

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

def update_genres():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    statement = " UPDATE `Games` SET `Genre1` = (SELECT Genre.Name From Genre where Genre.Id = Games.Genre1) "
    cur.execute(statement)
    statement = " UPDATE `Games` SET `Genre2` = (SELECT Genre.Name From Genre where Genre.Id = Games.Genre2) "
    cur.execute(statement)
    statement = " UPDATE `Games` SET `Genre3` = (SELECT Genre.Name From Genre where Genre.Id = Games.Genre3) "
    cur.execute(statement)
    conn.commit()
    conn.close()

def update_ratings():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    statement = " UPDATE `Games` SET `Rating` = (SELECT ESRB.Rating From ESRB where ESRB.Id = Games.Rating) "
    cur.execute(statement)
    conn.commit()
    conn.close()


def init_db():
    #code to create a new database goes here
    #handle exception if connection fails by printing the error

    try:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
    except Exception as e:
        print(e)
    #code to test whether table already exists goes here
    #if exists, prompt to user: "Table exists. Delete?yes/no"
    #if user input is yes, drop table. Else, use move on and use existing table


    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

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
    statement += '  `ReleaseMonth`  TEXT ,'
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
    #this function is not expected to return anything, you can modify this if you want
def add_esrb_ratings():
    # Connect to choc database
    conn = sqlite3.connect('test.db')
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


def add_genre_data():
    # Connect to choc database
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    with open(genre_cache) as json_data:
        g = json.load(json_data)

        for genre in g:
            params = (genre["id"], genre["name"])

            try:
                cur.execute(" INSERT INTO `Genre` (Id, Name) VALUES (?, ?)", params)

            except Exception as ex:
                print(ex)
                pass #bandaid for repeat Tweets
        conn.commit()

def add_games_data():
    # Connect to choc database
    conn = sqlite3.connect('test.db')
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
                print(ex)
                pass #bandaid for repeat Tweets
        conn.commit()
    conn.close()

def add_platform_data():
    # Connect to choc database
    conn = sqlite3.connect('test.db')
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
            print("168")
             #bandaid for repeat Tweets
    conn.commit()
    conn.close()

def query_platformCounts(releaseYear):
    # Connect to choc database
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    platform_list =[]
    platform_list_count = []


    statement = "Select Platform, Count(Platform) From Games "
    statement += " GROUP BY Platform "
    statement += " Having ReleaseYear = {} AND Count(Platform) > 10".format(releaseYear)
    cur.execute(statement)
    for x in cur:
        platform_list.append(x[0])
        platform_list_count.append(x[1])
    combined_list = [platform_list, platform_list_count]
    return combined_list



def query_releaseCounts(releaseYear):

        # Connect to choc database
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
        list_of_monthly_releases = []
        for x in range(12):

            statement = "Select Count(Name) From Games Where ReleaseYear = {} and ReleaseMonth = {}".format(releaseYear, str(x + 1))
            cur.execute(statement)
            for x in cur:
                list_of_monthly_releases.append(x[0])

        return list_of_monthly_releases

# get_platform_info()
def plot_pie_chart():
    combined_list = query_platformCounts(2017)
    platform_names = combined_list[0]
    platform_counts = combined_list[1]
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

def plot_line_data():
    list_of_monthly_releases = query_releaseCounts(2017)

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
    py.plot( fig, validate=True, filename='2017 Releases' )

plot_pie_chart()
# init_db()




 # Close the open file
