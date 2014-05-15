import gzip, timeit
from debian import deb822
from tribus.common.recorder import alt_record_package, record_package

def test():
    for section in deb822.Packages.iter_paragraphs(open("/home/fran/Escritorio/Packages")):
        #record_package(section)
        alt_record_package(section)
        
if __name__ == '__main__':
    print(timeit.timeit("test()", setup="from __main__ import test", number = 20))