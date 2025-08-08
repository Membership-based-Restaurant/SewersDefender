import pygame
import copy
import json
import entities
from constants import *

taskType = [SUMMON_TE,
            SUMMON_CE,
            SUMMON_AE,
            SUMMON_RE,
            WAVE_END,
            ]


class Map:
    def __init__(self, game, path='game_maps/map1/'):
        # load
        mapInfoDict = []  # all information of the map
        try:
            with open(f'{path}map.json', 'r', encoding='utf=8') as f:
                mapInfoDict = json.load(f)
        except FileNotFoundError:
            print('Map1:cannot find the file')
            return
        # routeIndex[routeNum][location]=(x,y)
        self.routeIndex = mapInfoDict['routeIndex']
        # mapTaskList[waveNum][routeNum][taskLoc]=task
        self.mapTaskList = mapInfoDict['mapTaskList']
        finishPosList = mapInfoDict['finishPosList']  # (x,y)
        self.finishManager = entities.FinManager(game)
        for pos in finishPosList:
            self.finishManager.create_finish(pos)
        self.towerBaseList = mapInfoDict['towerBaseList']
        self.numWaves = len(self.mapTaskList)  # num of waves
        self.numRoutes = len(self.routeIndex)  # num of routes
        # img
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        bkPath = f'{path}bk.png'
        self.img = pygame.image.load(bkPath).convert_alpha()
        # variable
        self.mapWaveList = []
        self.currentWave = 0
        for waveNum in range(self.numWaves):
            self.mapWaveList.append(
                Wave(self.numRoutes, self.mapTaskList[waveNum]))

    def get_task_dict(self, type=UPDATE):
        if type == UPDATE:
            taskDict = self.mapWaveList[self.currentWave].generate_task_dict()
            if not taskDict:
                if self.currentWave < self.numWaves-1:
                    self.currentWave += 1
                    taskDict = self.mapWaveList[self.currentWave].generate_task_dict(
                    )
                else:
                    print('task finished')
                    taskDict = {0: END}
            return taskDict
        elif type == RESET:
            self.reset()

    def map_blit(self):
        self.screen.blit(self.img, self.screen_rect)

    def reset(self):
        for wave in self.mapWaveList:
            wave.wa_rest()
        self.currentWave = 0

    def clear_list(self):
        self.waveTaskList.clear()


class Wave():
    def __init__(self, numRoutes: int, list: list):
        self.waveTaskList = []
        # testlist=list
        self.numRoutes = numRoutes
        for routeNum in range(self.numRoutes):
            self.waveTaskList.append(Task(routeNum, list[routeNum]))

    def generate_task_dict(self):
        taskDict = {}
        for task in self.waveTaskList:
            if task.ifEnd:
                continue
            else:
                taskDict[task.routeNum] = task.ta_next()
        return taskDict

    def wa_tasks(self):
        for task in self.waveTaskList:
            task.ta_reset()

    def clear_list(self):
        self.waveTaskList.clear()


class Task():
    def __init__(self, routeNum: int, list: list):
        self.routeNum = routeNum
        self.taskLoc = 0
        self.taskTimer = 0
        self.taskInterval = 0
        self.ifTaskPause = False
        self.ifEnd = False
        self.routeTaskList = []
        self.ta_set(list)

    def ta_set(self, list: list):
        self.routeTaskList = copy.copy(list)

    def ta_next(self):
        if not self.ifEnd:
            if self.ifTaskPause:
                self.taskTimer += 1
                if self.taskTimer == self.taskInterval:
                    self.taskInterval = 0
                    self.ifTaskPause = False
                    self.taskTimer = 1
                    self.taskLoc += 1
                return REST
            task = self.routeTaskList[self.taskLoc]
            if task in taskType:
                if task == WAVE_END:
                    self.ifEnd = True
                    return WAVE_END
                else:
                    self.taskLoc += 1
                    return task
            else:
                self.taskInterval = task
                self.ifTaskPause = True
                return REST

    def ta_reset(self):
        self.taskLoc = 0
        self.taskTimer = 0
        self.taskInterval = 0
        self.ifTaskPause = False
        self.ifEnd = False

    def clear_list(self):
        self.routeTaskList.clear()
