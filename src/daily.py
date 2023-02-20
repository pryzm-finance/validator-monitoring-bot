import requests
import datetime
from telegramBot import botMsg,verboseMsg
from functions import get_config_dict,manage_exception,print_and_save_error,get_updated_proposal_ids,get_proposals_votes_url,get_proposal_details
    


validator_configs=get_config_dict()


def get_active_proposal_details(validator_name,count=0):
    try:
        active_proposal_list=get_updated_proposal_ids(validator_name)['data']
        return_dict={validator_name:{}}
        for proposal_id in active_proposal_list:
            proposal_detail=get_proposal_details(validator_name,proposal_id)
            end_time = getDateTime(proposal_detail['proposal']['voting_end_time'])
            if datetime.datetime.now()<=end_time:
                return_dict[validator_name][proposal_id]={}
                prop=proposal_detail['proposal']
                voted=False
                vote="-"
                resp_json = dict(requests.get(get_proposals_votes_url(validator_name,proposal_id)).json())
                if 'vote' in resp_json.keys():
                    voted=True
                    if 'option' in resp_json['vote'].keys():
                        vote=resp_json['vote']['option']
                return_dict[validator_name][proposal_id]={'title':prop['content']['title'],"start time":str(getDateTime(prop['voting_start_time'])),
                                          "end time":str(getDateTime(prop['voting_end_time'])),"voted by PRISM":voted,"vote":vote,'validator':validator_name}
        return return_dict
            
    except Exception as e:
        count+=1
        manage_exception(e)
        print_and_save_error("get_active_proposal_details exception")
        # return get_proposal_votes_response(count=count)
        return return_dict
    

def getDateTime(time_str):
    try:
        time_splitted=str(time_str).split(".")[0]
        return_time = datetime.datetime.strptime(time_splitted, '%Y-%m-%dT%H:%M:%S')
        return return_time
    except Exception as e:
        # manage_exception(e)
        print_and_save_error("*exception in getDateTime of {}".format(time_str))
        # return get_proposal_votes_response(count=count)
    
def get_report_summary(validator_name,active_proposals_dict):
    try:
        msg="Active proposals report of {} validator:\n".format(validator_name)
        count=1
        validator_active_proposals_dict=active_proposals_dict[validator]
        for proposal_id,proposal_detail in validator_active_proposals_dict.items():
            
            msg+="#{}\nValidator: {}\nProposal id: {}\nTitle: {}\nStart Time: {}\nEnd Time: {}\nVoted by PRISM: {}\n".format(count,proposal_detail['validator'], proposal_id, proposal_detail['title'], proposal_detail['start time'], proposal_detail['end time'], proposal_detail['voted by PRISM'])
            if proposal_detail['voted by PRISM']==True:
                msg+="Vote: {}\n".format(proposal_detail['vote'])
            count+=1
        if len(validator_active_proposals_dict)==0:
            msg+="No active Proposal to vote!\n"
        msg+="#Daily_Report_{}".format(validator_name)
        botMsg(msg)
    except Exception as e:
        # manage_exception(e)
        print_and_save_error("*exception in get_report_summary of {}".format(active_proposals_dict))
        manage_exception(e)
    

for validator in validator_configs.keys():
    get_report_summary(validator,get_active_proposal_details(validator))