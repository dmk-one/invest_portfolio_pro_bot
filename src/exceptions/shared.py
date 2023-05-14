class RoleException(Exception):
    detail = 'Current user does not have access to this handler'

    def __init__(self):
        super().__init__(self.detail)
