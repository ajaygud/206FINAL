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
		self.top_actor = a_dic["Actors"].split(",")[0]
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


def get_user_info(userhandle):
	h = "twitter_" + userhandle

	if h in CACHE_DICTION:
		#print("accessing cache file")
		results = CACHE_DICTION[h]
		return(results)
	else:
		#print("searching twitter api for user information")
		#print(userhandle)
		user_info_results = api.get_user(userhandle) 
		CACHE_DICTION[h] = user_info_results
		cache_file = open(CACHE_FNAME, 'w') 
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		return (user_info_results)



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
		#print("using cached data for", unique_identifier)
		# cool, if so, grab the data that goes with it!
		python_obj_data = CACHE_DICTION[unique_identifier]
		return(python_obj_data)
	else: # if not
		#print("getting new data from the web for", unique_identifier)
		response = requests.get(base_url,params=params_diction)
		python_obj_data = json.loads(response.text)
		CACHE_DICTION[unique_identifier] = python_obj_data
		
		f = open(CACHE_FNAME,'w') # open our cache file to write
		f.write(json.dumps(CACHE_DICTION)) # write the JSON-string version of the cache dictionary to the file, which has everything in it
		f.close()
		return(python_obj_data)

movie_list = ["Finding Dory", "Up", "The Lion King"]
all_movies_list = []
for i in movie_list:
	movie_diction = get_omdb_data(i)
	movie_object = Movie(movie_diction)
	all_movies_list.append(movie_object)
# print(all_movies_list[0].get_actor())
# print(all_movies_list[0].title)
# print(all_movies_list[0].get_direc())

tweet_diction_list = []
for i in range(len(movie_list)):
	#print("entering movie list of dictionaries to retrieve director name")
	director_tweets = search_term(all_movies_list[i].get_direc())
	tweet_diction_list.append(director_tweets)

#print(type(tweet_diction_list[0]))


list_of_screen_names = []
user_id_list = []
num_favorites_list	= []
description_list = []
for i in range(len(movie_list)):
	for j in tweet_diction_list[i]["statuses"]:
		list_of_screen_names.append(j["user"]["screen_name"])
		user_id_list.append(j["user"]["id_str"])
		num_favorites_list.append(j["user"]["favourites_count"])
		description_list.append(j["user"]["description"])

# print(list_of_screen_names)
# print(user_id_list)
# print(num_favorites_list)

list_of_user_mentions = []
for i in range(len(movie_list)):
	for j in tweet_diction_list[i]["statuses"]:
		blob = j["entities"]["user_mentions"]
		list_of_user_mentions.append(blob)

final_list_of_user_mentions = []
for i in list_of_user_mentions:
	for j in i:
		final_list_of_user_mentions.append(j["screen_name"])
#print(final_list_of_user_mentions)

# for i in list_of_screen_names:
# 	try: 
# 		print(i)
# 		user_rep_diction = get_user_info(i)
# 	except:
# 		print("Failed")
# 		list_of_screen_names.remove(i)
# 		continue

# print(user_rep_diction[sangklp])


	#print(type(user_rep_diction))


# user_id_list = []









conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute("CREATE TABLE Tweets(tweet TEXT, tweet_id TEXT PRIMARY KEY,user_screen_name TEXT,movie_search TEXT,tweet_favs INTEGER,retweets INTEGER)")

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute("CREATE TABLE Users(user_id TEXT PRIMARY KEY,user_screen_name TEXT,num_favs INTEGER,description TEXT)")

cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute("CREATE TABLE Movies(movie_id TEXT PRIMARY KEY,title TEXT,director TEXT,num_lang TEXT,imdb_rating INTEGER,top_billed_actor TEXT)")

cur.execute('DROP TABLE IF EXISTS Users_Mentioned')
cur.execute("CREATE TABLE Users_Mentioned(user_id TEXT PRIMARY KEY,user_name TEXT)")
##movie_tweets 
#create tweet function to search and put it in movie_tweets

tweet_text_list = []
tweet_id_list = []
tweet_favorite_count_list = []
tweet_retweet_list = []
movie_search_list = []
for i in range(len(movie_list)):
	for j in tweet_diction_list[i]["statuses"]:
		tweet_text_list.append(j["text"])
		tweet_id_list.append(j["id_str"])
		movie_search_list.append(movie_list[i])	
		tweet_favorite_count_list.append(j["favorite_count"])
		tweet_retweet_list.append(j["retweet_count"])
			

tup = zip(tweet_text_list, tweet_id_list, list_of_screen_names, movie_search_list, tweet_favorite_count_list, tweet_retweet_list)
for i in tup:
	cur.execute('INSERT INTO Tweets VALUES (?,?,?,?,?,?)', i)
conn.commit()

# print(len(user_id_list))
# print(len(list_of_screen_names))
# print(len(num_favorites_list))
# print(len(description_list))
tup_2 = zip(user_id_list, list_of_screen_names, num_favorites_list, description_list)
for i in tup_2:
	cur.execute('INSERT OR IGNORE INTO Users VALUES (?,?,?,?)', i)
conn.commit()


imdb_id_list = []
movie_title_list = []
director_list = []
languages_list = []
imdb_rating_list = []
top_actor_list = []
for i in all_movies_list:
	imdb_id_list.append(i.diction['imdbID'])
	movie_title_list.append(i.title)
	director_list.append(i.get_direc())
	languages_list.append(i.get_langs())
	imdb_rating_list.append(i.imdb_rating)
	top_actor_list.append(i.top_actor)	

tup_3 = zip(imdb_id_list,movie_title_list,director_list,languages_list,imdb_rating_list,top_actor_list)
for i in tup_3:
	cur.execute('INSERT OR IGNORE INTO Movies VALUES (?,?,?,?,?,?)', i)
conn.commit()

user_mentions_id_list = []

for i in final_list_of_user_mentions:
	u = get_user_info(i)
	user_mentions_id_list.append(u["id_str"])

tup_3 = zip(user_mentions_id_list, final_list_of_user_mentions)
for i in tup_3:
	cur.execute('INSERT OR IGNORE INTO Users_Mentioned VALUES (?,?)', i)
conn.commit()


query_1 = "SELECT description, num_favs FROM Users"
result_1 = list(cur.execute(query_1))
num_favs = list(filter(lambda x: x[1] > 5, result_1))

query_2 = "SELECT movie_search, Tweets.tweet FROM Tweets INNER JOIN Users ON Tweets.user_screen_name = Users.user_screen_name WHERE Users.num_favs > 100"  #N
result_2 = list(cur.execute(query_2))
#print(len(result_2))

b = collections.defaultdict(list)
for i,j in result_2:
	b[i].append(j)
movie_tweets_dictionary = dict(b)

query_3 = "SELECT retweets, Tweets.tweet from Tweets INNER JOIN USERS ON Tweets.user_screen_name = Users.user_screen_name"
result_3 = list(cur.execute(query_3))
most_retweets = {}
for i in result_3:
	if i[0] > 25:
		most_retweets[i[0]] = i[1]
#print(most_retweets)

query_4 = "SELECT tweet, tweet_favs from Tweets"
result_4 = list(cur.execute(query_4))
list_comp = [r[0] for r in result_4 if r[1] > 0]
#print("tweets with more than 0 favorites")
#print(list_comp[0])
conn.close()

write_file = "moviefile.txt"
file = open(write_file, 'w')
file.write("SUMMARY OF OMDB TWEETS")
file.write("\n")
file.write("The movies that we will search for are:")
file.write("\n")
for i in movie_list:
	file.write(i)
	file.write("\n")
file.write("\n")
file.write("These are the tweets with the most retweets:")
file.write("\n")
file.write(str(most_retweets))
file.write("\n")
file.write("\n")
file.write("These are the tweets with more than 100 favorites:")
file.write("\n")
file.write(json.dumps(movie_tweets_dictionary))
file.write("\n")
file.close()

	
#Write your test cases here.
print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class twitter_functions(unittest.TestCase):
	def test_search_term(self):
		self.assertEqual(type(search_term("rihanna")), type({}))
	def test_get_user_info(self):
		self.assertEqual(type(get_user_info("rihanna")), type({}))
class OMDB(unittest.TestCase):
	def test_get_omdb_data(self):
		self.assertEqual(type(get_omdb_data("Up")), type({}))
	def test_movie_class(self):
		self.assertEqual(type(all_movies_list[0].get_actor()),type(""))
		self.assertEqual(type(all_movies_list[0].get_langs()),type(2))
		self.assertEqual(type(all_movies_list[0].get_direc()),type(""))
	def test_str_constr(self):
		self.assertEqual(type(all_movies_list[0].__str__()), type(""))





## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)
