#!/usr/local/bin/python
# coding: utf-8
import numpy as np
import pandas as pd

# global variable
_keywords_file = './keywords_dic.txt'
_courses_file = './courses.csv'

def load_keywords(f):
    with open(f, 'r', encoding='utf-8') as fd:
        data = fd.read()

    data = [i.split(',') for i in data.splitlines()]
    for n, i in enumerate(data):
        if len(i) == 2:
            continue

        msg = u'%s must follow <keyword>, <label> in each line.\n' % f
        msg += u'for example:\n\n'
        msg += u'兩性, 性別平等\n'
        msg += u'性別, 性別平等\n'
        msg += u'素養, 公民素養\n'
        msg += u'人權, 人權法治\n'
        msg += u'...\n\n'
        msg += u'The error happens on line %i:\n%s\n' % (n, ','.join(i))

        raise ValueError('\n\n########\n' + msg + '\n########\n')

    R = {}
    for i, j in data:
        i = i.strip()
        j = j.strip()

        x = R.get(j, set())
        x.add(i)
        R[j] = x
    return R

def load_courses(f):
    try:
        data = pd.read_csv(f)
    except:
        raise ValueError('%s must be a csv file' % f)

    if ('intro' not in data.columns) or \
       ('name' not in data.columns):

       msg = u'%s must have both "intro" and "name" fields in header.\n' % f
       msg += u'for example:\n\n'
       msg += u'name,   \tintro,    \tlabel\n'
       msg += u'油畫入門,\t油畫媒...,\t美感教育\n'
       msg += u'...\n'

       raise ValueError('\n\n########\n' + msg + '\n########\n')

    return data

def get_labels(data, dictionary):
    results = []
    for i, js in dictionary.items():
        for j in js:
            if j not in data:
                continue
            results.append(i)
            break
    return results

def main():
    global _keywords_file, _courses_file

    dic = load_keywords(_keywords_file)
    courses = load_courses(_courses_file)

    predict_labels = []

    for i, j in zip(courses['intro'], courses['name']):
        labels = get_labels(i, dic) + get_labels(j, dic)
        labels = sorted(set(labels))
        labels = u'、'.join(labels) if len(labels) else u'非上述屬性'
        predict_labels.append(labels)

    courses['predict_label'] = predict_labels
    #courses.to_csv('./predict_label.csv', index=False, encoding='utf-8-sig')
    courses.to_excel('./predict_label.xlsx', index=False)

if __name__ == '__main__':
    main()
