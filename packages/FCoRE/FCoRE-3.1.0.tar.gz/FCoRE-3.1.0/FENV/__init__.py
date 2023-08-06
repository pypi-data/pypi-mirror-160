import os

def get_os_variable(varName, default=False, convertType=str):
    try:
        raw = os.environ[varName]
        if convertType:
            return convertType(raw)
        return raw
    except:
        return default