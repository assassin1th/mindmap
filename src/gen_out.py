import openpyxl
import database
from openpyxl.writer.excel import save_workbook
from openpyxl.utils import get_column_letter

def gen_outputs (db, group_len):
    wb = openpyxl.Workbook ()

    sheet = wb.create_sheet ('groups')
    masters = list (map (lambda x: x[0], db.get_column_unique_values ('master_name')))
    gen_groups (masters, group_len, db, sheet)
    gen_groups_by_mindmap_type (db, group_len, wb)

    save_workbook (wb, '../out/log.xlsx')

def gen_groups_by_mindmap_type (db, group_len, wb):
    mindmap_types = list (map (lambda x: x[0], db.get_column_unique_values ('mindmap_type')))
    print (db.get_by_prop ('master_name', 'mindmap_type', ''))
    for mindmap_type in mindmap_types:
        sheet = wb.create_sheet (mindmap_type)

        masters = list (map (lambda x: x[0], db.get_by_prop ('master_name', 'mindmap_type', mindmap_type)))
        gen_groups (masters, group_len, db, sheet)

def group_weight (group, db):
    n = len (group)
    l_group = list (group)
    sum_weight = float (0)
    for first_master in l_group:
        l_group.remove (first_master)

        first_files_set = set (map (lambda x: x[0], db.get_by_prop ('id', 'master_name', first_master)))
        for second_master in l_group:
            second_files_set = set (map (lambda x: x[0], db.get_by_prop ('id', 'master_name', second_master)))
            sum_weight += len (first_files_set.intersection (second_files_set))

    return sum_weight * 2 / (n - 1) / n
    

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
            max_master = masters[0]
            max_sim_files = set ()

            for master in masters :
                master_files = set (map (lambda x: x[0], db.get_by_prop ('id', 'master_name', master)))
                
                tmp_sim_files = sim_files.intersection (master_files)
                if len (tmp_sim_files) > len (max_sim_files):
                    max_sim_files = tmp_sim_files
                    max_master = master
            if not max_sim_files:
                if i == 0:
                    masters.remove (max_master)
                break
            
            sim_files = max_sim_files
            group.add (max_master)

            masters.remove (max_master)

        if len (group) < group_len:
            continue
        l_group = list (group)
        
        for i in range (len (l_group)):
            sheet[get_column_letter (i+1) + str (row)] = l_group[i]

        sheet[get_column_letter (group_len + 1) + str (row)] = str (sim_files)
        sheet[get_column_letter (group_len + 2) + str (row)] = str (group_weight (group, db))
        
        row += 1









            
