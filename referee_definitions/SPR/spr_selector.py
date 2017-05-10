#! /usr/bin/env python
import csv
import random
import pprint
import itertools
from collections import OrderedDict

teams = ["ToBI", "Homer", "TechUnited", "SocRob", "b-it-bots", "SCC", "RT-Lions"]

questions = list(csv.DictReader(open("questions.csv")))


prefined = [question for question in questions if question["Category"] == "Predefined"] * 6
crowd = [question for question in questions if question["Category"] == "Crowd"] * 6
arena = [question for question in questions if question["Category"] == "Arena"] * 6
objects = [question for question in questions if question["Category"] == "Objects"] * 6

generated_question_lists = [crowd, arena, objects]

# import ipdb; ipdb.set_trace()

team_questions = OrderedDict()
for team in teams:
    team_questions[team] = {1:[], 2:[], 3:[]}
    for attempt in [1, 2, 3]:
        random.shuffle(generated_question_lists)

        team_riddle_qs = []
        team_riddle_qs += [prefined.pop()]  # 1 predefined Q in the riddle game
        team_riddle_qs += [crowd.pop()] # At least 1 about the crowd
        team_riddle_qs += [arena.pop()] # At least 1 about the arena
        team_riddle_qs += [objects.pop()] # At least 1 about the objects
        team_riddle_qs += [generated_question_lists[0].pop()]  # Take a question from either crowd, arena, objects

        team_blind_qs = []
        team_blind_qs += [prefined.pop()]  # 1 predefined Q in the riddle game
        team_blind_qs += [generated_question_lists[0].pop()]  # Take a question from either crowd, arena, objects
        team_blind_qs += [generated_question_lists[1].pop()]  # Take a question from either crowd, arena, objects
        team_blind_qs += [generated_question_lists[2].pop()]  # Take a question from either crowd, arena, objects
        team_blind_qs += [generated_question_lists[0].pop()]  # Take a question from either crowd, arena, objects
        team_blind_qs += [generated_question_lists[1].pop()]  # Take a question from either crowd, arena, objects

        team_questions[team][attempt] = (team_riddle_qs, team_blind_qs)
        # pprint.pprint(team_questions)

for team, attemps in team_questions.items():
    with open("SPR_{}.txt".format(team), "w") as team_file:
        for attempt_index, (riddle_qs, blind_qs) in attemps.items():
            team_file.write(team + " (Attempt {})".format(attempt_index)+"\n")
            team_file.write("-"*10+"\n")

            for index, Q in enumerate(riddle_qs):
                team_file.write("{i}: {q}".format(i=index+1, q=Q["Question"])+"\n")

            team_file.write("-"*20+"\n")

            for index, Q in enumerate(blind_qs):
                team_file.write("{i}: {q}".format(i=index+1, q=Q["Question"])+"\n")
            
            team_file.write("\n\n")