## By: Guy Soffer (GSOF) 11/Nov/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = "MIT"
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

def test(title, expected, actual, tol=0):
    if abs(actual -expected) <= tol:
        mark = "PASS"
        equ = "=="
    else:
        mark = "FAIL"
        equ = "!="
        
    print("[%s] %s, Expected vs Actual (%1.3f %s %1.3f +/-%1.3f)"%(mark, title, expected, equ, actual, tol))
