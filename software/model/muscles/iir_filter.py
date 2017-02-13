def iir_filter(b, a, x, y):
    y = list(reversed(y))
    x = list(reversed(x))

    tmp = sum(b[k]*x[k] for k in range(len(b))) + sum(-a[k+1]*y[k] for k in range(0,len(a)-1))
    return 1/a[0] * tmp
