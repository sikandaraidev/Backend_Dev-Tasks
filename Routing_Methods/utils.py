from json import dumps, loads


def Load_json(DATA_PATH):
    with open(DATA_PATH, 'r') as file:
        data = file.read()
    return loads(data)

def Save_json(data, DATA_PATH):
    with open(DATA_PATH, 'w') as file:
        file.write(dumps(data, indent=4))


print("utils.py loaded successfully", Save_json)