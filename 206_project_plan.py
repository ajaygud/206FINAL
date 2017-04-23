## Your name: Ajay Gudivada
## The option you've chosen: Option 2

# Put import statements you expect to need here!
#
#

import unittest
import itertools
import collections
import tweepy
import twitter_info 
import json
import sqlite3
import requests



consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = "final_project_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file_obj = open(CACHE_FNAME,'r')
	cache_contents = cache_file_obj.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

class Movie(object):
	def __init__(self, a_dic):
		self.title = a_dic["Title"]
		self.imdb_rating = a_dic["imdbRating"]
		self.plot = a_dic["Plot"]
		self.diction = a_dic
	def get_actor(self):
		self.actors = self.diction["Actors"]
		return self.actors
	def get_langs(self):
		self.num_lang = len(self.diction["Language"])
		return self.num_lang
	def get_direc(self):
		self.director = self.diction["Director"]
		return self.director
	def __str__(self):
		return "The movie we are looking up is {} and the plot is {}".format(self.title, self.plot)

def search_term(anything):
	if anything in CACHE_DICTION:
		results = CACHE_DICTION[anything]
		return(results)
	else:
		random_info_results = api.search(anything) 
		CACHE_DICTION[anything] = random_info_results
		cache_file = open(CACHE_FNAME, 'w') 
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		return (random_info_results)

search_term("blake griffin")

def get_user_info(userhandle):
	h = "twitter_" + userhandle

	if h in CACHE_DICTION:
		results = CACHE_DICTION[h]
		return(results)
	else:
		user_info_results = api.get_user(userhandle) 
		CACHE_DICTION[h] = user_info_results
		cache_file = open(CACHE_FNAME, 'w') 
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		return (user_info_results)

get_user_info("rihanna")


def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res
    
# This is the function that actually builds each URL to make a request with, so we can say "Have we made a request with this URL before?" It invokes the  canonical_order function in the process. For requests where we can access the URL, this is a good unique identifier.
def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url

def get_omdb_data(search_term):
	try:
		cache_file_obj = open(CACHE_FNAME,'r')
		cache_contents = cache_file_obj.read()
		CACHE_DICTION = json.loads(cache_contents)
	except: 
		CACHE_DICTION={}

	base_url = "http://www.omdbapi.com/?"

	params_diction = {} # you'll need to decide what key-val pairs go in here
	#e.g.
	params_diction["t"] = search_term

	unique_identifier = requestURL(base_url,params_diction)
	if unique_identifier in CACHE_DICTION:
		print("using cached data for", unique_identifier)
		# cool, if so, grab the data that goes with it!
		python_obj_data = CACHE_DICTION[unique_identifier]
		return(python_obj_data)
	else: # if not
		print("getting new data from the web for", unique_identifier)
		response = requests.get(base_url,params=params_diction)
		python_obj_data = json.loads(response.text)
		CACHE_DICTION[unique_identifier] = python_obj_data
		
		f = open(CACHE_FNAME,'w') # open our cache file to write
		f.write(json.dumps(CACHE_DICTION)) # write the JSON-string version of the cache dictionary to the file, which has everything in it
		f.close()
		return(python_obj_data)

movie_list = ["The Hangover", "Zootopia", "Boyhood"]
all_movies_list = []
for i in movie_list:
	movie_diction = get_omdb_data(i)
	movie_object = Movie(movie_diction)
	all_movies_list.append(movie_object)
print(all_movies_list[0].get_actor())
print(all_movies_list[0].title)
print(all_movies_list[0].get_direc())

tweet_diction_list = []
for i in range(len(movie_list)):
	print("entering movie list of dictionaries to retrieve director name")
	director_tweets = search_term(all_movies_list[i].get_direc())
	tweet_diction_list.append(director_tweets)

print(type(tweet_diction_list[0]))








# conn = sqlite3.connect('final_project.db')
# cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS Tweets')
# cur.execute("CREATE TABLE Tweets(tweet TEXT, tweet_id TEXT PRIMARY KEY,user_id TEXT,tweet_favs INTEGER,retweets INTEGER)")

# cur.execute('DROP TABLE IF EXISTS Users')
# cur.execute("CREATE TABLE Users(user_id TEXT PRIMARY KEY,screen_name TEXT,num_favs INTEGER,description TEXT)")


##movie_tweets 
#create tweet function to search and put it in movie_tweets


# list_of_screen_names = []
# user_id_list = []
# for j in movie_tweets:
# 	for k in j["entities"]["user_mentions"]:
# 		list_of_screen_names.append(k["screen_name"])
# 		umich_user_id_list.append(k["id_str"])


# for i in list_of_screen_names:
# 	users = api.get_user(i)
# 	blah = (users["id_str"], users["screen_name"], users["favourites_count"], users["description"])
# 	cur.execute('INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)', blah)
# conn.commit()

# tweet_id_list = []
# tweet_text_list = []
# tweet_time_list = []
# tweet_retweet_list = []
# for tweets in movie_tweets:
# 	tweet_id_list.append(tweets["id_str"])
# 	tweet_text_list.append(tweets["text"])
# 	tweet_time_list.append(tweets["created_at"]) 
# 	tweet_retweet_list.append(tweets["retweet_count"])
# tup = zip( tweet_text_list,tweet_id_list, user_id_list, tweet_time_list, tweet_retweet_list)
# for i in tup:
# 	cur.execute('INSERT INTO Tweets VALUES (?,?,?,?,?)', i)
# conn.commit()








# Write your test cases here.
# print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

# class twitter_cache_data(unittest.TestCase):
# 	def test_blah(self):
# 		self.assertTrue()
# class omdb_cache_data(unittest.Testcase):
# 	def test_cache(self):
# 		self.assertTrue()
# class movie_class(unittest.Testcase):
# random_movie = Movie()
# 	def test_constructor(self):
# 		self.assertEqual(type(self), type({}))
# 	def test_stri_init(self):
# 		self.assertEqual(random_movie.__str__(), "Boss Baby")
# 	def test_title(self):
# 		zoo = Movie({"Zootopia"})
# 		self.assertEqual(wizards.title, "Zootopia")
# 	def test_director(self):
# 		self.assertEqual(zoo.director, "Byron Howard")
# 	def test_rating(self):
# 		self.assertEqual(zoo.rating, 8.1)
# 	def test_actors(self):
# 		self.assertEqual(zoo.actors, "Ginnifer Goodwin, Jason Bateman, Idris Elba")
# 	def test_num_lang(self):
# 		self.assertEqual(zoo.number_of_lang, 1)
# class tweets_table(unittest.Testcase):
# 	def test_tweets_table(self):
# 		conn = sqlite3.connect('final_proj_tweets.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Tweets');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)>=20, "Testing there are at least 20 records in the Tweets database")
# 		conn.close()
# class users_table(unittest.Testcase):
# 	def test_users_table(self):
# 		conn = sqlite3.connect('final_proj_tweets.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Users');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
# 		conn.close()




## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)