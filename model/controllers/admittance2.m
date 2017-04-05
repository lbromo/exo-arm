function x_ref = admittance2(new_tau, params, cpars)
  Ts = 0.01;

  persistent tau k x_pre;
  if isempty(tau)
	  tau = zeros(2,2);
  end
  if isempty(k)
	  k = 2;
  end
  if isempty(x_pre)
	  x_pre = zeros(6,1);
  end

  k = k+1;
  tau(:,k) = new_tau;

  psi = 60;
  Tm = 0.01;
  Km = 175;

  Kc = (20 * psi * Tm) / Km;
  Ti = 15 * psi * Tm;
  Td = Tm^2 / 10;

  x_ref = zeros(6,1);
  x_ref(1:2) = x_pre(1:2) + Kc * ((1 + Ts/Ti + Td/Ts).*tau(:,k) - (1 + 2*Td/Ts).*tau(:,k-1) + Td/Ts.*tau(:,k-2));
  x_ref(3:4) = x_ref(1:2) - x_pre(1:2);
  x_ref(5:6) = x_ref(3:4) - x_pre(3:4);
  x_pre = x_ref;

end
