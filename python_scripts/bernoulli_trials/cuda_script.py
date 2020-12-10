import random
import numpy as np
import pickle
import torch

bounds = []
Ntimes = 0
Ntrials = 100000

def trial():
    global bounds, Ntimes
    logprob = random.random() * (bounds[1] - bounds[0]) + bounds[0]
    prob = 10 ** logprob
    count = 0
    nums = torch.rand(Ntimes, dtype=torch.float64, device="cuda")
    # for i in range(Ntimes):
    #     if random.random() <= prob:
    #         count += 1
    count = torch.sum(nums)
    return count, prob


def run_trials():
    probs = []
    counts = []
    global Ntrials
    n_col = int(Ntrials * 0.05)
    n_line = int(Ntrials * 0.1)
    for i in range(Ntrials):
        if i % n_col == 0 and i != 0:
            print(' ', end='')
        if i % n_line == 0:
            if i != 0:
                print('')
            print("{}: ".format(int(i / n_line)), end='')
        if i % int(Ntrials * 0.01) == 0:
            print('x', end='', flush=True)
        count, prob = trial()
        probs += [prob]
        counts += [count]
        # if count == 0:
        #     probs += [prob]
    return probs, counts


def print_results(probs):
    print("\nMean: {}".format(np.mean(probs)))
    print("Variance: {}".format(np.var(probs)))


def main():
    result = []
    bs = [[-2.7532, -8.5918],
          [-3.0276, -9.1938],
          [-3.3036, -9.7959],
          [-3.5810, -10.3979],
          [-3.8597, -11.0000],
          [-4.2297, -11.7959],
          [-4.5108, -12.3979],
          [-4.7927, -13.0000],
          [-5.0754, -13.602],
          [-5.4503, -14.398],
          [-5.7347, -15],
          [-6.0197, -15.602],
          [-6.3973, -16.398],
          [-6.6835, -17],
          [-6.9703, -17.602],
          [-7.3500, -18.398]];
    ts = [6250, 12500, 25000, 50000, 100000, 250000, 500000, 1000000, 2000000, 5000000, 10000000, 20000000, 50000000, 100000000, 200000000, 500000000]


    global bounds, Ntimes
    for i in range(len(ts)):
        bounds = bs[i]; bounds[0] *= 0.94; bounds[1] *= 1.06
        Ntimes = ts[i]
        print("\nRun: {}, [{}, {}]".format(Ntimes, bounds[0], bounds[1]))
        probs, counts = run_trials()
        print_results(probs)
        result += [probs, counts]

        file = open('/storage/probs_{}.pydat'.format(Ntimes), 'wb')
        pickle.dump([probs, counts], file)
        file.close()


    globals()['ps'] = result


if __name__ == "__main__":
    main()
