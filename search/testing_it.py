#!/usr/bin/env python3

from process_search import Query

subdivision = 'WEST END'
block = '00012'
query = Query(block, subdivision)
for y in query.instrument:
    print(y['doc_num'], y['year'])
# for y in query.instrument:
#     did = y['did']
#     saveas = y['saveas']
#     if saveas != '--None.tif':
#         try:
#             query.grab_img(did, saveas)
#         except:
#             pass
#     else:
#         pass
# query.create_runsheet()
# query.archive()
# shutil.rmtree(default_storage.path('runsheets/'+str(runsheet_id)+"/"))
