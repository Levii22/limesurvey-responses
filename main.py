import base64
import requests
import json
from dotenv import load_dotenv
import os
from requests.structures import CaseInsensitiveDict
import logging
import sys

load_dotenv()

limeuser = os.getenv("LS_USER")
limepwd = os.getenv("LS_PWD")
limeurl = os.getenv("LS_API_URL")

logging.basicConfig(filename='console.log', level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def get_session_key():
    headers = CaseInsensitiveDict()
    headers["content-type"] = "'application/json'"
    headers["connection"] = "Keep-Alive"
    headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    logging.info('\n')
    logging.info('Getting session key')
    try:
        req = requests.post(limeurl,
                            headers=headers,
                            data=f'{{"method":"get_session_key","params":["{limeuser}","{limepwd}"],"id":1}}')
        req.raise_for_status()
        session_key = req.json()['result']
        logging.info(f'Got session key {session_key}')
        return session_key
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting session key: {str(e)}")
        raise


def export_responses(session_key, sid):
    headers = CaseInsensitiveDict()
    headers["content-type"] = "'application/json'"
    headers["connection"] = "Keep-Alive"
    headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    logging.info('Exporting responses')
    try:
        req = requests.post(limeurl,
                            headers=headers,
                            data=f'{{"method":"export_responses","params":["{session_key}","{sid}","json","en","complete","full"],"id":1}}')
        req.raise_for_status()
        result = json.loads(base64.b64decode(req.json()['result']))
        logging.info(f'Exported {len(result["responses"])} responses')
        return result['responses']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error exporting responses: {str(e)}")
        raise


def get_new_responses(fetched_responses):
    new_responses = []
    with open('responses.json', 'r') as f:
        data = json.load(f)
    for i in fetched_responses:
        if not i['Response ID'] in [x['Response ID'] for x in data]:
            logging.info(f'New response {i["Response ID"]}')
            new_responses.append(i)
    logging.info(f'Found {len(new_responses)} new responses')
    return new_responses


def save_responses(new_responses):
    if new_responses:
        logging.info('Saving responses')
        with open('responses.json', 'r') as f:
            data = json.load(f)
        data.extend(new_responses)
        with open('responses.json', 'w') as f:
            json.dump(data, f)


def get_survey_id():
    while True:
        suid = input("Enter the survey ID: ")
        if suid.isnumeric():
            return suid
        else:
            print("Invalid survey ID. Please enter a numeric value.")


if __name__ == '__main__':
    key = get_session_key()
    survey_id = get_survey_id()
    responses = export_responses(str(key), survey_id)
    n_responses = get_new_responses(responses)
    save_responses(n_responses)
