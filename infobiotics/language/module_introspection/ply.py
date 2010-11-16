import sys
try: raise RuntimeError
except RuntimeError:
    e, b, t = sys.exc_info()
    caller_dict = t.tb_frame.f_back.f_globals
#def lex():
#    for t in caller_dict['tokens']:
#        print t, '=', caller_dict['t_' + t]
for k, v in caller_dict.items():
    print k, '=', v
