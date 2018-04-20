# si-507-final-project ---Steven Hardge

## Introduction
This is a program that uses the  Internet Game Database (“IGDB”) to create a visualization tool with Plotly. IGDB is a online community that maintains a database of several facets of video game data. They have data points covering individual game characters, themes, release status (beta/alpha/etc), game genre, and the company that made it. IGDB offers a HTTP API, [https://igdb.github.io/api/](https://igdb.github.io/api/), that I will use to create a command line tool that will let the user create various visualization elements using data from the database.

## How to setup
This Program uses a python wrapper to access the API to make calls and data bit easier to read.
You can find the wrapper [here](https://github.com/igdb/igdb_api_python)
or you can install with `pip3 install igdb_api_python`

It also uses Plotly, which you can find [here](https://plot.ly/python/getting-started/)

All the requirements are in `requirements.txt`

## How to Use
The program has two main commands, `linechart`, which creates a line chart of game Releases
and `piechart`, which creates a pie chart of game releases. When you enter either of those commands
you are taken to a submenu where you can indicate which specific year you want to query. There are some
special queries you can indicate like with `2015 -g`.

You can get an API key [here](https://api.igdb.com/signup) which you can then put in your `secrets.py`

## Code Structure

The program is structured and laid out into groups of functions. The main functions are the Plotly calls starting on line 658,
`plot_pie_chart()` and `plot_line_data()`
The Database creation functions are `init_db()` starting on line 241.
The API call functions doing most of the work is `get_games_by_releaseYear()` on line 74. This gets most of the game data.

Then at the bottom there is the `interactive_prompt()` which handles user input

The SQL query functions return a list, or list of lists like `combined_list` which is to be passed to the plotly functions

## Warning
This program uses IGDBs expanded requests and makes a lot  of API Calls. The API is free to use,
however you can only make 100 of these expanded requests. For that reason, the repo contains
the json data for games going back to 2013. However this is only for getting Game data. Building
the Genre, Platform, and ESRB tables don't use expanded requests.
