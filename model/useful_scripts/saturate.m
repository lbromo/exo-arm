function [satsig] = saturate(sig, mi, ma)

for n = 1:length(sig)
	if sig(n) < mi
		satsig(n) = mi;
	elseif sig(n) > ma
		satsig(n) = ma;
	else
		satsig(n) = sig(n);
	end	
end

end