% -----------------------------------------
% LOAD DATA AND PARAMETERS
% -----------------------------------------
% params = ParametersScript();
N = params.N;
timeF=0;
timeL=0;
m2 = importdata('both/motor1_both_march_3.log');      %new_1              %time,angle,velocity,current
m1 = importdata('both/motor2_both_march_3.log');       %march_3            %time,angle,velocity,current
in = importdata('both/input_both_march_3.log');                    %on1,dir1,pwm1,on2,dir2,pwm2

%m1 and m2
time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));
ang_id = find(~cellfun(@isempty,strfind(m1.colheaders,'angle')));
vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));

time = (m1.data(:,time_id)- m1.data(1,time_id))./1000;              %to start from 0 and in ms
global Ts;                                                          %sample times
Ts = zeros(length(time(1:end-1)),1);
for a = 1:length(time(1:end-1))
    Ts(a)=time(a+1)-time(a);
end

time=time(1+timeF:end-timeL,:);                                     %the time vector wanted
Ts=Ts(1+timeF:end-timeL,:);                                         %the sample vector wanted
angle_m1  = (m1.data(1+timeF:length(time)+timeF,ang_id)); 
vel_m1  = (m1.data(1+timeF:length(time)+timeF,vel_id))/N;           %from before to after gear 
cur_m1 = m1.data(1+timeF:length(time)+timeF,cur_id);%.*params.kt1*N;  %to get torque input and after gears
angle_m2  = (m2.data(1+timeF:length(time)+timeF,ang_id)); 
vel_m2  = (m2.data(1+timeF:length(time)+timeF,vel_id))/N;           %from before to after gear 
cur_m2 = m2.data(1+timeF:length(time)+timeF,cur_id);%.*params.kt2*N;  %to get torque input and after gears 

%in  
on1_id = find(~cellfun(@isempty,strfind(in.colheaders,'on1')));
dir1_id = find(~cellfun(@isempty,strfind(in.colheaders,'dir1')));
pwm1_id = find(~cellfun(@isempty,strfind(in.colheaders,'pwm1')));
on2_id = find(~cellfun(@isempty,strfind(in.colheaders,'on2')));
dir2_id = find(~cellfun(@isempty,strfind(in.colheaders,'dir2')));
pwm2_id = find(~cellfun(@isempty,strfind(in.colheaders,'pwm2')));

on_m2 = in.data(1+timeF:length(time)+timeF,on1_id); 
dir_m2  = in.data(1+timeF:length(time)+timeF,dir1_id);
pwm_m2  = in.data(1+timeF:length(time)+timeF,pwm1_id);
on_m1 = in.data(1+timeF:length(time)+timeF,on2_id);
dir_m1  = in.data(1+timeF:length(time)+timeF,dir2_id); 
pwm_m1  = in.data(1+timeF:length(time)+timeF,pwm2_id); 


cur_in_m1 = zeros(length(time),1);
for k=1:length(time)
	cur_in_m1(k)=pwm2cur(pwm_m1(k), dir_m1(k), 2, 0);
end    
cur_in_m1=cur_in_m1.*params.kt1*N;


cur_in_m2= zeros(length(time),1);
for k=1:length(time)
	cur_in_m2(k)=pwm2cur(pwm_m2(k), dir_m2(k), 1, 0);
end  
cur_in_m2=cur_in_m2.*params.kt2*N;
