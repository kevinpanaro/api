import os
import json

def save_lanes(data, file_name):
    path = os.path.dirname(os.path.realpath(__file__))

    save_path = os.path.join(path, "../../specials", file_name)

    if os.path.exists(save_path):
        os.remove(save_path)


    with open(save_path, 'w+') as f:
        f.write(json.dumps(data))