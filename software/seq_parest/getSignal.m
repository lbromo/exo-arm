function sig = getSignal(data_obj, name)
	id = find(~cellfun(@isempty,strfind(data_obj.colheaders,name)));
	sig = data_obj.data(:,id);
end
