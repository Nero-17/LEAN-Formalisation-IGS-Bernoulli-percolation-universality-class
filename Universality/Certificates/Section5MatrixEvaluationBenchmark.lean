import Universality.Certificates.Section5MatrixEvaluation

namespace Universality.Certificates
set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem packedInitialVector_kernel_benchmark20 :
    (packedInitialVector (matrixPackingBase 20) 20).1 % matrixPackingBase 20 =
      (packedInitialVector 0 20).1 := by decide

#print axioms packedInitialVector_kernel_benchmark20

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem packedInitialVector_kernel_benchmark50 :
    (packedInitialVector (matrixPackingBase 50) 50).1 % matrixPackingBase 50 =
      (packedInitialVector 0 50).1 := by decide

#print axioms packedInitialVector_kernel_benchmark50

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem packedInitialVector_kernel_benchmark100 :
    (packedInitialVector (matrixPackingBase 100) 100).1 % matrixPackingBase 100 =
      (packedInitialVector 0 100).1 := by decide

#print axioms packedInitialVector_kernel_benchmark100

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem packedInitialVector_kernel_benchmark200 :
    (packedInitialVector (matrixPackingBase 200) 200).1 % matrixPackingBase 200 =
      (packedInitialVector 0 200).1 := by decide +kernel

#print axioms packedInitialVector_kernel_benchmark200



set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem packedInitialVector_kernel_benchmark952 :
    (packedInitialVector (matrixPackingBase 952) 952).1 % matrixPackingBase 952 =
      (packedInitialVector 0 952).1 := by decide +kernel

#print axioms packedInitialVector_kernel_benchmark952

end Universality.Certificates

