model dcMotor
parameter Modelica.SIunits.ElectricalTorqueConstant kt;
parameter Real ke;
parameter Modelica.SIunits.Resistance ra;
parameter Modelica.SIunits.Inductance la;

Modelica.SIunits.Voltage v;
Modelica.SIunits.Voltage ve;
Modelica.SIunits.Current i;
Modelica.SIunits.Angle phi;
Modelica.SIunits.AngularVelocity omega;
Modelica.SIunits.Torque tau;
Modelica.Mechanics.Rotational.Interfaces.Flange_b axel;
Modelica.Electrical.Analog.Interfaces.PositivePin p;
Modelica.Electrical.Analog.Interfaces.NegativePin n;
Modelica.Mechanics.Rotational.Interfaces.InternalSupport intsup(tau=-axel.tau);

equation

// Electrical part
v = i * ra + la * der(i) + ve "KVL";
p.v-n.v = v;
p.i = i;
p.i+n.i = 0 "KCL";


// Mechanical part
ve = -ke * omega;
axel.phi-intsup.phi = phi;
der(phi) = omega;
tau = kt * i;
axel.tau = tau;

end dcMotor;