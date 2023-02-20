from datetime import datetime
import time
from configparser import ConfigParser
from telegramBot import verboseMsg
import traceback
import requests

def getNow():
    return int(datetime.now().timestamp())

def getTime():
    return str(time.strftime('%a, %d %b %Y, %H:%M:%S'))

def getTimeFromTimestamp(timestamp):
    time = datetime.fromtimestamp(timestamp)
    return str(time.strftime('%a, %d %b %Y, %H:%M:%S'))


def write_into_file(filename, content, append_bool):
    if append_bool == True:
        f = open(filename, "a")
    else:
        f = open(filename, "w")
    f.write(content)
    f.close()

def getElapsedTime(sec):
    s = int(sec) % 60
    m = int(sec / 60) % 60
    h = int(sec / 3600) % 24
    d = int(sec / (3600 * 24))
    dif = ""
    if (d > 0):
        dif += str(d) + "d, "
    dif += str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
    return dif

def get_config(category,variable=''):
    config = ConfigParser()
    config.read('./config.cfg')
    # print("******")
    # print(config.items())
    if category in config.keys():
        if len(str(variable))==0:
            return dict(config[category])
        else:
            if variable in config[category].keys():
                return config[category][variable]
            else:
                return None
    else:
        return None
def get_config_dict():
    config = ConfigParser()
    config.read('./config.cfg')
    config_dict={}
    for validator in config.keys():
        if validator!='DEFAULT':
            config_dict[validator]=dict(config[validator])
    return config_dict


def manage_exception(e):
    try:
        # print(e)
        stackTrace = traceback.format_exc()
        # print(stackTrace)
        content = "\n*****\n✓✓✓✓✓✓Start: <Handled_Exception> @ ({})\nStacktrace: \n{}\n✓✓✓✓✓✓End: </Handled_Exception>\n\n".format(getTime(), stackTrace)
        # write_into_file("error_logs", content, append_bool=True)
        verboseMsg(content)
    except:
        verboseMsg("Failed to send manage exception message")
    
def print_and_save_error(error_msg):
    try:
        return_msg="\nStart: <My_Details> @ ({})\n\t{}\nEnd: </My_Details>\n".format(getTime(),error_msg)
        # write_into_file("error_logs", return_msg, append_bool=True)
        verboseMsg(return_msg)
    except:
        verboseMsg("Failed to send print_and_save_error message")


#Monitoring functions

def get_missing_block_url():
    return_url="https://7nkwv3z5t1.execute-api.us-east-1.amazonaws.com/prod/listData?type=getPool&frequencyHour=8H&frequencyDay=10D&address=terravaloper18vnm040mwk0d6plc60v5m9h2376gkcphknuwzs&key=2mwTEDr9zXJH323M&token={}&app=LUNA".format(int(getNow()))
    return return_url

def get_proposals_url(validator_name):
    try:
        active_proposal_path="/cosmos/gov/v1beta1/proposals?proposal_status=2&pagination.limit=20&pagination.count_total=true&pagination.reverse=true&pagination.key="
        lcd_url=get_config_dict()[validator_name]['lcd_url']
        return_url="{}{}".format(lcd_url,active_proposal_path)
        return return_url
    except Exception as e:
        manage_exception(e)
        print_and_save_error("get_proposals_url exception for {}".format(validator_name))
        return None

def get_proposal_response(validator_name,count=0):
    try:
        important_keys=['proposals']
        resp_json = requests.get(get_proposals_url(validator_name)).json()
        for key in important_keys:
            if key not in dict(resp_json).keys():
                count+=1
                max=3
                print("key: {} not in response:\n\t{}".format(key,resp_json))
                time.sleep(count)
                if count>max and count%max==0:
                    verboseMsg("{} unsuccessful tries to fetch data".format(count))
                return get_proposal_response(validator_name,count=count)
        return resp_json
    except Exception as e:
        count+=1
        manage_exception(e)
        print_and_save_error("get_proposal_response exception of validator: {}".format(validator_name))
        time.sleep(5)
        if count>max and count%max==0:
            verboseMsg("{} unsuccessful tries to fetch data".format(count))
        return get_proposal_response(validator_name,count=count)


def get_updated_proposal_ids(validator_name):
    try:
        json_resp=get_proposal_response(validator_name)
        proposals_list=list(json_resp['proposals'])
        key ='proposal_id'
        id_list=[]
        for proposal in proposals_list:
            id_list.append(proposal[key])
        msg="Open Proposals List:\n\t{}".format(id_list)
        return_value={'msg':msg,'data':id_list}
        return return_value
    except Exception as e:
        manage_exception(e)
        print_and_save_error("get_updated_proposal_ids exception")
        time.sleep(3)
        return get_updated_proposal_ids(validator_name)

def get_external_response(count=0):
    try:
        important_keys=['hourlyChartData','val']
        resp_json = requests.get(get_missing_block_url()).json()
        for key in important_keys:
            if key not in dict(resp_json).keys():
                count+=1
                max=3
                print("key: {} not in response:\n\t{}".format(key,resp_json))
                time.sleep(count)
                if count>max and count%max==0:
                    verboseMsg("{} unsuccessful tries to fetch data".format(count))
                return get_external_response(count=count)
        return resp_json
    except Exception as e:
        count+=1
        manage_exception(e)
        print_and_save_error("get_external_response exception")
        return get_external_response(count=count)

def get_hourly_block_stats():
    try:
        json_resp=get_external_response()
        hourly=list(json_resp['hourlyChartData'])
        hourly.reverse()
        hourly_stats={'missed':0,'signed':0,'signedPer':0}
        hours_count=0
        table_msg="Time | Missed | Signed | Sign%\n"
        for hourdata in hourly:
            hours_count+=1
            table_msg+="{} | {} | {} | {}%\n".format(hourdata['title'],hourdata['missed'],hourdata['signed'],hourdata['signedPer'])
            for key in hourly_stats.keys():
                hourly_stats[key]+=float(hourdata[key])

        hourly_stats['signedPer']/=hours_count
        lst=[]

        table_msg+="Total stats of previous {} hours:\n{}".format(hours_count,hourly_stats)
        return_value={'msg':table_msg,'data':hourly_stats}
        return return_value
    except Exception as e:
        manage_exception(e)
        print_and_save_error("get_hourly_block_stats exception")
        time.sleep(3)
        return get_hourly_block_stats()
    


def get_proposals_votes_url(validator_name,proposal_id):
    try:
        validator_configs=get_config_dict()
        prism_addr=validator_configs[validator_name]['prism_address']
        vote_path="/cosmos/gov/v1beta1/proposals/{}/votes/{}".format(proposal_id,prism_addr)
        lcd_url=validator_configs[validator_name]['lcd_url']
        return_url="{}{}".format(lcd_url,vote_path)
        return return_url
    except Exception as e:
        manage_exception(e)
        print_and_save_error("get_proposals_url exception for {}".format(validator_name))
        return None
    
    
def get_proposal_details(validator_name,proposal_id):
    path="/cosmos/gov/v1beta1/proposals/{}".format(proposal_id)
    lcd_url=get_config_dict()[validator_name]['lcd_url']
    url="{}{}".format(lcd_url,path)
    resp_json = requests.get(url).json()
    return dict(resp_json)