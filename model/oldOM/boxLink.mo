model boxLink

Modelica.Mechanical.MultiBody.Interfaces.Frame_a frame_a;
Modelica.Mechanical.MultiBody.Interfaces.Frame_b frame_b;

parameter Modelica.SIunits.Distance length;
parameter Modelica.SIunits.Distance width;
parameter Modelica.SIunits.Distance height;

parameter Modelica.SIunits.Density density;
final parameter Modelica.SIunits.Mass mass = length*width*height*density;

final parameter Modelica.SIunits.Inertia ineratiaTensor[3, 3] = diagonal(1/12 * mass(height*height+length*length), 1/12 * mass * (width*width+length*length), 1/12 * mass * (width*width+height*height));

parameter Modelica.SIunits.Angle angle(start=0) "Angle around the x-axis in frame_a";
parameter Modelica.SIunits.Position r[3](start={0,0,length}) "Vector from frame_a to frame_b, resolved in frame_a";

parameter Modelica.Mechanics.MultiBody.Axis heightDirection={0,0,1} "Axis in direction of the height of the box, resolved in frame_a";
parameter Modelica.SIunits.Position r_0[3](start={0,0,0}) "Position relative to origin of world";
parameter Modelica.SIunits.Velocity v_0[3](start={0,0,0}) "Velocity relative to origin of world";
parameter Modelica.SIunits.Acceleration a_0[3](start={0,0,0}) "Acceleration relative to origin of world";

equation



end boxLink;