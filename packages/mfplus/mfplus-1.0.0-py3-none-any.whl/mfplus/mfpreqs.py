"""Contains the supporting functions called by convert in mfpconvert
"""

from winreg import OpenKey as regOpenKey
from winreg import QueryInfoKey as regQInfo
from winreg import QueryValueEx as regQVEx
from winreg import EnumKey as regEnumKey
from winreg import HKEY_LOCAL_MACHINE as HKLM
from subprocess import run

def findmfplus():
    """Finds the location of MicroFile+.exe on the current system

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
        return loc + "Microfile+headless.exe"
    else:
        return None

def convertone(mfloc,inpath,**kwargs):
    """Converts one image

       Required Arguments:
          mfloc (str)  = path to MicroFile+.exe on this system
          inpath (str) = path to an image file to be converted

       Optional Keyword Arguments:
          outname (str)  = name of the file after converting
          outdir  (str)  = directory for output of converted file
          outtiff (bool) = if True, will convert to OME-TIFF instead of JPEG2000
    """
    outname = None
    if "outname" in kwargs.keys():
        if type(kwargs["outname"]) is str:
            outname = kwargs["outname"]
    outdir = None
    if "outdir" in kwargs.keys():
        if type(kwargs["outdir"]) is str:
            outdir = kwargs["outdir"]
    outtiff = False
    if "outtiff" in kwargs.keys():
        if type(kwargs["outtiff"]) is bool:
            outtiff = kwargs["outtiff"]
    cmds = list()
    cmds.append(mfloc)
    cmds.append("-i")
    cmds.append(inpath)
    if type(outname) is str:
        cmds.append("-o")
        cmds.append(outname)
    if type(outdir) is str:
        cmds.append("-d")
        cmds.append(outdir)
    if outtiff:
        cmds.append("--ometiff")
    run(cmds)

def convertmany(mfloc,inpaths,**kwargs):
    """Converts many images

       Required Arguments:
          mfloc (str)  -- path to MicroFile+.exe on this system
          inpaths (list of str) -- path to an image file to be converted

       Optional Keyword Arguments:
          outnames (list of str)  = names for each file after converting
          outdirs  (list of str)  = directories for output of each converted file
          outtiffs (list of bool) = for each image, if True, will convert to OME-TIFF
    """
    usenames = False
    usedirs = False
    usetiffs = False
    if "outnames" in kwargs.keys():
        if type(kwargs["outnames"]) is list:
            if len(kwargs["outnames"]) == len(inpaths):
                usenames = True
    if "outdirs" in kwargs.keys():
        if type(kwargs["outdirs"]) is list:
            if len(kwargs["outdirs"]) == len(inpaths):
                usedirs = True
    if "outtiffs" in kwargs.keys():
        if type(kwargs["outtiffs"]) is list:
            if len(kwargs["outtiffs"]) == len(inpaths):
                usetiffs = True
    for ind in range(len(inpaths)):
        outname = None
        outdir = None
        outtiff = False
        if usenames:
            outname = kwargs["outnames"][ind]
        if usedirs:
            outdir = kwargs["outdirs"][ind]
        if usetiffs:
            outtiff = kwargs["outtiffs"][ind]
        convertone(mfloc,inpaths[ind],outname=outname,outdir=outdir,outtiff=outtiff)
