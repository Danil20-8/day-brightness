import os

import yaml
import csv


configPath = os.path.join('config')
currentYearConfigYamlPath = os.path.join(configPath, f'map.yml')
currentYearConfigCSVPath = os.path.join(configPath, f'csv.yml')

if not os.path.exists(configPath):
    os.makedirs(configPath)

def load_config():    
    table = {}
    
    if os.path.exists(currentYearConfigCSVPath):
        with open(currentYearConfigCSVPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                month = row['month']
                if not month in table:
                    table[month] = {}
                table[month][row['day']] = { 'sunrise': row['sunrise'], 'sunset': row['sunset'] }
            return table

def load_config_yaml():
    if os.path.exists(currentYearConfigYamlPath):
        with open(currentYearConfigYamlPath) as file:
            table = yaml.full_load(file)
            return table

    
def save_config(table):
    with open(currentYearConfigCSVPath, 'w+') as file:
        fieldnames = ['month', 'day', 'sunrise', 'sunset']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for month in table:
            for day in table[month]:
                writer.writerow({'month': month, 'day': day, 'sunrise': table[month][day]['sunrise'], 'sunset': table[month][day]['sunset']})

def save_config_yaml(table):        
    with open(currentYearConfigYamlPath, 'w+') as file:
        documents = yaml.dump(table, file)
