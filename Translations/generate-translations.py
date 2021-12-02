import openpyxl
from pathlib import Path

file = Path('.', 'Tekstai.xlsx')
wb = openpyxl.load_workbook(file)
sheet = wb.active

ignore_rows = [1,2,6,10,25,35,43,48,55,63,67,70,82,91,106,108,126,140,167,171,173]
ignore_rows = [i-1 for i in ignore_rows]

lt_en = {}
lt_de = {}

# Populate dictionaries
for i_row, row in enumerate(sheet.iter_rows()):
    if i_row not in ignore_rows:
        lt_en[str(row[0].value).strip()] = str(row[1].value).strip()  # LT-EN
        lt_de[str(row[0].value).strip()] = str(row[2].value).strip()  # LT-DE

# Write to files
# LT-EN
try:
    with open('lt_en.txt', 'w') as f:
        for key, value in lt_en.items():
            msgid = 'msgid "{}"'.format(key)
            msgstr = 'msgstr "{}"'.format(value)

            translation = msgid+"\n"+msgstr+"\n\n"
            f.write(translation)
    # LT-DE
    with open('lt_de.txt', 'w') as f:
        for key, value in lt_de.items():
            msgid = 'msgid "{}"'.format(key)
            msgstr = 'msgstr "{}"'.format(value)

            translation = msgid+"\n"+msgstr+"\n\n"
            f.write(translation)
    # Success
    print('Translations successfully written to files.')
except:
    print('Error while writing to file.')