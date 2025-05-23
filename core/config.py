import configparser

config = configparser.ConfigParser()
config.read('config.ini')

VIRUS_TOTAL_API_KEY = config['VirusTotal']['apiKey']

NUM_SCAN_WORKERS = 2

DB_FILE = 'app.db'
