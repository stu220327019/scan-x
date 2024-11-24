import configparser

config = configparser.ConfigParser()
config.read('config.ini')

VIRUS_TOTAL_API_KEY = config['VirusTotal']['apiKey']
