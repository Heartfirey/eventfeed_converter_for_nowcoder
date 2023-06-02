import os
import json
import csv
import time
import yaml
import pandas as pd
contests_id = 1
DEBUG = False
start_time = "2000-01-01 00:00:00"
style = r"%Y-%m-%d %H:%M:%S"
tool_cfg = dict()
affiliations_id_list = list()
affiliations_id2name_dict = dict()      # The map of affiliations id and name
affiliations_name2id_dict = dict()      # The map of affiliations name and id
affiliations_id2teamicpcid_dict = dict()      # The map-list of affliations id and teams icpc id


def parser_config(config_dir: str = './tool_config.yaml') -> None:
    global tool_cfg
    with open(config_dir, 'r', encoding='utf8') as file:
        tool_cfg = yaml.safe_load(file)
    print("Detecting config files...")
    const_keys = ['contest_config', 'problem_config', 'status_config', 'groups_config', 'organizations_info', 'teams_info', 'submissions_info']
    for each_keys in const_keys:
        if each_keys not in tool_cfg.keys():
            raise IOError(f"Cannot detect target config: {each_keys}")
        if not os.path.exists(tool_cfg[each_keys]):
            raise IOError(f'Target config file {each_keys} -> ({tool_cfg[each_keys]}) not exists!')
    print("OK.")
    
def contests_converter(token=0) -> list:
    with open(tool_cfg['contest_config'], 'r', encoding='utf8') as file:
        contests_info = yaml.safe_load(file)
    contests_dict = {"id": "1", "type": "contest", "op":"create", "data": contests_info}
    # Update contests start time
    global start_time
    timeArray = time.strptime(contests_info['start_time'], "%Y-%m-%dT%H:%M:%S.000+08:00")
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("Runnning on contests:", contests_info['name'])
    print("Contests duration:", contests_info['duration'])
    print("Scoreboard freeze duration: ", contests_info['scoreboard_freeze_duration'])
    if DEBUG: print(contests_dict)
    return contests_dict

def add_head():
    head_list = list()
    head_list.append({"id":"2","type":"judgement-types","op":"create","data":{"id":"AC","name":"correct","penalty":False,"solved":True}})
    head_list.append({"id":"3","type":"judgement-types","op":"create","data":{"id":"CE","name":"compiler error","penalty":False,"solved":False}})
    head_list.append({"id":"4","type":"judgement-types","op":"create","data":{"id":"MLE","name":"memory limit","penalty":True,"solved":False}})
    head_list.append({"id":"5","type":"judgement-types","op":"create","data":{"id":"NO","name":"no output","penalty":True,"solved":False}})
    head_list.append({"id":"6","type":"judgement-types","op":"create","data":{"id":"OLE","name":"output limit","penalty":True,"solved":False}})
    head_list.append({"id":"7","type":"judgement-types","op":"create","data":{"id":"RTE","name":"run error","penalty":True,"solved":False}})
    head_list.append({"id":"8","type":"judgement-types","op":"create","data":{"id":"TLE","name":"timelimit","penalty":True,"solved":False}})
    head_list.append({"id":"9","type":"judgement-types","op":"create","data":{"id":"WA","name":"wrong answer","penalty":True,"solved":False}})
    head_list.append({"id":"10","type":"languages","data":{"id":"c","name":"C","entry_point_required":False,"extensions":["c"]}})
    head_list.append({"id":"11","type":"languages","data":{"id":"cpp","name":"C++","entry_point_required":False,"extensions":["cpp","cc","cxx","c++"]}})
    head_list.append({"id":"12","type":"languages","data":{"id":"java","name":"Java","entry_point_required":False,"entry_point_name":"Main class","extensions":["java"]}})
    head_list.append({"id":"13","type":"languages","data":{"id":"python3","name":"Python 3","entry_point_required":False,"entry_point_name":"Main file","extensions":["py","py3"]}})
    return head_list


def groups_converter(token_st):
    groups_list = list()
    with open(tool_cfg['groups_config'], "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "groups_name": continue
            if row[2] == "1":
                groups_list.append({"id": f"{token_st}", "type": "groups", "op":"create", "data": {"id": row[0], "name": row[1], "hidden": True}})
            else:
                groups_list.append({"id": f"{token_st}", "type": "groups", "op":"create", "data": {"id": row[0], "name": row[1]}})
            token_st += 1
    if DEBUG: print(groups_list)
    return groups_list, token_st


def organizations_converter(token_st):
    organizations_list = list()
    with open(tool_cfg['organizations_info'], "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "id": continue
            affiliations_id_list.append(row[0])         # Add current organization id to affiliation list
            affiliations_id2name_dict[row[0]] = row[1]  
            affiliations_name2id_dict[row[1]] = row[0]
            organizations_list.append({
                "id": str(token_st), 
                "type": "organizations",
                "op":"create",
                "data": {
                    "id": row[0],
                    "name": row[1],
                    "formal_name": row[2],
                    "logo": [
                        {
                            "href": f".\\contest_export\\organizations\\{row[0]}\\logo",
                            "filename": "logo.png",
                            "mime": "image/png",
                            "width": 64,
                            "height": 64
                        }
                    ]
                },
            })
            token_st += 1
    if DEBUG: print(organizations_list)
    return organizations_list, token_st


def teams_converter(token_st):
    teams_list = list()
    with open(tool_cfg['teams_info'], "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "team_id": continue
            current_team_id = row[0]
            current_team_name = row[1]
            current_team_icpc_id = f"nowcoder_{current_team_id}"
            current_team_affiliations_id = row[3]
            current_team_affiliations_name = affiliations_id2name_dict[current_team_affiliations_id]
            if current_team_affiliations_id not in affiliations_id2teamicpcid_dict.keys():
                affiliations_id2teamicpcid_dict[current_team_affiliations_id] = list()
            affiliations_id2teamicpcid_dict[current_team_affiliations_id].append(current_team_icpc_id)
            teams_list.append({
                "id": str(token_st), 
                "type": "teams",
                "op":"create",
                "data": {
                    "id": current_team_id,
                    "icpc_id": current_team_icpc_id,
                    "label": current_team_id,
                    "name": current_team_name,
                    "display_name": current_team_name,
                    "group_ids": [
                        row[2]
                    ],
                    "organization_id": current_team_affiliations_id,
                    "affiliation": current_team_affiliations_name,
                    "photo": [
                        {
                            "href": "contests/4/teams/1/photo",
                            "filename": "photo.jpg",
                            "mime": "image/jpeg",
                            "width": 960,
                            "height": 640
                        }
                    ]
                },
            })
            token_st += 1
    if DEBUG: print(teams_list)
    return teams_list, token_st


def state_generater(token_st):
    state_list = list()
    with open(tool_cfg['status_config'], 'r', encoding='utf8') as file:
        state_info = yaml.safe_load(file)
        state_list.append({"id": str(token_st), "type": "state", "op":"create", "data": {"started": state_info['started']}})
        state_list.append({"id": str(token_st + 1), "type": "state", "op":"create", "data": {"started": state_info['started'], "frozen": state_info['frozen']}})
        state_list.append({"id": str(token_st + 2), "type": "state", "op":"create", "data": {"started": state_info['started'], "frozen": state_info['frozen'],"ended": state_info['ended']}})
        token_st += 3
    if DEBUG: print(state_list)
    return state_list, token_st


def problem_converter(token_st):
    problem_list = list()
    with open(tool_cfg['problem_config'], 'r', encoding='utf8') as file:
        pbinfo = yaml.safe_load(file)
        # print(pbinfo)
    problem_count = pbinfo['problem_number']
    for i in range(1, problem_count + 1):
        current_problem = pbinfo[f'problem{i}']
        problem_list.append({
            "id": str(token_st), 
            "type": "problems",
            "op":"create",
            "data": {
                "id": current_problem['id'],
                "label": current_problem['label'],
                "name": current_problem['name'],
                "ordinal": current_problem['ordinal'],
                "color": current_problem['color'],
                "rgb": current_problem['rgb'],
                "test_data_count": current_problem['test_data_count'],
                "time_limit": current_problem['time_limit']
            }
        })
        token_st += 1
    if DEBUG: print(problem_list)
    return problem_list, token_st


def submission_and_judgements_converter(token_id):
    data_list = list()
    data = pd.read_csv(tool_cfg['submissions_info'],  usecols=["id","user_id", "problem_id","status","created_date"])
    cnt, run_cnt = 0, 0
    for _, row in data.iterrows():
        timeArray = time.strptime(row[4],style)
        judgements_start_time = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00", timeArray)
        judgements_ended_time = time.strftime("%Y-%m-%dT%H:%M:%S.901+08:00", timeArray)
        # Calculate the time delta
        delta_time_count = time.mktime(timeArray) - time.mktime(time.strptime(start_time,r"%Y-%m-%d %H:%M:%S"))
        # Calculate the start, running and end time
        start_contest_time = "%1d:%02d:%02d.001" % (int(delta_time_count//3600) ,int((delta_time_count - delta_time_count//3600 * 3600) // 60), int(delta_time_count%60))
        run_contest_time = "%1d:%02d:%02d.301" % (int(delta_time_count//3600) ,int((delta_time_count - delta_time_count//3600 * 3600) // 60), int(delta_time_count%60))
        end_contest_time = "%1d:%02d:%02d.901" % (int(delta_time_count//3600) ,int((delta_time_count - delta_time_count//3600 * 3600) // 60), int(delta_time_count%60))
        # Parase judge status
        status = "WA"
        state_map = {
            3: "RTE",
            4: "WA",
            5: "AC",
            6: "TLE",
            7: "MLE",
            12: "CE",
        }
        
        if row[3] in state_map.keys():
            status = state_map[row[3]]
        
        if row[3] == 12:
            assert status == "CE"
        if row[3] == 5:
            assert status == "AC"

        # Step1. Add submission info
        data_list.append({
            "id": str(token_id), 
            "type": "submissions",
            "op":"create",
            "data": {
                "id": str(int(row[0])),
                "problem_id": str(row[2]),
                "team_id": str(int(row[1])),
                "language_id": "cpp",
                "files": [],
                "contest_time": start_contest_time,
                "time": judgements_start_time
            }
        })
        token_id += 1
        
        # Step2. Add Judgemets-1
        data_list.append({
            "id": str(token_id), 
            "type": "judgements",
            "op":"create",
            "data": {
                "id": str(cnt),
                "submission_id": str(row[0]),
                "start_contest_time": start_contest_time,
                "start_time": judgements_start_time,
                "judgement_type_id": None
            }
        })
        token_id += 1
        
        # Step3. Add runs info
        data_list.append({
            "id": str(token_id), 
            "type": "runs",
            "op":"create",
            "data": {
                "id": str(row[0]),
                "judgement_id": str(cnt),
                "judgement_type_id": status,
                "ordinal": 1,
                "run_time": 0.1,
                "contest_time": run_contest_time,
                "time": judgements_start_time
            }
        })
        token_id += 1
        
        # Step4. Add Judgements-2
        data_list.append({
            "id": str(token_id), 
            "type": "judgements",
            "op":"update",
            "data": {
                "id": str(cnt),
                "submission_id": str(row[0]),
                "judgement_type_id": status,
                "max_run_time": 0.1,
                "start_contest_time": start_contest_time,
                "start_time": judgements_start_time,
                "end_contest_time": end_contest_time,
                "end_time": judgements_ended_time
            }
        })
        
        run_cnt += 1
        cnt += 1
        token_id += 1
    if DEBUG: print(data_list)
    return data_list, token_id

def make_json(base_directory: str = '.\\contest_export'):
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

    with open(os.path.join(base_directory, './eventfeed.json'), 'a+') as obj:
        for each_event in final_json:
            current_event = json.dumps(each_event)
            current_event += '\n'
            # print(current_event)
            obj.write(current_event)

def generate_resolver_directory_structure(base_directory: str = '.\\contest_export'):
    if os.path.exists(base_directory):
        raise IOError(f'{base_directory} has already exists, please delete it first!')
    # Make base directory
    os.makedirs(base_directory)
    # Make directory structure
    # folder_structures = ['contest', 'organizations', 'teams']
    # for each_folder in folder_structures:
    #     os.makedirs(os.path.join(base_directory, each_folder))
    

def generate_organization_logo_dir(base_directory: str = '.\\contest_export') -> None:
    print("Generating affiliation logo directory structure...")
    for current_affiliation_id in affiliations_id_list:
        current_affiliation_name = affiliations_id2name_dict[current_affiliation_id]
        current_affiliation_team_number = len(affiliations_id2teamicpcid_dict[current_affiliation_id])
        if current_affiliation_team_number <= 0:
            print(f'{current_affiliation_name} has zero teams, so skiped.')
            return None
        current_affiliation_example_team_icpcid = affiliations_id2teamicpcid_dict[current_affiliation_id][0]
        gen_path = os.path.join(base_directory, 'organizations', current_affiliation_example_team_icpcid)
        os.makedirs(gen_path)
        print(f"Affiliation '{current_affiliation_name}'(id-{current_affiliation_id}) will using {gen_path} as its logo path!")
        
        
def show_tool_info(version) -> None:
    print(f"===========|==========================================|===========")
    print(f"===========| ICPC Resolvers Eventfeed Converter V{version} |===========")
    print(f"===========|   Writen by HeartFireY, maomao, Lansong  |===========")
    print(f"===========|==========================================|===========")

if __name__ == "__main__":
    show_tool_info('0.0.1')
    parser_config()
    generate_resolver_directory_structure()
    make_json()
    # generate_organization_logo_dir()