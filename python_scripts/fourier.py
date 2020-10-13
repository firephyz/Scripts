import warnings

def main():
    N = 2002
    w = 1.0;
    Nf = 100

    freqs = np.arange(-Nf,Nf+1).reshape((2*Nf+1,1))
    xs = np.linspace(0, 2*np.pi, N).reshape((N, 1))

    signal = np.round(np.linspace(0,20,N)).reshape((N,1))
    res = fft(xs, freqs, signal)
    resig = ifft(xs, freqs, res)

    # shifted_signal = fft_shift(signal)
    # sres = fft(xs, freqs, shifted_signal)
    #
    # shifted_sres = fft_shift(sres)
    # resig = ifft(xs, freqs, shifted_sres)
    #
    N = 2001
    #xs = np.linspace(0,2*np.pi,N).reshape((N,1))
    test = signal
    signal = np.exp(-(4*(xs-np.pi) ** 2)) * signal

    res = fft(xs, freqs, signal)
    sres = fft(xs, freqs, fft_shift(signal))
    resig = ifft(xs, freqs, res)

    #plt.plot(xs, test, xs, signal); plt.show()
    #plt.plot(freqs, res.real, '', freqs, res.imag); plt.show()
    #plt.plot(xs, resig.real, '', xs, signal); plt.show()
    plt.plot(freqs, res.real, '', freqs, sres.real); plt.show()

    # # construct square wave
    # Ncycle = int(np.floor(N / 3))
    # Nones = int(np.round(Ncycle * (w / (2*np.pi))))
    # Nzeros = Ncycle - Nones
    # signal = np.concatenate((np.ones((Nones,)), np.zeros((Nzeros,))))
    # signal = np.tile(signal, (3,))
    # signal = np.concatenate((signal, np.zeros((N - signal.shape[0],))))
    #
    # # compute exact fft
    # with warnings.catch_warnings():
    #     warnings.simplefilter('ignore')
    #     coefs = (np.exp(-1j*(freqs*w-np.pi/2)) - 1j) / (freqs * 2 * np.pi)
    # coefs[Nf] = w / (2*np.pi)
    # coefs = coefs.conj()
    #
    # # compute reconstructed square wave
    # new_square = ifft(xs, freqs, coefs)
    #
    # signal = 2*np.cos(8*xs[667:1334]) + np.sin(5*xs[667:1334])
    # res = fft(xs[667:1334], freqs, signal)

    gvars = ['sres', 'shifted_sres', 'N', 'xs', 'signal', 'coefs', 'freqs', 'new_signal', 'integrand', 'integral', 'res', 'resig', 'shifted_signal']
    gvar_decl_string = ';'.join(map(lambda varident: 'globals()[\'{0}\'] = {0}'.format(varident), gvars))
    exec(gvar_decl_string)

def fft_shift(signal):
    middle = int(np.floor((signal.shape[0] + 1) / 2))
    return np.concatenate((signal[middle:], signal[:middle]))


def fft(xs, freqs, signal):
    integrand = signal * np.exp(-1j*freqs.T*xs)
    integral = np.sum(integrand, 0).T * (2*np.pi/xs.shape[0]) / (2*np.pi)
    integral = integral.conj()
    return integral

def ifft(xs, freqs, coefs):
    new_signal = (coefs.T.conj() * np.exp(1j*freqs.T*xs) + coefs.T * np.exp(-1j*freqs.T*xs)) / 2
    return np.sum(new_signal, 1)


if __name__ == '__main__':
    main()
