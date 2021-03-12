# _*_ coding: utf8 _*_
import sys
import json
import re


def get_inventorys(conf, app):
    with open(conf, 'r') as fr:
        lines = fr.read()
        lines_js = json.loads(lines)

        for line in lines_js:
            if app in line and app == re.match(r"\b[a-z]+\b", line).group():
                for ip in line[app]:
                    print(ip)

    fr.close()


if __name__ == "__main__":
    apps = sys.argv[1:]
    for app in apps:
        get_inventorys('machines.yml', app)
