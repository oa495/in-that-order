womanWithSpouse = 'partner|wife|spouse|married'
womanParent = 'mother|mom|mum|parent'
manWithSpouse = 'husband|partner|spouse|married'
manParent = 'father|dad|parent'

data = {
	"total": 0,
	"women": {
		"total": 0,
		"spouseAndParent": {
			"total": 0
		},
		"spouse": {
			"total": 0,
			"only": 0,
			"first": 0,
			"second": 0,
			"third": 0
		},
		"parent": {
			"total": 0,
			"only": 0,
			"first": 0,
			"second": 0,
			"third": 0
		},
		"other": {
			"total": 0,
			"first": 0,
			"second": 0,
			"third": 0,
			"only": 0
		}
	},
	"men": {
		"total": 0,
		"spouseAndParent": 0,
		"spouse": {
			"total": 0,
			"only": 0,
			"first": 0,
			"second": 0,
			"third": 0
		},
		"parent": {
			"total": 0,
			"only": 0,
			"first": 0,
			"second": 0,
			"third": 0
		},
		"other": {
			"total": 0,
			"first": 0,
			"second": 0,
			"third": 0,
			"only": 0
		}
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
	data["women"]["spouse"]["total"] = len(df_womanWithSpouse)

	# woman as parent
	df_womanAsParent = df[women & (df['bio'].str.contains(womanParent, case=False))]
	data["women"]["parent"]["total"] = len(df_womanAsParent)
	
	# both
	df_womenParentAndSpouse = df[women & ((df['bio'].str.contains(womanParent, case=False)) & (df['bio'].str.contains(womanWithSpouse, case=False)))]
	data["women"]["spouseAndParent"] = len(df_womenParentAndSpouse)
	
	# either parent or spouse
	data["women"]["spouse"]["only"] = len(df_womanWithSpouse) - len(df_womenParentAndSpouse)
	data["women"]["parent"]["only"] = len(df_womanAsParent) - len(df_womenParentAndSpouse)

	# only other
	df_womenParentOrSpouse = df[women & ((df['bio'].str.contains(womanParent, case=False)) | (df['bio'].str.contains(womanWithSpouse, case=False)))]
	data["women"]["other"]["total"] = len(df_women) - len(df_womenParentOrSpouse)

	#  ~ Men ~
	men = df['gender'] == "male"
	df_men = df[men]
	data["men"]["total"] = len(df_men)

	# man as spouse
	df_manWithSpouse = df[men & (df['bio'].str.contains(manWithSpouse, case=False))]
	data["men"]["spouse"]["total"] = len(df_manWithSpouse)

	# man as parent
	df_manAsParent = df[men & (df['bio'].str.contains(manParent, case=False))]
	data["men"]["parent"]["total"] = len(df_manAsParent)
	
	# both
	df_menParentAndSpouse = df[men & ((df['bio'].str.contains(manParent, case=False)) & (df['bio'].str.contains(manWithSpouse, case=False)))]
	data["men"]["spouseAndParent"] = len(df_menParentAndSpouse)
	
	# either parent or spouse
	data["men"]["spouse"]["only"] = len(df_manWithSpouse) - len(df_menParentAndSpouse)
	data["men"]["parent"]["only"] = len(df_manAsParent) - len(df_menParentAndSpouse)


	# only other
	df_menParentOrSpouse = df[men & ((df['bio'].str.contains(manParent, case=False)) | (df['bio'].str.contains(manWithSpouse, case=False)))]
	data["men"]["other"]["total"] = len(df_men) - len(df_menParentOrSpouse)


def getIndexOfNames(bio, names):
	arrayOfNames = names.split('|')
	wordFoundAt = -1
	bio = bio.lower()
	for word in arrayOfNames:
		if bio.find(word) != -1:
			wordFoundAt = bio.find(word)
			break
	return wordFoundAt

def compareIndexes(spouseIndex, parentIndex, key):
	# if bio has references to both being a spouse and parent
	if ((spouseIndex > -1) & (parentIndex > -1)):
		# both
		# spouse comes before
		if (spouseIndex < parentIndex):
			if spouseIndex == 0:
				# first of all
				data[key]["spouse"]["first"]+=1
				data[key]["parent"]["second"]+=1
				data[key]["other"]["third"]+=1
			else:
				data[key]["other"]["first"]+=1
				data[key]["spouse"]["second"]+=1
				data[key]["parent"]["third"]+=1
		else:
			if parentIndex == 0:
				data[key]["parent"]["first"]+=1
				data[key]["spouse"]["second"]+=1
				data[key]["other"]["third"]+=1

			else:
				data[key]["other"]["first"]+=1
				data[key]["parent"]["second"]+=1
				data[key]["spouse"]["third"]+=1
	elif ((spouseIndex > -1) & (parentIndex == -1)): 
		# just spouse reference
		if spouseIndex == 0:
			data[key]["spouse"]["first"]+=1
			data[key]["other"]["second"]+=1
		else:
			data[key]["other"]["first"]+=1
			data[key]["spouse"]["second"]+=1
	elif ((parentIndex > -1) & (spouseIndex == -1)): 
		# just parent reference
		if parentIndex == 0:
			data[key]["parent"]["first"]+=1
			data[key]["other"]["second"]+=1
		else:
			data[key]["other"]["first"]+=1
			data[key]["parent"]["second"]+=1

def getOrderOfBio():
	for row in df.iterrows():
		data = row[1]
		bio = data['bio']
		gender = data['gender']
		if gender == 'female':
			# get index for spouse
			spouseIndex = getIndexOfNames(bio, womanWithSpouse)
			# get index for parent
			parentIndex = getIndexOfNames(bio, womanParent)
			compareIndexes(spouseIndex, parentIndex, 'women')
		else:
			spouseIndex = getIndexOfNames(bio, manWithSpouse)
			parentIndex = getIndexOfNames(bio, manParent)
			compareIndexes(spouseIndex, parentIndex, 'men')

addCountsToData();
getOrderOfBio();
print data

