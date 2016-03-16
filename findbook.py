import os
import time
from findbooks import *


def checkCollection(barcodes, checker, hits, errors, len_title="short"):
    for barcode in barcodes:
        try:
            item = Item(barcode)
            item.get_marc_fields(len_title="long")
            c_return_item, c_hits = checker.check(item)
            if c_hits:
                msg = "Barcode: %s found at URL: %s\n" % (barcode, ", ".join(c_hits))
                print(msg)
                if barcode not in hits.keys():
                    hits[barcode] = c_hits
                else:
                    hits[barcode] += c_hits
        except Exception as e:
            error = "Barcode: %s experienced an error. %s\n" % (barcode, e)
            print(error)
            if barcode not in errors.keys():
                errors[barcode] = [error]
            else:
                errors[barcode].append(error)
    return hits, errors


def report(hits, errors, path=None):
    if not path:
        path = os.getcwd()
    hits_path = os.path.join(path, "hits-" + time.strftime("%Y%m%d%H%M%S", time.localtime())) + ".txt"
    errors_path = os.path.join(path, "errors-" + time.strftime("%Y%m%d%H%M%S", time.localtime())) + ".txt"
    with open(hits_path, 'a') as fout:
        for key in hits.keys():
            msg = "Barcode: %s found at URLs: %s\n" % (key, ", ".join(hits[key]))
            fout.write(msg)
    print("Hits written to: %s" % hits_path)
    with open(errors_path, 'a') as fout:
        for key in errors.keys():
            msg = "Barcode: %s experienced the following errors: %s\n" % (key, ", ".join(errors[key]))
            fout.write(msg)
    print("Errors written to: %s" % errors_path)

def checkAll(barcodes, hits, errors):
        ################################################################
        ###                         HATHI
        ################################################################
        h = HathiChecker()
        hits, errors = checkCollection(barcodes, h, hits, errors, len_title="long")
        ################################################################
        ###                    INTERNET ARCHIVE
        ################################################################
        i = IaChecker()
        hits, errors = checkCollection(barcodes, i, hits, errors, len_title="long")
        ################################################################
        ###                         JSTOR
        ################################################################
        #j = JstorChecker()
        #hits, errors = checkCollection(barcodes, j, hits, errors, len_title="short")
        ################################################################
        ###                      GOOGLE BOOKS
        ################################################################
        with open('google-api-key.txt', 'r') as fin:
            key = fin.read()
        g = GoogleChecker(key)
        hits, errors = checkCollection(barcodes, g, hits, errors, len_title="long")
        return hits, errors

def main():
    hits = dict()
    errors = dict()
    barcodes = []
    with open('not_online_1.txt', 'r') as fin:
        for line in fin:
            barcodes.append(line.strip())
    hits, errors = checkAll(barcodes, hits, errors)
    time.sleep(86400)#24 hrs
    barcodes = []
    with open('not_online_2.txt', 'r') as fin:
        for line in fin:
            barcodes.append(line.strip())
    hits, errors = checkAll(barcodes, hits, errors)
    report(hits, errors)

main()
