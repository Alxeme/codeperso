import os

class dir :
    def is_processable(self, path):
        if os.path.isdir(path) :
            try : os.listdir(path)
            except Exception : return False
            else : return True
        else :
            try : os.path.getsize(path)
            except Exception : return False
            else : return True
    
    def get_items(self, path) :
        items = os.listdir(path)
        for item in items :
            itempath = os.path.join(path, item)
            if os.path.isdir(itempath) and not self.is_processable(itempath) : items.remove(item)
        return items
    
    def __init__(self, path) :
        if not os.access(path, os.F_OK) : raise  ValueError(f"{path} doesn't exist!")
        if not os.access(path, os.R_OK) : raise  ValueError(f"{path} isn't readable!")
        if not os.path.isdir(path) : raise ValueError(f"{path} isn't a directory!")
        if not dir.is_processable(self, path) : raise PermissionError(f"{path} is not proccessable by the program!")
        self.path = path
        self.items = dir.get_items(self, path)
    
    
    def convert_to_paths(self, items_list) :
        return [os.path.join(self.path, os.path.basename(i)) for i in items_list]
    
    def get_all(self, basename_only=True) :
        if basename_only : return self.items
        else : return self.convert_to_paths(self.items)
    
    def get_subdirs(self, basename_only=True) :
        itemspath = dict(zip(self.items, self.convert_to_paths(self.items)))
        if basename_only : return [item for item, path in itemspath.items() if os.path.isdir(path)]
        else : return [path for path in itemspath.values() if os.path.isdir(path)]
    
    def get_files(self, basename_only=True) :
        itemspath = dict(zip(self.items, self.convert_to_paths(self.items)))
        if basename_only : return [item for item, path in itemspath.items() if not os.path.isdir(path)]
        else : return [path for path in itemspath.values() if not os.path.isdir(path)]
    

    def total_size(self, itempath, prescaler) :
        import time
        if os.path.getmtime(itempath) <= time.mktime((2023, 11, 1, 7, 0, 0, 2, 305, -1)) : return 0
        if not self.is_processable(itempath) : return 0
        s = os.path.getsize(itempath)/prescaler
        if not os.path.isdir(itempath) : return s
            
        for subitem in os.listdir(itempath) :
            subitempath = os.path.join(itempath, subitem)
            if self.is_processable(subitempath) :
                if not os.path.isdir(subitempath) : s += os.path.getsize(subitempath)/prescaler
                else : s += self.total_size(subitempath, prescaler)
        return s

    def get_size_subdirs(self, basename_only=True, prescaler=2**10) :
        subdirspath = dict(zip(self.get_subdirs(), self.get_subdirs(basename_only=False)))
        subdirssize = {}
        for subdir, subdirpath in subdirspath.items() :
            if basename_only : subdirssize[subdir] = self.total_size(subdirpath, prescaler)
            else : subdirssize[subdirpath] = self.total_size(subdirpath, prescaler)
        return subdirssize
    
    def get_size_files(self, basename_only=True, prescaler=2**10) :
        filespath = dict(zip(self.get_files(), self.get_files(basename_only=False)))
        filessize = {}
        for file, filepath in filespath.items() :
            if basename_only : filessize[file] = self.total_size(filepath, prescaler)
            else : filessize[filepath] = self.total_size(filepath, prescaler)
        return filessize

    

interest_path = r"C:\\ProgramData\\"    
MyDocs = dir(interest_path)
MyDocs_size = MyDocs.get_size_subdirs()
MyDocs_size["AUTRES"] = sum(MyDocs.get_size_files().values())

#and os.path.getmtime(subitempath) > time.mktime((2023, 11, 1, 7, 0, 0, 2, 305, -1))

print(MyDocs_size)



import matplotlib.pyplot as plt
import seaborn as sns


MyDocs_size_sorted = dict(sorted(MyDocs_size.items(), key=lambda item: item[1], reverse=True))
sns.barplot(x=list(MyDocs_size_sorted.values()), y=list(MyDocs_size_sorted.keys()))
plt.show()
