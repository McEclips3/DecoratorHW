from pprint import pprint
import re
# Читаем адресную книгу в формате CSV в список contacts_list:
import csv

from arglogger import logger


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pattern = r'(\+7|8)?\s?\(?(\d{3})\)?\D*?(\d{3})([\s-]+)?(\d{2})([\s-]+)?(\d{2})(\s*\(?([доб\.]*)(\s*)(\d{4})\)?)?'
subst_pattern = r'+7(\2)\3-\5-\7\10\9\11'


def fix_phone(raw_list):
    fix_phones = []
    for i in raw_list:
        phones = re.sub(pattern, subst_pattern, i[5])
        i[5] = phones
        fix_phones.append(i)
    return fix_phones


def fix_name(fix_numbers):
    fix_names = []
    for i in fix_numbers:
        fullname = i[0] + ' ' + i[1] + ' ' + i[2]
        fullname_list = fullname.split()
        if len(fullname_list) < 3:
            fullname_list.append('')
        i[0] = fullname_list[0]
        i[1] = fullname_list[1]
        i[2] = fullname_list[2]
        fix_names.append(i)
    return fix_names


@logger(log_path='log_cotacts.log')
def fix_duplicates(fix_names):
    contacts_dict = {}

    for contact in fix_names:
        full_name = f'{contact[0]} {contact[1]}'
        if contacts_dict.get(full_name):
            for pos, field in enumerate(contact):
                if field == '':
                    continue
                contacts_dict[full_name][pos] = field
        else:
            contacts_dict[full_name] = contact

    fix = [contact for contact in contacts_dict.values()]
    return fix


fixed_phones = fix_phone(contacts_list)
fixed_names = fix_name(fixed_phones)
fixed_list = fix_duplicates(fixed_names)
pprint(fixed_list)


# 1. Выполните пункты 1-3 задания.
# Ваш код

# 2. Сохраните получившиеся данные в другой файл.
# Код для записи файла в формате CSV:
# with open("phonebook.csv", 'w', encoding='utf8') as f:
#     datawriter = csv.writer(f, delimiter=',')
#
#     # Вместо contacts_list подставьте свой список:
#     datawriter.writerows(fixed_list)


# (\+7|8)?\s?\(?(\d{3})\)?\D*?(\d{3})([\s-]+)?(\d{2})([\s-]+)?(\d{2})(\s*\(?([доб\.]*)(\s*)(\d{4})\)?)?
#
# +7(\2)\3-\5-\7\10\9\11
