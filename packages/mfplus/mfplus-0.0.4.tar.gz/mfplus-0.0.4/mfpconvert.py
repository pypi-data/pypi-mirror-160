"""Provides a single convert function for converting any number of image files, with options
"""

from . mfpreqs import findmfplus, convertone, convertmany

def convert(inpaths,**kwargs):
    """Converts one or more images

       Required Arguments:
          inpaths:
             (str)         = path to an image file to be converted
             (list of str) = list of paths to image files to be converted

       Optional Keyword Arguments:
          for one image file:
             outname (str) = name of the file after converting
             outdir  (str) = directory for output of converted file
             dojpx  (bool) = if True, will convert to a JPEG2000 (True by default)
             dotiff (bool) = if True, will convert to an OME-TIFF
          for multiple image files:
             outnames (list of str) = names for each file after converting
             outdirs  (list of str) = directories for output of each converted file
             dojpxs  (list of bool) = for each image, if True, will convert to a JPEG2000 (True by default)
             dotiffs (list of bool) = for each image, if True, will convert to an OME-TIFF
    """
    if type(inpaths) is list:
        convertmany(findmfplus(),inpaths,**kwargs)
    elif type(inpaths) is str:
        convertone(findmfplus(),inpaths,**kwargs)
