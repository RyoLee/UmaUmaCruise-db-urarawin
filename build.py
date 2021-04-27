#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json

raw_data = {}
raw_events = {}
trans_rule = {}
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


def loadDB():
    global raw_data
    global raw_events
    global trans_rule
    # with open('./tmp/cn.json', 'r') as f:
    #    trans_rule = json.load(f)
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
        if len(choiceList) > 3 :
            continue
        for opt in choiceList:
            effects = opt[1]
            effect_str = ''
            for effect in effects:
                effect_str += effect+'\n'
            #    effect_str += trans(effect)+'\n'
            tmp = {}
            tmp["Option"] = opt[0]
            tmp["Effect"] = effect_str.rstrip("\n")
            opts.append(tmp)
        p_event[name] = opts
        raw_events[id] = p_event


def saveData():
    with open('./UmaMusumeLibrary.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def trans(input):
    output = input
    for k in trans_rule:
        output = output.replace(k, trans_rule[k])
    return output


def build():
    players = raw_data['players']
    supports = raw_data['supports']
    p_rare = {"3": "☆3", "2": "☆2", "1": "☆1"}
    for p in players:
        name = p["name"]
        charaName = p['charaName']
        rare = p['rare']
        events = p['eventList']
        eventsJSON = {}
        eventsList = list()
        for e_id in events:
            if not raw_events.get(e_id, False):
                continue
            eventsList.append(raw_events[e_id])
        eventsJSON['Event'] = eventsList
        data['Charactor'][p_rare[rare]]['【'+name+'】'+charaName] = eventsJSON
    for s in supports:
        name = s['name']
        charaName = s['charaName']
        rare = s['rare']
        events = s['eventList']
        eventsJSON = {}
        eventsList = list()
        for e_id in events:
            if not raw_events.get(e_id, False):
                continue
            eventsList.append(raw_events[e_id])
        eventsJSON['Event'] = eventsList
        data['Support'][rare]['［'+name+'］'+charaName] = eventsJSON


loadDB()
build()
saveData()
