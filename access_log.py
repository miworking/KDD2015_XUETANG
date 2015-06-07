import pandas as pd
import numpy as np

class AccessLog(object):
    def __init__(self):
        self.id = None
        self.timestamp = None
        self.source = None
        self.event = None
        self.enrollment_id = None

    def __init__(self,id,timestamp,source,event,enrollment_id):
        self.id = id
        self.timestamp = timestamp
        self.source = source
        self.event = event
        self.enrollment_id = enrollment_id

    def get_id(self):
        return self.id



    def get_timestamp(self):
        return self.timestamp

    def get_source(self):
        return self.source

    def get_event(self):
        return self.event

