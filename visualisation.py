import csv
import matplotlib.pyplot as pypl
import numpy
from collections import Counter
import geojson

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
    data_list =[
        counter["Monday"],
        counter["Tuesday"],
        counter["Wednesday"],
        counter["Thursday"],
        counter["Friday"],
        counter["Saturday"],
        counter["Sunday"]
    ]
    day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    # Set y using matplotlib
    pypl.plot(data_list)
    # Set x labels
    pypl.xticks(range(7), day_tuple)
    # Save plot as png image(create)
    pypl.savefig("Days.png")
    # Close figure
    pypl.clf()

def visualize_type():
    """Visualization by category in bar chart"""
    #Similar algorithm as in visualize_data()
    #Take data
    data_file = parse(FILE, ',')
    # Counter for iterating throw the data and count
    # how many crimes were each day of week
    counter = Counter(item["DayOfWeek"] for item in data_file)
    # Labels for chart
    labels = tuple(counter.keys())
    # Set for x
    xlocations = numpy.arange(len(labels)) + 0.5
    # Set labels
    width = 0.5
    # Assign for bars
    pypl.bar(xlocations, counter.values(), width=width)
    pypl.xticks(xlocations + width / 2, labels, rotation=90)
    # More space
    pypl.subplots_adjust(bottom=0.4)
    # Setting for charts
    pypl.rcParams['figure.figsize'] = 12, 8
    # Save results as png image
    pypl.savefig("Type.png")

    pypl.clf()

def create_map(data_file):
    """Create GeoJSON map to visualize"""
    # Set type of map
    geo_map = {"type": "FeatureCollection"}
    # Set list for each point
    item_l = []
    # Iterate over data to create JSON map
    for index, line in enumerate(data_file):
        # Is x or y == 0 it wil throw out of map
        if line['X'] == '0' or line['Y'] == '0':
            continue
        # New dict for each iteration
        data = {}
        # Set some GeoJSON parameters
        data["type"] = "Feature"
        data["id"] = index
        data['properties'] = {'title': line['Category'],
                              'description': line['Descript'],
                              'date': line['Date']}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (line['X'], line['Y'])}
        item_l.append(data)

    # Add each point to map
    for point in item_l:
        geo_map.setdefault('features', []).append(point)
    # Load data to file
    with open('file_sf.geojson', 'w') as f:
        f.write(geojson.dumps(geo_map))


def main():
    """Main funnction for call parsing function"""
    data = parse(FILE, ',')
    visualize_days()
    visualize_type()
    create_map(data)


if __name__ == "__main__":
    main()
