function cur = pwm2cur(pwm, dir, joint, offset)

	if ~exist('offset')
		offset=0;
	end

	pwm = (pwm-25) .* sign(dir-0.5);

	if joint == 1 % elbow
		cur = (pwm)./(205/1) + sign(dir-0.5).*offset;
	elseif joint == 2 % shoulder
		cur = (pwm)./(205/3) + sign(dir-0.5).*offset;;
	end
end