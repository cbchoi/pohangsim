from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import subprocess as sp
import datetime
from pathlib import Path 
from subprocess import STDOUT, check_output, TimeoutExpired

import pandas as pd
import numpy as np

MONTH = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

from config import *
from instance.config import *
import pygsheets
import http

#authorization
gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)
sh = gc.open(GOOGLE_SPREADSHEET_NAME)

import urllib.request
from urllib.parse import quote

import json
from pprint import pprint

class Crawler(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", REQUEST_FREQ)

        self.insert_input_port("report")

        self.assessed_students = {}
        self.current_student = None
        self.asessment_file_path = ""

    def ext_trans(self,port, msg):
        if port == "report":
            self._cur_state = "PROCESS"
            

    def output(self):
        if self._cur_state == "PROCESS":
            url = PUBLIC_DATA_REQUEST_URL.format(quote(STATION), PUBLIC_DATA_SERVICE_KEY)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            
            if(rescode == 200):
                try:
                    response_body = response.read()
                except (http.client.IncompleteRead) as e:
                    response_body = e.partial

                parse = json.loads(response_body)
                for ret in parse['list']:
                    print(type(ret))
                    values = list(ret.values())
                    wks = sh.worksheet('title', GOOGLE_WORKSHEET)
                    wks.insert_rows(row=1, values=values)     
                
            else:
                print("Error Code:" + rescode)
                #select the first sheet 
            

        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "PROCESS"