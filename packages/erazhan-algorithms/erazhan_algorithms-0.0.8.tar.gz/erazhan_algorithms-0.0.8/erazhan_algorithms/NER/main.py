# -*- coding:utf-8 -*-
# @time: 2022/6/28 4:45 下午
# @Author: erazhan
# @File: main.py

# ----------------------------------------------------------------------------------------------------------------------
import os
import copy
from transformers import BertTokenizer

from train import train_ner
from models import init_ner_model
from predict import eval_ner,predict_on_batch_ner
from utils import get_ner_parser,read_json_file

ner_tags = ["O","B-疾病","I-疾病","S-疾病","B-症状","I-症状","S-症状","B-角色","I-角色","S-角色"]

NER_DEFAULT_PARAM_DICT = {"gpu": 2,
                         "maxlen": 256,
                         "batch_size":32,
                         "predict_batch_size":4,
                         "learning_rate":2e-5,
                         "warmup_proportion":0.1,
                         "epochs": 1,
                         "save_steps": 500,
                         "print_steps": 20,
                         "disable": False}

NER_OTHER_PARAM_DICT = {"bert_model": "/home/zhanjiyuan/code/pretrained_model/chinese-roberta-wwm-ext",
                        "train_file": "./data/single_tags.json",
                        "eval_file": "./data/single_tags.json",
                        "output_dir": "./model_ner_test",
                        "predict_dir":"./model_ner_test",
                        "ner_tags": ner_tags,
                        "num_tags": len(ner_tags),
                        "ner_tag2id": {v:k for k,v in enumerate(ner_tags)},
                        "ner_id2tag": {k:v for k,v in enumerate(ner_tags)},
                       }


os.environ["CUDA_VISIBLE_DEVICES"] = "%d"%NER_DEFAULT_PARAM_DICT["gpu"]

def train_or_eval_from_eralgo(mode = "train"):

    param_dict = copy.deepcopy(NER_DEFAULT_PARAM_DICT)
    param_dict.update(NER_OTHER_PARAM_DICT)

    ner_args = get_ner_parser(param_dict)
    tokenizer = BertTokenizer.from_pretrained(ner_args.bert_model)

    train_data = read_json_file(param_dict["train_file"])
    eval_data = read_json_file(param_dict["eval_file"])

    train_text,train_tags,eval_text,eval_tags = [],[],[],[]

    for one_data in train_data:
        train_text.append(one_data["text"])
        train_tags.append(one_data["tags"])

    for one_data in eval_data:
        eval_text.append(one_data["text"])
        eval_tags.append(one_data["tags"])

    if mode == "train":
        kwargs = {"args": ner_args,
                  "train_text": train_text,
                  "eval_text": eval_text,
                  "train_tags": train_tags,
                  "eval_tags": eval_tags,
                  "tokenizer": tokenizer}
        train_ner(**kwargs)
    elif mode == "eval" or mode == "test":
        eval_kwargs = {"args": ner_args, "tokenizer": tokenizer}
        model = init_ner_model(ner_args, from_scratch=False)
        # eval_ner(model, text_list = eval_text, label_list = eval_tags, **eval_kwargs)
    else:
        eval_kwargs = {"args": ner_args, "tokenizer": tokenizer}
        model = init_ner_model(ner_args, from_scratch=False)

        text_list = ["上呼吸道感染","烧灼感"]
        result = predict_on_batch_ner(model, text_list, **eval_kwargs)
        print(result)

if __name__ == "__main__":

    mode = "train"
    mode = "predict"
    train_or_eval_from_eralgo(mode = mode)
