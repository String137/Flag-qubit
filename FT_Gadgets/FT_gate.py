from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import Aer, AerSimulator
# Import from Qiskit Aer noise module

from qiskit.visualization import plot_histogram


def FT_Hadamard(qc, q):
  for i in range(7):
    qc.h(q[i])

def FT_CNOT(qc, c, t):
  for i in range(7):
    qc.cx(c[i],t[i])

