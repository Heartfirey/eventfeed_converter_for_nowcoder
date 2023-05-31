import json
import csv
import time

import yaml
import pandas as pd
contests_id = 1
DEBUG = False
start_time = "2022-10-23 10:00:00"
style = r"%Y-%m-%d %H:%M:%S"
# style2 = r"%Y-%m-%d, %H:%M"
def get_token_str(token_id):
    return f"cdA{token_id}"


def contests_converter(token=0) -> list:
    with open('./config/contests.yaml', 'r', encoding='utf8') as file:
        contests_info = yaml.safe_load(file)
    contests_dict = {"type": "contest", "id": f"{contests_id}", "data": contests_info, "token": f"cdA{token}"}
    print(contests_dict)
    return contests_dict

def add_head():
    head_list = list()
    head_list.append({"type":"judgement-types","id":"AC","data":{"id":"AC","name":"correct","penalty":False,"solved":True},"token":"cdA2"})
    head_list.append({"type":"judgement-types","id":"CE","data":{"id":"CE","name":"compiler error","penalty":False,"solved":False},"token":"cdA3"})
    head_list.append({"type":"judgement-types","id":"MLE","data":{"id":"MLE","name":"memory limit","penalty":True,"solved":False},"token":"cdA4"})
    head_list.append({"type":"judgement-types","id":"NO","data":{"id":"NO","name":"no output","penalty":True,"solved":False},"token":"cdA5"})
    head_list.append({"type":"judgement-types","id":"OLE","data":{"id":"OLE","name":"output limit","penalty":True,"solved":False},"token":"cdA6"})
    head_list.append({"type":"judgement-types","id":"RTE","data":{"id":"RTE","name":"run error","penalty":True,"solved":False},"token":"cdA7"})
    head_list.append({"type":"judgement-types","id":"TLE","data":{"id":"TLE","name":"timelimit","penalty":True,"solved":False},"token":"cdA8"})
    head_list.append({"type":"judgement-types","id":"WA","data":{"id":"WA","name":"wrong answer","penalty":True,"solved":False},"token":"cdA9"})
    head_list.append({"type":"languages","id":"c","data":{"id":"c","name":"C","entry_point_required":False,"extensions":["c"]},"token":"cdA10"})
    head_list.append({"type":"languages","id":"cpp","data":{"id":"cpp","name":"C++","entry_point_required":False,"extensions":["cpp","cc","cxx","c++"]},"token":"cdA11"})
    head_list.append({"type":"languages","id":"java","data":{"id":"java","name":"Java","entry_point_required":False,"entry_point_name":"Main class","extensions":["java"]},"token":"cdA12"})
    head_list.append({"type":"languages","id":"python3","data":{"id":"python3","name":"Python 3","entry_point_required":False,"entry_point_name":"Main file","extensions":["py","py3"]},"token":"cdA13"})
    return head_list


def groups_converter(token_st):
    groups_list = list()
    with open("./config/groups.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "groups_name": continue
            if row[2] == "1":
                groups_list.append(
                    {"type": "groups", "id": row[0], "data": {"id": row[0], "name": row[1], "hidden": True},
                     "token": f"cdA{token_st}"})
            else:
                groups_list.append({"type": "groups", "id": row[0], "data": {"id": row[0], "name": row[1]},
                                    "token": f"cdA{token_st}"})
            token_st += 1
    if DEBUG: print(groups_list)
    return groups_list, token_st


def organizations_converter(token_st):
    organizations_list = list()
    with open("./config/organizations.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "id": continue
            organizations_list.append({
                "type": "organizations",
                "id": row[0],
                "data": {
                    "id": row[0],
                    "name": row[1],
                    "formal_name": row[2],
                    "logo": [
                        {
                            "href": f"contests/4/organizations/{contests_id}/logo64x64",
                            "filename": "logo64x64.png",
                            "mime": "image/png",
                            "width": 64,
                            "height": 64
                        }
                    ]
                },
                "token": get_token_str(token_st)
            })
            token_st += 1
    if DEBUG: print(organizations_list)
    return organizations_list, token_st


def teams_converter(token_st):
    teams_list = list()
    with open("./config/teams.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "team_id": continue
            teams_list.append({
                "type": "teams",
                "id": row[0],
                "data": {
                    "id": row[0],
                    "label": row[0],
                    "name": row[1],
                    "display_name": row[1],
                    "group_ids": [
                        row[2]
                    ],
                    "photo": [
                        {
                            "href": "contests/4/teams/1/photo960x640",
                            "filename": "photo960x640.jpg",
                            "mime": "image/jpeg",
                            "width": 960,
                            "height": 640
                        }
                    ]
                },
                "token": get_token_str(token_st)
            })
            token_st += 1
    if DEBUG: print(teams_list)
    return teams_list, token_st


def state_generater(token_st):
    state_list = list()
    with open('./config/state_config.yaml', 'r', encoding='utf8') as file:
        state_info = yaml.safe_load(file)
        state_list.append(
            {"type": "state", "data": {"started": state_info['started']}, "token": get_token_str(token_st)})
        state_list.append({"type": "state", "data": {"started": state_info['started'], "frozen": state_info['frozen']},
                           "token": get_token_str(token_st + 1)})
        state_list.append({"type": "state", "data": {"started": state_info['started'], "frozen": state_info['frozen'],
                                                     "ended": state_info['ended']},
                           "token": get_token_str(token_st + 2)})
        token_st += 3
    if DEBUG: print(state_list)
    return state_list, token_st


def problem_converter(token_st):
    problem_list = list()
    with open('./config/problems.yaml', 'r', encoding='utf8') as file:
        pbinfo = yaml.safe_load(file)
        # print(pbinfo)
    problem_count = pbinfo['problem_number']
    for i in range(1, problem_count + 1):
        current_problem = pbinfo[f'problem{i}']
        problem_list.append({
            "type": "problems",
            "id": current_problem['id'],
            "data": {
                "id": current_problem['id'],
                "label": current_problem['label'],
                "name": current_problem['name'],
                "ordinal": current_problem['ordinal'],
                "color": current_problem['color'],
                "rgb": current_problem['rgb'],
                "test_data_count": current_problem['test_data_count'],
                "time_limit": current_problem['time_limit']
            },
            "token": get_token_str(token_st)
        })
        token_st += 1
    if DEBUG: print(problem_list)
    return problem_list, token_st


def submission_and_judgements_converter(token_id):
    data_list = list()
    data = pd.read_csv('./config/submissions.csv',  usecols=["id","user_id", "problem_id","status","created_date"])
    # if DEBUG: print(data)
    cnt = 0
    run_cnt = 0
    for i,row in data.iterrows():
        timeArray = time.strptime(row[4],style)
        # if DEBUG: print(timeArray)
        otherStyleTime = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00", timeArray)
        otherStyleTime_2 = time.strftime("%Y-%m-%dT%H:%M:%S.901+08:00", timeArray)

        const_time = time.mktime(timeArray) - time.mktime(time.strptime(start_time,r"%Y-%m-%d %H:%M:%S"))
        # print(time.mktime(timeArray), '@@@', time.mktime(time.strptime(start_time,r"%Y-%m-%d %H:%M:%S")))
        # st = "{0}:{1}:{2}".format(int(const_time//3600) ,int((const_time - const_time//3600 * 3600) // 60), int(const_time%60) )
        st = "%1d:%02d:%02d.001" % (int(const_time//3600) ,int((const_time - const_time//3600 * 3600) // 60), int(const_time%60))
        rt = "%1d:%02d:%02d.301" % (int(const_time//3600) ,int((const_time - const_time//3600 * 3600) // 60), int(const_time%60))
        ed = "%1d:%02d:%02d.901" % (int(const_time//3600) ,int((const_time - const_time//3600 * 3600) // 60), int(const_time%60))
        status = "WA"
        if row[3] == 5:
            status = "AC"
        
        # Step1. Add submission info
        data_list.append({
            "type": "submissions",
            "id": str(int(row[0])),
            "data": {
                "id": str(int(row[0])),
                "problem_id": str(row[2]),
                "team_id": str(int(row[1])),
                "language_id": "cpp",
                "files": [],
                "contest_time": st,
                "time": otherStyleTime
            },
            "token": get_token_str(token_id)
        })
        token_id += 1
        
        # Step2. Add Judgemets-1
        data_list.append({
            "type": "judgements",
            "id": str(cnt),
            "data": {
                "id": str(cnt),
                "submission_id": row[0],
                "start_contest_time": st,
                "start_time": otherStyleTime,
            },
            "token": get_token_str(token_id)
        })
        token_id += 1
        
        # Step3. Add runs info
        data_list.append({
            "type": "runs",
            "id": str(run_cnt),
            "data": {
                "id": str(row[0]),
                "judgement_id": str(cnt),
                "judgement_type_id": status,
                "ordinal": 1,
                "run_time": 0.001,
                "contest_time": rt,
                "time": otherStyleTime
            },
            "token": get_token_str(token_id)
        })
        token_id += 1
        
        # Step4. Add Judgements-2
        data_list.append({
            "type": "judgements",
            "id": str(cnt),
            "data": {
                "id": str(cnt),
                "submission_id": row[0],
                "judgement_type_id": status,
                "max_run_time": 0.001,
                "start_contest_time": st,
                "start_time": otherStyleTime,
                "end_contest_time": ed,
                "end_time": otherStyleTime_2
            },
            "token": get_token_str(token_id)
        })
        
        run_cnt += 1
        cnt += 1
        token_id += 1
    if DEBUG: print(data_list)
    return data_list, token_id

def award_converter(token_st):
    award_list = list()
    with open('./config/awards.yaml', 'r', encoding='utf8') as file:
        awards_info = yaml.safe_load(file)
    awards_number = awards_info['awards_number']
    for i in range(1, awards_number + 1):
        current_award = awards_info[f'award{i}']
        award_list.append({
            "type": "awards",
            "id": current_award['award_name'],
            "data": {
                "id": current_award['award_name'],
                "team_ids": current_award['team_list'],
                "citation": current_award['award_citation']
            },
            "token": get_token_str(token_st)
        })
        token_st += 1
    return award_list, token_st


def make_json():
    final_json = list()
    current_token = 14
    # Addd contests
    contests_info = contests_converter()
    final_json.append(contests_info)
    # Add heads
    contest_head = add_head()
    final_json += contest_head
    # Add groups
    groups_list, current_token = groups_converter(current_token)
    final_json += groups_list
    # Add organizations
    organizations_list, current_token = organizations_converter(current_token)
    final_json += organizations_list
    # Add teams
    team_list, current_token = teams_converter(current_token)
    final_json += team_list
    # Add prblems
    problem_list, current_token = problem_converter(current_token)
    final_json += problem_list
    # Add states
    state_list, current_token = state_generater(current_token)
    final_json += state_list
    # Add submission and judgements
    submission_data_list, current_token = submission_and_judgements_converter(current_token)
    final_json += submission_data_list
    # Add awards
    # award_list, current_token = award_converter(current_token)
    # final_json += award_list
    with open('./eventfeed.json', 'a+') as obj:
        for each_event in final_json:
            current_event = json.dumps(each_event)
            current_event += '\n'
            # print(current_event)
            obj.write(current_event)
        


if __name__ == "__main__":
    # problem_converter(1)
    # submission_and_judgements_converter(1)
    make_json()