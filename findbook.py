from findbooks import *

h = HathiChecker()
i = IaChecker()
barcodes = []
errors = []
with open(r'C:\Scanning\find-vols\not_online.txt', 'r') as fin:
    for line in fin:
        barcodes.append(line.strip())
with open(r'C:\Scanning\find-vols\cat_check_long_title.txt', 'a') as fout:
    for barcode in barcodes:
        try:
            item = Item(barcode)
            item.get_marc_fields(len_title="long")
            h_return_item, h_hits = h.check(item)
            i_return_item, i_hits = i.check(item)
            if h_hits or i_hits:
                msg = "Barcode: %s found. URLs: %s\n" % (barcode, ", ".join(h_hits + i_hits))
                fout.write(msg)
                print(msg)
        except Exception as e:
            error = "Barcode: %s experienced an error. %s\n" % (barcode, e)
            print(error)
            errors.append(error)
with open(r'C:\Scanning\find-vols\errors_long_title.txt', 'a') as ferror:
    for error in errors:
        ferror.write(error)
print("findbooks has completed checking barcodes.")
