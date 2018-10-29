import csv 
import json
import os
import sys
from pprint import pprint

for filename in os.listdir(os.path.join(sys.path[0])):
	if filename.endswith(".json"):

		filepath = os.path.join(sys.path[0], filename)
		pprint(filepath)
		file = open(filepath)
		json_file = json.load(file)
		
		types = json_file["interactionModel"]["languageModel"]["types"]
		
		new_lexicon = []
		
		for type in types:
			for value in type["values"]:
				new_entry = {}
				new_entry["keyphrase"] = value["name"]["value"]
				new_entry["synonyms"] = list()
				new_entry["synonyms"].append(value["name"]["synonyms"])
				new_entry["tags"] = list()
				new_entry["tags"].append(type["name"])
				new_entry["data"] = ""
				
				keyphrase_exists = False
				
				for entry in new_lexicon:
					if entry["keyphrase"] == new_entry ["keyphrase"]:
						keyphrase_exists = True
						new_entry["synonyms"] = list(set(new_entry["synonyms"]) + set(entry["synonyms"]))
						new_entry["tags"] = list(set(new_entry["tags"]) + set(entry["tags"]))
						new_lexicon[entry] = new_entry
						break
				
				if not keyphrase_exists:
					new_lexicon.append(new_entry)
		
		pprint(new_lexicon)
		
		new_file = ""
		
		for row in new_lexicon:
			if len(row["tags"]) > 1:
				tags_string = "\""  + ','.join(map(str, row["tags"])) + "\""
			else:
				tags_string = "\""  + row["tags"][0]+ "\""
			
			if len(row["synonyms"]) > 1:
				synonyms_string = "\""  + ','.join(map(str, row["synonyms"])) + "\""
			else:
				synonyms_string = "\""  + row["synonyms"][0] + "\""
			sequence = (row["keyphrase"], tags_string, synonyms_string , "\"" + row["data"] + "\"" )
			new_file +=  ','.join(sequence)
			new_file += "\n"
		
		filepath = os.path.join(sys.path[0], "cognigy")
		# try to create the ouput directory
		try:
			os.makedirs(filepath)
		except:
			pass
		filepath = os.path.join(filepath, "cognigy-" + filename + ".csv")
		file = open(filepath, encoding='UTF-8', mode='w')
		file.write(str(new_file))