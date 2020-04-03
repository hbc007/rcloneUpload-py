import os
import json
import time
import sys
import shutil


def Log(filewriter,info:str):
    info="["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"] "+info
    print(info)
    filewriter.write(info+"\n")


def SearchFile(path,basepath):
    fileList=[]
    for root, dirs, files in os.walk(path):
        for f in files:
            fileList.append(os.path.join(root,f).replace(basepath,""))
    return fileList


def DelelteEmptyDir(path):
    dirList=[]
    for root,dirs,files in os.walk(path):
        dirList.append(root)
    for root in dirList[:0:-1]:
        try:
            os.rmdir(root)
        except Exception as e:
            pass


def main():
    f = open(workPath+'/rcloneUpload.log', 'w')
    Log(f,"------Job Start------")

    try:
        with open(workPath+"/config.json",encoding="utf-8") as load_f:
            options=json.load(load_f)
        downloadDir=options["downloadDir"].rstrip("/")
        mountDir=options["mountDir"].rstrip("/")
        if os.path.exists(downloadDir) and os.path.exists(mountDir):
            pass
        else:
            Log(f,"Path does not exist")
            Log(f,"------Job Abort------")
            f.close()
            return
    except Exception as e:
        Log(f,"%s"%e)
        Log(f,"------Job Abort------")
        f.close()
        return

    dpathList=fnameSample.replace(downloadDir+"/","").split("/")
    if len(dpathList)==1:
        Log(f,"Download Method: HTTP/FTP/SFTP")
        fileList=[dpathList[0]]
    else:
        Log(f,"Download Method: BitTorrent")
        fileList=SearchFile(os.path.join(downloadDir,dpathList[0]),downloadDir)

    Log(f,"Data Transfer Start:")
    for itm in fileList:
        sourcePath=downloadDir+itm
        targetPath=mountDir+itm
        if sourcePath.find("_____padding_file")!=-1:
            os.remove(sourcePath)
            continue
        Log(f,"Start move file {"+sourcePath+"} to {"+targetPath+"}")
        targetDir,_=os.path.split(targetPath)
        if not os.path.exists(targetDir):
            Log(f,"  --Directory {"+targetDir+"} does not exist")
            os.makedirs(targetDir)
            time.sleep(0.2)
            if os.path.exists(targetDir):
                Log(f,"-- Directory {"+targetDir+"} has been created")
        try:
            if os.path.exists(targetPath):
                Log(f,"-- Target {"+targetPath+"} file already exist,it will be overwritten")
                os.remove(targetPath)
            shutil.copy(sourcePath,targetPath)
            if os.path.exists(targetPath):
                os.remove(sourcePath)
                Log(f,"-- Move successed,source file has been deleted")
        except IOError as e:
            Log(f,"-- Move failed[1]: %s"%e)
            Log(f,"-- Please try to remounted the drive")
        except:
            Log(f,"-- Move failed[2]: ",sys.exc_info())
    DelelteEmptyDir(downloadDir)
    Log(f,"------Job Finished------")
    f.close()
    return

if __name__ == "__main__":
    args=sys.argv
    workPath,_=os.path.split(args[0])
    gid=args[1]
    filenum=args[2]
    if int(filenum)>0:
        fnameSample=args[3]
        main()