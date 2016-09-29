#!/usr/bin/env python3


from doc_pull import Runsheet
runsheet = Runsheet('/Users/johnwilshusen/Desktop/projects/doc_new_db/upload_me.xlsx')

for x in runsheet.instrument:
    print(x)
