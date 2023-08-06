"""Provides a single convert function for converting any number of image files, with options
"""

from .mfpreqs import findmfplus, convertone, convertmany

def convert(inpaths,**kwargs):
    """Converts one or more images

       Required Arguments:
          inpaths:
             (str)         = path to an image file to be converted
             (list of str) = list of paths to image files to be converted

       Optional Keyword Arguments:
          for one image file:
             outname (str)  = name of the file after converting
             outdir  (str)  = directory for output of converted file
             outtiff (bool) = if True, will convert to OME-TIFF instead of JPEG2000
          for multiple image files:
             outnames (list of str)  = names for each file after converting
             outdirs  (list of str)  = directories for output of each converted file
             outtiffs (list of bool) = for each image, if True, will convert to OME-TIFF
    """
    mfloc = findmfplus()
    if type(inpaths) is list:
        convertmany(mfloc,inpaths,**kwargs)
    elif type(inpaths) is str:
        convertone(mfloc,inpaths,**kwargs)
