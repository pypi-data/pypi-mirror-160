import os
import sys
import warnings

ERROR_LOOKUP = {}



def error(e, kill=False, message=None):
    print("ERROR OCCURRED:")
    if message is not None:
        print(message)
    print(f"Error: {e}")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f"Error Type: {exc_type}, File Name: {fname}, Line Number: {exc_tb.tb_lineno}")
    if kill == True:
        print("Exiting Program...")
        sys.exit()

def out_warning(w):
    warnings.warn(w)



