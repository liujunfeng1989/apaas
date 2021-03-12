# _*_ coding: utf8 _*_
import sys
import json
import markup_template


def markup_templates(app, conf='machines.yml', value_file='jagle.env'):

    with open(conf, 'r') as fr:
        lines = fr.read()
        lines_js = json.loads(lines)
        for i in app:
            if lines_js[i]:
                for temp_file in lines_js[i]:
                    markup_template.markup_templates(temp_file + ".faketpl", value_file, temp_file)
            else:
                print('bad')

    fr.close()


if __name__ == "__main__":
    apps = sys.argv[1:]
    for app in apps:
        markup_templates(apps, 'machines.yml', "jagle.env")
