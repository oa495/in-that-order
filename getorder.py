# women
# ['mother', 'mom', 'mum', 'parent']
# ['partner', 'wife', 'spouse', 'married']
# <--------->
# men
# # ['father', 'dad', 'parent']
# ['husband', 'partner', 'spouse', 'married']

womanWithSpouse = 'partner|wife|spouse|married'
womanParent = 'mother|mom|mum|parent'
manWithSpouse = 'husband|partner|spouse|married'
manParent = 'father|dad|parent'

data = {
	"total": 0,
	"women": {
		"total": 0,
		"spouse": 0,
		"parent": 0,
		"work": 0
	},
	"men": {
		"total": 0,
		"spouse": 0,
		"parent": 0,
		"work": 0
	}
}


import pandas as pd
pd.set_option("display.width", 120)
df = pd.read_csv("data/us-congress.csv", header=None, names=["display_name", "bio", "gender"])

def addCountsToData():
	data["total"] = len(df)

	# ~ Women ~
	women = df['gender'] == "female"
	df_women = df[women]
	data["women"]["total"] = len(df_women)

	# woman as spouse
	df_womanWithSpouse = df[women & (df['bio'].str.contains(womanWithSpouse, case=False))]
	data["women"]["spouse"] = len(df_womanWithSpouse)

	# woman as parent
	df_womanAsParent = df[women & (df['bio'].str.contains(womanParent, case=False))]
	data["women"]["parent"] = len(df_womanAsParent)

	#  ~ Men ~
	men = df['gender'] == "male"
	df_men = df[men]
	data["men"]["total"] = len(df_men)

	# man as spouse
	df_manWithSpouse = df[men & (df['bio'].str.contains(manWithSpouse, case=False))]
	data["men"]["spouse"] = len(df_manWithSpouse)

	# man as parent
	df_manAsParent = df[men & (df['bio'].str.contains(manParent, case=False))]
	data["men"]["parent"] = len(df_manAsParent)

	# print data

def getOrderOfBio():
	for row in df.iterrows():
		data = row[1]
		bio = data['bio']
		gender = data['gender']


# def bioContainsSpouse(bio, spouseArray):
# 	print bio
# 	spouseWordFound = -1
# 	# for word in spouseArray:
# 	# 	if bio.find(word) != 1:
# 	# 		spouseWordFound = bio.find(word)
# 	# 		break
# 	if spouseWordFound > -1:
# 		return True
# 	else:
# 		return False

# def bioContainsParent(bio, parentArray):
# 	parentWordFound = -1
# 	for word in parentArray:
# 		if bio.find(word) != 1:
# 			parentWordFound = bio.find(word)
# 			break
# 	if parentWordFound > -1:
# 		return True
# 	else:
# 		return False

addCountsToData();
getOrderOfBio();
