#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import json
import jinja2


def markup_templates(template_file, value_file, output_file):
    if markup_templates.func_code.co_argcount != 3:
        print >> sys.stderr, 'Useage: python drive.py TEMPLATE_FILE VALUE_FILE OUTPUT_FILE'
        exit(1)

    # template_file, value_file, output_file = sys.argv[1:]

    if not os.path.isfile(template_file):
        print >> sys.stderr, 'template file %s does not exit' % template_file
        exit(1)
    if not os.path.isfile(value_file):
        print >> sys.stderr, 'value file %s does not exit' % value_file
        exit(1)

    template_content = ''
    try:
        with open(template_file) as f:
            template_content = f.read().decode('utf-8')
    except Exception as e:
        print >> sys.stderr, 'fail to read template file: ', e
        exit(1)

    ## 私有化部署场景中,不需要二次解析
    ## 加载环境变量，如果环境变量里给的 json object 也解析它
    value_dict = dict(os.environ)
    # for k in value_dict:
    #    print >> sys.stdout, "{}:{}".format(k,value_dict[k])
    #    try:
    #        value_dict[k] = json.loads(value_dict[k])
    #    except Exception as e:
    #        pass

    try:
        with open(value_file) as f:
            value_file_dict = json.loads(f.read())
            value_dict.update(value_file_dict)
    except ValueError as e:
        print >> sys.stderr, 'value file content is not a valid JSON'
        exit(1)
    except Exception as e:
        print >> sys.stderr, 'fail to read template file: ', e
        exit(1)
    template = jinja2.Template(template_content)
    output = template.render(value_dict)
    print(output)

    try:
        with open(output_file, 'w+') as f:
            f.write(output.encode('utf-8'))
    except Exception as e:
        print >> sys.stderr, 'write output file failed: ', e
