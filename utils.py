import sys, os, datetime, shutil

def get_datetime() :
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")

def get_datetime_stamp() :
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def get_rsc_path() :
    return "./rsc"
