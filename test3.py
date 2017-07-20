class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class User(object):
    __metaclass__ = IterRegistry
    _registry = []


    def _setName(self, name=None):
        self._name = name

    def _getName(self):
        return self._name

    def _setPassword(self, password):
        self._password = password

    def _getPassword(self):
        return self._password

    def commit(self):
        pass

    name = property(_getName, _setName)
    password = property(_getPassword, _setPassword)

u = User()
u.name = 'Jason Martinez'
u.password = 'linebreak'
u.commit()


z = User()
z.name = 'Nathan Kuhl'
z.password = 'running back'
z.commit()


for i in User:
    print i.name

