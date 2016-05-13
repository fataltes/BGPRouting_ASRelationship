#!/usr/bin/python

import json
import sys
import pygeoip
import glob
import os

# parameters:  1: json file with probes 2: GeoIP database file 3: output file
dir = sys.argv[1]
database = pygeoip.GeoIP(sys.argv[2])
out_file = open(sys.argv[3], "w")

probes_found = 0
probes_accepted = 0

for filename in glob.glob(os.path.join(dir, '*.json')):
    print filename
    f = open(filename)
    for probe in json.load(f):
        probes_found += 1
        as_list = []
        probefrom = probe["from"]
        if probefrom:  # probefrom is the IP address
            foo = database.org_by_addr(probefrom) # look up the AS name in the database
            if isinstance(foo,basestring):
                foo.encode('utf8')
            else:
                unicode(foo).encode('utf8')
            as_list.append(foo)
            #as_list.append(str(database.org_by_addr(probefrom)))  # look up the AS name in the database
        else:
            continue
        result = probe["result"]
        found_result = 0  # found at least one hop
        for proberesult in result:
            if "result" in proberesult:
                hopresult = proberesult["result"]
                hopfrom = ""
                for hr in hopresult:
                    if "error" in hr:
                        pass
                    elif "x" in hr:
                        pass
                    else:
                        hopfrom = hr["from"]  # get the from IP address of the hop
                if hopfrom:
                    # check that this is not a form of a local IP address;  if it is, ignore and simply continue to the next hop
                    ip_list = map(int, hopfrom.split('.'))
                    if (ip_list[0] == 192 and ip_list[1] == 168):
                        continue
                    if (ip_list[0] == 10):
                        continue
                    if (ip_list[0] == 172 and ip_list[1] >= 16 and ip_list[1] <= 31):
                        continue
                    found_result += 1
                    # hopfrom is the IP address
                    as_list.append(str(database.org_by_addr(hopfrom)))  # look up the AS name in the database
        if (
            found_result > 0):  # got results for this probe, now collapse the repeating AS names (hops, within the same AS), discard the probe where some AS did not resolve
            last_as_name = ""
            print_string = ""
            none_after_last_as = False
            print_probe = True
            for as_name in as_list:
                if (as_name != last_as_name):  # if it is the same as the last name, the hop is in the same AS, and we don't duplicate it
                    if (as_name == 'None'):
                        none_after_last_as = True
                    else:  # this is a resolved AS name;
                        if (none_after_last_as == True):
                            # we have a situtation with AS1 None AS2, and we can not assume that None hop was in AS1 or AS2, therefore an error
                            print_probe = False
                            break
                        else:
                            # output this name
                            if last_as_name != "":
                                print_string += ", "
                            print_string += as_name
                            last_as_name = as_name
                else:
                    # name is the same as before, if there were None's in between, we ignore them - not an error
                    none_after_last_as = False
            if (none_after_last_as == True):
                # we have a situtation with probes ending on AS1 None, therefore an error
                print_probe = False
            # if we have just one AS and no path
            if "," not in print_string:
                print_probe = False
            # passed all checks, print the list of AS names for the probe
            if print_probe == True:
                #out_file.write(print_string + "\n\n")
                out_file.write(unicode(print_string + "\n\n").encode('utf8'))
                probes_accepted += 1  # we have results for this probe, will output it
                # else:
                # print "rejecting due to unresolved AS names:"
                # print as_list

print "Found ", probes_found, "probes in the file"
print "Sucessfully processed ", probes_accepted, " probes"
