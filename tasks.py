import json, sys, os

class T1:

    def __init__(self, params):
        """
        params is a dictionary that contains all variables and parameters needed to execute the task.
        In particular, params contains all input values to the task.
        """
        print("Task T1 initializing...")
        self.data = None
        self.params = params


    def extract(self):
        print("Task T1 extracting...")
        with open(os.path.join(sys.path[0], self.params["path"])) as f:
            self.data = json.load(f)

    def transform():
        pass

    def load(self):
        print ("Task T1 loading...")
        return self.data

class T2:

    def __init__(self, params):
        """
        params is a dictionary that contains all variables and parameters needed to execute the task.
        In particular, params contains all input values to the task.
        """
        print("Task T2 initializing...")
        self.data = None
        self.params = params

    def extract(self):
        print("Task T2 extracting...")
        with open(os.path.join(sys.path[0], self.params["path"])) as f:
            self.data = json.load(f)

    def transform():
        pass

    def load(self):
        print ("Task T2 loading...")
        return self.data


class T3:

    def __init__(self, params):
        """
        params is a dictionary that contains all variables and parameters needed to execute the task.
        In particular, params contains all input values to the task.
        """
        print("Task T3 initializing...")
        self.data = None
        self.params = params

    def extract(self):
        print("Task T3 extracting...")
        with open(os.path.join(sys.path[0], self.params["path"])) as f:
            self.data = json.load(f)

    def transform():
        pass

    def load(self):
        print ("Task T3 loading...")
        return self.data

        
class Taches:

    def __init__(self):
        pass
    
    def T1(params):
        return T1(params)
    
    def T2(params):
        return T2(params)

    def T3(params):
        return T3(params)