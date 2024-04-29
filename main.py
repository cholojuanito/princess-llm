import logging
import json
import requests

def setup_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f'logs/{log_file}')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

logger = setup_logger('princess.logs')
model_name = 'opus-princess-llama3'

def chat(messages):
    data = {"model": model_name, "messages": messages, "stream": True}
    logger.info(f'Sending req {data}')
    r = requests.post(
        'http://127.0.0.1:11434/api/chat',
        json=data
    )
    r.raise_for_status()

    output = ''

    for line in r.iter_lines():
        body = json.loads(line)
        
        if 'error' in body:
            logger.error(f'ERROR: {body}')
            raise Exception(body['error'])
        if body.get('done') is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            print(content, end='', flush=True)
        else:
            message = body.get('message', '')
            message['content'] = output
            logger.info(f'Final response: {message}')
            return message
            


def main():
    messages = []

    while True:
        user_input = input('> ')
        if not user_input or user_input == 'exit':
            exit()
        print()
        messages.append({'role': 'user', 'content': user_input})
        response = chat(messages)
        messages.append(response)
        print('\n\n')

if __name__ == "__main__":
    main()