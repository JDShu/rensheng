class Result(object):
    """
    Message object that is returned to Service method caller.
    """

    def __init__(self, result_id, *args):
        self.id = result_id
        self.args = args
