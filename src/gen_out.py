import openpyxl
import database
from openpyxl.writer.excel import save_workbook

def gen_outpuths (db, group_len)
    wb = openpyxl.Workbook ()

    sheet = wb.create_sheet ('groups')
    masters = list (map (lambda x: x[2], db.get_data_by_prop ('master_name')))
    gen_groups (masters, group_len, db, sheet)

    save_workbook (wb, '../out/log.xlsx')
    

def gen_groups (masters, group_len, db, sheet):
    for i in range (group_len):
        sheet[get_column_letter (i + 1) + '1'] = 'чел №' + str (i)

    sheet[get_column_letter (group_len + 1) + '1'] = 'общие'
    sheet[get_column_letter (group_len + 2) + '1'] = 'вес группы'

    row = 2
    while len (masters) >= group_len:
        sim_files = set (map (lambda x: x[0], db.get_data_by_prop ('id')))
        group = set ()

        for i in range (group_len):
            max_master = None
            max_sim_files = set ()

            for master in masters :
                master_files = set (map (lambda x: x[0], db.get_by_prop ('id', 'master_name', master)))
                
                tmp_sim_files = sim_files.intersection (master_files)
                if len (tmp_sim_files) > len (max_sim_files):
                    max_sim_files = tmp_sim_files
                    max_maset = master
            sim_files = max_sim_files
            group.add (max_master)
            masters.remove (max_master)

        for i in range (group_len)
            sheet[get_column_letter (i+1) + str (row)] = group[i]

        sheet[get_column_letter (group_len + 1) + str (row)] = str (sim_files)
        sheet[get_column_letter (group_len + 2) + str (row)] = str (group_wight (group, db))
        
        row += 1

def groub_weight (group, db):
    n = len (group)

    sum_weight = float (0)
    for first_master in group:
        group.remove (master)

        first_files_set = set (map (lambda x: x[0], db.get_by_prop ('id', 'master_name', first_master)))
        for second_master in group:
            second_files_set = set (map (lambda x: x[0], db.get_by_prop ('id', 'master_name', second_master)))
            sum_weight += len (first_files_set.intersection (second_files_set))

    return sum_weight * 2 / (n - 1) / n










            
