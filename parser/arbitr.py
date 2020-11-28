from bs4 import BeautifulSoup
import requests
import os


def parse_civil():
    def find_plaintiff(tag):
        return tag.has_attr("class") and tag["class"] == ["plaintiff"]

    def find_court(tag):
        return tag.has_attr("class") and tag["class"] == ["respondent"]

    def find_data(tag):
        return tag.has_attr("class") and tag["class"] == ["js-rolloverHtml"]

    def filter(line: str) -> str:
        res = ""
        l = 0
        while l < len(line) and line[l] == ' ':
            l += 1
        r = len(line) - 1
        while r >= 0 and line[r] == ' ':
            r -= 1
        for i in range(l, r):
            if line[i].isalnum() or line[i].isalpha() or line[i] == ' ':
                res += line[i]
        return res

    with open("civil.html", "rb") as f:
        content = f.read()
        soup = BeautifulSoup(content, "html.parser")
        entries = soup.find_all("tr")
        data = {"court": [], "plaintiff": [], "respondent": []}
        print(len(entries))
        for e in entries:
            plaintiff = e.find(find_plaintiff)
            if plaintiff:
                plt_data = plaintiff.find(find_data).get_text()
                info = []
                for d in plt_data.split('\n'):
                    filtered = filter(d)
                    if filtered != "":
                        info.append(filtered)
                data["plaintiff"].append({'name': info[0], 'address': info[1], 'id': info[2]})


if __name__ == "__main__":
    parse_civil()
