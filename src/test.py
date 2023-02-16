from functions import get_config,get_config_dict

print(get_config_dict())
validator_configs=get_config_dict()
active_proposal_path="/cosmos/gov/v1beta1/proposals?proposal_status=2&pagination.limit=20&pagination.count_total=true&pagination.reverse=true&pagination.key="
def get_proposals_url(validator_name):
    try:
        lcd_url=validator_configs[validator_name]['lcd_url']
        return_url="{}{}".format(lcd_url,active_proposal_path)
        return return_url
    except Exception as e:
        return None
print(get_proposals_url(validator_name='terra'))