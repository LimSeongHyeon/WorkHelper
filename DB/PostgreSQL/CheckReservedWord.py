from requests import *
from bs4 import BeautifulSoup
from pprint import pprint


res = request(method="GET", url="https://www.postgresql.org/docs/current/sql-keywords-appendix.html#KEYWORDS-TABLE")
soup = BeautifulSoup(res.text, 'html.parser')

table = soup.find('table', attrs={'class': 'table'})
table_headers = list(map(lambda x: x.text, table.find('thead').find_all('th')))
table_body = table.find('tbody').find_all('tr')

rows = []
for table_row in table_body:
    row = list(map(lambda x: x.text.replace(u'\xa0', u''), table_row.find_all('td')))
    rows.append(row)

def is_reserved(word):
    for row in rows:
        if word == row[0]:
            result_dict = dict(zip(table_headers, row))
            pprint(result_dict)
            print()
            return result_dict

    return None

while True:
    word = input("Check: ").upper()
    if not is_reserved(word):
        print("It is not a reserved word in postgresql.\n")

