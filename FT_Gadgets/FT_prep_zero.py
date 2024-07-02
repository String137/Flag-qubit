from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import Aer, AerSimulator
# Import from Qiskit Aer noise module

from qiskit.visualization import plot_histogram


def FT_prep_zero_trial(sp, q, anc, c):

  sp.h(q[0])
  sp.h(q[1])
  sp.h(q[3])

  sp.cx(q[0], anc[0])
  sp.cx(q[1], anc[0])
  sp.cx(q[3], anc[0])



  sp.barrier()

  sp.cx(q[3],q[4])
  sp.cx(q[3],q[5])
  sp.cx(q[3],q[6])
  sp.cx(q[1],q[2])
  sp.cx(q[1],q[5])
  sp.cx(q[1],q[6])
  sp.cx(q[0],q[2])
  sp.cx(q[0],q[4])
  sp.cx(q[0],q[6])

  sp.barrier()

  sp.cx(q[0], anc[0])
  sp.cx(q[1], anc[0])
  sp.cx(q[3], anc[0])

  sp.measure(anc[0],c[0])

def FT_prep_zero(qc, q, anc, c, max_trials = 5):
  n = 7
  qc.reset(q)
  qc.reset(anc)
  FT_prep_zero_trial(qc, q, anc, c)

  for _ in range(max_trials-1):
    with qc.if_test((c,1)):
      # retry
      qc.reset(q)
      qc.reset(anc)
      FT_prep_zero_trial(qc, q, anc, c)

  

