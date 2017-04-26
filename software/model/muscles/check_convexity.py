if __name__ == '__main__':
    import sympy as sp

    vars = sp.symbols('F_ce_max L_max, L_ts Delta_L_ce Delta_L_pe L_ms L_ce0 phi_m phi_v V_ce V_ce0, Spe')
    Fce_max, Lmax, Lts, dLce, dLpe, Lms, Lce0, phi_m, phi_v, Vce, Vce0, Spe = vars


    f_le = sp.exp(-1/2*(((dLce-Lms/Lce0) - phi_m)/phi_v)**2)
    g_ve = 0.1433/(0.1074 + sp.exp(-1.3 * sp.sinh(2.8*Vce/Vce0 + 1.64)))

    Fpe_max = 0.05 * Fce_max
    dLpe_max = Lmax - (Lce0 - Lts)

    f_pe = Fpe_max/(sp.exp(Spe)-1) * (sp.exp(Spe/dLpe_max * dLpe) - 1)

    f = f_le * g_ve * f_pe * Fce_max

    lf = sp.log(g_ve)

    sp.pprint(g_ve)
    print('#' * 80)
    sp.pprint(sp.expand_log(lf))
    input()

    dlf = sp.zeros(len(vars))
    for j in range(len(vars)):
        for k in range(len(vars)):
            tmp = lf.diff(vars[j], vars[k])
            dlf[j,k] = tmp


    ddlf = sp.zeros(len(vars))
    for j in range(len(vars)):
        for k in range(len(vars)):
            tmp = dlf[j,k].diff(vars[j], vars[k])
            ddlf[j,k] = tmp

    sp.pprint(ddlf)


    print('#' * 80)
    print(sp.latex(ddlf))


    # ddlf = []
    # for v, _dlf in zip(vars, dlf):
    #     ddlf.append(_dlf.diff(v))


    # for _ddlf in ddlf:
    #     print('#' * 40)
    #     sp.pprint(sp.simplify(_ddlf))
