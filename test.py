import json


class Test:
    def __init__(self):
        self.x = 1
        self.y = 2


t = Test()
# js = json.dumps(t)

print(t.__dict__)
print(json.loads('{"a": 1}'))
