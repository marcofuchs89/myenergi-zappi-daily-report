# MyEnergi Zappi Daily Report

This repository/script was inspired by a need of a colleague of mine.  
He needed to have a daily summary of the total kWh value of the Zappi Wallbox.

## Components

**zappi.py** - is the main script that should be executed at the end of the day to calculate the total kWh value.  
It fetches the hourly status from the MyEnergi Cloud and calculates the total amount from each of the three phases of the Zappi Wallbox and divides the output in Joules by 3.600.000 which leads to the output value in kWh.

**config.py** - holds the necessary values/constants that are needed to run zappi.py

* user - Insert your MyEnergi Hub Serial number
* password - Insert the corresponding MyEnergi password
* zappi_sno - Insert the serial number of your Zappi Wallbox
* status & zappi_url - Don't change these values
* data_target_path - Change to the path where the .csv files should be stored (daily report value) - e.g. "/opt/_zappi/"

## Usage

* Clone the repository and edit the config.py to suit your needs
* Open a terminal and ```cd``` into the directory
* Install the python requirements with ```pip3 install -r requirements.txt```
* Run the script with ```python3 zappi.py```

### Tip

Execute the zappi.py script in a cron job to be run on a daily basis, e.g. close to midnight, to get the daily total automatically written to the .csv file

## Outcome

At the location defined in the **config.py** ("data_target_path") you'll find a .csv file in the format "YYYY-MM.csv".  
The file will contain the information of the day in the format > Year, Month, Day, Total_kWh

## CREDITS

The work made in this repository/scripts is based on several efforts of other contributors:

* [twonk/MyEnergi-App-Api][https://github.com/twonk/MyEnergi-App-Api]
* [ashleypittman/mec][https://github.com/ashleypittman/mec]
* [G6EJD/MyEnergi-Python-Example][https://github.com/G6EJD/MyEnergi-Python-Example]