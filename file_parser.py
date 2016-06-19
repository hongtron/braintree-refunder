import csv


class FileParser:
    def __init__(self, input_file):
        self.reader = csv.reader(open(input_file, 'rU'))

    def advance(self):
        try:
            return self.reader.next()
        except StopIteration:
            return False
