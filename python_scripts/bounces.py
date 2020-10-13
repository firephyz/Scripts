# Calculate ellastic collisions of two masses from 3BlueOneBrown's
# pi from colliding balls video on YouTube.

import fractions
import time

def main():
    N = 100000
    n = 1
    #M = fractions.Fraction(1000000000000,1)
    M = 10e7
    a = 2/(M+1)
    b = a*M

    fs = np.zeros((int(N/n)+1,1))
    #fs[0] = 4.7
    #fs_actual = fs[0]
    fs[0] = 2.3
    fs_actual = 2.3
    fsi = 0

    Wzero = -2
    w = Wzero
    #w = -20004
    #w = 2/M
    ans = 0
    is_greater = False
    #values = np.zeros((N,1))
    #values[0] = w

    start_time = time.time()
    print(float(w))
    for i in range(N):
        #w = (w*(b-1)-b) / (w*a+1-a)
        #w = M * w / (2*w+M)
        w = M * (w - 2) / (2*w+M)
        fs_actual = fs_actual / (w+1)*(w-1)
        #w = w / (2*w-1)
        #w = w.limit_denominator(10000)
        #values[i+1] = w
        if i%n == 0:
            print(float(w))
            fs[fsi+1] = fs_actual
            fsi += 1
        if not is_greater and (w > 1):
            is_greater = True
        if is_greater and (w < 1):
            ans = i+1
            break

    print('ANSWER: {}'.format(ans))
    print('Time: {}'.format(time.time() - start_time))
    plt.plot(fs); plt.show()

    gvars = []
    gvar_decl_string = ';'.join(map(lambda varident: 'globals()[\'{0}\'] = {0}'.format(varident), gvars))
    exec(gvar_decl_string)


if __name__ == '__main__':
    main()
