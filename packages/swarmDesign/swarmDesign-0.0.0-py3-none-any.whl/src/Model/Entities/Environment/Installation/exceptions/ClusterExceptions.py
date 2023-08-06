
class ClusterError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def get_error(self):
        return self.msg
