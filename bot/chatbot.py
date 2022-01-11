""" implement Chatbot functionality
"""

import json
import logging
import pyjq                 # jq like functionality to handle nested structure of FHIR like json bundle
import re                   # regex for lookup
import sys                  # added for function support
import uuid                 # unique id for a given interaction.
import yaml
import nested_dict as nd
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def getEntity(path):
    # //TODO:
    #   Read from Neo4j or kafka
    f = open(path)
    apptData = json.load(f)

    extractEntities = {}
    extractEntities['entity_BundleId'] = pyjq.first('.id', apptData)
    extractEntities['entity_AppointmentId'] = pyjq.first(
        '.entry[]|select(.resource.resourceType=="Appointment")|.resource.id', apptData)
    extractEntities['entity_PatientFirstName'] = pyjq.first(
        '.entry[]|select(.resource.resourceType=="Patient")|.resource.name[].given[]', apptData)
    extractEntities['entity_DoctorLastName'] = pyjq.first(
        '.entry[]|select(.resource.resourceType=="Doctor")|.resource.name[].family', apptData)
    extractEntities['entity_Diagnosis'] = pyjq.first(
        '.entry[]|select(.resource.resourceType=="Diagnosis" and .resource.status=="final")|.resource.code.coding[].name',
        apptData)
    # logging.debug(extractEntities)
    return extractEntities


def getRules(filter: str):
    data = yaml.safe_load(open('files/BOT_PostApptFeedback.yaml'))[filter]
    # logging.debug('getRules', data)
    return data


def getUtterText(step, data):
    # loop over entities within a rule
    rules = getRules(filter='rules')
    textBefore = rules[step]['text']
    textAfter = textBefore
    if rules[step]['entity'] is not None:
        for entity in range(len(rules[step]['entity'])):
            # get text from rules, within text get entities and replace them with extracted appointment data
            ruleEntity = rules[step]['entity'][entity]
            # logging.debug('ruleEntity', ruleEntity)
            lookupVal = dict.__getitem__(data, ruleEntity)
            # logging.debug('lookupVal', lookupVal)
            textAfter = re.sub(ruleEntity, lookupVal, textBefore)
            textBefore = textAfter
    return textAfter


def getFormNumber(min:int,max:int):
    while True:
        response: str = getRawInput()
        try:
            isNumber = int(response)
        except:
            print('Please try again, Enter a number between 1 and 10\n')
        else:
            if min <= isNumber <= max:
                break
            # //TODO: add else msg here
    return response


def getRawInput():
    raw_response: str = input(">>: ")
    return raw_response


def getRuleActions (step):
    rules = getRules(filter='rules')
    actions = rules[step]['action']
    if actions is not None:
        # print (type(actions[0]), actions[0])
        return actions


def applyRulesActions(actions: dict, tracker: dict) :
    response = {}
    # print (type(actions), actions)
    if 'FormNumber' in actions:
        action_name = actions['FormNumber']['name']
        action_args = actions['FormNumber']['range']
        response = applyRuleAction(action_name, action_args)
    elif 'FormOption' in actions:
        raw_response = getRawInput()
        response = {}
        response['value'] = 0
        for options in actions['range']:
            # print (type(options['Synonyms']),options['Synonyms'])
            for option_val in options['Synonyms']:
                if option_val in raw_response :
                    response_value = 1
                    print (response)
                    response['option_val'] = option_val
                    response['value'] = response_value
                    response['display'] = options['Display']
                    response['raw_response'] = raw_response
                    print (response)
                    break
    elif 'UserEntry' in actions:
        raw_response = getRawInput()
        return raw_response
    elif 'Goodbye' in actions:
        summary = ''
        for steps in tracker['response']:
            if steps != 3 :
                line1: str = tracker['response'][steps]['question']
                try:
                    line2: str = tracker['response'][steps]['response']['display']
                except:
                    line2: str = tracker['response'][steps]['response']

                # print (steps, type(line1), line1, type(line2), line2)
                summary : str = ( summary + '\n\t' + line1 + '\n\t\t' + line2 )
                # print (type(response), response)
        print (summary)
        return
    else:
        print ('no action defined')
    return response


def applyRuleAction (action_name: str, action_args: list ):
    response = getattr(sys.modules[__name__], action_name)(*action_args)
    return response


def main():


    apptDetail = getEntity('files/patient-feedback-raw-data.json')

    bot = getRules(filter='bot')
    tracker = nd.nested_dict()
    tracker['refcontextId'] = str(uuid.uuid4())
    tracker['refBundleId'] = apptDetail['entity_BundleId']
    tracker['refApptId'] = apptDetail['entity_AppointmentId']
    tracker['refBotName'] = bot['name']

    rules = getRules(filter='rules')
    # get and process rules for a given bot.
    for rule in range(len(rules)):
        # logging.debug(rule)
        text = (getUtterText(rule, apptDetail))
        print(text)
        tracker['response'][rule]['question'] = text
        tracker['response'][rule]['rule'] = rule

        # get actions for a step
        actions = getRuleActions(rule)
        # apply available actions
        response = applyRulesActions(actions, tracker)
        tracker['response'][rule]['response'] = response

        # logging.debug (tracker)

    response_file_name = ('files/'+ tracker['refcontextId'] + '.json')
    with open(response_file_name, "w") as outfile:
        json.dump(tracker, outfile)


if __name__ == "__main__":
    main()


# EOF