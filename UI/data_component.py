class Parameter:
    def __init__(self):
        self.TIME_DENSITY = 0
        self.AVG_TIME = 0
        self.AVG_TRASH = 0
        self.GARBAGECAN_SIZE = 0
        self.GARBAGETRUCK_SIZE = 0
        self.TIME_STDDEV = 0
        self.TRASH_STDDEV = 0
        self.TRUCK_INITIAL = 0
        self.TRUCK_CYCLE = 0
        self.TRUCK_DELAY = 0
        self.simulation_time = 0
        self.RANDOM_SEED = 0
        self.SIMULATION_MODE = 'VIRTUAL_TIME'
        self.VERBOSE = False
        self.text = ""

    def update_config(self):
        self.text = "TIME_DENSITY=" + str(self.TIME_DENSITY) + \
            "\nAVG_TIME=" + str(self.AVG_TIME) + \
            "\nAVG_TRASH=" + str(self.AVG_TRASH) + \
            "\nGARBAGECAN_SIZE=" + str(self.GARBAGECAN_SIZE) + \
            "\nGARBAGETRUCK_SIZE=" + str(self.GARBAGETRUCK_SIZE) + \
            "\nTIME_STDDEV=" + str(self.TIME_STDDEV) + \
            "\nTRASH_STDDEV=" + str(self.TRASH_STDDEV) + \
            "\nTRUCK_INITIAL=" + str(self.TRUCK_INITIAL) + \
            "\nTRUCK_CYCLE=" + str(self.TRUCK_CYCLE) + \
            "\nTRUCK_DELAY=" + str(self.TRUCK_DELAY) + \
            "\nsimulation_time=" + str(self.simulation_time) + \
            "\nVERBOSE=" + str(self.VERBOSE) +\
            "\nSIMULATION_MODE=" + '"'+self.SIMULATION_MODE +'"'+ \
            "\nRANDOM_SEED=" + str(self.RANDOM_SEED)
        file = open("UI/config.py", "w")
        file.write(self.text)