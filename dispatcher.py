class User:
    '''
    state: 0 - начало общения
            1 - ввод ФИО
            2 - ввод проблеммы
            3 - ввод адреса
            4 - сохранение обращения
    '''
    def __init__(self, id):
        self.id = id
        self.fio = None
        self.problem = None
        self.address = None
        self.state = 0


class Dispatcher:
    '''
    self.users {
    key - id uset
    value - User
    }
    '''
    users = dict()

    def check_user(self, id):
        return id in self.users