import os
import xlrd
import psycopg2
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from shutil import copy
from os import remove
from glob import glob
from shutil import make_archive

class Runsheet:

    def __init__(self, xls_file):
        try:
            self.conn = psycopg2.connect("dbname='midland_dr' user='postgres' \
                                    host='192.168.1.20' password='Chlstdow2'"
                                    )
            self.cur = self.conn.cursor()
        except:
            print("Error Connecting")

        self.path = xls_file
        workbook = xlrd.open_workbook(self.path)
        sheet = workbook.sheet_by_index(0)
        self.data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)]
                for r in range(sheet.nrows)
                ]

        self.doc_count = sheet.nrows - 1
        self.instrument = []
        for x in range(1, 1+self.doc_count):
            if self.data[x][2]:
                self.rec_type = str(self.data[x][2])
                self.doc_num = ''
                self.year = ''
                if self.data[x][0]:
                    self.volume = str(int(self.data[x][0]))
                    if self.data[x][1]:
                        self.page = str(int(self.data[x][1]))
                    else:
                        self.page = ''
                else:
                    self.volume = ''
            else:
                self.volume = ''
                self.page = ''
                self.rec_type = ''
                if self.data[x][0]:
                    self.year = int(self.data[x][0])
                    if self.data[x][1]:
                        self.doc_num = str(int(self.data[x][1]))
                    else:
                        self.doc_num = ''
                else:
                    self.year = ''
            if self.rec_type != '':
                # vol and page in the datbase have leading zeros to make them 4 digits.
                # Adding leading digits for search
                vol = self.volume.zfill(4)
                pg = self.page.zfill(4)
                self.rec_type = self.rec_type.upper()
                query1 = "Select did from deed_records.vp_doc where volume \
                            = (%s) and page = (%s) and rec_type = (%s);"
                # vol, page, and rec_type are all being fed in from an excel spreadsheet
                # in this version.
                query2 = (vol, pg, self.rec_type)
                try:
                    self.cur.execute(query1,query2)
                except:
                    pass
                try:
                    self.did = self.cur.fetchone()[0]
                except:
                    self.did = ""
            else:
                doc_num1 = self.doc_num.zfill(8)
                query1 = "Select did from deed_records.vp_doc where year = (%s) \
                            and doc_num = (%s);"
                query2 = (self.year, doc_num1)
                try:
                    self.cur.execute(query1,query2)
                except:
                    pass
                try:
                    self.did = self.cur.fetchone()[0]
                except:
                    self.did = ''
            if self.did != '':
                queryconstant = "Select doc_type, file_date, instrument_date \
                                from deed_records.index_constants where did = (%s);"
                querya = (self.did,)
                try:
                    self.cur.execute(queryconstant, querya)
                except:
                    pass
                try:
                    self.doc_type = self.cur.fetchone()[0]
                except:
                    self.doc_type = ''
                try:
                    self.file_date = self.cur.fetchone()[1]
                except:
                    self.file_date = ''
                try:
                    self.instrument_date = self.cur.fetchone()[2]
                except:
                    self.instrument_date = ''

                query_grantor = "Select grantor from deed_records.grantor_index \
                                where did = (%s);"
                query_grantee  = "Select grantee from deed_records.grantee_index \
                                where did = (%s);"
                query_legal = "Select legal from deed_records.legal_index where \
                                did = (%s);"
                query_img = "select year, img_name from deed_records.img_links \
                            where did = (%s);"
                try:
                    self.cur.execute(query_grantor, querya)
                except:
                    self.grantor = []
                    pass

                self.grantor = []
                try:
                    for x in self.cur:
                        self.grantor.append(x[0])
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
                        self.grantee.append(x[0])
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
                        self.legal.append(x[0])
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
                        self.img_page.append(str(x[0])+"/"+x[1])
                except:
                    pass
            else:
                self.img_page = ""
                self.legal_1 = ""
                self.grantee_1 = ""
                self.grantor_1 = ""
                self.file_date = ""
                self.doc_type = ""
                self.instrument_date = ""

            if self.rec_type == '':
                self.saveas = str(self.year) + "-" + str(self.doc_num) + ".tif"
            else:
                self.saveas = str(self.volume) + "-" + str(self.page) + "-" \
                                    + str(self.rec_type) + ".tif"

            self.instrument.append({"did" : self.did,
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

    def create_request(self):

        querydown = "INSERT INTO logs.runsheet_requests (landman, broker, \
                    section, subdivision, block, lot, document_count) VALUES \
                    (%s, %s, %s, %s, %s, %s, %s) returning pull_id;"
        queryup = (self.username, self.broker, self.section,
                   self.subdivision, self.block, self.lot, self.doc_count
                   )
        self.cur.execute(querydown, queryup)
        self.runsheet_id = self.cur.fetchone()[0]
        self.temp = self.base + str(self.runsheet_id) + "/"
        self.dest = self.temp + "Documents/"
        self.conn.commit()

    def document_log(self):

        querydown = "INSERT INTO logs.document_log (runsheet_id, did) VALUES \
                    (%s, %s);"
        for x in self.instrument:
            queryup = (self.runsheet_id, x["did"])
            self.cur.execute(querydown, queryup)
        self.conn.commit()


    def create_folder(self):
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)

    def grab_img(self, did, saveas_1):
        self.create_folder()
        temp = self.temp
        #year is the subfolder, img_name is the file name.
        query3 = "select img_path from deed_records.img_links \
                    where did = (%s) ORDER BY img_path;"
        query4 = (did,)
        if did != "":
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
        # As parameters, pass the output file name, then the input file names in order.
            out = self.dest+saveas_1
            if len(image_names) > 0:
                print(len(image_names), image_names)
                with Image() as img:
                    try:
                        img.sequence.extend( [ Image(filename=f)
                                            for f in image_names
                                            ] )
                        img.save(filename=out)
                    except:
                        pass
            else:
                pass


    def authorize(self, username1):
        query_img = "select security_key from logs.security_keys \
                    where username = (%s);"
        query4 = (username1,)
        try:
            self.cur.execute(query_img,query4)
        except:
            print("error")
        try:
            key = self.cur.fetchone()[0]
        except:
            print("error")
        return key

    def archive(self):
        out = "/var/www/FlaskApp/FlaskApp/tmp/runsheets/"+str(self.runsheet_id)
        make_archive(out, 'zip', self.temp)
        return out

    def create_runsheet(self):
        self.create_folder()

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
        worksheet.write(0,1, self.section, formtop1)
        worksheet.write(1,0, "Subdivision:", formtop)
        worksheet.write(1,1, self.subdivision, formtop1)
        worksheet.write(2,0, "Block:", formtop)
        worksheet.write(2,1, self.block, formtop1)
        worksheet.write(3,0, "Lot:", formtop)
        worksheet.write(3,1, self.lot, formtop1)
        worksheet.write(4,0, "Landman:", formtop)
        worksheet.write(4,1, self.username, formtop1)
        worksheet.write(5,0, "Broker:", formtop)
        worksheet.write(5,1, self.broker, formtop1)
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
        workbook.close()
