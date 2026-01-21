import msvcrt


checklist = {}

checklist['Adult children in household'] =\
"""    +include [People] [Households] [is a member]
AND +include [People] [Adult/Child] [is] [Adult]
AND +include [People] [Birthdate (with year)] [on or after] [9/1/2005]"""

checklist['Extremely old'] =\
"""+include [People] [Age] [at least] [120] [years]"""

checklist['Households with 3+ adults'] =\
"""Household Filter:
    Adults: At least [3] parent/guardians
    Children: At least [1] child"""

checklist['Invalid email address'] =\
"""+include [People] [Email address] [Any Type] [contains] [lcbcsgc@gmail.com]"""

checklist['Mislabeled adults'] =\
"""    Rule 1
        +include [People] [Adult/Child] [is] [Adult]
AND Rule 2
           +include [People] [Grade] [is set]
        OR +include [People] [Age] [at most] [18] [years]

* For more accurate result, replace the age rule with:
    +include [People] [Birthdate (with year) [on or after] [9/1/YYYY]"""

checklist['Mislabeled children'] =\
"""    +include [People] [Adult/Child] [is] [Child]
AND +include [People] [Age] [at least] [18] [years]

* For more accurate result, replace age rule with:
    +include [People] [Birthdate (with year)] [on or before] [8/31/YYYY]"""


def print_checklist_item(title, detail):
	print(title)
	print('-' * 30)
	print(detail)
	print()
	print()

def prompt_for_continue():
	print('(continue)', end='\n', flush=True)
	msvcrt.getch()

def remove_continue_prompt():
	print('\033[F\033[K')


print('Check using PCO People:\n')

for title, detail in checklist.items():
	print_checklist_item(title, detail)
	prompt_for_continue()
	remove_continue_prompt()
