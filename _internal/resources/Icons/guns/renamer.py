from pathlib import Path
import os
import shutil
path_ = 'B:\Projects Windows\Gray Factory\resources\Icons\guns'

for x in os.listdir(path_):
    baseName = os.path.basename(x)
    name = os.path.splitext(x)
    if(os.path.splitext(baseName)[1] == ".png"):

        _name = os.path.basename(name[0])
        #print(_name[1:2])
        if(_name[1:2] == "_"):
            
            try:
                
                #os.rename(f"B:\\Projects Windows\\Gray Factory\\resources\\Icons\\weapons\\{x}", f"B:\\Projects Windows\\Gray Factory\\resources\\Icons\\weapons\\{_name[2:]}.png")
                print(_name[2:])
            except:pass
        #try:
        #shutil.move(str(x), str(tof))
        #except: print(f"Error {x} to {tof}")