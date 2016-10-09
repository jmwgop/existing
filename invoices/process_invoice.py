import xlsxwriter
import xlrd
from glob import glob


# invoices = glob(folder+"*.xlsx")

class Invoice:
    def __init__(self, invoice):
        workbook = xlrd.open_workbook(invoice)
        sheet = workbook.sheet_by_index(0)
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        self.landman = data[0][1]
        self.dayrate = data[8][5]
        self.daysbilled = data[8][4]
        self.mileage = data[43][7]
        self.meals = data[44][7]
        self.lodging = data[45][7]
        self.phone = data[46][7]
        self.misc = data[47][7]

    # def process_invoices(invoices):
    #     workbook = xlsxwriter.Workbook(cover+"Invoice Cover 1.xlsx")
    #     worksheet = workbook.add_worksheet()
    #
    #     merge_format = workbook.add_format({
    #         'valign': 'top',
    #         'text_wrap': 'true',
    #         'font_name': 'Times New Roman',
    #         'font_size': '12'
    #     })
    #
    #
    #     header_format = workbook.add_format({
    #         'valign': 'vcenter',
    #         'align': 'center',
    #         'text_wrap': 'true',
    #         'bold': 'true',
    #         'font_name': 'Times New Roman',
    #         'font_size': '12'
    #     })
    #
    #     header_format_1 = workbook.add_format({
    #         'valign': 'vcenter',
    #         'align': 'right',
    #         'bold': 'true',
    #         'font_name': 'Times New Roman',
    #         'font_size': '12'
    #     })
    #
    #     format_1 = workbook.add_format({
    #         'valign': 'vcenter',
    #         'font_name': 'Times New Roman',
    #         'font_size': '12'
    #     })
    #
    #     format_2 = workbook.add_format({
    #         'valign': 'vcenter',
    #         'align': 'center',
    #         'font_name': 'Times New Roman',
    #         'font_size': '12'
    #     })
    #
    #     currency_format = workbook.add_format()
    #     currency_format.set_num_format('_($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_)')
    #     currency_format.set_font_size(12)
    #     currency_format.set_font_name('Times New Roman')
    #
    #     days_format = workbook.add_format()
    #     days_format.set_num_format('#,##0.00')
    #     days_format.set_font_size(12)
    #     days_format.set_font_name('Times New Roman')
    #
    #     worksheet.set_column(0, 1, 21)
    #     worksheet.set_column(2, 4, 12)
    #     worksheet.set_column(5, 5, 14.5)
    #     worksheet.set_column(5, 5, 15)
    #     worksheet.set_column(6, 11, 12)
    #
    #     worksheet.set_row(0, 32)
    #     worksheet.set_row(1, 2)
    #     worksheet.set_row(2, 2)
    #     worksheet.set_row(3, 2)
    #     worksheet.set_row(4, 20)
    #     worksheet.set_row(5, 20)
    #     worksheet.set_row(6, 20)
    #     worksheet.set_row(7, 15)
    #     worksheet.set_row(8, 15)
    #     worksheet.set_row(9, 33)
    #     worksheet.set_row(10, 10)
    #     worksheet.set_row(11, 33)
    #
    #
    #     worksheet.write(11,0,'Landman',header_format)
    #     worksheet.write(11,1,'Day Rate',header_format)
    #     worksheet.write(11,2,'Days Billed',header_format)
    #     worksheet.write(11,3,'Broker Fee',header_format)
    #     worksheet.write(11,4,'Total Day Rate',header_format)
    #     worksheet.write(11,5,'Mileage',header_format)
    #     worksheet.write(11,6,'Meals',header_format)
    #     worksheet.write(11,7,'Lodging',header_format)
    #     worksheet.write(11,8,'Phone',header_format)
    #     worksheet.write(11,9,'Misc',header_format)
    #     worksheet.write(11,10,'Total',header_format)
    #
    #     worksheet.write(4,0,'Contractor Name:', header_format_1)
    #     worksheet.write(4,1, 'WilTex Consulting, Inc.', format_1)
    #     worksheet.write(5,0,'Address:', header_format_1)
    #     worksheet.merge_range('B6:B7', 'P.O. Box 3262\nMidland, TX 79702', merge_format)
    #     worksheet.write(7,0,'Tax I.D:', header_format_1)
    #     worksheet.write(7,1,'46-5536918', format_1)
    #     worksheet.write(4,2,'State:', header_format_1)
    #     worksheet.merge_range('D5:E5','Texas', format_2)
    #     worksheet.write(5,2,'County:', header_format_1)
    #     worksheet.merge_range('D6:E6','Midland', format_2)
    #     worksheet.write(6,2,'Prospect:', header_format_1)
    #     worksheet.merge_range('D7:E7','Midland Prospect', format_2)
    #     worksheet.write(8,2,'Client Name:', header_format_1)
    #     worksheet.merge_range('D9:F10','Midland-Petro D.C. Partners, LLC\nP.O. Box 2071 \
    #                             \nMidland, TX 79702-2071', merge_format)
    #     worksheet.write(4,5,'Date Submitted:', header_format_1)
    #     worksheet.merge_range('G5:H5',date_submitted, format_2)
    #     worksheet.write(5,5,'Period Covered:', header_format_1)
    #     worksheet.merge_range('G6:H6',period_covered, format_2)
    #
    #     y = 12
    #     for x in range (0, len(landman)):
    #         worksheet.write(y,0,landman[x])
    #         worksheet.write(y,1, dayrate[x], currency_format)
    #         worksheet.write(y,2, daysbilled[x], days_format)
    #         if dayrate[x] >= 450:
    #             brokerfee = 0
    #         else:
    #             if 450 - dayrate[x] >= 75:
    #                 brokerfee = 75
    #             else:
    #                 brokerfee = 450-dayrate[x]
    #         totaldayrate = (dayrate[x]+brokerfee)*daysbilled[x]
    #         worksheet.write(y,3, brokerfee, currency_format)
    #         worksheet.write(y,4, totaldayrate, currency_format)
    #         worksheet.write(y,5, mileage[x], currency_format)
    #         worksheet.write(y,6, meals[x], currency_format)
    #         worksheet.write(y,7, lodging[x], currency_format)
    #         worksheet.write(y,8, phone[x], currency_format)
    #         worksheet.write(y,9, misc[x], currency_format)
    #         total = totaldayrate+mileage[x]+meals[x]+lodging[x]+phone[x]+misc[x]
    #         worksheet.write(y,10, total, currency_format)
    #         y+=1
    #     workbook.close()
