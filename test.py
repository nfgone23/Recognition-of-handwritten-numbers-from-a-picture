from datetime import datetime, timedelta

class A:
    def __init__(self):
        self._time_created = datetime.now()

    def foo(self):
        if datetime.now() - self._time_created < timedelta(minutes=1):
            return None
        # do the stuff you want to happen after one minute here, e.g.
        return 1

a = A()
while True:
    if a.foo() is not None:
        break