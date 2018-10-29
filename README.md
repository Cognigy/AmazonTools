# AmazonTools

this repository contains helper scripts that convert Cognigy files to Amazon Alexa compatible .jsons and vice versa

## Currently the following scripts are available

### *alexa-to-cognigy*

contains all conversions from Alexa json content to importable Cognigy files

#### types-to-lexicon.py

this scripts tries to convert all .json files in the same directory to Cognigy lexicon compatible .csvs,
the results are stored in a "cognigy" folder


### *cognigy-to-alexa*

contains all conversions from Cognigy files to Alexa

#### lexicon-to-types.py

this scripts tries to convert all .csv files in the same directory to Alexa compatible .jsons,
the results are stored in an "alexa" folder
