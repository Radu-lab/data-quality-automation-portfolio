from os import mkdir
from pathlib import Path

rules = {
    "Archives" : [".zip",".rar",".7z"],
    "Images" : [".png",".gif",".jpeg",".jpg"],
    "Documents" : [".pdf",".xlsx",".docx",".dotx",".csv"],
    "Executables" : [".exe",".msi"],
    "Media file" : [".mp4"]

}
folder = Path("C:/Users/Radu/Proba1")
dry_run = False

for file in folder.iterdir():
    if file.is_file():
        print(file.stem, file.suffix)
        for rule,value in rules.items():
            if file.suffix.lower() in value:
                if dry_run:
                    print(file.name, "->", rule)
                else:
                   (folder/rule).mkdir(exist_ok=True)
                   #file.rename(folder / rule / file.name)
                   dest = folder/rule/file.name
                   counter =1
                   while dest.exists():
                       dest = folder/rule/f"{file.stem}_{counter}{file.suffix}"
                       counter+=1
                   file.rename(dest)

