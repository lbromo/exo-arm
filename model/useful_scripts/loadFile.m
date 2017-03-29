function d = loadFile(fn)

	fid = fopen(fn);

	junk = fgetl(fid);
	junk = fgetl(fid);

	fmt = '[u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'', u\''%d\'']\n';
	data = fscanf(fid,fmt);
	data = vec2mat(data,13);

	d.time = data(:,1);
	d.spos = data(:,3)*0.01;
	d.svel = data(:,4)*0.01;
	d.scur = data(:,5)*0.01;
	d.sdir = data(:,6);
	d.spwm = data(:,7);
	d.epos = data(:,9)*0.01;
	d.evel = data(:,10)*0.01;
	d.ecur = data(:,11)*0.01;
	d.edir = data(:,12);
	d.epwm = data(:,13);
end