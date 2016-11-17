function [xdot] = hill_muscle_model(x, a, params)
  length = x(1);
  velocity = x(2);
  
 
  
  Fl=exp(-0.5*(((DLce/Lce0)-phim)/(phiv))^2);
  Fv=0.1433/(0.1074+ep(-1.3*sinh(2.8*(Vce/Vce0)+1.64)));
  Fce=a*Fl*Fv*Fcemax;
  Fpe=(Fmax/(exp(S)-1))*(exp((S/DLmax)*DL)-1);
  acceleration = (1/M)*(Fce+Fpe);

  xdot = [velocity; acceleration];
end
