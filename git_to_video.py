#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     08/06/2020
# Copyright:   (c) alex 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import moviepy.editor as mp

filename = "unknwon_pleasures"
clip = mp.VideoFileClip(filename + ".gif")
clip.write_videofile(filename + ".mp4")


