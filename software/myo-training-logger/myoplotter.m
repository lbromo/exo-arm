% myoplotter(name,fid)
function myoplotter(name, fid)

if isempty(fid)
	fid=1
end

% Load data
data = getmyo(name);
NO_OF_SAMPLES = length(data);
NO_OF_PODS = 9;

fig = figure(fid);
clf
set(fig, 'Name', name);
whitebg('w');

for pod_id = 2:NO_OF_PODS
	ax = subplot(4,2,pod_id-1);
	for sample_no = 1:NO_OF_SAMPLES
		plot(data{sample_no}(:,pod_id));
		hold on;
	end
	titlestr = sprintf('Pod no %d', pod_id-1);
	title(titlestr)
	grid on;
end
suptitle(name)
end