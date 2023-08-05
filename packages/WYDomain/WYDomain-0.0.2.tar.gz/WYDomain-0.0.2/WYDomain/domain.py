# -*- coding: utf-8 -*-
import os


class WYDomain(object):
    def __init__(self):
        self.domain_dict = {}

    def load(self):
        path = os.path.dirname(__file__)
        filename = os.path.join(path, "domain.txt")
        with open(filename) as f:
            while True:
                line = f.readline()
                if line:
                    domain, num, date = line.split(",")
                    self.domain_dict[domain] = {"num": num, "date": date}
                else:
                    break

    def is_licensed(self, domain):
        return domain in self.domain_dict

# if __name__ == '__main__':
#     o = WYDomain()
#     o.load()
#     print (o.is_licensed("gldmachinery.com"))