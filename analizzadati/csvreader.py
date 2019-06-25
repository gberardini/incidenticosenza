import csv


with open('../../dati incidenti secondo semestre 2013.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    # print(str(csv_reader))
    # line_count = 0
    for row in csv_reader:
        print(row["Data"])
        #break

    #     if line_count == 0:
    #         print(f'Column names are {", ".join(row)}')
    #         line_count += 1
    #     print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
    #     line_count += 1
    # print(f'Processed {line_count} lines.')
