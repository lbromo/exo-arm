% function s = makeFIR(num,den)
% returns string with difference equation corresponding to discrete input filter
function s = makeFIR(num,den,iname,oname)

numlen = length(num);
denlen = length(den);

if numlen > denlen
	disp('Noncausal system. No solution for you')
end

if ~exist('iname')
	iname = 'u';
end
if ~exist('oname')
	oname = 'y';
end

s = [oname '(n) ='];

ins = sprintf('1/%f * (%f * %s(n) + ', den(1),num(1), iname);
for idx = 1:numlen-1
	ins = [ins sprintf('%f * %s(n-%d)',num(idx+1),iname,idx)];
	if idx ~= numlen-1
		ins = [ins ' + '];
	end
end

os = '';
for idx = 1:denlen-1
	os = [os sprintf(' - %f * %s(n-%d)', den(idx+1), oname,idx)];
	if idx ~= denlen-1
		os = [os ' + '];
	end
end
os = [os ')'];

s = [s ins os];

end