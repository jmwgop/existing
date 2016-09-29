#!/usr/bin/env python3

import os
import xlrd
import psycopg2
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from shutil import copy
from os import remove
from glob import glob
from shutil import make_archive
import tiffany
import datetime

class Query:

    img_source = r"/home/jmwgop/midland/midland/media/images/Midland Raw/MidlandTX"
    base = '/home/jmwgop/midland/midland/media/runsheets/'

    def __init__(self, block, subdivision):
        self.instrument = []
        try:
            self.conn = psycopg2.connect("dbname='midland_index'                user='postgres' host='192.168.1.20' password='Chlstdow2'"
                                    )
            self.cur = self.conn.cursor()
        except:
            print("Error Connecting")
        query1 = "Select vp_index_id from public.legal_index where block = (%s) and addition_name ILIKE (%s);"
        query2 = (block, subdivision,)
        self.cur.execute(query1, query2)
        self.did = []
        for records in self.cur.fetchall():
            self.did.append(records[0])
        self.doc_count = 0
        for z in self.did:
            self.doc_count+=1
            if z != '':
                queryconstant = "Select doc_type\
                                from public.constant_index where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(queryconstant, querya)
                except:
                    print("error")
                try:
                    self.doc_type = self.cur.fetchone()[0].title()
                except:
                    self.doc_type = ''


                querycons = "Select page \
                                from public.vp_doc where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycons, querya)
                except:
                    pass
                try:
                    self.page = int(self.cur.fetchone()[0])
                except:
                    self.page = ''

                querycons = "Select rec_type \
                                from public.vp_doc where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycons, querya)
                except:
                    pass
                try:
                    self.rec_type = self.cur.fetchone()[0]
                except:
                    self.rec_type = ''

                querycons = "Select volume \
                                from public.vp_doc where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycons, querya)
                except:
                    pass
                try:
                    self.volume = int(self.cur.fetchone()[0])
                except:
                    self.volume = ''


                querycons = "Select year \
                                from public.vp_doc where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycons, querya)
                except:
                    pass
                try:
                    self.year = int(self.cur.fetchone()[0])
                except:
                    self.year = ''

                querycons = "Select doc_num \
                                from public.vp_doc where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycons, querya)
                except:
                    pass
                try:
                    self.doc_num = int(self.cur.fetchone()[0])
                except:
                    self.doc_num = ''

                querycons = "Select file_date \
                                from public.constant_index where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycons, querya)
                except:
                    pass
                try:
                    self.file_date = self.cur.fetchone()[0]
                except:
                    self.file_date = ''

                querycon = "Select instrument_date \
                                from public.constant_index where vp_index_id = (%s);"
                querya = (z,)
                try:
                    self.cur.execute(querycon, querya)
                except:
                    pass
                try:
                    self.instrument_date = self.cur.fetchone()[0]
                except:
                    self.instrument_date = ''

                query_grantor = "Select grantor from public.grantor_index \
                                where vp_index_id = (%s);"
                query_grantee  = "Select grantee from public.grantee_index \
                                where vp_index_id = (%s);"
                query_legal = "Select legal from public.legal_index where \
                                vp_index_id = (%s);"
                query_img = "select img_path from public.img_index \
                            where vp_index_id = (%s);"
                try:
                    self.cur.execute(query_grantor, querya)
                except:
                    self.grantor = []
                    pass

                self.grantor = []
                try:
                    for x in self.cur:
                        self.grantor.append(x[0].title())
                except:
                    pass
                self.grantor_1 = " \n".join(self.grantor)

                try:
                    self.cur.execute(query_grantee, querya)
                except:
                    pass

                self.grantee = []
                try:
                    for x in self.cur:
                        self.grantee.append(x[0].title())
                except:
                    pass
                self.grantee_1 = " \n".join(self.grantee)

                try:
                    self.cur.execute(query_legal, querya)
                except:
                    pass

                self.legal = []
                try:
                    for x in self.cur:
                        self.legal.append(x[0].title())
                except:
                    pass
                self.legal_1 = " \n".join(self.legal)

                try:
                    self.cur.execute(query_img, querya)
                except:
                    pass

                self.img_page = []
                try:
                    for x in self.cur:
                        self.img_page.append(x[0].title())
                except:
                    pass
            else:
                self.img_page = ""
                self.legal_1 = ""
                self.grantee_1 = ""
                self.grantor_1 = ""
                file_date = ""
                self.doc_type = ""
                self.instrument_date = ""
            if self.rec_type == '':
                self.saveas = str(self.year) + "-" + str(self.doc_num) + ".tif"
            else:
                self.saveas = str(self.volume) + "-" + str(self.page) + "-" \
                                    + str(self.rec_type) + ".tif"

            self.instrument.append({"did" : z,
                                    "volume" : self.volume,
                                    "page" : self.page,
                                    "rec_type" : self.rec_type,
                                    "year" : self.year,
                                    "doc_num" : self.doc_num,
                                    "doc_type" : self.doc_type,
                                    "file_date": self.file_date,
                                    "instrument_date" : self.instrument_date,
                                    "grantor" : self.grantor_1,
                                    "grantee" : self.grantee_1,
                                    "legal" : self.legal_1,
                                    "img_page" : self.img_page,
                                    "saveas" : self.saveas
                                    })
        self.conn.commit()

    def create_request(self, landman):
        try:
            conn = psycopg2.connect("dbname='midland' user='jmwgop' \
                                    host='localhost' password='Chlstdow2'"
                                    )
            cur = conn.cursor()
        except:
            print("Error Connecting")

        querydown = "INSERT INTO upload_runreq (document_count, landman, created) VALUES \
                    (%s, %s, %s) returning pull_id;"
        queryup = (self.doc_count, landman, str(datetime.datetime.now()).split('.')[0])
        cur.execute(querydown, queryup)
        self.runsheet_id = cur.fetchone()[0]
        self.temp = self.base + str(self.runsheet_id) + "/"
        self.dest = self.temp + "Documents/"
        conn.commit()
        return self.runsheet_id

    def archive(self):
        out = self.base+str(self.runsheet_id)
        make_archive(out, 'zip', self.temp)
        return out

    def create_folder(self):
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)

    def grab_img(self, did, saveas_1):
        self.create_folder()
        # temp = self.temp
        # year is the subfolder, img_name is the file name.
        query3 = "select img_path from img_index \
                    where vp_index_id = (%s) ORDER BY img_path;"
        query4 = (did,)
        if did != "" and saveas_1 != '--None.tif':
            try:
                self.cur.execute(query3,query4)
            except:
                pass
            try:
                image_names = []
                # there can be multiple pages, but all will be returned by the
                # query
                for records in self.cur:
                    img_path = records[0]
                    source = self.img_source+img_path
                    image_names.append(source)
            except:
                pass
            last_link = None
            with open(self.dest+saveas_1, "wb") as f:
                for file in image_names:
                    tif = tiffany.open(file)
                    if last_link:
                        tif.im.last_linkoffset = last_link
                    tif.save(f)
                    last_link = tif.im.last_linkoffset
                    if f.tell() & 1:
                        f.write(b"\0")

    def create_runsheet(self):
        workbook = xlsxwriter.Workbook(self.temp+str(self.runsheet_id)+".xlsx")

        formheader = workbook.add_format()
        formheader.set_align('center')
        formheader.set_align('vcenter')
        formheader.set_border(1)
        formheader.set_bold(True)
        formheader.set_text_wrap(True)
        formheader.set_bg_color('silver')
        formheader.set_text_wrap()

        formcells = workbook.add_format()
        formcells.set_align('center')
        formcells.set_align('vcenter')
        formcells.set_border(1)
        formcells.set_text_wrap()

        formtop = workbook.add_format()
        formtop.set_align('left')
        formtop.set_align('vcenter')
        formtop.set_border(1)
        formtop.set_bold(True)
        formtop.set_text_wrap()

        date_format = workbook.add_format({'num_format': 'MM/DD/YYYY'})
        date_format.set_align('center')
        date_format.set_align('vcenter')
        date_format.set_border(1)
        date_format.set_text_wrap()

        formtop1 = workbook.add_format()
        formtop1.set_align('center')
        formtop1.set_align('vcenter')
        formtop1.set_border(1)
        formtop1.set_text_wrap()

        formhyper = workbook.add_format({
        'font_color': 'blue',
        'underline':  1
        })
        formhyper.set_align('center')
        formhyper.set_align('vcenter')

        red = workbook.add_format()
        red.set_bg_color('red')

        worksheet = workbook.add_worksheet()
        worksheet.freeze_panes(7, 0)

        worksheet.write(0,0, "Section:", formtop)
        worksheet.write(1,0, "Subdivision:", formtop)
        worksheet.write(2,0, "Block:", formtop)
        worksheet.write(3,0, "Lot:", formtop)
        worksheet.write(4,0, "Landman:", formtop)
        worksheet.write(5,0, "Broker:", formtop)
        worksheet.write(6, 0, "Grantor", formheader)
        worksheet.write(6, 1, "Grantee", formheader)
        worksheet.write(6, 2, "Type of Instrument", formheader)
        worksheet.write(6, 3, "Effective Date", formheader)
        worksheet.write(6, 4, "File Date", formheader)
        worksheet.write(6, 5, "Volume or Year", formheader)
        worksheet.write(6, 6, "Page or Instrument Number", formheader)
        worksheet.write(6, 7, "Record Type", formheader)
        worksheet.write(6, 8, "Legal Description", formheader)
        worksheet.write(6, 9, "Comments", formheader)
        worksheet.write(6, 10, "Image", formheader)

        worksheet.set_column(0, 1, 31)
        worksheet.set_column(2, 2, 18)
        worksheet.set_column(3, 7, 9)
        worksheet.set_column(8, 9, 39)
        worksheet.set_column(10, 10, 9)

        y = 7
        for x in self.instrument:
            worksheet.write(y, 0, x["grantor"], formcells)
            worksheet.write(y, 1, x["grantee"], formcells)
            worksheet.write(y, 2, x["doc_type"], formcells)
            if x["instrument_date"] != '':
                try:
                    worksheet.write_datetime(y, 3, x["instrument_date"],
                                             date_format
                                            )
                except:
                    pass
            if x["file_date"] != '':
                try:
                    worksheet.write_datetime(y, 4, x["file_date"], date_format)
                except:
                    pass
            if x["rec_type"] == '':
                worksheet.write(y, 5, x["year"], formcells)
                worksheet.write(y, 6, x["doc_num"], formcells)
                save = str(x["year"])+"-"+str(x["doc_num"])+".tif"
                hyper = xl_rowcol_to_cell(y, 10)
                if os.path.isfile(self.dest+save) == True:
                    worksheet.write_url(hyper, r'external:'+"Documents/"+save,
                                        formhyper, "Document"
                                        )
                else:
                    worksheet.write(hyper, '', red)
            else:
                save = str(x["volume"])+"-"+str(x["page"])+"-" \
                        +str(x["rec_type"])+".tif"
                hyper = xl_rowcol_to_cell(y, 10)
                if os.path.isfile(self.dest+save) == True:
                    worksheet.write_url(hyper, r'external:'+"Documents/"+save,
                                        formhyper, "Document"
                                        )
                else:
                    worksheet.write(hyper, '', red)
                worksheet.write(y, 5, x["volume"], formcells)
                worksheet.write(y, 6, x["page"], formcells)
                worksheet.write(y, 7, x["rec_type"], formcells)
            worksheet.write(y, 8, x["legal"], formcells)
            y+=1
        cell2 = xl_rowcol_to_cell(y-1, 10)
        cellsformat1 = str('A8:'+cell2)
        worksheet.conditional_format(cellsformat1, {'type': 'no_errors',
                                                    'format': formcells
                                                    })
        cellsformat2 = str('B2:B6')
        worksheet.conditional_format(cellsformat2, {'type': 'no_errors',
                                                    'format': formcells
                                                    })
        workbook.close()
