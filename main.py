import csv
import matplotlib.pyplot as pypl
import numpy
from collections import Counter

"""Visualize CSV/Ecxel"""

FILE = "Data.csv"

def parse(raw_file, delimiter):
    """Parses a raw CSV file to a JSON-like object"""
    # Open CSV file
    with open(raw_file) as opened_file:
        # Read the CSV data
        csv_data = csv.reader(opened_file, delimiter=delimiter)

        # Setup an empty list
        parsed_data = []

        # Skip over the first line of the file for the headers
        fields = next(csv_data)

        # Iterate over each row of the csv file, zip together field -> value
        for row in csv_data:
            parsed_data.append(dict(zip(fields, row)))

        return parsed_data

def visualize_days():
    """Visualize data by days"""
    # Take parsed data
    data_file = parse(FILE, ',')
    # Counter for iterating throw the data and count
    # how many crimes were each day of week
    counter = Counter(item["DayOfWeek"] for item in data_file)
    # Seperated days for visualisation
    data_list ={
        counter["Monday"],
        counter["Tuesday"],
        counter["Wednesday"],
        counter["Thursday"],
        counter["Friday"],
        counter["Saturday"],
        counter["Sunday"]
    }
    day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    # Set y using matplotlib
    pypl.ploy(data_list)
    # Set x labels
    pypl.xticks(range(7), day_tuple)
    # Save plot as png image(create)
    pypl.savefig("Days.png")
    # Close figure
    pypl.clf()





def main():
    """Main funnction for call parsing function"""
    visualize_days()

if __name__ == "__main__":
    main()
