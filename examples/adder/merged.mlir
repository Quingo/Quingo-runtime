Time taken by options:    1.1700000 ms
[36mAdding path: [0m/home/xiangfu/quingo-tutorials/src/quingo
[36mAdding path: [0m/tmp/tmpnb4a7ykx
[34mmainFilePath: [0m/tmp/tmpnb4a7ykx/main_draper_test_test_sc_adder.qu
Time taken by frontend:   26.4340000 ms
Time taken by mlirgen:   41.0410000 ms
  ===================== MLIR after removeoperation =====================
builtin.module @"/tmp/tmpnb4a7ykx/main_draper_test_test_sc_adder.qu"  {
  builtin.func @power_of_2(%arg0: i32) -> i32 attributes {kind = "operation", llvm.emit_c_interface} {
    %c0_i32 = constant 0 : i32
    %c2_i32 = constant 2 : i32
    %c1_i32 = constant 1 : i32
    %0 = scf.execute_region -> i32 {
      %1:2 = scf.while (%arg1 = %c1_i32, %arg2 = %c0_i32) : (i32, i32) -> (i32, i32) {
        %2 = cmpi slt, %arg2, %arg0 : i32
        scf.condition(%2) %arg1, %arg2 : i32, i32
      } do {
        ^bb0(%arg1: i32, %arg2: i32):  // no predecessors
        %2 = scf.execute_region -> i32 {
          %4 = muli %arg1, %c2_i32 : i32
          scf.yield %4 : i32
        }
        %3 = addi %arg2, %c1_i32 : i32
        scf.yield %2, %3 : i32, i32
      }
      scf.yield %1#0 : i32
    }
    return %0 : i32
  }
  builtin.func @c_phase_k(%arg0: !quingo.qubit, %arg1: !quingo.qubit, %arg2: i32) attributes {kind = "operation", llvm.emit_c_interface} {
    %cst = constant 6.2831853071795862 : f64
    %0 = call @power_of_2(%arg2) : (i32) -> i32
    %1 = quingo.to_double %0 : i32
    %2 = divf %cst, %1 : f64
    %3 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %4 = "quingo.control"(%3) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%4, %arg0, %arg1, %2) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    return
  }
  builtin.func @c_phase_k_m(%arg0: !quingo.qubit, %arg1: !quingo.qubit, %arg2: i32) attributes {kind = "operation", llvm.emit_c_interface} {
    %cst = constant 2.000000e+00 : f64
    %cst_0 = constant 3.1415926535897931 : f64
    %0 = negf %cst : f64
    %1 = mulf %0, %cst_0 : f64
    %2 = call @power_of_2(%arg2) : (i32) -> i32
    %3 = quingo.to_double %2 : i32
    %4 = divf %1, %3 : f64
    %5 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %6 = "quingo.control"(%5) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%6, %arg0, %arg1, %4) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    return
  }
  builtin.func @qft_ns(%arg0: !quingo.list<!quingo.qubit>) attributes {kind = "operation", llvm.emit_c_interface} {
    %c0_i32 = constant 0 : i32
    %c1_i32 = constant 1 : i32
    %0 = quingo.list_length %arg0 : !quingo.list<!quingo.qubit> -> index
    %1 = index_cast %0 : index to i32
    scf.execute_region {
      %2 = subi %1, %c1_i32 : i32
      %3 = scf.while (%arg1 = %2) : (i32) -> i32 {
        %4 = cmpi sge, %arg1, %c0_i32 : i32
        scf.condition(%4) %arg1 : i32
      } do {
        ^bb0(%arg1: i32):  // no predecessors
        scf.execute_region {
          %5 = index_cast %arg1 : i32 to index
          %6 = quingo.list_get %arg0[%5] : !quingo.qubit
          quingo.H(%6)
          scf.execute_region {
            %7 = subi %arg1, %c1_i32 : i32
            %8 = scf.while (%arg2 = %7) : (i32) -> i32 {
              %9 = cmpi sge, %arg2, %c0_i32 : i32
              scf.condition(%9) %arg2 : i32
            } do {
              ^bb0(%arg2: i32):  // no predecessors
              scf.execute_region {
                %10 = index_cast %arg2 : i32 to index
                %11 = quingo.list_get %arg0[%10] : !quingo.qubit
                %12 = index_cast %arg1 : i32 to index
                %13 = quingo.list_get %arg0[%12] : !quingo.qubit
                %14 = subi %arg1, %arg2 : i32
                %15 = addi %14, %c1_i32 : i32
                call @c_phase_k(%11, %13, %15) : (!quingo.qubit, !quingo.qubit, i32) -> ()
                scf.yield
              }
              %9 = subi %arg2, %c1_i32 : i32
              scf.yield %9 : i32
            }
            scf.yield
          }
          scf.yield
        }
        %4 = subi %arg1, %c1_i32 : i32
        scf.yield %4 : i32
      }
      scf.yield
    }
    return
  }
  builtin.func @iqft_ns(%arg0: !quingo.list<!quingo.qubit>) attributes {kind = "operation", llvm.emit_c_interface} {
    %c0_i32 = constant 0 : i32
    %c1_i32 = constant 1 : i32
    %0 = quingo.list_length %arg0 : !quingo.list<!quingo.qubit> -> index
    %1 = index_cast %0 : index to i32
    scf.execute_region {
      %2 = scf.while (%arg1 = %c0_i32) : (i32) -> i32 {
        %3 = cmpi slt, %arg1, %1 : i32
        scf.condition(%3) %arg1 : i32
      } do {
        ^bb0(%arg1: i32):  // no predecessors
        scf.execute_region {
          scf.execute_region {
            %6 = scf.while (%arg2 = %c0_i32) : (i32) -> i32 {
              %7 = cmpi slt, %arg2, %arg1 : i32
              scf.condition(%7) %arg2 : i32
            } do {
              ^bb0(%arg2: i32):  // no predecessors
              scf.execute_region {
                %8 = index_cast %arg2 : i32 to index
                %9 = quingo.list_get %arg0[%8] : !quingo.qubit
                %10 = index_cast %arg1 : i32 to index
                %11 = quingo.list_get %arg0[%10] : !quingo.qubit
                %12 = subi %arg1, %arg2 : i32
                %13 = addi %12, %c1_i32 : i32
                call @c_phase_k_m(%9, %11, %13) : (!quingo.qubit, !quingo.qubit, i32) -> ()
                scf.yield
              }
              %7 = addi %arg2, %c1_i32 : i32
              scf.yield %7 : i32
            }
            scf.yield
          }
          %4 = index_cast %arg1 : i32 to index
          %5 = quingo.list_get %arg0[%4] : !quingo.qubit
          quingo.H(%5)
          scf.yield
        }
        %3 = addi %arg1, %c1_i32 : i32
        scf.yield %3 : i32
      }
      scf.yield
    }
    return
  }
  builtin.func @sc_adder(%arg0: !quingo.list<!quingo.qubit>, %arg1: !quingo.list<i32>, %arg2: i1) attributes {kind = "operation", llvm.emit_c_interface} {
    %cst = constant 0.000000e+00 : f64
    %c0_i32 = constant 0 : i32
    %cst_0 = constant 1.000000e+00 : f64
    %cst_1 = constant 6.2831853071795862 : f64
    %c1_i32 = constant 1 : i32
    %0 = quingo.list_length %arg1 : !quingo.list<i32> -> index
    %1 = index_cast %0 : index to i32
    scf.execute_region {
      %2 = subi %1, %c1_i32 : i32
      %3 = scf.while (%arg3 = %2) : (i32) -> i32 {
        %4 = cmpi sge, %arg3, %c0_i32 : i32
        scf.condition(%4) %arg3 : i32
      } do {
        ^bb0(%arg3: i32):  // no predecessors
        scf.execute_region {
          %5 = scf.execute_region -> f64 {
            %10:2 = scf.while (%arg4 = %cst, %arg5 = %arg3) : (f64, i32) -> (f64, i32) {
              %11 = cmpi sge, %arg5, %c0_i32 : i32
              scf.condition(%11) %arg4, %arg5 : f64, i32
            } do {
              ^bb0(%arg4: f64, %arg5: i32):  // no predecessors
              %11 = scf.execute_region -> f64 {
                %13 = index_cast %arg5 : i32 to index
                %14 = quingo.list_get %arg1[%13] : i32
                %15 = cmpi eq, %14, %c1_i32 : i32
                %16 = scf.if %15 -> (f64) {
                  %17 = scf.execute_region -> f64 {
                    %18 = subi %arg3, %arg5 : i32
                    %19 = addi %18, %c1_i32 : i32
                    %20 = call @power_of_2(%19) : (i32) -> i32
                    %21 = quingo.to_double %20 : i32
                    %22 = divf %cst_0, %21 : f64
                    %23 = addf %arg4, %22 : f64
                    scf.yield %23 : f64
                  }
                  scf.yield %17 : f64
                } else {
                  scf.yield %arg4 : f64
                }
                scf.yield %16 : f64
              }
              %12 = subi %arg5, %c1_i32 : i32
              scf.yield %11, %12 : f64, i32
            }
            scf.yield %10#0 : f64
          }
          %6 = mulf %cst_1, %5 : f64
          %7 = scf.if %arg2 -> (f64) {
            %10 = scf.execute_region -> f64 {
              %11 = negf %6 : f64
              scf.yield %11 : f64
            }
            scf.yield %10 : f64
          } else {
            scf.yield %6 : f64
          }
          %8 = index_cast %arg3 : i32 to index
          %9 = quingo.list_get %arg0[%8] : !quingo.qubit
          quingo.dyn_phase(%9, %7)
          scf.yield
        }
        %4 = subi %arg3, %c1_i32 : i32
        scf.yield %4 : i32
      }
      scf.yield
    }
    return
  }
  builtin.func @test_sc_adder(%arg0: !quingo.list<i32>, %arg1: !quingo.list<i32>, %arg2: i1) -> !quingo.list<i1> attributes {kind = "operation", llvm.emit_c_interface} {
    %c0_i32 = constant 0 : i32
    %c1_i32 = constant 1 : i32
    %0 = quingo.list_length %arg1 : !quingo.list<i32> -> index
    %1 = index_cast %0 : index to i32
    %2 = quingo.list_decl : !quingo.list<i1> [%0]
    %3 = scf.execute_region -> !quingo.list<i1> {
      %4 = quingo.alloc : !quingo.list<!quingo.qubit>[%0]
      %5 = scf.execute_region -> !quingo.list<i1> {
        scf.execute_region {
          %7 = scf.while (%arg3 = %c0_i32) : (i32) -> i32 {
            %8 = cmpi slt, %arg3, %1 : i32
            scf.condition(%8) %arg3 : i32
          } do {
            ^bb0(%arg3: i32):  // no predecessors
            scf.execute_region {
              %9 = index_cast %arg3 : i32 to index
              %10 = quingo.list_get %arg0[%9] : i32
              %11 = cmpi eq, %10, %c1_i32 : i32
              scf.if %11 {
                scf.execute_region {
                  %12 = index_cast %arg3 : i32 to index
                  %13 = quingo.list_get %4[%12] : !quingo.qubit
                  quingo.pauli_x(%13)
                  scf.yield
                }
              }
              scf.yield
            }
            %8 = addi %arg3, %c1_i32 : i32
            scf.yield %8 : i32
          }
          scf.yield
        }
        call @qft_ns(%4) : (!quingo.list<!quingo.qubit>) -> ()
        call @sc_adder(%4, %arg1, %arg2) : (!quingo.list<!quingo.qubit>, !quingo.list<i32>, i1) -> ()
        call @iqft_ns(%4) : (!quingo.list<!quingo.qubit>) -> ()
        %6 = scf.execute_region -> !quingo.list<i1> {
          %7:2 = scf.while (%arg3 = %2, %arg4 = %c0_i32) : (!quingo.list<i1>, i32) -> (!quingo.list<i1>, i32) {
            %8 = cmpi slt, %arg4, %1 : i32
            scf.condition(%8) %arg3, %arg4 : !quingo.list<i1>, i32
          } do {
            ^bb0(%arg3: !quingo.list<i1>, %arg4: i32):  // no predecessors
            %8 = scf.execute_region -> !quingo.list<i1> {
              %10 = index_cast %arg4 : i32 to index
              %11 = quingo.list_get %4[%10] : !quingo.qubit
              %12 = quingo.measure(%11) : (!quingo.qubit) -> i1
              %13 = index_cast %arg4 : i32 to index
              %14 = quingo.list_set %arg3[%13] = %12 : !quingo.list<i1>
              scf.yield %14 : !quingo.list<i1>
            }
            %9 = addi %arg4, %c1_i32 : i32
            scf.yield %8, %9 : !quingo.list<i1>, i32
          }
          scf.yield %7#0 : !quingo.list<i1>
        }
        scf.yield %6 : !quingo.list<i1>
      }
      quingo.dealloc %4 : !quingo.list<!quingo.qubit>
      scf.yield %5 : !quingo.list<i1>
    }
    return %3 : !quingo.list<i1>
  }
  builtin.func @main() -> !quingo.list<i1> attributes {kind = "operation", llvm.emit_c_interface} {
    %c0_i32 = constant 0 : i32
    %true = constant true
    %0 = quingo.list_assemble {%c0_i32, %c0_i32} : !quingo.list<i32> [2]
    %1 = quingo.list_assemble {%c0_i32, %c0_i32} : !quingo.list<i32> [2]
    %2 = call @test_sc_adder(%0, %1, %true) : (!quingo.list<i32>, !quingo.list<i32>, i1) -> !quingo.list<i1>
    return %2 : !quingo.list<i1>
  }
}
  ================ end of MLIR dump for removeoperation ================
  ===================== MLIR after offline =====================
builtin.module @"/tmp/tmpnb4a7ykx/main_draper_test_test_sc_adder.qu"  {
  builtin.func @power_of_2(%arg0: i32) -> i32 attributes {kind = "operation", llvm.emit_c_interface} {
    %c0_i32 = constant 0 : i32
    %c2_i32 = constant 2 : i32
    %c1_i32 = constant 1 : i32
    br ^bb1(%c1_i32, %c0_i32 : i32, i32)
    ^bb1(%0: i32, %1: i32):  // 2 preds: ^bb0, ^bb2
    %2 = cmpi slt, %1, %arg0 : i32
    cond_br %2, ^bb2(%0, %1 : i32, i32), ^bb3(%0 : i32)
    ^bb2(%3: i32, %4: i32):  // pred: ^bb1
    %5 = muli %3, %c2_i32 : i32
    %6 = addi %4, %c1_i32 : i32
    br ^bb1(%5, %6 : i32, i32)
    ^bb3(%7: i32):  // pred: ^bb1
    return %7 : i32
  }
  builtin.func @c_phase_k(%arg0: !quingo.qubit, %arg1: !quingo.qubit, %arg2: i32) attributes {kind = "operation", llvm.emit_c_interface} {
    %c1_i32 = constant 1 : i32
    %c2_i32 = constant 2 : i32
    %c0_i32 = constant 0 : i32
    %cst = constant 6.2831853071795862 : f64
    br ^bb1(%c1_i32, %c0_i32 : i32, i32)
    ^bb1(%0: i32, %1: i32):  // 2 preds: ^bb0, ^bb2
    %2 = cmpi slt, %1, %arg2 : i32
    cond_br %2, ^bb2(%0, %1 : i32, i32), ^bb3(%0 : i32)
    ^bb2(%3: i32, %4: i32):  // pred: ^bb1
    %5 = muli %3, %c2_i32 : i32
    %6 = addi %4, %c1_i32 : i32
    br ^bb1(%5, %6 : i32, i32)
    ^bb3(%7: i32):  // pred: ^bb1
    %8 = quingo.to_double %7 : i32
    %9 = divf %cst, %8 : f64
    %10 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %11 = "quingo.control"(%10) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%11, %arg0, %arg1, %9) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    return
  }
  builtin.func @c_phase_k_m(%arg0: !quingo.qubit, %arg1: !quingo.qubit, %arg2: i32) attributes {kind = "operation", llvm.emit_c_interface} {
    %c1_i32 = constant 1 : i32
    %c2_i32 = constant 2 : i32
    %c0_i32 = constant 0 : i32
    %cst = constant 3.1415926535897931 : f64
    %cst_0 = constant 2.000000e+00 : f64
    %0 = negf %cst_0 : f64
    %1 = mulf %0, %cst : f64
    br ^bb1(%c1_i32, %c0_i32 : i32, i32)
    ^bb1(%2: i32, %3: i32):  // 2 preds: ^bb0, ^bb2
    %4 = cmpi slt, %3, %arg2 : i32
    cond_br %4, ^bb2(%2, %3 : i32, i32), ^bb3(%2 : i32)
    ^bb2(%5: i32, %6: i32):  // pred: ^bb1
    %7 = muli %5, %c2_i32 : i32
    %8 = addi %6, %c1_i32 : i32
    br ^bb1(%7, %8 : i32, i32)
    ^bb3(%9: i32):  // pred: ^bb1
    %10 = quingo.to_double %9 : i32
    %11 = divf %1, %10 : f64
    %12 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %13 = "quingo.control"(%12) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%13, %arg0, %arg1, %11) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    return
  }
  builtin.func @qft_ns(%arg0: !quingo.list<!quingo.qubit>) attributes {kind = "operation", llvm.emit_c_interface} {
    %cst = constant 6.2831853071795862 : f64
    %c2_i32 = constant 2 : i32
    %c1_i32 = constant 1 : i32
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_length %arg0 : !quingo.list<!quingo.qubit> -> index
    %1 = index_cast %0 : index to i32
    %2 = subi %1, %c1_i32 : i32
    br ^bb1(%2 : i32)
    ^bb1(%3: i32):  // 2 preds: ^bb0, ^bb8
    %4 = cmpi sge, %3, %c0_i32 : i32
    cond_br %4, ^bb2(%3 : i32), ^bb9
    ^bb2(%5: i32):  // pred: ^bb1
    %6 = index_cast %5 : i32 to index
    %7 = quingo.list_get %arg0[%6] : !quingo.qubit
    quingo.H(%7)
    %8 = subi %5, %c1_i32 : i32
    br ^bb3(%8 : i32)
    ^bb3(%9: i32):  // 2 preds: ^bb2, ^bb7
    %10 = cmpi sge, %9, %c0_i32 : i32
    cond_br %10, ^bb4(%9 : i32), ^bb8
    ^bb4(%11: i32):  // pred: ^bb3
    %12 = index_cast %11 : i32 to index
    %13 = quingo.list_get %arg0[%12] : !quingo.qubit
    %14 = index_cast %5 : i32 to index
    %15 = quingo.list_get %arg0[%14] : !quingo.qubit
    %16 = subi %5, %11 : i32
    %17 = addi %16, %c1_i32 : i32
    br ^bb5(%c1_i32, %c0_i32 : i32, i32)
    ^bb5(%18: i32, %19: i32):  // 2 preds: ^bb4, ^bb6
    %20 = cmpi slt, %19, %17 : i32
    cond_br %20, ^bb6(%18, %19 : i32, i32), ^bb7(%18 : i32)
    ^bb6(%21: i32, %22: i32):  // pred: ^bb5
    %23 = muli %21, %c2_i32 : i32
    %24 = addi %22, %c1_i32 : i32
    br ^bb5(%23, %24 : i32, i32)
    ^bb7(%25: i32):  // pred: ^bb5
    %26 = quingo.to_double %25 : i32
    %27 = divf %cst, %26 : f64
    %28 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %29 = "quingo.control"(%28) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%29, %13, %15, %27) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    %30 = subi %11, %c1_i32 : i32
    br ^bb3(%30 : i32)
    ^bb8:  // pred: ^bb3
    %31 = subi %5, %c1_i32 : i32
    br ^bb1(%31 : i32)
    ^bb9:  // pred: ^bb1
    return
  }
  builtin.func @iqft_ns(%arg0: !quingo.list<!quingo.qubit>) attributes {kind = "operation", llvm.emit_c_interface} {
    %cst = constant 2.000000e+00 : f64
    %cst_0 = constant 3.1415926535897931 : f64
    %c2_i32 = constant 2 : i32
    %c1_i32 = constant 1 : i32
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_length %arg0 : !quingo.list<!quingo.qubit> -> index
    %1 = index_cast %0 : index to i32
    br ^bb1(%c0_i32 : i32)
    ^bb1(%2: i32):  // 2 preds: ^bb0, ^bb8
    %3 = cmpi slt, %2, %1 : i32
    cond_br %3, ^bb2(%2 : i32), ^bb9
    ^bb2(%4: i32):  // pred: ^bb1
    br ^bb3(%c0_i32 : i32)
    ^bb3(%5: i32):  // 2 preds: ^bb2, ^bb7
    %6 = cmpi slt, %5, %4 : i32
    cond_br %6, ^bb4(%5 : i32), ^bb8
    ^bb4(%7: i32):  // pred: ^bb3
    %8 = index_cast %7 : i32 to index
    %9 = quingo.list_get %arg0[%8] : !quingo.qubit
    %10 = index_cast %4 : i32 to index
    %11 = quingo.list_get %arg0[%10] : !quingo.qubit
    %12 = subi %4, %7 : i32
    %13 = addi %12, %c1_i32 : i32
    %14 = negf %cst : f64
    %15 = mulf %14, %cst_0 : f64
    br ^bb5(%c1_i32, %c0_i32 : i32, i32)
    ^bb5(%16: i32, %17: i32):  // 2 preds: ^bb4, ^bb6
    %18 = cmpi slt, %17, %13 : i32
    cond_br %18, ^bb6(%16, %17 : i32, i32), ^bb7(%16 : i32)
    ^bb6(%19: i32, %20: i32):  // pred: ^bb5
    %21 = muli %19, %c2_i32 : i32
    %22 = addi %20, %c1_i32 : i32
    br ^bb5(%21, %22 : i32, i32)
    ^bb7(%23: i32):  // pred: ^bb5
    %24 = quingo.to_double %23 : i32
    %25 = divf %15, %24 : f64
    %26 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %27 = "quingo.control"(%26) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%27, %9, %11, %25) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    %28 = addi %7, %c1_i32 : i32
    br ^bb3(%28 : i32)
    ^bb8:  // pred: ^bb3
    %29 = index_cast %4 : i32 to index
    %30 = quingo.list_get %arg0[%29] : !quingo.qubit
    quingo.H(%30)
    %31 = addi %4, %c1_i32 : i32
    br ^bb1(%31 : i32)
    ^bb9:  // pred: ^bb1
    return
  }
  builtin.func @sc_adder(%arg0: !quingo.list<!quingo.qubit>, %arg1: !quingo.list<i32>, %arg2: i1) attributes {kind = "operation", llvm.emit_c_interface} {
    %c2_i32 = constant 2 : i32
    %c1_i32 = constant 1 : i32
    %cst = constant 6.2831853071795862 : f64
    %cst_0 = constant 1.000000e+00 : f64
    %c0_i32 = constant 0 : i32
    %cst_1 = constant 0.000000e+00 : f64
    %0 = quingo.list_length %arg1 : !quingo.list<i32> -> index
    %1 = index_cast %0 : index to i32
    %2 = subi %1, %c1_i32 : i32
    br ^bb1(%2 : i32)
    ^bb1(%3: i32):  // 2 preds: ^bb0, ^bb12
    %4 = cmpi sge, %3, %c0_i32 : i32
    cond_br %4, ^bb2(%3 : i32), ^bb13
    ^bb2(%5: i32):  // pred: ^bb1
    br ^bb3(%cst_1, %5 : f64, i32)
    ^bb3(%6: f64, %7: i32):  // 2 preds: ^bb2, ^bb9
    %8 = cmpi sge, %7, %c0_i32 : i32
    cond_br %8, ^bb4(%6, %7 : f64, i32), ^bb10(%6 : f64)
    ^bb4(%9: f64, %10: i32):  // pred: ^bb3
    %11 = index_cast %10 : i32 to index
    %12 = quingo.list_get %arg1[%11] : i32
    %13 = cmpi eq, %12, %c1_i32 : i32
    cond_br %13, ^bb5, ^bb9(%9 : f64)
    ^bb5:  // pred: ^bb4
    %14 = subi %5, %10 : i32
    %15 = addi %14, %c1_i32 : i32
    br ^bb6(%c1_i32, %c0_i32 : i32, i32)
    ^bb6(%16: i32, %17: i32):  // 2 preds: ^bb5, ^bb7
    %18 = cmpi slt, %17, %15 : i32
    cond_br %18, ^bb7(%16, %17 : i32, i32), ^bb8(%16 : i32)
    ^bb7(%19: i32, %20: i32):  // pred: ^bb6
    %21 = muli %19, %c2_i32 : i32
    %22 = addi %20, %c1_i32 : i32
    br ^bb6(%21, %22 : i32, i32)
    ^bb8(%23: i32):  // pred: ^bb6
    %24 = quingo.to_double %23 : i32
    %25 = divf %cst_0, %24 : f64
    %26 = addf %9, %25 : f64
    br ^bb9(%26 : f64)
    ^bb9(%27: f64):  // 2 preds: ^bb4, ^bb8
    %28 = subi %10, %c1_i32 : i32
    br ^bb3(%27, %28 : f64, i32)
    ^bb10(%29: f64):  // pred: ^bb3
    %30 = mulf %cst, %29 : f64
    cond_br %arg2, ^bb11, ^bb12(%30 : f64)
    ^bb11:  // pred: ^bb10
    %31 = negf %30 : f64
    br ^bb12(%31 : f64)
    ^bb12(%32: f64):  // 2 preds: ^bb10, ^bb11
    %33 = index_cast %5 : i32 to index
    %34 = quingo.list_get %arg0[%33] : !quingo.qubit
    quingo.dyn_phase(%34, %32)
    %35 = subi %5, %c1_i32 : i32
    br ^bb1(%35 : i32)
    ^bb13:  // pred: ^bb1
    return
  }
  builtin.func @test_sc_adder(%arg0: !quingo.list<i32>, %arg1: !quingo.list<i32>, %arg2: i1) -> !quingo.list<i1> attributes {kind = "operation", llvm.emit_c_interface} {
    %cst = constant 3.1415926535897931 : f64
    %cst_0 = constant 2.000000e+00 : f64
    %cst_1 = constant 0.000000e+00 : f64
    %cst_2 = constant 1.000000e+00 : f64
    %c2_i32 = constant 2 : i32
    %cst_3 = constant 6.2831853071795862 : f64
    %c1_i32 = constant 1 : i32
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_length %arg1 : !quingo.list<i32> -> index
    %1 = index_cast %0 : index to i32
    %2 = quingo.list_decl : !quingo.list<i1> [%0]
    %3 = quingo.alloc : !quingo.list<!quingo.qubit>[%0]
    br ^bb1(%c0_i32 : i32)
    ^bb1(%4: i32):  // 2 preds: ^bb0, ^bb4
    %5 = cmpi slt, %4, %1 : i32
    cond_br %5, ^bb2(%4 : i32), ^bb5
    ^bb2(%6: i32):  // pred: ^bb1
    %7 = index_cast %6 : i32 to index
    %8 = quingo.list_get %arg0[%7] : i32
    %9 = cmpi eq, %8, %c1_i32 : i32
    cond_br %9, ^bb3, ^bb4
    ^bb3:  // pred: ^bb2
    %10 = index_cast %6 : i32 to index
    %11 = quingo.list_get %3[%10] : !quingo.qubit
    quingo.pauli_x(%11)
    br ^bb4
    ^bb4:  // 2 preds: ^bb2, ^bb3
    %12 = addi %6, %c1_i32 : i32
    br ^bb1(%12 : i32)
    ^bb5:  // pred: ^bb1
    %13 = index_cast %0 : index to i32
    %14 = subi %13, %c1_i32 : i32
    br ^bb6(%14 : i32)
    ^bb6(%15: i32):  // 2 preds: ^bb5, ^bb13
    %16 = cmpi sge, %15, %c0_i32 : i32
    cond_br %16, ^bb7(%15 : i32), ^bb14
    ^bb7(%17: i32):  // pred: ^bb6
    %18 = index_cast %17 : i32 to index
    %19 = quingo.list_get %3[%18] : !quingo.qubit
    quingo.H(%19)
    %20 = subi %17, %c1_i32 : i32
    br ^bb8(%20 : i32)
    ^bb8(%21: i32):  // 2 preds: ^bb7, ^bb12
    %22 = cmpi sge, %21, %c0_i32 : i32
    cond_br %22, ^bb9(%21 : i32), ^bb13
    ^bb9(%23: i32):  // pred: ^bb8
    %24 = index_cast %23 : i32 to index
    %25 = quingo.list_get %3[%24] : !quingo.qubit
    %26 = index_cast %17 : i32 to index
    %27 = quingo.list_get %3[%26] : !quingo.qubit
    %28 = subi %17, %23 : i32
    %29 = addi %28, %c1_i32 : i32
    br ^bb10(%c1_i32, %c0_i32 : i32, i32)
    ^bb10(%30: i32, %31: i32):  // 2 preds: ^bb9, ^bb11
    %32 = cmpi slt, %31, %29 : i32
    cond_br %32, ^bb11(%30, %31 : i32, i32), ^bb12(%30 : i32)
    ^bb11(%33: i32, %34: i32):  // pred: ^bb10
    %35 = muli %33, %c2_i32 : i32
    %36 = addi %34, %c1_i32 : i32
    br ^bb10(%35, %36 : i32, i32)
    ^bb12(%37: i32):  // pred: ^bb10
    %38 = quingo.to_double %37 : i32
    %39 = divf %cst_3, %38 : f64
    %40 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %41 = "quingo.control"(%40) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%41, %25, %27, %39) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    %42 = subi %23, %c1_i32 : i32
    br ^bb8(%42 : i32)
    ^bb13:  // pred: ^bb8
    %43 = subi %17, %c1_i32 : i32
    br ^bb6(%43 : i32)
    ^bb14:  // pred: ^bb6
    %44 = quingo.list_length %arg1 : !quingo.list<i32> -> index
    %45 = index_cast %44 : index to i32
    %46 = subi %45, %c1_i32 : i32
    br ^bb15(%46 : i32)
    ^bb15(%47: i32):  // 2 preds: ^bb14, ^bb26
    %48 = cmpi sge, %47, %c0_i32 : i32
    cond_br %48, ^bb16(%47 : i32), ^bb27
    ^bb16(%49: i32):  // pred: ^bb15
    br ^bb17(%cst_1, %49 : f64, i32)
    ^bb17(%50: f64, %51: i32):  // 2 preds: ^bb16, ^bb23
    %52 = cmpi sge, %51, %c0_i32 : i32
    cond_br %52, ^bb18(%50, %51 : f64, i32), ^bb24(%50 : f64)
    ^bb18(%53: f64, %54: i32):  // pred: ^bb17
    %55 = index_cast %54 : i32 to index
    %56 = quingo.list_get %arg1[%55] : i32
    %57 = cmpi eq, %56, %c1_i32 : i32
    cond_br %57, ^bb19, ^bb23(%53 : f64)
    ^bb19:  // pred: ^bb18
    %58 = subi %49, %54 : i32
    %59 = addi %58, %c1_i32 : i32
    br ^bb20(%c1_i32, %c0_i32 : i32, i32)
    ^bb20(%60: i32, %61: i32):  // 2 preds: ^bb19, ^bb21
    %62 = cmpi slt, %61, %59 : i32
    cond_br %62, ^bb21(%60, %61 : i32, i32), ^bb22(%60 : i32)
    ^bb21(%63: i32, %64: i32):  // pred: ^bb20
    %65 = muli %63, %c2_i32 : i32
    %66 = addi %64, %c1_i32 : i32
    br ^bb20(%65, %66 : i32, i32)
    ^bb22(%67: i32):  // pred: ^bb20
    %68 = quingo.to_double %67 : i32
    %69 = divf %cst_2, %68 : f64
    %70 = addf %53, %69 : f64
    br ^bb23(%70 : f64)
    ^bb23(%71: f64):  // 2 preds: ^bb18, ^bb22
    %72 = subi %54, %c1_i32 : i32
    br ^bb17(%71, %72 : f64, i32)
    ^bb24(%73: f64):  // pred: ^bb17
    %74 = mulf %cst_3, %73 : f64
    cond_br %arg2, ^bb25, ^bb26(%74 : f64)
    ^bb25:  // pred: ^bb24
    %75 = negf %74 : f64
    br ^bb26(%75 : f64)
    ^bb26(%76: f64):  // 2 preds: ^bb24, ^bb25
    %77 = index_cast %49 : i32 to index
    %78 = quingo.list_get %3[%77] : !quingo.qubit
    quingo.dyn_phase(%78, %76)
    %79 = subi %49, %c1_i32 : i32
    br ^bb15(%79 : i32)
    ^bb27:  // pred: ^bb15
    %80 = index_cast %0 : index to i32
    br ^bb28(%c0_i32 : i32)
    ^bb28(%81: i32):  // 2 preds: ^bb27, ^bb35
    %82 = cmpi slt, %81, %80 : i32
    cond_br %82, ^bb29(%81 : i32), ^bb36(%2, %c0_i32 : !quingo.list<i1>, i32)
    ^bb29(%83: i32):  // pred: ^bb28
    br ^bb30(%c0_i32 : i32)
    ^bb30(%84: i32):  // 2 preds: ^bb29, ^bb34
    %85 = cmpi slt, %84, %83 : i32
    cond_br %85, ^bb31(%84 : i32), ^bb35
    ^bb31(%86: i32):  // pred: ^bb30
    %87 = index_cast %86 : i32 to index
    %88 = quingo.list_get %3[%87] : !quingo.qubit
    %89 = index_cast %83 : i32 to index
    %90 = quingo.list_get %3[%89] : !quingo.qubit
    %91 = subi %83, %86 : i32
    %92 = addi %91, %c1_i32 : i32
    %93 = negf %cst_0 : f64
    %94 = mulf %93, %cst : f64
    br ^bb32(%c1_i32, %c0_i32 : i32, i32)
    ^bb32(%95: i32, %96: i32):  // 2 preds: ^bb31, ^bb33
    %97 = cmpi slt, %96, %92 : i32
    cond_br %97, ^bb33(%95, %96 : i32, i32), ^bb34(%95 : i32)
    ^bb33(%98: i32, %99: i32):  // pred: ^bb32
    %100 = muli %98, %c2_i32 : i32
    %101 = addi %99, %c1_i32 : i32
    br ^bb32(%100, %101 : i32, i32)
    ^bb34(%102: i32):  // pred: ^bb32
    %103 = quingo.to_double %102 : i32
    %104 = divf %94, %103 : f64
    %105 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %106 = "quingo.control"(%105) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%106, %88, %90, %104) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    %107 = addi %86, %c1_i32 : i32
    br ^bb30(%107 : i32)
    ^bb35:  // pred: ^bb30
    %108 = index_cast %83 : i32 to index
    %109 = quingo.list_get %3[%108] : !quingo.qubit
    quingo.H(%109)
    %110 = addi %83, %c1_i32 : i32
    br ^bb28(%110 : i32)
    ^bb36(%111: !quingo.list<i1>, %112: i32):  // 2 preds: ^bb28, ^bb37
    %113 = cmpi slt, %112, %1 : i32
    cond_br %113, ^bb37(%111, %112 : !quingo.list<i1>, i32), ^bb38(%111 : !quingo.list<i1>)
    ^bb37(%114: !quingo.list<i1>, %115: i32):  // pred: ^bb36
    %116 = index_cast %115 : i32 to index
    %117 = quingo.list_get %3[%116] : !quingo.qubit
    %118 = quingo.measure(%117) : (!quingo.qubit) -> i1
    %119 = index_cast %115 : i32 to index
    %120 = quingo.list_set %114[%119] = %118 : !quingo.list<i1>
    %121 = addi %115, %c1_i32 : i32
    br ^bb36(%120, %121 : !quingo.list<i1>, i32)
    ^bb38(%122: !quingo.list<i1>):  // pred: ^bb36
    quingo.dealloc %3 : !quingo.list<!quingo.qubit>
    return %122 : !quingo.list<i1>
  }
  builtin.func @main() -> !quingo.list<i1> attributes {kind = "operation", llvm.emit_c_interface} {
    %c2 = constant 2 : index
    %c1_i32 = constant 1 : i32
    %cst = constant 6.2831853071795862 : f64
    %c2_i32 = constant 2 : i32
    %cst_0 = constant 1.000000e+00 : f64
    %cst_1 = constant 0.000000e+00 : f64
    %cst_2 = constant 2.000000e+00 : f64
    %cst_3 = constant 3.1415926535897931 : f64
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_assemble {%c0_i32, %c0_i32} : !quingo.list<i32> [2]
    %1 = quingo.list_assemble {%c0_i32, %c0_i32} : !quingo.list<i32> [2]
    %2 = quingo.list_decl : !quingo.list<i1> [%c2]
    %3 = quingo.alloc : !quingo.list<!quingo.qubit>[%c2]
    br ^bb1(%c0_i32 : i32)
    ^bb1(%4: i32):  // 2 preds: ^bb0, ^bb4
    %5 = cmpi slt, %4, %c2_i32 : i32
    cond_br %5, ^bb2(%4 : i32), ^bb5(%c1_i32 : i32)
    ^bb2(%6: i32):  // pred: ^bb1
    %7 = index_cast %6 : i32 to index
    %8 = quingo.list_get %0[%7] : i32
    %9 = cmpi eq, %8, %c1_i32 : i32
    cond_br %9, ^bb3, ^bb4
    ^bb3:  // pred: ^bb2
    %10 = index_cast %6 : i32 to index
    %11 = quingo.list_get %3[%10] : !quingo.qubit
    quingo.pauli_x(%11)
    br ^bb4
    ^bb4:  // 2 preds: ^bb2, ^bb3
    %12 = addi %6, %c1_i32 : i32
    br ^bb1(%12 : i32)
    ^bb5(%13: i32):  // 2 preds: ^bb1, ^bb12
    %14 = cmpi sge, %13, %c0_i32 : i32
    cond_br %14, ^bb6(%13 : i32), ^bb13(%c1_i32 : i32)
    ^bb6(%15: i32):  // pred: ^bb5
    %16 = index_cast %15 : i32 to index
    %17 = quingo.list_get %3[%16] : !quingo.qubit
    quingo.H(%17)
    %18 = subi %15, %c1_i32 : i32
    br ^bb7(%18 : i32)
    ^bb7(%19: i32):  // 2 preds: ^bb6, ^bb11
    %20 = cmpi sge, %19, %c0_i32 : i32
    cond_br %20, ^bb8(%19 : i32), ^bb12
    ^bb8(%21: i32):  // pred: ^bb7
    %22 = index_cast %21 : i32 to index
    %23 = quingo.list_get %3[%22] : !quingo.qubit
    %24 = index_cast %15 : i32 to index
    %25 = quingo.list_get %3[%24] : !quingo.qubit
    %26 = subi %15, %21 : i32
    %27 = addi %26, %c1_i32 : i32
    br ^bb9(%c1_i32, %c0_i32 : i32, i32)
    ^bb9(%28: i32, %29: i32):  // 2 preds: ^bb8, ^bb10
    %30 = cmpi slt, %29, %27 : i32
    cond_br %30, ^bb10(%28, %29 : i32, i32), ^bb11(%28 : i32)
    ^bb10(%31: i32, %32: i32):  // pred: ^bb9
    %33 = muli %31, %c2_i32 : i32
    %34 = addi %32, %c1_i32 : i32
    br ^bb9(%33, %34 : i32, i32)
    ^bb11(%35: i32):  // pred: ^bb9
    %36 = quingo.to_double %35 : i32
    %37 = divf %cst, %36 : f64
    %38 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %39 = "quingo.control"(%38) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%39, %23, %25, %37) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    %40 = subi %21, %c1_i32 : i32
    br ^bb7(%40 : i32)
    ^bb12:  // pred: ^bb7
    %41 = subi %15, %c1_i32 : i32
    br ^bb5(%41 : i32)
    ^bb13(%42: i32):  // 2 preds: ^bb5, ^bb22
    %43 = cmpi sge, %42, %c0_i32 : i32
    cond_br %43, ^bb14(%42 : i32), ^bb23(%c0_i32 : i32)
    ^bb14(%44: i32):  // pred: ^bb13
    br ^bb15(%cst_1, %44 : f64, i32)
    ^bb15(%45: f64, %46: i32):  // 2 preds: ^bb14, ^bb21
    %47 = cmpi sge, %46, %c0_i32 : i32
    cond_br %47, ^bb16(%45, %46 : f64, i32), ^bb22(%45 : f64)
    ^bb16(%48: f64, %49: i32):  // pred: ^bb15
    %50 = index_cast %49 : i32 to index
    %51 = quingo.list_get %1[%50] : i32
    %52 = cmpi eq, %51, %c1_i32 : i32
    cond_br %52, ^bb17, ^bb21(%48 : f64)
    ^bb17:  // pred: ^bb16
    %53 = subi %44, %49 : i32
    %54 = addi %53, %c1_i32 : i32
    br ^bb18(%c1_i32, %c0_i32 : i32, i32)
    ^bb18(%55: i32, %56: i32):  // 2 preds: ^bb17, ^bb19
    %57 = cmpi slt, %56, %54 : i32
    cond_br %57, ^bb19(%55, %56 : i32, i32), ^bb20(%55 : i32)
    ^bb19(%58: i32, %59: i32):  // pred: ^bb18
    %60 = muli %58, %c2_i32 : i32
    %61 = addi %59, %c1_i32 : i32
    br ^bb18(%60, %61 : i32, i32)
    ^bb20(%62: i32):  // pred: ^bb18
    %63 = quingo.to_double %62 : i32
    %64 = divf %cst_0, %63 : f64
    %65 = addf %48, %64 : f64
    br ^bb21(%65 : f64)
    ^bb21(%66: f64):  // 2 preds: ^bb16, ^bb20
    %67 = subi %49, %c1_i32 : i32
    br ^bb15(%66, %67 : f64, i32)
    ^bb22(%68: f64):  // pred: ^bb15
    %69 = mulf %cst, %68 : f64
    %70 = negf %69 : f64
    %71 = index_cast %44 : i32 to index
    %72 = quingo.list_get %3[%71] : !quingo.qubit
    quingo.dyn_phase(%72, %70)
    %73 = subi %44, %c1_i32 : i32
    br ^bb13(%73 : i32)
    ^bb23(%74: i32):  // 2 preds: ^bb13, ^bb30
    %75 = cmpi slt, %74, %c2_i32 : i32
    cond_br %75, ^bb24(%74 : i32), ^bb31(%2, %c0_i32 : !quingo.list<i1>, i32)
    ^bb24(%76: i32):  // pred: ^bb23
    br ^bb25(%c0_i32 : i32)
    ^bb25(%77: i32):  // 2 preds: ^bb24, ^bb29
    %78 = cmpi slt, %77, %76 : i32
    cond_br %78, ^bb26(%77 : i32), ^bb30
    ^bb26(%79: i32):  // pred: ^bb25
    %80 = index_cast %79 : i32 to index
    %81 = quingo.list_get %3[%80] : !quingo.qubit
    %82 = index_cast %76 : i32 to index
    %83 = quingo.list_get %3[%82] : !quingo.qubit
    %84 = subi %76, %79 : i32
    %85 = addi %84, %c1_i32 : i32
    %86 = negf %cst_2 : f64
    %87 = mulf %86, %cst_3 : f64
    br ^bb27(%c1_i32, %c0_i32 : i32, i32)
    ^bb27(%88: i32, %89: i32):  // 2 preds: ^bb26, ^bb28
    %90 = cmpi slt, %89, %85 : i32
    cond_br %90, ^bb28(%88, %89 : i32, i32), ^bb29(%88 : i32)
    ^bb28(%91: i32, %92: i32):  // pred: ^bb27
    %93 = muli %91, %c2_i32 : i32
    %94 = addi %92, %c1_i32 : i32
    br ^bb27(%93, %94 : i32, i32)
    ^bb29(%95: i32):  // pred: ^bb27
    %96 = quingo.to_double %95 : i32
    %97 = divf %87, %96 : f64
    %98 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %99 = "quingo.control"(%98) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%99, %81, %83, %97) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    %100 = addi %79, %c1_i32 : i32
    br ^bb25(%100 : i32)
    ^bb30:  // pred: ^bb25
    %101 = index_cast %76 : i32 to index
    %102 = quingo.list_get %3[%101] : !quingo.qubit
    quingo.H(%102)
    %103 = addi %76, %c1_i32 : i32
    br ^bb23(%103 : i32)
    ^bb31(%104: !quingo.list<i1>, %105: i32):  // 2 preds: ^bb23, ^bb32
    %106 = cmpi slt, %105, %c2_i32 : i32
    cond_br %106, ^bb32(%104, %105 : !quingo.list<i1>, i32), ^bb33(%104 : !quingo.list<i1>)
    ^bb32(%107: !quingo.list<i1>, %108: i32):  // pred: ^bb31
    %109 = index_cast %108 : i32 to index
    %110 = quingo.list_get %3[%109] : !quingo.qubit
    %111 = quingo.measure(%110) : (!quingo.qubit) -> i1
    %112 = index_cast %108 : i32 to index
    %113 = quingo.list_set %107[%112] = %111 : !quingo.list<i1>
    %114 = addi %108, %c1_i32 : i32
    br ^bb31(%113, %114 : !quingo.list<i1>, i32)
    ^bb33(%115: !quingo.list<i1>):  // pred: ^bb31
    quingo.dealloc %3 : !quingo.list<!quingo.qubit>
    return %115 : !quingo.list<i1>
  }
}
  ================ end of MLIR dump for offline ================
Time taken by offline:  185.0810000 ms
Time taken by online: 2369.7460000 ms
Time taken by decompose:  201.4460000 ms
Time taken by offline:  181.4500000 ms
Time taken by online:   91.1610000 ms
Time taken by codegen:  303.3040000 ms
Time taken by the entire compiler:    3.4016160 sec
