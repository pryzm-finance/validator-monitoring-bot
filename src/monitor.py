import random

import time
from telegramBot import botMsg,verboseMsg
from functions import getNow, getTimeFromTimestamp,getTime, manage_exception,print_and_save_error,get_updated_proposal_ids,get_proposal_response,get_hourly_block_stats,get_config_dict


all_stats={}
initialized=0



def controller_proposals(validator_name,prev_proposal_list):
    updated_proposals=get_updated_proposal_ids(validator_name)
    proposal_id_list=list(updated_proposals['data'])
    for proposal_id in proposal_id_list:
        if proposal_id not in prev_proposal_list:
            msg='Alert: New Proposal Arrived with id: {}\nValidator: {}\nOpen Proposals:\n\t{}\n#new_proposal_to_vote #proposal_{} #{}_validator'.format(proposal_id,validator_name,updated_proposals['msg'],proposal_id,validator_name)
            print(msg)
            botMsg(msg)
            try:
                proposals_full=get_proposal_response(validator_name)['proposals']
                for proposal in proposals_full:
                    if proposal['proposal_id']==proposal_id:
                        proposal_details="Validator: {}\nid: {}\nTitle: {}\nVoting_start_time: {}\nVoting_end_time: {}\n#proposal_{} #{}_validator".format(
                            validator_name,proposal['proposal_id'],proposal['content']['title'],proposal['voting_start_time'],proposal['voting_end_time'],proposal_id,validator_name)
                        print(proposal_details)
                        botMsg(proposal_details)
            except Exception as e:
                manage_exception(e)
                print_and_save_error("fetch new proposal details exception exception")

            update_proposal_stats(validator_name,proposal_id_list)

def controller_hourly_block_stats(prev_hourly_stats):
    updated_hourly_block_stats=get_hourly_block_stats()
    updated_data=updated_hourly_block_stats['data']
    if updated_data['missed']>prev_hourly_stats['missed']:
        msg='Alert: {} New Missed Blocks Detected\n{}'.format(int(updated_data['missed']-prev_hourly_stats['missed']),updated_hourly_block_stats['msg'])
        botMsg(msg)
    update_hourly_block_stats(updated_data)
    
def update_hourly_block_stats(new_hourly_block_stats):
    try:
        global all_stats
        all_stats['hourly']=new_hourly_block_stats
    except Exception as e:
        manage_exception(e)
        print_and_save_error("update_hourly_block_stats exception")
        time.sleep(3)
        update_hourly_block_stats(new_hourly_block_stats)

def update_proposal_stats(validator_name,new_proposal_list):
    try:
        global all_stats
        all_stats[validator_name]['proposals']=new_proposal_list
    except Exception as e:
        manage_exception(e)
        print_and_save_error("update_hourly_block_stats exception")
        time.sleep(3)
        update_proposal_stats(validator_name,new_proposal_list)    
    
def initialize_stats():
    try:
        #without val stats
        return_dict={'hourly':get_hourly_block_stats()['data']}
        for validator in get_config_dict().keys():
            return_dict[validator]={'proposals':get_updated_proposal_ids(validator)['data']}
        return return_dict
    except Exception as e:
        manage_exception(e)
        print_and_save_error("initialize_stats exception")
        time.sleep(3)
        return initialize_stats()


# Start of logic
# print(get_url())
def main_function():
    try:
        global all_stats
        global initialized
        if(initialized == 0):
            verboseMsg("Monitoring service started at {}".format(getTimeFromTimestamp(getNow())))
            all_stats=initialize_stats()
            verboseMsg(str(all_stats))
        initialized=1
        count=0
        start_time=getTime()
        while True:
            try:
                count+=1
                if count%100==1:
                    verboseMsg("Count: {}\nstart_time: {}\n#count".format(count,start_time))
                try:
                    controller_hourly_block_stats(all_stats['hourly'])
                except Exception as e:
                    manage_exception(e)
                    print_and_save_error("controller_hourly_block_stats exception")
                
                try:
                    for validator in get_config_dict().keys():
                        controller_proposals(validator,all_stats[validator]['proposals'])
                except Exception as e:
                    manage_exception(e)
                    print_and_save_error("controller_proposals exception")
                #   controller_integrity_check_params
                
                if int(random.randint(0,10))==1:
                    verboseMsg(str(all_stats))
                time.sleep(30)
            except Exception as e:
                manage_exception(e)
                print_and_save_error("While Main loop exception")
    except Exception as e:
        manage_exception(e)
        print_and_save_error("#main_function exception")
        time.sleep(3)
        main_function()

main_function()