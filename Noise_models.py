from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
import random
from qiskit.circuit import CircuitInstruction, Instruction
def noise_model(qc, p):
  error_reset = pauli_error([('X', p),('I', 1-p)])
  error_meas = pauli_error([('X', p),('I', 1-p)])
  error_gate1 = depolarizing_error(p, 1)
  error_gate2 = depolarizing_error(p, 2)
  noise_model = NoiseModel()
  noise_model.add_all_qubit_quantum_error(error_reset, "reset")
  noise_model.add_all_qubit_quantum_error(error_meas, "measure")
  noise_model.add_all_qubit_quantum_error(error_gate1, ['u1','u2','u3'])
  noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"])
  
  

  return noise_model

def count_inst(qc): 
    cnt = 0
    for i, inst in enumerate(qc.data):
        # print(inst[0].name)
        if inst[0].name == 'barrier':
            continue
        if inst[0].name in ['reset', 'h', 'x', 'y', 'z', 'cx', 'measure']:
            if inst[0].name == 'cx':
              cnt+=1
            continue
        if inst[0].name == 'if_else':
            for circ in inst[0].params:
                # print(inst[0].params)
                if circ is not None:
                    cnt += count_inst(circ)
        else:
            raise Exception("NameError: "+inst[0].name)
    return cnt

def occur_random_single_fault(qc, num_inst):
    x_error = Instruction(name='x',num_qubits=1,num_clbits=0,params=[])
    y_error = Instruction(name='y',num_qubits=1,num_clbits=0,params=[])
    z_error = Instruction(name='z',num_qubits=1,num_clbits=0,params=[])
    iden = Instruction(name='id',num_qubits=1,num_clbits=0,params=[])
    for i, inst in enumerate(qc.data):
        # print(inst[0].name)
        if inst[0].name == 'barrier':
            continue
        if inst[0].name in ['reset', 'h', 'x', 'y', 'z', 'cx', 'measure']:
            if random.random() < 1/num_inst:
                # fault occurs
                if inst[0].name == 'reset':
                    qc.data.insert(i+1,CircuitInstruction(x_error,inst[1]))
                    return qc, inst
                # if inst[0].name in ['h', 'x', 'y', 'z']:
                #     err = random.choice([x_error,y_error,z_error])
                #     qc.data.insert(i+1,CircuitInstruction(err,inst[1]))
                #     return qc, inst
                if inst[0].name == 'cx':
                    err1 = random.choice([iden,x_error,y_error,z_error])
                    err2 = random.choice([iden,x_error,y_error,z_error])
                    qc.data.insert(i+1,CircuitInstruction(err1,[inst[1][0]]))
                    qc.data.insert(i+2,CircuitInstruction(err2,[inst[1][1]]))
                    return qc, inst
                # if inst[0].name == 'measure':
                #     qc.data.insert(i,CircuitInstruction(x_error,inst[1]))
                #     return qc, inst
            continue

        if inst[0].name == 'if_else':
            for circ in inst[0].params:
                # print(inst[0].params)
                if circ is not None:
                    return occur_random_single_fault(qc,num_inst)
        else:
            raise Exception("NameError: "+inst[0].name)
    return qc, None # no error occured

def custom_noise_model(qc):
  num_inst = count_inst(qc)
  return occur_random_single_fault(qc,num_inst)