#!/usr/bin/env python
# encoding: utf-8
# import dependencies
import tweepy #https://github.com/tweepy/tweepy
import csv
import sexmachine.detector as gender
from utils import open_csv_w
# import authentication credentials
from secrets import TWITTER_C_KEY, TWITTER_C_SECRET, TWITTER_A_KEY, TWITTER_A_SECRET

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_C_KEY, TWITTER_C_SECRET)
auth.set_access_token(TWITTER_A_KEY, TWITTER_A_SECRET)
api = tweepy.API(auth)


# which Twitter list and who owns it
slug = 'members-of-congress'
owner = 'cspan'

import sexmachine.detector as gender
d = gender.Detector()



slug = 'members-of-congress'
owner = 'cspan'

def get_list_members(api, owner, slug):
	members = []
	# without this you only get the first 20 list members
	for page in tweepy.Cursor(api.list_members, owner, slug).items():
		members.append(page)
		# create a list containing all usernames
  	return [m.screen_name for m in members]













# create new CSV file and add column headings
def create_csv(filename, usernames):
	csvfile = open(filename, 'w')
	c = csv.writer(csvfile)
	# write the header row for CSV file
	c.writerow( [ "name",
				"display_name",
				"bio",
				"location",
				"gender" ] )
	# add each member to the csv
	for name in usernames:
		user_info = get_userinfo(name)
		c.writerow( user_info )
	# close and save the CSV
	csvfile.close()

def get_userinfo(name):
	# get all user data via a Tweepy API call
	user = api.get_user(screen_name = name)
	# create row data as a list
	user_info = [ name.encode('utf-8'),
				user.name.encode('utf-8'),
				user.description.encode('utf-8'),
				user.location.encode('utf-8'),
				d.get_gender((user.name.encode('utf-8')).split()[0])
				]
	# send that one row back
	return user_info

def main():
	# provide name for new CSV
	filename = "us-congress.csv"
	# create list of all members of the Twitter list
	usernames = get_list_members(api, owner, slug)
	# create new CSV and fill it
	create_csv(filename, usernames)
	# tell us how many we got
	print "Number of rows should be %d, plus the header row." % len(usernames)

if __name__ == '__main__':
	main()
