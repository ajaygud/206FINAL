************README****************
***********Ajay Gudivada**************
Option 2: OMDB API Mashup
Search anything on twitter api (tweepy)
Search data about a twitter user.
the twitter api takes in any search term and any user handle. 
You can use the program to gather tweets about a certain movie and import
it into a database. 
The database creates 4 tables.
The program creates a cache file, a database file for the tables, and a .txt files
for a quick summary of the results.

run it by typing in python 206_project_plan.py in the terminal 
No modules need installation via pip. 
You must have a twitter_info.py file to run which contains the access keys and tokens
The files that are included are:
1) final_project_readme.txt- Overview of the project
2) final_project.db- database file that includes 4 tables
3) moviefile.txt- summary of the results of the program
4) 206_project_plan.py - program
5) final_project_cache.json- cache file used so program does not repeatedly access api

search_term function searches for anything on the twitter api and returns it.
required input is a string and no optional inputs. 
Return value is a dictionary of all tweets regarding the search string

get_user_info function searches for userhandle on the twitter api and returns information about that user.
required input is a string and no optional inputs. 
Return value is a dictionary of all information regarding the user

canonical_order function creates a sorted dictionary 
required input is a dictionary 
return value is a list sorted by key

requestURL is a that retrieves the url from a api and prepares the url to be used
required input is a baseurl and a dictionary of parameters
return value a string

get_omdb_data is a function that accesses the omdb api and reads it into a cache file
required input is a movie name and no optional parameters
return value is a dictionary with information about the movie searched.

One instance of the movie class represents a movie that you inputted as a dictionary
required input is a dictionary
no optional parameters
get_actor method retrieves all the actors for a movie
get_langs method retrieves the number of languages for a movie
get_direc method retrieves all the directors for a movie

The code searches for the directors of 3 movies of my choosing and searches
for mentions of them on twitter and retrieves all user info as well. 

The code also creates 4 useful tables that you can retrieve information from

I choose this project because it access any and all information about certain 
movies and what people are saying about them. I find this is useful in the future
if you ever want to look scrape the web for whats being talked about

Line(s) on which each of your data gathering functions begin(s):line 133-
Line(s) on which your class definition(s) begin(s):line 38-
Line(s) where your database is created in the program: line 204-
Line(s) of code that load data into your database: line 207-
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used? line 281
Line(s) of code that generate the output. line 309-
