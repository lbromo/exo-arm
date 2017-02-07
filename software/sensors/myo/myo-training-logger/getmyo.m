% data = getmyo(name)
function data = getmyo(name)

addpath('./logs');
idx = 0;

while(exist(strcat(name,num2str(idx),'.log')))
	filenames{idx+1} = strcat(name,num2str(idx),'.log');
	data{idx+1} = load(filenames{idx+1});
	idx = idx+1;
end
	
end