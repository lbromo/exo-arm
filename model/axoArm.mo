model axoArm
inner Modelica.Mechanics.MultiBody.World world;

// Electrical
dcMotor shoulderMotor(ra = 0.128, la=0.000062, kt = 0.0305, ke=313);
dcMotor elbowMotor(ra = 1.24, la=0.00056, ke=374, kt=0.0255);
Modelica.Electrical.Analog.Sources.ConstantVoltage vShoulder(V=12);
Modelica.Electrical.Analog.Sources.ConstantVoltage vElbow(V=12);
Modelica.Electrical.Analog.Basic.Ground gnd;

// Mechanical
Modelica.Mechanics.Rotational.Components.Fixed fixed;
Modelica.Mechanics.Rotational.Components.IdealGear shoulderGear (ratio=50);
Modelica.Mechanics.Rotational.Components.IdealGear elbowGear (ratio=50);
Modelica.Mechanics.MultiBody.Joints.Revolute shoulderJoint;
Modelica.Mechanics.MultiBody.Joints.Revolute elbowJoint;


Modelica.Mechanics.MultiBody.Parts.BodyBox upperArm (density=2700, length=0.2, width=0.05, height=0.01);
Modelica.Mechanics.MultiBody.Parts.BodyBox foreArm (density=2700, length=0.2, width=0.05, height=0.01);
Modelica.Mechanics.MultiBody.Parts.Fixed fixedFrame;
Modelica.Mechanics.MultiBody.Parts.PointMass mass(m=0);

equation

// Electrical
connect(vShoulder.p, shoulderMotor.p);
connect(vShoulder.n, shoulderMotor.n);
connect(vElbow.p, elbowMotor.p);
connect(vElbow.n, elbowMotor.n);
connect(vElbow.n, gnd.p);
connect(vShoulder.n, gnd.p);

// Mechanical

// Motor init
// Connect to mechanical Zero, and referece frame
connect(fixed.flange, shoulderMotor.intsup.flange);
connect(world.frame_b, shoulderJoint.frame_a);
connect(shoulderGear.fixed, fixed.flange);
connect(shoulderJoint.Support, fixed.flange);


// Shoulder Motor and gear, and connect to upper arm
connect(shoulderMotor.axel, shoulderGear.flange_a);
connect(upperArm.frame_b, elbowMount.frame_a);

// Elbow Motor and gear and connect to forearm
connect(elbowMount.flange_b, elbowMotor.intsup.flange);
connect(elbowMotor.axel, elbowGear.flange_a);
connect(foreArm.frame_b, mass.frame_a);

end axoArm;