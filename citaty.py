import config 


quotes = []
try:
    file = open(config.path_to_quotes, 'r').read()
except: 
    file = open(config.path_to_quotes, 'r', encoding='utf8').read()
lines = file.split('\n')
for line in lines:
    quotes.append(line)

quotes