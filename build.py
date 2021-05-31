#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json

raw_data = {}
raw_events = {}
trans_rules = {}
rules = {}
skill_effects = {}
data = {
    "Charactor": {
        "☆3": {},
        "☆2": {},
        "☆1": {}
    },
    "Support": {
        "SSR": {},
        "SR": {},
        "R": {}
    }
}
skills = {
    "Skill":{
        "ノーマル": [],
        "レア": [],
        "固有": [],
        "Buff": []
    }
}

def loadDB():
    global raw_data
    global raw_events
    global trans_rules
    global skill_effects
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
            tmp = {}
            tmp["Option"] = opt_name
            tmp["Effect"] = effect_str
            opts.append(tmp)
        if opts != None:
            p_event[name] = opts
            raw_events[id] = p_event
    for skill_effect in raw_data['effects']:
        id = skill_effect
        name = raw_data['effects'][id]['name']
        description = raw_data['effects'][id]['description']
        description = cover(trans(description)).rstrip("\n")
        skill_effects[id] = (name,description)
def saveData():
    with open('./UmaMusumeLibrary.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    with open('./SkillLibrary.json', 'w') as f:
        json.dump(skills, f, ensure_ascii=False)



def trans(input):
    output = input
    if output in trans_rules:
        output = trans_rules[output]
    return output

def cover(input):
    output = input
    for k in rules:
        output = output.replace(k, rules[k])
    return output


def build():
    players = raw_data['players']
    supports = raw_data['supports']
    p_rare = {"3": "☆3", "2": "☆2", "1": "☆1"}
    for p in players:
        name = p["name"]
        charaName = p['charaName']
        rare = p['rare']
        if rare is None or  rare == '':
            rare = '3'
        events = p['eventList']
        eventsJSON = {}
        eventsList = list()
        for e_id in events:
            if not raw_events.get(e_id, False):
                continue
            eventsList.append(raw_events[e_id])
        eventsJSON['Event'] = eventsList
        data['Charactor'][p_rare[rare]]['['+name+']'+charaName] = eventsJSON
    for s in supports:
        name = s['name']
        charaName = s['charaName']
        rare = s['rare']
        if rare is None or  rare == '':
            rare = 'SSR'
        events = s['eventList']
        eventsJSON = {}
        eventsList = list()
        for e_id in events:
            if not raw_events.get(e_id, False):
                continue
            eventsList.append(raw_events[e_id])
        eventsJSON['Event'] = eventsList
        data['Support'][rare]['［'+name+'］'+charaName] = eventsJSON
    for skill in raw_data['skills']:
        if not 'describe' in skill or not 'name' in skill:
            continue
        item={}
        item['Name'] = cover(skill['name']).rstrip("\n")
        value_score = 'N/A'
        if 'grade_value' in skill:
            value_score = skill['grade_value']
        item['Effect'] = cover(trans(skill['describe'])).rstrip("\n") + '\nScore:' + str(value_score)
        rare = skill['rare']
        skills['Skill'][rare].append(item)
    for buff in raw_data['buffs']:
        if not 'describe' in skill or not 'name' in buff:
            continue
        item={}
        item['Name'] = cover(buff['name']).rstrip("\n")
        item['Effect'] = buff['describe'].rstrip("\n")
        rare = 'Buff'
        skills['Skill'][rare].append(item)
loadDB()
build()
saveData()
