import pandas as pd
import xlrd

sheet_path = "sheets/England_1209-1914_(Clark).xls"
pkl_path = "data/england_prices_wages.pkl"

wb = xlrd.open_workbook(sheet_path)
sheet = wb.sheet_by_name("main data sheet")
names = ["Year"]
i = 1
while True:
    cell_type = sheet.cell(5, i).ctype
    if cell_type == xlrd.XL_CELL_EMPTY:
        break
    good = sheet.cell_value(5, i)
    unit = sheet.cell_value(8, i)
    names.append(f"{good} ({unit})")
    i += 1


english_pence_df = pd.read_excel(
                                 sheet_path,
                                 sheet_name="main data sheet",
                                 index_col=0,
                                 usecols="A:CF",
                                 # usecols=[0, i],
                                 names=names,
                                 skiprows=9,
                             )

english_pence_df.to_pickle(pkl_path)

