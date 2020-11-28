from bs4 import BeautifulSoup
import requests
import os
import json


def parse(fname: str):
    def find_plaintiff(tag):
        return tag.has_attr("class") and tag["class"] == ["plaintiff"]

    def find_respondent(tag):
        return tag.has_attr("class") and tag["class"] == ["respondent"]

    def find_data(tag):
        return tag.has_attr("class") and tag["class"] == ["js-rolloverHtml"]

    def find_court(tag):
        return tag.has_attr("class") and tag["class"] == ["court"]

    def find_date(tag):
        return tag.has_attr("class") and tag["class"] == ["num"]

    def clean(line: str) -> str:
        res = ""
        l = 0
        acceptable_symbols = [' ', '.']
        for c in line:
            if c.isalnum() or c.isalpha() or c in acceptable_symbols:
                res += c
        while l < len(res) and res[l] == ' ':
            l += 1
        r = len(res) - 1
        while r >= 0 and res[r] == ' ':
            r -= 1
        res = res[l: r + 1]
        return res

    def involved_info(tag):
        try:
            inv_data = tag.find(find_data).get_text()
            res = []
            for d in inv_data.split('\n'):
                filtered = clean(d)
                if filtered != "":
                    res.append(filtered)
            if len(res) < 3:
                while len(res) < 3:
                    res.append(None)
            return res
        except AttributeError:
            return [None, None, None]

    data = {"respondent": [], "plaintiff": [], "court": [], "date": []}

    with open(fname, "rb") as f:
        content = f.read()
        soup = BeautifulSoup(content, "html.parser")
        entries = soup.find_all("tr")
        for e in entries:
            plaintiff = e.find(find_plaintiff)
            if plaintiff:
                info = involved_info(plaintiff)
                data["plaintiff"].append({"name": info[0], "address": info[1], "id": info[2]})
            respondent = e.find(find_respondent)
            if respondent:
                info = involved_info(respondent)
                data["respondent"].append({"name": info[0], "address": info[1], "id": info[2]})
            court = e.find(find_court)
            if court:
                court = court.find("div")
                divs = court.find_all("div")
                info = {"judge": "", "court": ""}
                if len(divs) == 2:
                    info["judge"] = clean(divs[0].get_text())
                    info["court"] = clean(divs[1].get_text())
                else:
                    info["court"] = clean(divs[0].get_text())
                data["court"].append(info)
            num = e.find(find_date)
            if data:
                num = num.find("div")
                date = clean(num.find("div").get_text())
                case = clean(num.find("a").get_text())
                data["date"] = {"date": date, "case": case}

    name = fname.split('.')[0]
    with open(f"{name}.json", "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    parse("bankrupt.html")
