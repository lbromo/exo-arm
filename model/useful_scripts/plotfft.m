function plotfft(fs, sig)

	dt = 1/fs;
	N  = size(sig,1);

	X = fftshift(fft(sig));
	dF = fs/N;                      % hertz
   f = -fs/2:dF:fs/2-dF;           % hertz
   %% Plot the spectrum:
   figure;
   plot(f,abs(X)/N);
   xlabel('Frequency (in hertz)');
   title('Magnitude Response');

end