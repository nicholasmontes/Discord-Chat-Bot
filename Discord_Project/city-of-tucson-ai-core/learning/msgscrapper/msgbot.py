import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

channelid = os.getenv('DISCORD_CHANNEL_ID')
auth_key = os.getenv('DISCORD_AUTH_KEY')

def get_channel_name(channelid):
    headers = {
        'authorization': auth_key
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}', headers=headers)
    if r.status_code != 200:
        print(f'Error: {r.status_code}')
        return None
    channel_info = r.json()
    return channel_info['name']

def retrieve_messages(channelid):
    channel_name = get_channel_name(channelid)
    if not channel_name:
        print('Failed to retrieve channel name.')
        return

    num = 0
    limit = 10

    headers = {
        'authorization': auth_key
    }

    last_message_id = None

    filename = f'{channel_name}.txt'

    with open(filename, 'w', encoding='utf-8') as file:
        while True:
            query_parameters = f'limit={limit}'
            if last_message_id is not None:
                query_parameters += f'&before={last_message_id}'

            r = requests.get(
                f'https://discord.com/api/v9/channels/{channelid}/messages?{query_parameters}', headers=headers
            )

            if r.status_code != 200:
                print(f'Error: {r.status_code}')
                break

            jsonn = r.json()
            if len(jsonn) == 0:
                break

            for value in jsonn:
                author_id = value['author']['id']
                username = value['author']['username']
                name = value['author']['global_name']
                content = value['content']
                file.write(f'ID: {author_id}\nUsername: {username}\nName: {name}\nMessage: {content}\n\n')
                last_message_id = value['id']
                num += 1

retrieve_messages(channelid)