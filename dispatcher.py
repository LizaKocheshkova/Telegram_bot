class User:
    '''
    state: 0 - начало общения
            1 - ввод ФИО
            2 - ввод проблеммы
            3 - ввод адреса
            4 - сохранение обращения
    update: редактирование поля
    '''
    def __init__(self, id):
        self.id = id
        self.fio = None
        self.problem = None
        self.address = None
        self.state = 0
        self.update = False


class Dispatcher:
    '''
    self.users {
    key - id user
    value - User
    }
    '''
    users = dict()

    def check_user(self, id):
        return id in self.users