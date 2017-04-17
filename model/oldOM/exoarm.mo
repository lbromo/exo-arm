model exoarm
  Modelica.Mechanics.MultiBody.Joints.Revolute revolute1(phi(displayUnit = "rad"))  annotation(Placement(visible = true, transformation(origin = {-32, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.MultiBody.Joints.Revolute revolute2 annotation(Placement(visible = true, transformation(origin = {36, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.MultiBody.Parts.BodyBox bodyBox1(angles_start(displayUnit = "rad"), density(displayUnit = "kg/m3"), r = {0.5, 0, 0})  annotation(Placement(visible = true, transformation(origin = {2,0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.MultiBody.Parts.BodyBox bodyBox2(angles_start(displayUnit = "rad"), density(displayUnit = "kg/m3"), r = {0.5, 0, 0})  annotation(Placement(visible = true, transformation(origin = {66, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Mechanics.MultiBody.World world annotation(Placement(visible = true, transformation(origin = {-64, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Electrical.Analog.Sources.TrapezoidCurrent trapezoidCurrent1(I = 1, period = 1 / 150000, startTime = 2 / 450000, width = 1 / 450000) annotation(Placement(visible = true, transformation(origin = {10, 70}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  bldcMotor bldcMotor1 annotation(Placement(visible = true, transformation(origin = {36, 28}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
equation
  connect(trapezoidCurrent1.n, bldcMotor1.v_c) annotation(Line(points = {{20, 70}, {20, 58}, {33, 58}, {33, 38}}, color = {0, 0, 255}));
  connect(bldcMotor1.GND, trapezoidCurrent1.p) annotation(Line(points = {{29, 38}, {0, 38}, {0, 70}}, color = {0, 0, 255}));
  connect(revolute2.axis, bldcMotor1.flange_a) annotation(Line(points = {{36, 10}, {36, 18}}));
  connect(revolute1.frame_a, world.frame_b) annotation(Line(points = {{-42, 0}, {-54, 0}}, color = {95, 95, 95}));
  connect(revolute2.frame_b, bodyBox2.frame_a) annotation(Line(points = {{46, 0}, {56, 0}, {56, 0}, {56, 0}}, color = {95, 95, 95}));
  connect(bodyBox1.frame_b, revolute2.frame_a) annotation(Line(points = {{12, 0}, {26, 0}, {26, 0}, {26, 0}}, color = {95, 95, 95}));
  connect(revolute1.frame_b, bodyBox1.frame_a) annotation(Line(points = {{-22, 0}, {-8, 0}, {-8, 0}, {-8, 0}}, color = {95, 95, 95}));
  annotation(uses(Modelica(version = "3.2.2")));
end exoarm;