function [s] = serialInit(port)
	% Initialize Serial object
	s = serial(port);
	set(s,'DataBits',8);
	set(s,'StopBits',1);
	set(s,'BaudRate',230400);
	set(s,'TimeOut',5);
	set(s,'Parity','none');
	
end