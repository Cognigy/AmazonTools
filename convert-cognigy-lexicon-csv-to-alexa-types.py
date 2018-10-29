import csv 
import json
import os
import sys
from pprint import pprint

for filename in os.listdir(os.path.join(sys.path[0])):
	if filename.endswith(".csv"):
		filepath = os.path.join(sys.path[0], filename)
		pprint(filepath)
		file = open(filepath)
		
		fieldnames = ("keyphrase","tags","synonyms","data")
		reader = csv.DictReader( file, fieldnames)
		json_file = []
		for row in reader:
			json_file.append(json.loads(json.dumps(row)))
		
		# generate new alexa json
		new_types = []
		
		for entry in json_file:
			keyphrase = entry["keyphrase"]
			# generate synonyms list 
			synonyms = entry["synonyms"].split(",")
			# remove whitespaces at both ends
			synonyms = [synonym.strip() for synonym in synonyms]
			
			new_value = {}
			new_value["name"] = {}
			new_value["name"]["value"] = keyphrase
			new_value["name"]["synonyms"] = synonyms
			
			for tag in entry["tags"].split(","):
				# remove whitespaces at both ends
				tag = tag.strip()
				# if user has missing tags put them in a noType type
				if tag == "":
					tag = "noType"
				
				new_type = {}
				new_type["name"] = tag
				new_type["values"] = []
				
				type_exists = False
				# check whether we need to generate type structure
				for type in new_types:
					if type["name"] == new_type["name"]:
						type_exists = True
						type["values"].append(new_value)
						break
				# generate type structure if necessary
				if not type_exists:
					new_type["values"].append(new_value)
					new_types.append(new_type)
			
			
		languageModel = {}
		languageModel["invocationName"] = "change this"
		languageModel["intents"] = json.loads("""[
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.HelpIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.StopIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.NavigateHomeIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.YesIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.NoIntent",
                    "samples": []
                }
            ]""")
		languageModel["types"] = new_types
		
		interactionModel = {}
		interactionModel["languageModel"] = languageModel
		
		new_json = {}
		new_json["interactionModel"] = interactionModel
		
		filepath = os.path.join(sys.path[0], "alexa")
		# try to create the ouput directory
		try:
			os.makedirs(filepath)
		except:
			pass
		filepath = os.path.join(filepath, "alexa-" + filename + ".json")
		new_file = json.dumps(new_json, sort_keys=False, indent=3, ensure_ascii=False)
		file = open(filepath, encoding='UTF-8', mode='w')
		file.write(str(new_file))
	
