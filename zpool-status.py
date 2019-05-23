#!/usr/bin/python

# Text scraper for Prometheus node_exporter
# Checks ZPOOL list status

# needs cronjob with output written to node exporter text.collecter
# e.g. crontab
# */1 * * * * USERNAME /usr/bin/python /opt/node-exporter/zpoolcheck.py > /opt/node-exporter/textfile-collector/zpool-status.prom

# node-exporter needs extra cli options to look for prom files
# e.g. node-exporter --collector.textfile.directory="/opt/node-exporter/textfile-collector"

import subprocess
from collections import Counter

base_name = "node_zfs_zpool_list_"

def main():
    output = subprocess.check_output(["/sbin/zpool", "list", "-H", "-p", "-o", "name,size,alloc,frag,dedup,health"], universal_newlines=True)

    for line in output.split("\n"):
        columns = line.split()
        if len(columns)>1:
            poolname = columns[0].lower()
            print("{}{}{{poolname=\"{}\"}} {}".format(base_name, 'size', poolname, columns[1]))
            print("{}{}{{poolname=\"{}\"}} {}".format(base_name, 'alloc', poolname, columns[2]))
            print("{}{}{{poolname=\"{}\"}} {}".format(base_name, 'frag', poolname, columns[3]))
            print("{}{}{{poolname=\"{}\"}} {}".format(base_name, 'dedup', poolname, columns[4]))

            statusdict = {
                "online" : 0,
                "degraded" : 1,
                "faulted" : 2,
                "offline" : 3,
                "removed" : 4,
                "unavail" : 5
            }

            health = columns[5].lower()

            print("{}{}{{poolname=\"{}\"}} {}".format(base_name, 'health', poolname, statusdict[health]))


if __name__ == "__main__":
    main()
