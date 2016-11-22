%function plotSeries(dataStruct, nm, fid, scaling)
function plotSeries(dataStruct, nm, fid, scaling)

if ~exist('fid')
	fid = 1;
end

if ~exist('scaling')
	scaling = 1;
end

dataid = find(~cellfun(@isempty,strfind(dataStruct.colheaders,nm)));
timeid = find(~cellfun(@isempty,strfind(dataStruct.colheaders,'time')));

if isempty(dataid)
	disp('Signal not found');
	return;
else
	figure(fid);
	plot(dataStruct.data(:,timeid), dataStruct.data(:,dataid)*scaling);
	ylabel(nm);
	xlabel('Time');
	grid on;
end 

end