# Quingo Examples for quantumcomputer.ac.cn

This directory hold the examplar quingo programs as used by quantumcomputer.ac.cn.

These files can be directly put inside the program input textbox at quantumcomputer.ac.cn. These files already contains the `main` operation, so it can be directly compiled by the Quingo compiler without the assist of the runtime system.

You can simply run the following command to compile each of these files, for example:
```shell
quingoc ghz.qu
```

If you encounter the following error:
```shell
error: std_qcis: No such module
```

It means that the file `std_qcis.qu` is not put inside any of the include paths:
You can figure out the include paths using the following command:
```shell
> quingoc --dump-include-path
The default include paths of the quingoc compiler:
~/.quingo/include
~/.local/include
~/include
/usr/local/include
/usr/include
```

The content of `std_qcis.qu` is currently:
```quingo
// measurement
opaque MEASURE (qs: qubit[]): bool[];     // measure a list of qubits.
opaque measure (qs: qubit): bool;         // measure a single qubit.

// single-qubit gates
opaque RX (q:qubit, angle:double): unit;  // Rx(angle)
opaque X (q:qubit): unit;                 // Rx( pi  )
opaque X2P (q:qubit): unit;               // Rx( pi/2)
opaque X2M (q:qubit): unit;               // Rx(-pi/2)

opaque RY (q:qubit, angle:double): unit;  // Ry(angle)
opaque Y (q:qubit): unit;                 // Ry( pi  )
opaque Y2P (q:qubit): unit;               // Ry( pi/2)
opaque Y2M (q:qubit): unit;               // Ry(-pi/2)

opaque RZ (q:qubit, angle:double): unit;  // Rz(angle)
opaque Z (q:qubit): unit;                 // Rz( pi  )
opaque S (q:qubit): unit;                 // Rz( pi/2), S
opaque Sd (q:qubit): unit;                // Rz(-pi/2), S dagger
opaque T (q:qubit): unit;                 // Rz( pi/4), T
opaque Td (q:qubit): unit;                // Rz(-pi/4), T dagger

opaque H (q:qubit): unit;


// This operation performs the following rotation on the state:
//  - the angle between the positive x-axis and the rotation axis is `azimuth`;
//  - the rotation angle is `angle`.
opaque XYARB (q:qubit, azimuth:double, angle:double): unit;

// two-qubit gates
opaque CZ (control_qubit:qubit, target_qubit:qubit ): unit;     // CPhase gate
```