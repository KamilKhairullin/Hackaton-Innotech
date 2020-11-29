import json
import time

from bs4 import BeautifulSoup
import urllib.request


def parse():
    def clean(line: str) -> str:
        res = ""
        l = 0
        acceptable_symbols = ['.', '(', ')', '-', '/']
        for c in line:
            if c.isalnum() or c.isalpha() or c in acceptable_symbols:
                res += c
            if len(res) and c == ' ' and res[len(res) - 1] != ' ':
                res += ' '
        while l < len(res) and res[l] == ' ':
            l += 1
        r = len(res) - 1
        while r >= 0 and res[r] == ' ':
            r -= 1
        res = res[l: r + 1]
        return res

    def split_defendants_info(info: str) -> []:
        def_with_article = info.split(', ')
        res = []
        for dwa in def_with_article:
            defendant_data = dwa.split('. (')
            name = defendant_data[0]
            article = '(' + defendant_data[1]
            res.append((name, article))
        return res

    data = []
    for i in range(1, 156):
        url = f'https://mos-gorsud.ru/rs/zamoskvoreckij/services/cases/criminal?page={i}'
        page = urllib.request.urlopen(url).read().decode('utf-8')

        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('tbody')
        entries = table.find_all('tr')
        for e in entries:
            tds = e.find_all('td')
            case = clean(tds[0].get_text())
            defendants_with_article = clean(tds[1].get_text())
            status = clean(tds[2].get_text())
            dwas = split_defendants_info(defendants_with_article)
            for dwa in dwas:
                data.append({'defendant': dwa[0], 'article': dwa[1], 'case': case, 'status': status})
        print(f"Page {i} is parsed")
        time.sleep(1)
    with open('../financial_profile/data/trails.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    parse()
