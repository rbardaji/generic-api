import csv
import datetime
import math

# Set the start and end dates for the time series
start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)
end_date = datetime.datetime(2023, 1, 15, 23, 0, 0)

# Create CSV file and write data
with open('water_data.csv', mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    # Write column headers
    csv_writer.writerow(['Date and Time', 'Temperature', 'Salinity'])
    current_date = start_date
    while current_date <= end_date:
        # Calculate temperature based on time of year and time of day
        temperature = 10 * math.sin(2 * math.pi * (current_date.month - 1) / 12) + 10 * math.sin(2 * math.pi * (current_date.day - 1) / 365) + 5 * math.sin(2 * math.pi * current_date.hour / 24) + 20
        # Calculate salinity based on time of day and time of year
        salinity = 35.5 + 0.2 * math.sin(2 * math.pi * (current_date.month - 1) / 12) + 0.1 * math.sin(2 * math.pi * (current_date.day - 1) / 365) + 0.1 * math.sin(2 * math.pi * current_date.hour / 24)
        # Write current date and time and corresponding data
        csv_writer.writerow([current_date, temperature, salinity])
        # Add an hour to the current date and time
        current_date += datetime.timedelta(hours=1)
