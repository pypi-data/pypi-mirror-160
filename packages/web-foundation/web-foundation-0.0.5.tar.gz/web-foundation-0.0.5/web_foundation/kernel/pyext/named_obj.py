import random
import string
from typing import Set

from .singleton import Singleton


class NamedObject(Singleton):
    sname: str
    _named: Set[str] = set()

    def __new__(cls, *args, **kwargs):
        super(NamedObject, cls).__new__(cls, *args, **kwargs)
        while True:
            cls.sname = cls._gensname()
            if cls.sname in NamedObject._named:
                continue
            NamedObject._named.add(cls.sname)
            break
        return cls._instance

    @classmethod
    def _gensname(cls) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

# if __name__ == '__main__':
#     s = ShadowNamedSpace()
#     t = Test()
#     print(Test.sname)
#     s.set_shadow(t)
#     print(s.get_shadow(Test))
#     print(type(s.__iter__()))
#     for k, v in s:
#         print(k, v)
