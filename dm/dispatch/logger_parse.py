#!/usr/bin/python
# -*- coding:utf-8 -*-


#LOG = 'bidding-access'
#LOG = 'dispatch-access'
#LOG = 'dispatch-dev-access'
LOG = 'dispatch-assignrate-access'

MAPPING = {
    'bidding-access' : 'data/psf/bidding-access.log',
    'dispatch-access' : 'data/psf/dispatch-access.log',
    'dispatch-dev-access' : 'data/psf/dispatch-dev-access.log',
    'dispatch-assignrate-access' : 'data/watchd/dispatch-assignrate-access.log'
}


def parse(type):

    uri_dict = {}

    try:
        # load log file
        file_path = MAPPING.get(type)
        if file_path is None:
            print "[ERROR] input wrong type"
            exit(-1)

        # split log line by line
        fp = open(file_path, 'r')
        for i, line in enumerate(fp):
            # skip first line
            if i == 0:
                continue

            segs = line.strip().split(' ')
            if type == "bidding-access":
                uri_dict[segs[3]] = uri_dict[segs[3]] + 1 if segs[3] in uri_dict else 1
            elif type == "dispatch-access" or type == "dispatch-dev-access":
                key = (segs[3].split('?'))[0]
                uri_dict[key] = uri_dict[key] + 1 if key in uri_dict else 1
            else:
                print "[ERROR] input wrong type"

    finally:
        fp.close()

    for k, v in uri_dict.items():
        print k + " -> "  + str(v)



if __name__ == '__main__':
    parse(LOG)
