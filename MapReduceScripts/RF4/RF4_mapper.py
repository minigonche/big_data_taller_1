#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import datetime

#init

# Date Format YYYY-MM-DD hh:mm:ss


format = '%Y-%m-%d %H:%M:%S'
inTimeFrame = False
hour = None
location_dictionary = {'Borough': ['LocationID'], 'EWR': ['1'], 'Queens': ['2', '7', '8', '9', '10', '15', '16', '19', '27', '28', '30', '38', '53', '56', '57', '64', '70', '73', '82', '83', '86', '92', '93', '95', '96', '98', '101', '102', '117', '121', '122', '124', '129', '130', '131', '132', '134', '135', '138', '139', '145', '146', '157', '160', '171', '173', '175', '179', '180', '191', '192', '193', '196', '197', '198', '201', '203', '205', '207', '215', '216', '218', '219', '223', '226', '252', '253', '258', '260'], 'Bronx': ['3', '18', '20', '31', '32', '46', '47', '51', '58', '59', '60', '69', '78', '81', '94', '119', '126', '136', '147', '159', '167', '168', '169', '174', '182', '183', '184', '185', '199', '200', '208', '212', '213', '220', '235', '240', '241', '242', '247', '248', '250', '254', '259'], 'Manhattan': ['4', '12', '13', '24', '41', '42', '43', '45', '48', '50', '68', '74', '75', '79', '87', '88', '90', '100', '103', '104', '105', '107', '113', '114', '116', '120', '125', '127', '128', '137', '140', '141', '142', '143', '144', '148', '151', '152', '153', '158', '161', '162', '163', '164', '166', '170', '186', '194', '202', '209', '211', '224', '229', '230', '231', '232', '233', '234', '236', '237', '238', '239', '243', '244', '246', '249', '261', '262', '263'], 'Staten Island': ['5', '6', '23', '44', '84', '99', '109', '110', '115', '118', '156', '172', '176', '187', '204', '206', '214', '221', '245', '251'], 'Brooklyn': ['11', '14', '17', '21', '22', '25', '26', '29', '33', '34', '35', '36', '37', '39', '40', '49', '52', '54', '55', '61', '62', '63', '65', '66', '67', '71', '72', '76', '77', '80', '85', '89', '91', '97', '106', '108', '111', '112', '123', '133', '149', '150', '154', '155', '165', '177', '178', '181', '188', '189', '190', '195', '210', '217', '222', '225', '227', '228', '255', '256', '257'], 'Unknown': ['264', '265']}


def location_by_ID_lookup(value):
    '''
    This method uses the dictionary created by the location_by_ID method
    to return the Borough (e.g. Queens, Bronx...) of an specific value.
    '''
    value = str(value)
    keys = list(location_dictionary.keys())
    matched_key = ''

    for key in keys:
        if value in location_dictionary[key]:
            matched_key = key

    return matched_key

for line in sys.stdin:

    line = line.strip()
    data = line.split(',')
    data_lenght = len(data)
    pickupTime = None
    PUlocation = None

    if data_lenght in [3, 5, 17, 18, 19, 20, 21]:
            pickupTimeStr = data[1]
            if pickupTimeStr[0].isdigit():
                pickupTime = pickupTimeStr
    else:
        continue

    if (data_lenght in [5, 17, 19]):

        if (data_lenght == 5):
            PUlocation = data[3]

        elif (data_lenght == 17):
            PUlocation = data[7]

        elif (data_lenght == 19):  # More than one type of header has this length
            # Checks that is not a coordinate (lattitude or longitud)
            if ('.' in data[6] or data[6] == 0):
                PUlocation = None
            else:
                PUlocation = data[5]

    if pickupTime:
        pickupTime = datetime.strptime(pickupTime, format)
        hour = pickupTime.hour
        month = pickupTime.month

    else:
        hour = None

    if PUlocation and hour:
        #translate destination zone to borough
        PUlocation = location_by_ID_lookup(PUlocation)
        print('%s\t%s\t%s' % (month, hour, PUlocation))