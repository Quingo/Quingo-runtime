Time taken by options:    0.6920000 ms
[36mAdding path: [0m/home/xiangfu/quingo-tutorials/src/quingo
[36mAdding path: [0m/tmp/tmpnb4a7ykx
[34mmainFilePath: [0m/tmp/tmpnb4a7ykx/main_draper_test_test_sc_adder.qu
Time taken by frontend:   25.1130000 ms
Time taken by mlirgen:   40.7410000 ms
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
    %c1_i32 = constant 1 : i32
    %c2_i32 = constant 2 : i32
    %c0_i32 = constant 0 : i32
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
    %cst = constant 3.1415926535897931 : f64
    %cst_0 = constant 2.000000e+00 : f64
    %0 = negf %cst_0 : f64
    %1 = mulf %0, %cst : f64
    %2 = call @power_of_2(%arg2) : (i32) -> i32
    %3 = quingo.to_double %2 : i32
    %4 = divf %1, %3 : f64
    %5 = quingo.getval @quingo.dyn_phase {operandTypes = [!quingo.qubit, f64], returnTypes = []} : !quingo<"qugate(!quingo.qubit, f64)->()">
    %6 = "quingo.control"(%5) {numCtrls = 1 : i32} : (!quingo<"qugate(!quingo.qubit, f64)->()">) -> !quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">
    "quingo.apply"(%6, %arg0, %arg1, %4) {operand_segment_sizes = dense<[1, 1, 2]> : vector<3xi32>} : (!quingo<"qugate[num_ctrls: 1](!quingo.qubit, f64)->()">, !quingo.qubit, !quingo.qubit, f64) -> ()
    return
  }
  builtin.func @qft_ns(%arg0: !quingo.list<!quingo.qubit>) attributes {kind = "operation", llvm.emit_c_interface} {
    %c1_i32 = constant 1 : i32
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_length %arg0 : !quingo.list<!quingo.qubit> -> index
    %1 = index_cast %0 : index to i32
    %2 = subi %1, %c1_i32 : i32
    br ^bb1(%2 : i32)
    ^bb1(%3: i32):  // 2 preds: ^bb0, ^bb5
    %4 = cmpi sge, %3, %c0_i32 : i32
    cond_br %4, ^bb2(%3 : i32), ^bb6
    ^bb2(%5: i32):  // pred: ^bb1
    %6 = index_cast %5 : i32 to index
    %7 = quingo.list_get %arg0[%6] : !quingo.qubit
    quingo.H(%7)
    %8 = subi %5, %c1_i32 : i32
    br ^bb3(%8 : i32)
    ^bb3(%9: i32):  // 2 preds: ^bb2, ^bb4
    %10 = cmpi sge, %9, %c0_i32 : i32
    cond_br %10, ^bb4(%9 : i32), ^bb5
    ^bb4(%11: i32):  // pred: ^bb3
    %12 = index_cast %11 : i32 to index
    %13 = quingo.list_get %arg0[%12] : !quingo.qubit
    %14 = index_cast %5 : i32 to index
    %15 = quingo.list_get %arg0[%14] : !quingo.qubit
    %16 = subi %5, %11 : i32
    %17 = addi %16, %c1_i32 : i32
    call @c_phase_k(%13, %15, %17) : (!quingo.qubit, !quingo.qubit, i32) -> ()
    %18 = subi %11, %c1_i32 : i32
    br ^bb3(%18 : i32)
    ^bb5:  // pred: ^bb3
    %19 = subi %5, %c1_i32 : i32
    br ^bb1(%19 : i32)
    ^bb6:  // pred: ^bb1
    return
  }
  builtin.func @iqft_ns(%arg0: !quingo.list<!quingo.qubit>) attributes {kind = "operation", llvm.emit_c_interface} {
    %c1_i32 = constant 1 : i32
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_length %arg0 : !quingo.list<!quingo.qubit> -> index
    %1 = index_cast %0 : index to i32
    br ^bb1(%c0_i32 : i32)
    ^bb1(%2: i32):  // 2 preds: ^bb0, ^bb5
    %3 = cmpi slt, %2, %1 : i32
    cond_br %3, ^bb2(%2 : i32), ^bb6
    ^bb2(%4: i32):  // pred: ^bb1
    br ^bb3(%c0_i32 : i32)
    ^bb3(%5: i32):  // 2 preds: ^bb2, ^bb4
    %6 = cmpi slt, %5, %4 : i32
    cond_br %6, ^bb4(%5 : i32), ^bb5
    ^bb4(%7: i32):  // pred: ^bb3
    %8 = index_cast %7 : i32 to index
    %9 = quingo.list_get %arg0[%8] : !quingo.qubit
    %10 = index_cast %4 : i32 to index
    %11 = quingo.list_get %arg0[%10] : !quingo.qubit
    %12 = subi %4, %7 : i32
    %13 = addi %12, %c1_i32 : i32
    call @c_phase_k_m(%9, %11, %13) : (!quingo.qubit, !quingo.qubit, i32) -> ()
    %14 = addi %7, %c1_i32 : i32
    br ^bb3(%14 : i32)
    ^bb5:  // pred: ^bb3
    %15 = index_cast %4 : i32 to index
    %16 = quingo.list_get %arg0[%15] : !quingo.qubit
    quingo.H(%16)
    %17 = addi %4, %c1_i32 : i32
    br ^bb1(%17 : i32)
    ^bb6:  // pred: ^bb1
    return
  }
  builtin.func @sc_adder(%arg0: !quingo.list<!quingo.qubit>, %arg1: !quingo.list<i32>, %arg2: i1) attributes {kind = "operation", llvm.emit_c_interface} {
    %c1_i32 = constant 1 : i32
    %cst = constant 6.2831853071795862 : f64
    %cst_0 = constant 1.000000e+00 : f64
    %c0_i32 = constant 0 : i32
    %cst_1 = constant 0.000000e+00 : f64
    %0 = quingo.list_length %arg1 : !quingo.list<i32> -> index
    %1 = index_cast %0 : index to i32
    %2 = subi %1, %c1_i32 : i32
    br ^bb1(%2 : i32)
    ^bb1(%3: i32):  // 2 preds: ^bb0, ^bb9
    %4 = cmpi sge, %3, %c0_i32 : i32
    cond_br %4, ^bb2(%3 : i32), ^bb10
    ^bb2(%5: i32):  // pred: ^bb1
    br ^bb3(%cst_1, %5 : f64, i32)
    ^bb3(%6: f64, %7: i32):  // 2 preds: ^bb2, ^bb6
    %8 = cmpi sge, %7, %c0_i32 : i32
    cond_br %8, ^bb4(%6, %7 : f64, i32), ^bb7(%6 : f64)
    ^bb4(%9: f64, %10: i32):  // pred: ^bb3
    %11 = index_cast %10 : i32 to index
    %12 = quingo.list_get %arg1[%11] : i32
    %13 = cmpi eq, %12, %c1_i32 : i32
    cond_br %13, ^bb5, ^bb6(%9 : f64)
    ^bb5:  // pred: ^bb4
    %14 = subi %5, %10 : i32
    %15 = addi %14, %c1_i32 : i32
    %16 = call @power_of_2(%15) : (i32) -> i32
    %17 = quingo.to_double %16 : i32
    %18 = divf %cst_0, %17 : f64
    %19 = addf %9, %18 : f64
    br ^bb6(%19 : f64)
    ^bb6(%20: f64):  // 2 preds: ^bb4, ^bb5
    %21 = subi %10, %c1_i32 : i32
    br ^bb3(%20, %21 : f64, i32)
    ^bb7(%22: f64):  // pred: ^bb3
    %23 = mulf %cst, %22 : f64
    cond_br %arg2, ^bb8, ^bb9(%23 : f64)
    ^bb8:  // pred: ^bb7
    %24 = negf %23 : f64
    br ^bb9(%24 : f64)
    ^bb9(%25: f64):  // 2 preds: ^bb7, ^bb8
    %26 = index_cast %5 : i32 to index
    %27 = quingo.list_get %arg0[%26] : !quingo.qubit
    quingo.dyn_phase(%27, %25)
    %28 = subi %5, %c1_i32 : i32
    br ^bb1(%28 : i32)
    ^bb10:  // pred: ^bb1
    return
  }
  builtin.func @test_sc_adder(%arg0: !quingo.list<i32>, %arg1: !quingo.list<i32>, %arg2: i1) -> !quingo.list<i1> attributes {kind = "operation", llvm.emit_c_interface} {
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
    call @qft_ns(%3) : (!quingo.list<!quingo.qubit>) -> ()
    call @sc_adder(%3, %arg1, %arg2) : (!quingo.list<!quingo.qubit>, !quingo.list<i32>, i1) -> ()
    call @iqft_ns(%3) : (!quingo.list<!quingo.qubit>) -> ()
    br ^bb6(%2, %c0_i32 : !quingo.list<i1>, i32)
    ^bb6(%13: !quingo.list<i1>, %14: i32):  // 2 preds: ^bb5, ^bb7
    %15 = cmpi slt, %14, %1 : i32
    cond_br %15, ^bb7(%13, %14 : !quingo.list<i1>, i32), ^bb8(%13 : !quingo.list<i1>)
    ^bb7(%16: !quingo.list<i1>, %17: i32):  // pred: ^bb6
    %18 = index_cast %17 : i32 to index
    %19 = quingo.list_get %3[%18] : !quingo.qubit
    %20 = quingo.measure(%19) : (!quingo.qubit) -> i1
    %21 = index_cast %17 : i32 to index
    %22 = quingo.list_set %16[%21] = %20 : !quingo.list<i1>
    %23 = addi %17, %c1_i32 : i32
    br ^bb6(%22, %23 : !quingo.list<i1>, i32)
    ^bb8(%24: !quingo.list<i1>):  // pred: ^bb6
    quingo.dealloc %3 : !quingo.list<!quingo.qubit>
    return %24 : !quingo.list<i1>
  }
  builtin.func @main() -> !quingo.list<i1> attributes {kind = "operation", llvm.emit_c_interface} {
    %true = constant true
    %c0_i32 = constant 0 : i32
    %0 = quingo.list_assemble {%c0_i32, %c0_i32} : !quingo.list<i32> [2]
    %1 = quingo.list_assemble {%c0_i32, %c0_i32} : !quingo.list<i32> [2]
    %2 = call @test_sc_adder(%0, %1, %true) : (!quingo.list<i32>, !quingo.list<i32>, i1) -> !quingo.list<i1>
    return %2 : !quingo.list<i1>
  }
}
  ================ end of MLIR dump for offline ================
Time taken by offline:  113.2990000 ms
Time taken by online:   30.6670000 ms
Time taken by decompose:   64.1370000 ms
Time taken by offline:   42.6870000 ms
Time taken by online:   28.7110000 ms
Time taken by codegen:    0.3360000 ms
Time taken by the entire compiler:    0.3471730 sec
