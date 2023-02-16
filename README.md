# validator-monitoring-bot
This repository is a bot to monitor Cosmos-based validator proposals and alert on telegram channel


# Main Features
This bot uses the chain LCD to query:</br>
- The active proposals list on a chain
- Alerts as a new proposal arrives and sends the details to a telegram chat.
- Checks if a validator has voted for any of the active proposals or not.
- It also has a feature to send scheduled integrated reports to a telegram chat about the status of a specific validator's votes on active proposals of a specific chain.

# Customizations before start
1. Open telegramBot.py and enter the details of your telegram bot id and channel ids in the variables.
2. Open config.cfg and replace your Chain LCDs and validator addresses that you want to monitor

# Quick Start Using Docker
**Using docker-compose:**  
1. To access the challenges, you need <a href="https://docs.docker.com/install">docker</a> and <a href="https://docs.docker.com/compose/install/">docker-compose</a> installed.</br>
2. Clone the repository</br>`git clone https://github.com/prism-finance/validator-monitoring-bot`
3. Open the main directory of the project (where docker-compose.yml file exists) and run: `docker-compose up -d`
