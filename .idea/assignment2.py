#!/usr/bin/env python
# -*- Coding: utf-8 -*-

"""
IS 211 Assignment 2
"""

import os
import sys
import csv
import urllib2
import datetime
import logging
import argparse


def downloadfile(url):
    """
    :param url: (String)
        URL to fetch
    :return:
        Data fetched from URL
    :examples:
        >>> downloadfile('http://www.google.com')
    """
    data = urllib2.urlopen(urllib2.Request(url)).read()
    return data


def processdata(datafile):
    """
    Process fetched data file
    :param datafile: csv.DictReader
    :return: dict
    :examples:
        >>>processdata(csvfile)
        {'24': ('Stewart Bond', datetime.datetime(2008, 2, 15, 0, 0)),
         '25': ('Colin Turner', datetime.datetime(1994, 6, 6, 0, 0)),
         '26': ('Pippa Glover', datetime.datetime(2001, 8, 15, 0, 0)),
         '20': ('Jack Poole', datetime.datetime(1997, 8, 3, 0, 0))}
    """
    pdlogger = logging.getLogger('assignment2::processdata')
    mydb = {}
    with open(datafile, 'r') as infile:
        csvfile = csv.DictReader(infile)
        line = 0
        for row in csvfile:
            try:
                line += 1
                id = row['id']
                name = row['name']
                day, month, year = row['birthday'].split('/')
                bdate = datetime.date(int(year), int(month), int(day))
                bday = datetime.datetime.combine(bdate, datetime.time())
                mydb[id] = (name, bday)
            except ValueError:
                msg = 'Error processing line# {} for ID# {}'.format(line - 1, id)
                pdlogger.error(msg)
                continue
    return mydb


def displayperson(id, data):
    """
    Find entry with 'id' index from 'data'
    :param id (int): ID to find
    :param data (dict): dataset to search
    :return (string): notify matched entry or no match
    """
    msg = ''
    try:
        idx = str(id)
        name = data[idx][0]
        bday = data[idx][1].strftime('%Y-%m-%d')
        return 'Person #{} is {} with a birthday of {}'.format(idx, name, bday)
    except KeyError:
        return 'No user found with that id'


parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, type=str)
args = parser.parse_args()
if args.url:
    URL = args.url
    print URL
logging.basicConfig(filename='errors.log', level=logging.ERROR)
mainlog = logging.getLogger('assignment2::main')
try:
    DATAFILE = downloadfile(URL)
    if not DATAFILE:
        raise InvalidUrlException()
    CSVFILE = os.path.basename(URL)
    with open(CSVFILE, 'w') as outfile:
        outfile.write(DATAFILE)
    PERSONDATA = processdata(CSVFILE)
    print 'There are ', len(PERSONDATA), ' entries.'
    RESP = raw_input('Enter a person ID: ')
    while int(RESP) > 0:
        ID = int(RESP)
        print displayperson(ID, PERSONDATA)
        RESP = raw_input('Find another birthday (y/n):')
        if str(RESP).lower() != 'y' or str(RESP).lower() == 'n':
            break
        RESP = raw_input('Enter a person ID: ')

except InvalidUrlException:
    print 'Invalid URL, could not download the data file.'

except IOError:
    print 'Could not open ' + CSVFILE
