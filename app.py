from flask import Flask, request
from dotenv import load_dotenv
import requests
import os
import json
from twilio.twiml.messaging_response import MessagingResponse, Message
load_dotenv()

app = Flask(__name__)


@app.route('/vocabulary', methods=['POST'])
def vocabulary():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    message = Message()
    responded = False
    words = incoming_msg.split('-')
    if len(words) == 1 and incoming_msg == "help":
        help_string = create_help_message()
        message.body(help_string)
        resp.append(message)
        responded = True
    elif len(words) == 2:
        search_type = words[0].lstrip().rstrip()
        input_string = words[1].lstrip().rstrip()
        if search_type == "meaning":
            word_definitions = find_word_meaning(input_string)
            for word_definition in word_definitions:
                resp.message(word_definition)
            print(resp)
            responded = True
        elif search_type == "examples":
            word_examples = find_word_usage(input_string)
            for word_example in word_examples:
                resp.message(word_example)
            print(resp)
            responded = True
        elif search_type == "synonyms":
            synonyms = find_synonyms(input_string)
            for word_synonyms in synonyms:
                resp.message(word_synonyms)
            print(resp)
            responded = True
        elif search_type == "antonyms":
            word_antonyms = find_antonyms(input_string)
            for word_antonyms in word_antonyms:
                resp.message(word_antonyms)
            print(resp)
            responded = True
    if not responded:
        message.body('Incorrect request format. Please enter help to see the correct format')
        resp.append(message)

    return str(resp)


def create_help_message():
    """
    Returns help message for using VocabBot
    :return: string
    """
    help_message = "Improve your vocabulary using VocabBot! \n\n" \
        "You can ask the bot the below listed things:  \n"\
        "meaning - enter the word \n"\
        "examples - enter the word \n"\
        "synonyms - enter the word \n"\
        "antonyms - enter the word \n"
    return help_message


def find_word_meaning(word):
    """
    Returns word meaning
    :return:
    """
    definitions = []
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/definitions'
    headers = os.getenv("WORDS_API_KEYS")
    headers = json.loads(headers)
    response = requests.get(url, headers=headers)
    content = json.loads(response.text)
    if response.status_code == 200:
        for definition in content["definitions"]:
            definitions.append("- " + definition["definition"] + ".")
    else:
        definitions.append(content["message"])
    return definitions


def find_word_usage(word):
    """
    Return word usage
    :param word:
    :return:
    """
    word_usage = []
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/examples"
    headers = os.getenv("WORDS_API_KEYS")
    headers = json.loads(headers)
    response = requests.get(url, headers=headers)
    content = json.loads(response.text)
    if response.status_code == 200:
        for usage in content["examples"]:
            word_usage.append("- " + usage +".")
    else:
        word_usage.append(content["message"])
    return word_usage


def find_synonyms(word):
    """
    Returns synonyms of the word.
    :param word:
    :return:
    """
    word_synonyms = []
    counter = 0
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = os.getenv("WORDS_API_KEYS")
    headers = json.loads(headers)
    response = requests.get(url, headers=headers)
    content = json.loads(response.text)
    if response.status_code == 200:
        for synonym in content["synonyms"]:
            counter += 1
            word_synonyms.append("- " + synonym + ".")
    else:
        word_synonyms.append(content["synonyms"])

    return word_synonyms


def find_antonyms(word):
    """
    Returns antonyms of the word
    :param word:
    :return:
    """
    word_antonyms = []
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/antonyms"
    headers = os.getenv("WORDS_API_KEYS")
    headers = json.loads(headers)
    response = requests.get(url, headers=headers)
    content = json.loads(response.text)
    if response.status_code == 200:
        for antonym in content["antonyms"]:
            word_antonyms.append("- " + antonym + ".")
    else:
        word_antonyms.append(content["antonyms"])

    return word_antonyms


if __name__ == "__main__":
    app.run(port=5000)