#DEBUG = True
def dbg(*s):
  if DEBUG:
    if isinstance(s, tuple):
      print(''.join(map(str,s)))