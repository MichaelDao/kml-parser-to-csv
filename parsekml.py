#!/usr/bin/env python
# encoding: utf-8


import os
import csv
import logging
import re
from optparse import OptionParser
from bs4 import BeautifulSoup


class KmlParser(object):
    """
        KmlParser
    """

    def __init__(self, kmlfile, csvfile):
        self.kmlfile = kmlfile
        self.csvfile = csvfile
        self.outputfile = ''
        self.outputdata = []

    def ParseKml(self):
        """
            parse_kml
        """
        try:
            # open the kml file with beatiful soup 4
            handler = open(self.kmlfile).read()
            soup = BeautifulSoup(handler, "html.parser")

            # Loop through eacgh <placemark> tag to find the coordinates
            for message in soup.findAll('placemark'):
                locationdata = {}

                """
                    parse_altitude
                """
                kmlaltitude = message.find('altitude')
                altitude = str(kmlaltitude)

                # remove prefix 
                if altitude.startswith('<altitude>'):
                    altitude = altitude[10:]

                # remove suffix
                if altitude.endswith('</altitude>'):
                    altitude = altitude[:-11]

                locationdata['altitude'] = altitude

                """
                    parse_coordinates
                """
                kmlcoordinates = message.find('coordinates')
                coordinates = str(kmlcoordinates)

                # remove prefix
                if coordinates.startswith('<coordinates>'):
                    coordinates = coordinates[14:]

                # remove suffix
                if coordinates.endswith('</coordinates>'):
                    coordinates = coordinates[:-14]

                # seperate longitude and latitude
                splitString = coordinates.split()
                locationdata['latitude'] = splitString[0]
                locationdata['longitude'] = splitString[1]

                # append data to array
                self.outputdata.append(locationdata)

        # File reading error detected
        except IOError as (errno, strerror):
            logging.error("I/O error(%d): %s" % (errno, strerror))

    def WriteCsv(self):
        """
            write_csv        
        """
        self.outputfile = os.getcwd() + '/' + self.csvfile
        try:
            # Prepare output to csv file
            out = open(self.outputfile, 'w')
            print 'Writing output to file ', self.outputfile

            try:
                # Create the headers for the spreadsheet
                fieldnames = sorted(self.outputdata[0].keys())
                writer = csv.DictWriter(out, dialect='excel', fieldnames=fieldnames,
                                        extrasaction='ignore', quoting=csv.QUOTE_NONNUMERIC)
                headers = dict((n, n) for n in fieldnames)
                writer.writerow(headers)

                # Write each row with data
                for row in self.outputdata:
                    writer.writerow(row)
                print 'Output file ', self.outputfile, ' written'

            finally:
                # Close output
                out.close()

        # File Reading error
        except IOError as (errno, strerror):
            logging.error("I/O error(%d): %s" % (errno, strerror))

        return self.outputfile


def main():
    """
        Main method 
    """
    parser = OptionParser()

    # input flag
    parser.add_option("-f", "--file", dest="kmlfile",
                      help="KML file to be parsed",
                      metavar="FILE")
    # output flag
    parser.add_option("-d", "--output", dest="csvfile",
                      help="CSV output file",
                      metavar="FILE")
    (options, args) = parser.parse_args()

    # error checking for wrong input
    if not options.kmlfile:
        print "please type python " \
              "kmlparser.py --file=[kmlfilename] --output=[csvfilename]"
    elif not options.csvfile:
        print "please type python " \
              "kmlparser.py --file=[kmlfilename] --output=[csvfilename]"

    # files defined properly, begin parsing
    else:
        kmlparser = KmlParser(kmlfile=options.kmlfile, csvfile=options.csvfile)
        kmlparser.ParseKml()

        # Create the csv
        kmlparser.WriteCsv()


if __name__ == "__main__":
    main()
