function tau = cur2torque(cur,joint,params)
	if joint == 1
		tau = cur * params.kt1 * params.N;
	elseif joint == 2
		tau = cur * params.kt2 * params.N;
	end
end