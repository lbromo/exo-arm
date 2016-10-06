model axoArm
inner Modelica.Mechanics.MultiBody.World world(enableAnimation=false);
extends Modelica.Icons.Example;

// Electrical
dcMotor shoulderMotor(ra = 0.128, la=0.000062, kt = 0.0305, ke=313);
//dcMotor elbowMotor(ra = 1.24, la=0.00056, ke=374, kt=0.0255);
Modelica.Electrical.Analog.Sources.ConstantVoltage vShoulder(V=12);
//Modelica.Electrical.Analog.Sources.ConstantVoltage vElbow(V=12);
Modelica.Electrical.Analog.Basic.Ground gnd;

// Mechanical
Modelica.Mechanics.Rotational.Components.Fixed fixed;
Modelica.Mechanics.Rotational.Components.IdealGear shoulderGear (ratio=1/50);
//Modelica.Mechanics.Rotational.Components.IdealGear elbowGear (ratio=1/50);

Modelica.Mechanics.MultiBody.Parts.Mounting1D fixedMount;
Modelica.Mechanics.MultiBody.Joints.Revolute shoulderJoint(useAxisFlange=true);
//Modelica.Mechanics.MultiBody.Joints.Revolute elbowJoint;
Modelica.Mechanics.MultiBody.Parts.BodyBox upperArm (density=2700, length=0.2, width=0.05, height=0.01);
//Modelica.Mechanics.MultiBody.Parts.BodyBox foreArm (density=2700, length=0.2, width=0.05, height=0.01);


equation

// Electrical
connect(vShoulder.p, shoulderMotor.p);
connect(vShoulder.n, shoulderMotor.n);
//connect(vElbow.p, elbowMotor.p);
//connect(vElbow.n, elbowMotor.n);
//connect(vElbow.n, gnd.p);
connect(vShoulder.n, gnd.p);

// Mechanical

// Connect to mechanical Zero, and referece frame
connect(fixed.flange, shoulderMotor.intsup.flange);
connect(fixed.flange, shoulderGear.support);
connect(fixed.flange, shoulderJoint.support);
connect(fixed.flange, shoulderJoint.fixed.flange);
connect(fixedMount.flange_b, fixed.flange);
connect(world.frame_b, fixedMount.frame_a);


// Shoulder Motor and gear, and connect to upper arm
// Rotational
connect(shoulderMotor.axel, shoulderGear.flange_a);
connect(shoulderGear.flange_b, shoulderJoint.axis);
// Kinematic
connect(shoulderJoint.frame_a, world.frame_b);
connect(shoulderJoint.frame_b, upperArm.frame_a);

//connect(upperArm.frame_b, elbowJoint.frame_a);


// Elbow motor and gear and connection to arm.
// Rotational
//connect(elbowJoint.support, elbowGear.support);
//connect(elbowJoint.support, elbowMotor.intsup.flange);
//connect(elbowMotor.axel, elbowJoint.axis);
//connect(elbowMotor.axel, elbowGear.flange_a);
//connect(elbowGear.flange_b, elbowJoint.axis);
// Kinematic
// connect(elbowJoint.frame_b, foreArm.frame_a);


end axoArm;