function [smoothStruct] = smoothData(dataStruct, ids)

	smoothStruct = dataStruct;

	for i = 1:length(ids)
		smoothStruct.data(:,ids(i)) = smooth(dataStruct.data(:,ids(i)));
	end

end