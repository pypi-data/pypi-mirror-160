class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            s = super(Singleton, cls)
            cls._instance = s.__new__(cls)
        return cls._instance
