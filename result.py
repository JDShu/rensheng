from enums import ResultIds

class Result(object):
    """
    Message object that is returned to Service method caller.
    """

    def __init__(self, result_id, *args):
        self.id = result_id
        self.args = args

    @property
    def is_success(self):
        return self.id == ResultIds.SUCCESS

    @property
    def is_error(self):
        return self.id == ResultIds.ERROR
