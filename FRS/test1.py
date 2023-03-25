import openpyxl

wb = openpyxl.load_workbook("Detection.xlsx")
ws = wb["Sheet1"]

jump = 2
naqw = 'A'+str(jump)
ws[naqw] = "hello"
jump = jump + 1

wb.save("Detection.xlsx")
