close all; clear all;

delete(instrfindall);
s = serialInit('/dev/ttyS01');
fopen(s);
pause(2);


while true

	fwrite(s, '&');

	data = fgets(s);

	data = str2num(data);

	

	pause(0.5);

end