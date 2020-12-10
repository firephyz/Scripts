import pickle
import numpy as np
import matplotlib.pyplot as plt


def main():
    local_start = locals().copy()

################################################################################
    file = open('/home/kyle/dev/probs/run_5/probs_25000.pydat', 'rb')
    data = pickle.load(file)
    file.close()

    cs = data[1]
    data = data[0]

    ps = list(zip(iter(data), iter(cs)))
    ps = sorted(ps, key=lambda v: v[0])

    ns = np.transpose(np.array(ps))

################################################################################
    l = []
    for l in local_start:
        print("Removing '{}'".format(l))
        exec('del({})'.format(l))
    del(local_start)
    del(l)
    _new_globals = {}
    _old_locals = locals().copy()
    for g in _old_locals.keys():
        if g != '_new_globals':
            print("Adding '{}'".format(g))
            _new_globals[g] = locals()[g]
    for g in _new_globals.keys():
        globals()[g] = _new_globals[g]

# def probfunc(prob, count, n):
#      if count < 2:
#          countlog = 1
#      else:
#          countlog = int(np.log10(count) + 0.5)
#      print(countlog)
#      if count < 2:
#          numscale = 0
#      else:
#          numscale = int(np.log10(n) - 0.5) - countlog
#          if numscale < 0:
#              numscale = 0
#      print("numscale: {}".format(numscale))
#      a = prob ** count
#      b = (1-prob) ** (n - count)
#      print("b: {}".format(b))
#      prod = 1
#      fact = 1.0
#      for i in range(count):
#          prod *= (n / (10 ** numscale)) - i
#          fact *= i + 1
#      print("prod scale: {}\nfact: {}".format(prod, fact))
#      c = (10.0 ** (numscale * count)) * prod / fact
#      print("{}\n{}\n{}".format(a, b, c))
#      return a * b * c



if __name__ == "__main__":
    main()
