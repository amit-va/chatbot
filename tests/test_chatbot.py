#!usr/bin/env python3
"""Test the functions in `bot/chatbot.py`.
"""

from .. import bot


data= {}
data['entity_BundleId']='0c3151bd-1cbf-4d64-b04d-cd9187a4c6e0'
data['entity_AppointmentId'] =  'be142dc6-93bd-11eb-a8b3-0242ac130003'
data['entity_PatientFirstName']= 'Mickey'
data['entity_DoctorLastName'] =  'Duck'
data['entity_Diagnosis']='Diabetes without complications'
def test_step_1():


    assert (bot.chatbot.getUtterText(0, data) == 'Hi Mickey, on a scale of 1-10, would you recommend Dr Duck to a friend or family member? 1 = Would not recommend, 10 = Would strongly recommend' )
