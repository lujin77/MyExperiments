from optparse import OptionParser

usage = "usage: python %prog [options] args"
parser = OptionParser(usage)

parser.add_option("-v", "--verbose",
				  action="store_true", dest="verbose", default=False,
				  help="make lots of noise [default]")

parser.add_option("-f", "--filename", type="string", dest="filename",
				  metavar="FILE", help="write output to FILE")

parser.add_option("-w", "--worker", type="int", dest="worker",
				  metavar="INT", help="set subprocess num for work", default="4")

(options, args) = parser.parse_args()

print args
print options

print options.worker
