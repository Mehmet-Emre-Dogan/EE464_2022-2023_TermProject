from PyPDF2 import PdfFileMerger
import os
from msvcrt import getch
import datetime
import re

# references
# https://stackoverflow.com/questions/3444645/merge-pdf-files

# https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
def naturalSort(arr): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(arr, key=alphanum_key)

currDir = ".\\" # Get the current directory
pdfCou = 0
merger = PdfFileMerger()
files = naturalSort(os.listdir(currDir)) 

for i, item in enumerate(files):
    if str(item).lower().endswith(".pdf") and not "Merged__" in str(item):
        if "ignoremerge" in str(item).lower():
            print(f"{'   --> Ignoring file:'} {item}")
            continue
        else:
            print(f"{str(pdfCou+1).zfill(2).rjust(3)}- PDF found: {item}")
            pdfCou += 1
            merger.append(item)
if pdfCou:
    customDT = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    print("Merging your files. Please wait...")
    merger.write(f"Merged__{customDT}.pdf")
    merger.close()
    print("Merging completed. Press any key to exit.")
else:
    print("There is no PDF file. Press any key to exit.")
getch()