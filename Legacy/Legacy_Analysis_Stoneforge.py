import csv, numpy, pandas, pylab

"""This method will turn my crappy attempt t a placeholder dictionary for the deck stats,
decklists, and sideboards into a proper dictionary."""

def dict_eval(n):
	placeholder = "".join(n.split(','))
	placeholder = placeholder.lstrip("{").lstrip(" {").rstrip("; }").rstrip(";}")
	placeholder = dict(x.split(": ") for x in placeholder.split(";"))
	for key in placeholder:
		if key.isdigit() == True:
			placeholder[key] = int(placeholder[key])
	return placeholder

#Load the data/
	
data=[]

with open("Legacy.csv") as datafile:
	raw_data = csv.reader(datafile, delimiter="%")
	for row in raw_data:
		data.append(row)
del data[0]		#Get rid of the column headers

#Format data for use with pandas

for i in data:
	i[0] = int(i[0])
	print(i[0])
	i[5] = int(i[5])
	i[9] = dict_eval(i[9])
	i[10] = dict_eval(i[10])
	if "}" in i[11]:
		i[11] = dict_eval(i[11])
	i[6] = "{0}/{1}/{2}".format(i[8], i[7], i[6])
	del i[8]
	del i[7]
	
"""What you have now is a list of lists called data. Each sublist is a different deck in the following format:

["DeckID", "Format", "Archetype", "Player", "Event", "Placed", "Date", "Deck Stats", "Maindeck", "Sideboard"]
Index: 0	   1 		   2		  3		   4		 5		  6			7			  8			  9

The stats, Maindeck, and Sideboard are dictionaries with the card names as keys (without any spaces) and the values
are the number of times that card appears in either the main deck or sideboard. Stats has a bunch of information I
didn't want to delete like number of creatures, lands, noncreature spells, etc...

Now make a few empty dictionaries to analyse the data:"""
	

data_1 = {}		#Number of decks with Stoneforge Mystic
data_2 = {}		#Number of W decks
data_3 = {}		#Number of UW decks
data_4 = {}		#Number of UB decks
data_5 = {}		#Number of UWR decks
data_6 = {} 	#Number of Esper decks
data_7 = {}		#Number of Bant decks
data_8 = {}		#Number of Junk decks
data_9 = {}		#Number of 4c decks
data_10 = {}		#Total Number of decks for that date for normalization


for i in data: 				#Loop over each deck in data
	count_sfm = 0
	count_monowhite = 0
	count_UW = 0
	count_deadguy = 0
	count_UWR = 0
	count_esper = 0
	count_bant = 0
	count_junk = 0
	count_4c = 0
	set_archetypes = [i[2]]
	if i[6] in data_7.keys():
		data_10[i[6]] += set_archetypes  #Count the number of decks for each date
	else:
		data_10[i[6]] = set_archetypes
	if "StoneforgeMystic" in i[8]: 		#Look for decks that contain Stoneforge Mystic in the main
		count_sfm = 1
		listlands = ["Tundra", "Savannah", "Scrubland", "Plateau",\
		"UndergroundSea", "VolcanicIsland", "TropicalIsland", "Island",\
		"Badlands", "Taiga", "Bayou"]
		if not any(s in i[8] for s in listlands):   
			count_monowhite = 1	
		listlands = ["Tundra", "Savannah", "Plateau",\
		"UndergroundSea", "VolcanicIsland", "TropicalIsland", "Island",\
		"Badlands", "Taiga", "Bayou"]	
		if not any(s in i[8] for s in listlands)\
		and ("Scrubland" in i[8] or "Swamp" in i[8]):
			count_deadguy = 1
		listlands = ["Savannah", "Scrubland", "Plateau",\
		"UndergroundSea", "VolcanicIsland", "TropicalIsland",\
		"Badlands", "Taiga", "Bayou"]
		if not any(s in i[8] for s in listlands)\
		and ("Tundra" in i[8] or "Island" in i[8]):
			count_UW = 1
		listlands = ["Savannah", "Scrubland",\
		"UndergroundSea", "TropicalIsland",\
		"Badlands", "Taiga", "Bayou"]
		if not any(s in i[8] for s in listlands)\
		and ("VolcanicIsland" in i[8] and "Tundra" in i[8]):   
			count_UWR = 1
		listlands = ["Savannah", "Plateau",\
		"VolcanicIsland", "TropicalIsland",\
		"Badlands", "Taiga", "Bayou"]
		if not any(s in i[8] for s in listlands)\
		and ("UndergroundSea" in i[8] and "Tundra" in i[8]):   
			count_esper = 1
		listlands = ["Scrubland", "Plateau",\
		"VolcanicIsland", "UndergroundSea",\
		"Badlands", "Taiga", "Bayou"]
		if not any(s in i[8] for s in listlands)\
		and ("TropicalIsland" in i[8] and "Tundra" in i[8]):
			count_bant = 1
		listlands = ["Tundra"\
		"VolcanicIsland", "UndergroundSea","TropicalIsland"]
		if not any(s in i[8] for s in listlands)\
		and ("Scrubland" in i[8] and "Bayou" in i[8] and "Savannah" in i[8]):
			count_junk = 1
		elif "UndergroundSea" in i[8] and "Tundra" in i[8] and ("Bayou" in i[8] or "TropicalIsland" in i[8]):   
			count_4c = 1
	if "StarCityGames.com" in i[4]: 		#Event types contain "StarCityGames.com"
		if i[5] > 0 and i[5] < 17: 			#Top 16 decks only
			if i[6] in data_1.keys():		#If we already have an entry for this date, just add the current count
				data_1[i[6]] += count_sfm
			else:							#Otherwise make a new entry with the date and add the count
				data_1[i[6]] = count_sfm
			if i[6] in data_2.keys():
				data_2[i[6]] += count_monowhite
			else:
				data_2[i[6]] = count_monowhite
			if i[6] in data_3.keys():
				data_3[i[6]] += count_UW
			else:
				data_3[i[6]] = count_UW
			if i[6] in data_4.keys():
				data_4[i[6]] += count_deadguy
			else:
				data_4[i[6]] = count_deadguy
			if i[6] in data_5.keys():
				data_5[i[6]] += count_UWR
			else:
				data_5[i[6]] = count_UWR		
			if i[6] in data_6.keys():
				data_6[i[6]] += count_esper
			else:
				data_6[i[6]] = count_esper	
			if i[6] in data_7.keys():
				data_7[i[6]] += count_bant
			else:
				data_7[i[6]] = count_bant	
			if i[6] in data_8.keys():
				data_8[i[6]] += count_junk
			else:
				data_8[i[6]] = count_junk	
			if i[6] in data_9.keys():
				data_9[i[6]] += count_4c
			else:
				data_9[i[6]] = count_4c	

# Put the whole thing into an array for pandas
				
data_1_lst = []

for key, value in data_1.items():
	data_1_lst.append([key, (value/len(data_10[key]))])	#Divide the number of countertop decks by the total number of decks for that period.

for i in data_1_lst:
	j = [(data_2[i[0]])/len(data_10[i[0]]),\
	#For each card, divide the number of decks that contain that card by the number
	#of countertop decks for that date.
	(data_3[i[0]])/len(data_10[i[0]]),\
	(data_4[i[0]])/len(data_10[i[0]]),\
	(data_5[i[0]])/len(data_10[i[0]]),\
	(data_6[i[0]])/len(data_10[i[0]]),\
	(data_7[i[0]])/len(data_10[i[0]]),\
	(data_8[i[0]])/len(data_10[i[0]]),\
	(data_9[i[0]])/len(data_10[i[0]])]
	i += j

#The following makes sure everything is the right kind of data.
	
data = numpy.array(data_1_lst) 
data_1_pd = pandas.DataFrame(data)
data_1_pd.columns = ["Date", "Number of SFM Decks", "Mono White", "UW",\
 "Deadguy Ale", "UWR", "Esper", "Bant", "Junk", "4c"]
data_1_pd["Date"] = pandas.to_datetime(data_1_pd["Date"])
data_1_pd.index = data_1_pd["Date"]
data_1_pd["Number of SFM Decks"] = data_1_pd["Number of SFM Decks"].astype(float)
data_1_pd["Mono White"] = data_1_pd["Mono White"].astype(float)
data_1_pd["UW"] = data_1_pd["UW"].astype(float)
data_1_pd["Deadguy Ale"] = data_1_pd["Deadguy Ale"].astype(float)
data_1_pd["UWR"] = data_1_pd["UWR"].astype(float)
data_1_pd["Esper"] = data_1_pd["Esper"].astype(float)
data_1_pd["Bant"] = data_1_pd["Bant"].astype(float)
data_1_pd["Junk"] = data_1_pd["Junk"].astype(float)
data_1_pd["4c"] = data_1_pd["4c"].astype(float)

#Regroup everything by month and calculate the mean for each month.

data_2_pd = data_1_pd.set_index('Date').resample("M").mean()

#Plot and export as a csv to be used in excel

data_2_pd.plot()

print(data_2_pd)
data_2_pd.to_csv("SFM_Analysis.csv")
pylab.show()
