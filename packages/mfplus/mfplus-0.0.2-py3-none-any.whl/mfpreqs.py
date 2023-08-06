"""Contains the supporting functions called by convert in mfpconvert
"""

from winreg import OpenKey as regOpenKey
from winreg import QueryInfoKey as regQInfo
from winreg import QueryValueEx as regQVEx
from winreg import EnumKey as regEnumKey
from winreg import HKEY_LOCAL_MACHINE as HKLM
from subprocess import run

def findmfplus():
    """Finds the install location of MicroFile+.exe on the current system

       Returns: str containing path to MicroFile+.exe
    """
    unstkey = regOpenKey(HKLM, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    (nkeys,_,_) = regQInfo(unstkey)
    mfkey = None
    ind = 0
    while ind < nkeys:
        try:
            keystr = regEnumKey(unstkey,ind)
            appkey = regOpenKey(unstkey,keystr)
            (dispname,_) = regQVEx(appkey,"DisplayName")
            if dispname == "Microfile+":
                mfkey = appkey
                break
            else:
                ind += 1
        except:
            ind += 1
    if mfkey is not None:
        (loc,_) = regQVEx(mfkey,"InstallLocation")
        return loc + "Microfile+.exe"
    else:
        return None

def convertone(mfloc,inpath,**kwargs):
    """Converts one image

       Required Arguments:
          mfloc (str)  = path to MicroFile+.exe on this system
          inpath (str) = path to an image file to be converted

       Optional Keyword Arguments:
          outname (str) = name of the file after converting
          outdir  (str) = directory for output of converted file
          dojpx  (bool) = if True, will convert to a JPEG2000 (True by default)
          dotiff (bool) = if True, will convert to a OME-TIFF
    """
    outname = None
    if "outname" in kwargs.keys():
        if type(kwargs["outname"]) is str:
            outname = kwargs["outname"]
    outdir = None
    if "outdir" in kwargs.keys():
        if type(kwargs["outdir"]) is str:
            outdir = kwargs["outdir"]
    dojpx = True
    if "dojpx" in kwargs.keys():
        if type(kwargs["dojpx"]) is bool:
            dojpx = kwargs["dojpx"]
    dotiff = False
    if "dotiff" in kwargs.keys():
        if type(kwargs["dotiff"]) is bool:
            dotiff = kwargs["dotiff"]
    if dojpx or not (dojpx or dotiff):
        cmds = list()
        cmds.append(mfloc)
        cmds.append("-i")
        cmds.append(inpath)
        if type(outname) is str:
            cmds.append("-o")
            if outname.find(".jpx") != len(outname)-4:
                cmds.append(outname+".jpx")
            else:
                cmds.append(outname)
        if type(outdir) is str:
            cmds.append("-d")
            cmds.append(outdir)
        run(cmds)
    if dotiff:
        cmds = list()
        cmds.append(mfloc)
        cmds.append("-i")
        cmds.append(inpath)
        if type(outname) is str:
            cmds.append("-o")
            extpos = outname.find(".tif")
            if (extpos != len(outname)-4) or (extpos != len(outname)-5):
                cmds.append(outname+".tif")
            else:
                cmds.append(outname)
        if type(outdir) is str:
            cmds.append("-d")
            cmds.append(outdir)
        cmds.append("--ometiff")
        run(cmds)

def convertmany(mfloc,inpaths,**kwargs):
    """Converts many images

       Required Arguments:
          mfloc (str)  -- path to MicroFile+.exe on this system
          inpaths (list of str) -- path to an image file to be converted

       Optional Keyword Arguments:
          outnames (list of str) = names for each file after converting
          outdirs  (list of str) = directories for output of each converted file
          dojpxs  (list of bool) = for each image, if True, will convert to a JPEG2000 (True by default)
          dotiffs (list of bool) = for each image, if True, will convert to an OME-TIFF
    """
    usenames = False
    usedirs = False
    usejpxs = False
    usetiffs = False
    if "outnames" in kwargs.keys():
        if type(kwargs["outnames"]) is list:
            if len(kwargs["outnames"]) == len(inpaths):
                usenames = True
    if "outdirs" in kwargs.keys():
        if type(kwargs["outdirs"]) is list:
            if len(kwargs["outdirs"]) == len(inpaths):
                usedirs = True
    if "dojpxs" in kwargs.keys():
        if type(kwargs["dojpxs"]) is list:
            if len(kwargs["dojpxs"]) == len(inpaths):
                usejpxs = True
    if "dotiffs" in kwargs.keys():
        if type(kwargs["dotiffs"]) is list:
            if len(kwargs["dotiffs"]) == len(inpaths):
                usetiffs = True
    for ind in range(len(inpaths)):
        outname = None
        outdir = None
        dojpx = True
        dotiff = False
        if usenames:
            outname = kwargs["outnames"][ind]
        if usedirs:
            outdir = kwargs["outdirs"][ind]
        if usejpxs:
            dojpx = kwargs["dojpxs"][ind]
        if usetiffs:
            dotiff = kwargs["dotiffs"][ind]
        if (dojpx or dotiff):
            convertone(mfloc,inpaths[ind],outname=outname,outdir=outdir,dojpx=dojpx,dotiff=dotiff)
        else:
            convertone(mfloc,inpaths[ind],outname=outname,outdir=outdir)
