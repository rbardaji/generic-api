## Water Data Generator

This Python script generates a time series of water temperature and salinity data and writes it to a CSV file. The data is generated for every hour of a given year, and the temperature and salinity values vary based on the season and time of day.

### How it Works

The script uses the built-in `csv` and `datetime` modules to create a CSV file and generate a series of dates and times. It then calculates the temperature and salinity values for each date and time using sinusoidal functions that vary with the season and time of day.

The temperature is calculated as a combination of three sinusoidal functions, each with a different period and amplitude. The first function depends on the month, and produces a sinusoidal variation with a period of one year. The second function depends on the day of the year, and produces a sinusoidal variation with a period of one year. The third function depends on the hour of the day, and produces a sinusoidal variation with a period of 24 hours. The resulting values are scaled and shifted to produce a temperature in the range of 0 to 30 degrees Celsius.

The salinity is calculated in a similar way, as a combination of three sinusoidal functions that depend on the month, day of the year, and hour of the day, respectively. The resulting values are added to a base salinity value of 35.5 parts per thousand, which corresponds to the average salinity of seawater.

The resulting data is written to a CSV file with three columns: date and time, temperature, and salinity. The CSV file can be used for data analysis, modeling, or visualization of water temperature and salinity patterns over time.

### Usage

To use the script, simply run it in a Python environment or from the command line. The resulting CSV file, `water_data.csv`, will be created in the current directory. The script can be modified to generate data for different time periods, or to adjust the parameters of the sinusoidal functions that control the temperature and salinity values.

```python
python water_data_generator.py
