from distutils import extension
import shutil
import sys
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#Main source 
Source_dir=""
dest_dir_Musique=""
dest_dir_videos=""
dest_dir_image=""
dest_dir_pdf=""

class bouncer(FileSystemEventHandler):
    def __init__(self) -> None:
        super( bouncer,self).__init__()
        
    #make a single file
    def unique_file(self,path):
        filename,extension=os.path.splittext(path)
        compt=1
        while os.path.exists(path):
            path=filename+" (" + str(compt) +")" + extension
            compt=compt+1
        return path
    
    #Moved file manager 
    
    def move(self,dest,entry,name):
        file_exists=os.path.exists(dest+"/"+name)
        
        if file_exists:
            unique_name=self.unique_file=name
            os.rename(entry,unique_name)
        shutil.move(entry,dest)
    
    #this function is triggered if something new happens in the source directory
    def on_modified(self, event):
        
        with os.scandir(Source_dir) as entries:
            
            for entry in entries:
                name=entry.name
                dest=Source_dir
                
                if name.endswith(".wav") or name.endswith(".mp3"):
                    dest=dest_dir_Musique
                    self.move(dest,entry,name)
                elif name.endswith(".mp4") or name.endswith(".mov"):
                    dest=dest_dir_videos
                    self.move(dest,entry,name)
                    
                elif name.endswith(".png") or name.endswith(".jpeg") or name.endswith(".jpg"):
                    dest=dest_dir_image
                    self.move(dest,entry,name)
                    
                elif name.endswith(".pdf") or name.endswith(".doc") or name.endswith(".docx") or name.endswith(".txt") :
                    dest=dest_dir_pdf
                    self.move(dest,entry,name)
            
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path =Source_dir
    event_handler = bouncer()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print("Monitoring")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Tasks Done")
        observer.stop()
    observer.join()
