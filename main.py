from openpyxl import load_workbook

workbook = load_workbook(filename="p.xls")
sheet = workbook['Sheet1']