## By: Guy Soffer (GSOF) 11/FNov/2025
def test(title, expected, actual, tol=0):
    if abs(actual -expected) <= tol:
        mark = "PASS"
        equ = "=="
    else:
        mark = "FAIL"
        equ = "!="
        
    print("[%s] %s, Expected vs Actual (%1.3f %s %1.3f +/-%1.3f)"%(mark, title, expected, equ, actual, tol))
