# -*- coding:utf-8 -*-
# @time: 2022/6/28 4:45 下午
# @Author: erazhan
# @File: utils.py

# ----------------------------------------------------------------------------------------------------------------------
import json

class ner_params(object):

    def __init__(self, param_dict):

        for param_name, param_value in param_dict.items():

            if type(param_value) == str:
                exec("self.%s = '%s'" % (param_name, param_value))
                continue

            if type(param_value) in [int,float]:
                param_value = str(param_value)

            exec("self.%s = %s"%(param_name,param_value))

def get_ner_parser(param_dict):

    P = ner_params(param_dict)

    return P

def save_json_file(filename,entities,mode = "indent"):

    # 需要将mode改成w才行
    # mode = 'w'正常，如果mode = 'a'那么用read_json_file读数据时会报错,因为此时写数据是接着之前的数据写，不会覆盖原有数据
    with open(filename,encoding='utf-8',mode = 'w') as f:

        if mode == "indent":
            f.write(json.dumps(entities,indent = 4,ensure_ascii=False, sort_keys = False, separators=(',', ':') ))
        else:
            f.write(json.dumps(entities, ensure_ascii=False))
        # f.write(json.dumps(entities,indent = 4,ensure_ascii=False, sort_keys = False, separators=(',',':') ))

def read_json_file(filename):

    with open(filename,'r',encoding = 'utf-8') as f:
        data = json.loads(f.read())

    return data

def search_entity(tokens, tags, user_dict = False):

    '''
    :param tokens: ['感','冒']
    :param tags: ['B-疾病','I-疾病']
    :param user_dict: 为True时，保留：1、模型+字典识别一致的; 2、模型和规则均识别出，但位置不等只是部分交叉，则以规则为准; 3、模型或规则之一识别出，另一个为识别出的
    实际使用中，user_dict为True时，会破坏模型识别较好的结果，所以暂不考虑
    :return: {'type': '疾病', 'text': '感冒', 'offset': [0, 2]}
    '''

    assert len(tokens) == len(tags)
    model_entity_list = []
    i = 0
    while i < len(tags):

        tag = tags[i]

        if tag.startswith('B'):

            entity_type = tag[2:]
            value = tokens[i]
            start_index = i
            j = i + 1
            while j < len(tags):
                if tags[j].startswith('I') and tags[j][2:] == tag[2:]:

                    if tokens[j].startswith('##'):
                        value += tokens[j][2:]
                    else:
                        value += tokens[j]
                    i += 1
                    j += 1
                else:
                    break
            if len(value) > 1:
                one_entity = {"type": entity_type, "text": value, "offset": [start_index,start_index+len(value)]}
                model_entity_list.append(one_entity)

        elif tag.startswith("S"):
            entity_type = tag[2:]
            value = tokens[i]
            one_entity = {"type":entity_type,"text":value,"offset":[i,i+1]}
            model_entity_list.append(one_entity)

        i += 1

    model_entity_list = sorted(model_entity_list,key = lambda x:x['offset'][0])

    return model_entity_list

if __name__ == "__main__":

    tokens =['我', '爸', '突', '然', '大', '汗', '，', '还', '有', '糖', '尿', '病', ',', '头', '突', '然', '痛']
    tags = ['O', 'S-角色', 'B-症状', 'I-症状', 'I-症状', 'I-症状', 'O', 'O', 'O', 'B-疾病', 'I-疾病', 'I-疾病', 'O', 'B-症状', 'I-症状', 'I-症状', 'I-症状']
    ans = search_entity(tokens,tags)
    print(ans)
