from resources import resources
import os
from pathlib import Path
import glob
from functools import lru_cache

Debug = False

class SystemPath(object):
    def __init__(self):
        self.path = resources()
        folder = f"{self.path}/resources/Icons"
        allImageFile = []            

        for item in glob.glob(f'{folder}/**/*.png', recursive=True):
            if(os.path.splitext(item)[1] == ".png"):
                allImageFile.append(((str(Path(item)),os.path.splitext(os.path.basename(item))[0])))
                
        for item in glob.glob(f'{folder}/**/*.jpg', recursive=True):
            if(os.path.splitext(item)[1] == ".jpg"):
                allImageFile.append(((str(Path(item)),os.path.splitext(os.path.basename(item))[0])))
                
        self.listImages = allImageFile
        
    @lru_cache()
    def get(self, name : str, path : str = ""):
        if name is None:
            return None
        find = None
        name = name.replace(".png","").replace(".jpg","")
        
        path_png = f"{resources()}\\{path}\\{name}.png"
        if path_png in self.listImages:
            return path_png
        
        path_jpg = f"{resources()}\\{path}\\{name}.jpg"
        if path_jpg in self.listImages:
            return path_jpg
        
        if name in self.listImages:
            return self.listImages[name]
        
        for item in self.listImages:

            if (name == item[1]) and (path in item[0]):
                find = item[0]
                return str((find).replace("\\", "/"))

            if (name in item[1]) and (path in item[0]):
                find = item[0]
                return str((find).replace("\\", "/"))
            
            if (item[1].find(name) != -1) and (path in item[0]):
                if(Debug):
                    print(f"[DEBUG : Pathes] get path for name '{name}' | find and return : '{Path (item[0])}'  GOOD")
                find = (item[0])
                #return str(Path(find))
                return str((find).replace("\\", "/"))
                        
        if(find == None):
            if(Debug):
                print(f"[DEBUG : Pathes] get path for name '{name}' | ! CANT FIND FILE ! <ERROR>")
            pass