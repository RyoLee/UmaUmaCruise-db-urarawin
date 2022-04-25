#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import copy

raw_data = {}
raw_events = {}
trans_rules = {}
rules = {}
data_cn = {}
data_jp = {
    "Charactor": {
        "☆3": {},
        "☆2": {},
        "☆1": {}
    },
    "Support": {
        "SSR": {},
        "SR": {},
        "R": {}
    }, "Skill": {
        "ノーマル": [],
        "レア": [],
        "固有": [],
        "Buff": []
    }, "Race": {
        "G1": [],
        "G2": [],
        "G3": [],
        "OP": [],
        "Pre-OP": []
    }
}
races = {
    "G1": {},
    "G2": {},
    "G3": {},
    "OP": {},
    "Pre-OP": {}
}


def loadDB():
    global raw_data
    global raw_events
    global trans_rules
    global rules
    with open('./tmp/cn.json', 'r') as f:
        trans_rules = json.load(f)
    with open('./rules.json', 'r') as f:
        rules = json.load(f)
    with open('./tmp/db.json', 'r') as f:
        raw_data = json.load(f)
    events = raw_data['events']
    for event in events:
        id = event['id']
        if not event.get('name', False):
            continue
        name = event['name']
        choiceList = event['choiceList']
        p_event = {}
        opts = list()
        count = len(choiceList)
        if count == 1:
            continue
        for opt in choiceList:
            opt_name = opt[0]
            effects = opt[1]
            effect_str = ''
            for effect in effects:
                effect_str += effect+'\n'
            effect_str = cover(effect_str).rstrip("\n")
            if '選択肢なし' == opt_name or '選択肢無し' == opt_name:
                count -= 1
            if count == 0:
                opts = None
                break
            for k in rules["addprefix"]:
                if k in opt_name:
                    effect_str = rules["addprefix"][k] + effect_str
            tmp = {}
            tmp["Option"] = opt_name
            tmp["Effect"] = effect_str
            opts.append(tmp)
        if opts != None:
            p_event[name] = opts
            raw_events[id] = p_event


def saveData():
    with open('./tmp/UmaMusumeLibrary.cn.json', 'w') as f:
        json.dump(data_cn, f, ensure_ascii=False)
    with open('./tmp/UmaMusumeLibrary.jp.json', 'w') as f:
        json.dump(data_jp, f, ensure_ascii=False)


def trans(input):
    output = input
    if output in trans_rules:
        output = trans_rules[output]
    return output


def cover(input):
    output = input
    for k in rules["replace"]:
        output = output.replace(k, rules["replace"][k])
    return output


def build():
    players = raw_data['players']
    supports = raw_data['supports']
    # P cards
    p_rare = {"3": "☆3", "2": "☆2", "1": "☆1"}
    for p in players:
        name = '???'
        if 'name' in p:
            name = p["name"]                           
        charaName = p['charaName']
        rare = p['rare']
        if rare is None or rare == '':
            rare = '3'
        events = p['eventList']
        eventsJSON = {}
        eventsList = list()
        for e_id in events:
            if not raw_events.get(e_id, False):
                continue
            eventsList.append(raw_events[e_id])
        eventsJSON['Event'] = eventsList
        data_jp['Charactor'][p_rare[rare]]['['+name+']'+charaName] = eventsJSON
    # S cards
    for s in supports:
        name = '???'
        if 'name' in s:
            name = s["name"]
        charaName = s['charaName']
        rare = 'SSR'
        if 'rare' in s:
            rare = s['rare']
        events = s['eventList']
        eventsJSON = {}
        eventsList = list()
        for e_id in events:
            if not raw_events.get(e_id, False):
                continue
            eventsList.append(raw_events[e_id])
        eventsJSON['Event'] = eventsList
        data_jp['Support'][rare]['［'+name+'］'+charaName] = eventsJSON
    # buff effects
    for buff in raw_data['buffs']:
        if not 'describe' in buff or not 'name' in buff:
            continue
        item = {}
        item['Name'] = cover(buff['name']).rstrip("\n")
        item['Effect'] = buff['describe'].rstrip("\n")
        rare = 'Buff'
        data_jp['Skill'][rare].append(item)
    # build races
    for race in raw_data['races']:
        rank = race['grade']
        name = race['name']
        if '天皇賞春' == name or '天皇賞秋' == name:
            name = name[:-1]+'（'+name[-1]+'）'
        r_date = race['date'].replace("1年目 ", "ジュニア級").replace(
            "2年目 ", "クラシック級").replace("3年目 ", "シニア級")
        if name in races[rank]:
            races[rank][name]['Date'].append(r_date)
        else:
            item = {}
            item['Name'] = name
            item['Location'] = race['place']
            item['GroundCondition'] = race['ground']
            item['DistanceClass'] = race['distanceType']
            item['Distance'] = race['distance']
            item['Rotation'] = race['direction']
            item['Date'] = []
            item['Date'].append(r_date)
            races[rank][name] = item
    # cover format
    for rank in races:
        for race in races[rank]:
            if rank in data_jp['Race']:
                data_jp['Race'][rank].append(races[rank][race])
    # deepcoye
    global data_cn
    data_cn = copy.deepcopy(data_jp)
    # skill effects
    for skill in raw_data['skills']:
        if not 'describe' in skill or not 'name' in skill:
            continue
        item_jp = {}
        item_jp['Name'] = cover(skill['name']).rstrip("\n")
        value_score = 'N/A'
        if 'grade_value' in skill:
            value_score = skill['grade_value']
        item_cn = copy.deepcopy(item_jp)
        item_jp['Effect'] = cover(skill['describe']).rstrip(
            "\n") + '\nScore:' + str(value_score)
        item_cn['Effect'] = cover(trans(skill['describe'])).rstrip(
            "\n") + '\nScore:' + str(value_score)
        rare = skill['rare']
        data_cn['Skill'][rare].append(item_cn)
        data_jp['Skill'][rare].append(item_jp)

loadDB()
build()
saveData()
