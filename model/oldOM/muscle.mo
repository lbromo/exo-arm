model muscle
  Modelica.Mechanics.Translational.Components.Spring spring1(c = 1)  annotation(Placement(visible = true, transformation(origin = {26, 46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Spring spring2(c = 1)  annotation(Placement(visible = true, transformation(origin = {6, 14}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Fixed fixed1 annotation(Placement(visible = true, transformation(origin = {-30, -8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sources.Position position1 annotation(Placement(visible = true, transformation(origin = {-10, 46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass1(m = 1)  annotation(Placement(visible = true, transformation(origin = {80, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 1, height = -1, offset = 1)  annotation(Placement(visible = true, transformation(origin = {-54, 46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Damper damper1(d = 0.1)  annotation(Placement(visible = true, transformation(origin = {78, -4}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
equation
  connect(damper1.flange_b, fixed1.flange) annotation(Line(points = {{68, -4}, {-30, -4}, {-30, -8}, {-30, -8}}, color = {0, 127, 0}));
  connect(fixed1.flange, spring2.flange_a) annotation(Line(points = {{-30, -8}, {-30, 2}, {-4, 2}, {-4, 14}}, color = {0, 127, 0}));
  connect(mass1.flange_b, damper1.flange_a) annotation(Line(points = {{90, 30}, {90, 13}, {88, 13}, {88, -4}}, color = {0, 127, 0}));
  connect(position1.s_ref, ramp1.y) annotation(Line(points = {{-22, 46}, {-44, 46}, {-44, 46}, {-42, 46}}, color = {0, 0, 127}));
  connect(spring1.flange_b, mass1.flange_a) annotation(Line(points = {{36, 46}, {70, 46}, {70, 30}, {70, 30}}, color = {0, 127, 0}));
  connect(position1.flange, spring1.flange_a) annotation(Line(points = {{0, 46}, {16, 46}, {16, 46}, {16, 46}}, color = {0, 127, 0}));
  connect(spring2.flange_a, position1.support) annotation(Line(points = {{-4, 14}, {-10, 14}, {-10, 36}, {-10, 36}}, color = {0, 127, 0}));
  connect(spring1.flange_b, spring2.flange_b) annotation(Line(points = {{36, 46}, {60, 46}, {60, 14}, {16, 14}, {16, 14}}, color = {0, 127, 0}));
  annotation(uses(Modelica(version = "3.2.2")));
end muscle;