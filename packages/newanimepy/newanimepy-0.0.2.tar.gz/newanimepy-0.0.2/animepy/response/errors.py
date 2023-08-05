#Error output

class Error_type:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def status_error(self, e_code: int):
        return 'Requests failed: {}'.format(str(e_code))

    def no_result(self):
        return "No result!"

    def no_keyword(self):
        return "No keyword!\nPlease input a keyword!"