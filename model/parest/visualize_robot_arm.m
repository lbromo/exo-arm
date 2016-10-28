function visualize_robot_arm(Ts, theta1, theta2)
run('../ParametersScript');

params.arm.plot([theta1 theta2], 'fps', 1/Ts);

end