from mrjob.job import MRJob


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        yield "chars", len(line)
        yield "words", len(line.split())
        yield "lines", 1

    def reducer(self, key, values):
        yield key, sum(values)

# python MRWordFrequencyCount.py -r hadoop hdfs:///user/lujin/input/ -o hdfs:///user/lujin/output/
if __name__ == '__main__':
    MRWordFrequencyCount.run()