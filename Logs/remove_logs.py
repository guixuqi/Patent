import os
import re


def remove_log():
    logs = os.path.dirname(os.path.abspath(__file__)) + "\\All_Logs"
    # logs = os.path.dirname(os.path.abspath(__file__)) + "\\Error_Logs"
    fs = os.listdir(logs)
    for f in fs:
        if re.search(r".log", f):
            ff = os.path.join(logs, f)
            os.remove(ff)


if __name__ == '__main__':
    remove_log()