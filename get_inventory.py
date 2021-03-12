# _*_ coding: utf8 _*_
import sys
import json
import re


def get_inventorys(conf, apps, user="admin", group="admin"):
    with open(conf, 'r') as fr:
        with open('inventory_hosts', 'w') as fw:
            lines = fr.read()
            lines_js = json.loads(lines)
            apps_list = []
            if 'full' in apps:
                for key in lines_js:
                    apps_list.append(key)
            else:
                apps_list = apps

            for line in lines_js:
                for key in apps_list:
                    if key in line and key == re.match(r"\b[a-z]+\b", line).group():
                        fw.write("[" + key + "]" + "\n")
                        for ip in lines_js[key]:
                            fw.write(ip + "\t" + "app=" + key + "\t" + "user=" + user + "\t" + "group=" + group)
                            fw.write('\n')
                        fw.write('\n')
            fw.close()
        fr.close()


if __name__ == "__main__":
    apps = sys.argv[1:]
    get_inventorys('machines.conf', apps, "admin", "admin")