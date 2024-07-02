from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import Aer, AerSimulator
# Import from Qiskit Aer noise module

from qiskit.visualization import plot_histogram

def decode_steane(bitstr):
  # Hamming code
  cw0 = ['0000000', '1010101', '0110011', '1100110', '0001111', '1011010', '0111100', '1101001']
  cw1 = ['1111111', '0101010', '1001100', '0011001', '1110000', '0100101', '1000011', '0010110']
  # reverse it
  cw0 = ['0000000', '1010101', '1100110', '0110011', '1111000', '0101101', '0011110', '1001011']
  cw1 = ['1111111', '0101010', '0011001', '1001100', '0000111', '1010010', '1100001', '0110100']
  # find the nearest codeword
  
  near = None
  dist0 = 1000
  dist1 = 1000
  for i in range(8):
    dist = sum(c != d for c, d in zip(bitstr, cw0[i]))
    if dist < dist0:
      dist0 = dist
  for i in range(8):
    dist = sum(c != d for c, d in zip(bitstr, cw1[i]))
    if dist < dist1:
      dist1 = dist
  if dist0 < dist1:
    return 0
  else:
    return 1

def FT_meas(qc, q, c):
  qc.measure(q,c)