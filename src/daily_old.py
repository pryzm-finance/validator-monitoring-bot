import requests
import datetime
from telegramBot import botMsg,verboseMsg
from error_handling import manage_exception,print_and_save_error
def get_proposals_votes_url():
    return_url="https://extraterra-assets.s3.us-east-2.amazonaws.com/terra/gov/recent-valiator-votes.json"
    return return_url

def get_proposal_terrascope_url(proposal_id):
    return "https://terrasco.pe/mainnet/governance/proposal/{}".format(proposal_id)

def get_active_proposal_details(count=0):
    prism_address="terravaloper18vnm040mwk0d6plc60v5m9h2376gkcphknuwzs"
    try:
        resp_json = requests.get(get_proposals_votes_url()).json()
        return_dict={}
        for proposal in resp_json:
            proposal_id=proposal['proposal']['proposal_id']
            end_time = getDateTime(proposal['proposal']['voting_end_time'])
            if datetime.datetime.now()<=end_time:
                return_dict[proposal_id]={}
                prop=proposal['proposal']
                voted=False
                vote="-"
                if 'option' in proposal['votes_by_validator'][prism_address].keys():
                    voted=True
                    vote=proposal['votes_by_validator'][prism_address]['option']
                return_dict[proposal_id]={'title':prop['content']['title'],"start time":str(getDateTime(prop['voting_start_time'])),
                                          "end time":str(getDateTime(prop['voting_end_time'])),"voted by PRISM":voted,"vote":vote}
        return return_dict
    except Exception as e:
        count+=1
        manage_exception(e)
        print_and_save_error("get_active_proposal_details exception")
        # return get_proposal_votes_response(count=count)
        print("*3")
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
    
def get_report_summary(active_proposals_dict):
    try:
        msg="Active Proposals Report:\n"
        count=1
        for proposal_id,proposal_detail in active_proposals_dict.items():
            
            msg+="*****{}*****\nProposal id: {}\nTitle: {}\nStart Time: {}\nEnd Time: {}\nVoted by PRISM: {}\n".format(count,proposal_id, proposal_detail['title'], proposal_detail['start time'], proposal_detail['end time'], proposal_detail['voted by PRISM'])
            if proposal_detail['voted by PRISM']==True:
                msg+="Vote: {}\n".format(proposal_detail['vote'])
            count+=1
        if len(active_proposals_dict)==0:
            msg+="No active Proposal to vote!\n"
        msg+="#Daily_Report"
        verboseMsg(msg)
    except Exception as e:
        # manage_exception(e)
        print_and_save_error("*exception in get_report_summary of {}".format(active_proposals_dict))
        manage_exception(e)
    
    
get_report_summary(get_active_proposal_details())