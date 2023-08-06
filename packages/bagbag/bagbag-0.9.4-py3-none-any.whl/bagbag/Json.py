import json
from typing import Any

def Dumps(obj, indent=4, ensure_ascii=False) -> str:
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii)

def Loads(s:str) -> Any:
    return json.loads(s)

if __name__ == "__main__":
    j = Dumps({1: 3, 4: 5})
    print(j)

    d = Loads(j)
    print(d)

    print(type(d))