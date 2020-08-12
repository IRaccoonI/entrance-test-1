import pandas as pd
import re

def find_most_low_quality_of_tutors(tutors):
    res = None
    for tutor_id, data in tutors.items():
        cur_average_score = data['sum_quality'] / data['number_of_lesson']
        if res == None or res['average_score'] > cur_average_score:
            res = {'tutor_id': tutor_id, 'average_score': cur_average_score}
    return res

# regex to search in string for year, month and day only
find_date = re.compile('\d{4}-\d{2}-\d{2}')

# dict where key-day and value-dict of tutors with count of lesson and summ of quality
date_dict = {}

# read *.txt files as pandas DataFrame
def my_cvs_reader(file_name):
    return pd.read_csv(file_name, sep=r'\s*\|\s*', engine='python')[1:-1]

lessons = my_cvs_reader('./lessons.txt')
users = my_cvs_reader('./users.txt')
quality = my_cvs_reader('./quality.txt')
participants = my_cvs_reader('./participants.txt')

# loop for find tutor of lesson and update date_dict
for ind, les_row in lessons.iterrows():
    if les_row['subject'] != 'phys':
        continue
    les_participants = participants.loc[participants['event_id'] == str(int(les_row['event_id']))]['user_id']

    les_quality = quality.loc[quality['lesson_id'] == les_row['id']]['tech_quality'][:1]
    if les_quality.empty or les_quality.isnull().values.any():
        continue
    les_quality = int(les_quality)

    for i in les_participants:
        if (users.loc[users['id'] == i]['role'] == 'tutor').all():
            les_tutor = i
            break
    else:
        raise Exception('teacher of lesson not found, lesson id: %s' % les_row['id'])

    les_data = find_date.findall(les_row['scheduled_time'])[0]

    if not les_data in date_dict:
        date_dict[les_data] = {}
    
    if not les_tutor in date_dict[les_data]:
        date_dict[les_data][les_tutor] = {'sum_quality': les_quality, 'number_of_lesson': 1}
    else:
        cur_record = date_dict[les_data][les_tutor]
        cur_record['sum_quality'] += les_quality
        cur_record['number_of_lesson'] += 1

# dict for create res pandas DataFrame
tmp_dict = {'day': [], 'tutor_id': [], 'average_score': []}

for day, tutors in date_dict.items():
    tutor_with_most_low_quality = find_most_low_quality_of_tutors(tutors)
    tmp_dict['day'].append(day)
    tmp_dict['tutor_id'].append(tutor_with_most_low_quality['tutor_id'])
    tmp_dict['average_score'].append(tutor_with_most_low_quality['average_score'])

res_df = pd.DataFrame(tmp_dict).sort_values(by=['day'])

print(res_df)
