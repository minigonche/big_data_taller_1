'''
This method takes in an specific ID and returns the corresponding Bourough
(e.g Queens, Bronx, Brooklyn... etc) by looking at the the taxi_zone_lookup file
'''


def location_by_ID(value):

    ##Make sure the path tot he taxi_zone_lookup.csv is correct
    f = open('taxi_zone_lookup.csv', 'r')
    data = f.read()
    data = data.split('\n')

    zones = []
    location_by_ID = {}
    locations = []

    for line in data:
        line = line.strip()
        #print(line)
        location, zone, trash = line.split(',', 2)

        if zone not in zones:
            location_by_ID[zone] = []

    for line in data:
        line = line.strip()
        location, zone, trash = line.split(',', 2)

        if (location not in location_by_ID[zone]):
            location_by_ID[zone].append(location)

    value = 10
    keys = list(location_by_ID.keys())
    print(keys)
    for key in keys:
        if str(value) in location_by_ID[key]:
            return(key)
