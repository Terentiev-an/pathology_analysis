import os
from typing import Union

import pandas as pd
import aspose.words as aw

path_pdf = './pdf_docs/'
path_txt = './txt_docs/'



def pdf_to_txt(filenames: Union[tuple, list], path_to_get, path_to_save) -> None:
    for filename in filenames:
        pdf = aw.Document(path_to_get+filename)
        pdf.save(f'{path_to_save}{filename}.txt')
    return


def get_info_from_text(filenames: Union[tuple, list], path) -> dict:
    data = dict()
    patient_id = dict()
    for patient_number, filename in enumerate(filenames):
        f = open(path+filename,'r').read().splitlines()

        for row_number, row in enumerate(f):

            if 'ФИО' in row:
                patient = ' '.join(row.split()[2:])
                patient_id[patient_number] = patient
                data[patient_number] = dict()


            if 'Дата рождения' in row:

                birth_date = row.split()[2]
                data[patient_number]['birth_date'] = birth_date

                start = row.find('(') + 1
                end = row.find(')')
                
                dates = ' '.join(x for x in row[start:end].split() if x.replace('(', '').replace(')','').isdigit()).split()
                dates = list(map(int, dates))
                
                if len(dates) == 1:
                    days = dates[0]
                    months = 0
                    years = 0
                    
                elif len(dates) == 2:
                    days = dates[1]
                    months = dates[0]
                    years = 0
                    
                elif len(dates) == 3:
                    days = dates[2]
                    months = dates[1]
                    years = dates[0]
   
                data[patient_number]['age_admission(y,m,d)'] = (years,months,days)

            if 'Клинический диагноз' in row:
                start = row.find('диагноз:')
                diagnosis = ' '.join(row[start:].split()[1:])
                data[patient_number]['input_diagnosis'] = diagnosis

            if 'МИКРОСКОПИЧЕСКОЕ ОПИСАНИЕ' in row:
                start_row_number = row_number + 1

            if 'ЗАКЛЮЧЕНИЕ' in row:
                end_row_number = row_number
                data[patient_number]['microscop_desc'] = ' '.join(f[start_row_number:end_row_number])
                data[patient_number]['conclusion'] = f[end_row_number + 1]
            

                
    return data, patient_id




filenames_pdf = os.listdir(path_pdf)
pdf_to_txt(filenames_pdf, path_pdf, path_txt)

filenames_txt = os.listdir(path_txt)
data, patient_names = get_info_from_text(filenames_txt, path_txt)
data = pd.DataFrame.from_dict(data, orient = 'index')
patient_names = pd.DataFrame.from_dict(patient_names, orient = 'index')

patient_names.to_csv('../data/patient_names.csv', header = True, index = True)
data.to_csv('../data/patient_data.csv', header = True, index = True)
