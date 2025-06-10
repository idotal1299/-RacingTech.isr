import psutil

def is_iracing_running():
    return any(proc.info['name'] == 'iRacingSim64DX11.exe' for proc in psutil.process_iter(['name']))
