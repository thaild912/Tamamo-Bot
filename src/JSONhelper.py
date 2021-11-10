import json
from tamaLINE import *


def send_normal_lines(method, line):
    if type(line) is list:
        method(line[0], line[1])
    else:
        method(line)


class JsonHelper:
    all_lines_dict = None
    info = None

    def __init__(self, filepath, info_path):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.all_lines_dict = json.load(f)
        with open(info_path, 'r', encoding='utf-8') as f:
            self.info = json.load(f)

    def normal_funcs_lines(self, ctx, func, param):
        # ex param: discovered/bath/yes = ['discovered']['bath']['yes']
        func_lines = self.all_lines_dict['command'][func]
        for servant in func_lines.keys():
            ser_obj = Servant(ctx, servant)
            lines_dict = None
            # traverse into the dict depth
            for key in param.split('/'):
                lines_dict = lines_dict[key]

            for line_type in lines_dict.keys:
                if line_type == 'start' or line_type == 'lines':
                    send_normal_lines(ser_obj.dialogbox, lines_dict[line_type])
                elif line_type == 'lines':
                    for line in lines_dict[line_type]:
                        send_normal_lines(ser_obj.convbox, line)
                elif line_type == 'knowledgebox':
                    for line in lines_dict[line_type]:
                        self.send_knowledge(ctx, ser_obj.knowledgebox, line)

    def send_knowledge(self, ctx, method, line):
        # is Ikaros
        if type(line[-1]) is bool and line[-1]:
            tag = self.info['People']['Ikaros']['Callable']
        else:
            tag = f'<@!{ctx.author.id}>'
        method(line[0], tag, line[1], line[2] if len(line >= 3) and type(line[2]) is not bool else None)



