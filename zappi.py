#!/usr/bin/env python

import config as cfg
import datetime
import requests
import logging

from   requests.auth import HTTPDigestAuth


CURRENT_DATE = datetime.datetime.today()

DAY = f'{CURRENT_DATE.day}'
MONTH = f'{CURRENT_DATE.month}'
YEAR = f'{CURRENT_DATE.year}'
USERNAME    = cfg.myenergi['user']
PASSWORD    = cfg.myenergi['password']
STATUS_URL  = cfg.myenergi['status_url']
ZAPPI_SNO   = cfg.myenergi['zappi_sno'] 
CSV_FILE    = cfg.myenergi['data_target_path'] + f'{YEAR}-{MONTH}.csv'
CSV_SEPARATOR = cfg.myenergi['csv_separator']
DECIMAL_SEPARATOR = cfg.myenergi['decimal_separator']
daily_statistic_url = cfg.myenergi['zappi_url'] + cfg.myenergi['zappi_sno'] + '-' + f'{YEAR}-{MONTH}-{DAY}'
hourly_statistic_url = cfg.myenergi['zappi_url_hour'] + cfg.myenergi['zappi_sno'] + '-' + f'{YEAR}-{MONTH}-{DAY}'

#https://s18.myenergi.net/cgi-jdayhour-Znnnnnnnn-YYYY-MM-DD

#function to access the server using a parsed URL 
def access_server(url_request):
    headers = {'User-Agent': 'Wget/1.14 (linux-gnu)'}
    r = requests.get(url_request, headers = headers, auth=HTTPDigestAuth(USERNAME, PASSWORD), timeout=10)
    if (r.status_code == 200):
        print ("") #"Login successful..") 
    elif (r.status_code == 401):
        print ("Login unsuccessful!!! Please check USERNAME, PASSWORD or URL..")
        quit()
    else:
        logging.info("Login unsuccessful, returned code: " + r.status_code)
        quit()
    #print (r.json())
    return r.json()

#function to calculate the daily total and return the result
def generate_daily_total():
    # initialize the variables
    sum_h1d = 0
    sum_h2d = 0
    sum_h3d = 0
    total = 0
    response_data = access_server(daily_statistic_url)
    for i in response_data[f'U{ZAPPI_SNO}']:
        for key in i.keys():
            if key == 'h1d':
                sum_h1d = sum_h1d + i[key]
            if key == 'h2d':
                sum_h2d = sum_h2d + i[key]
            if key == 'h3d':
                sum_h3d = sum_h3d + i[key]
    # calculate the total kWh from the joule values of the three phases of the zappi wallbox
    total = ((sum_h1d + sum_h2d + sum_h3d) / 3600000).__round__(2)
    return total


# get the time stamp of the first charge of the day
def get_first_charge_time():
    response_data = access_server(hourly_statistic_url)
    for i in response_data[f'U{ZAPPI_SNO}']:
        for key in i.keys():
            if key == 'h1d':
                if i[key] > 0:
                    timestamp = str(i['hr']) + ':' + str(i['min'])
                    return timestamp
    return None

#write the daily total to a .csv file
def write_daily_total():
    total = generate_daily_total()

    #only write if there is a value > 0 kWh
    if total > 0:
        #get the first charge time
        timestamp = get_first_charge_time()
        #write the data to the csv file
        with open(CSV_FILE, 'a') as f:
            f.write(f'{DAY}{CSV_SEPARATOR}{MONTH}{CSV_SEPARATOR}{YEAR}{CSV_SEPARATOR}' + str(timestamp) + CSV_SEPARATOR + str(total).replace('.', DECIMAL_SEPARATOR) + '\n')
        f.close()


if __name__ == "__main__":
    write_daily_total()
