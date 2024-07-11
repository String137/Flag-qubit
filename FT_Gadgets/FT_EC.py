from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import Aer, AerSimulator
# Import from Qiskit Aer noise module
def Flagged_Z_syn(qc,q,num,syn,flag,c):
    # num: 4 length list (corresponding to the syndrome)
    # c: 2
    # syn: 1
    # flag: 1
    qc.reset(syn)
    qc.reset(flag)
    qc.h(flag) # reset it to |+>

    qc.cx(q[num[0]],syn)
    qc.cx(flag,syn)

    qc.cx(q[num[1]],syn)
    qc.cx(q[num[2]],syn)
    qc.cx(flag,syn)
    qc.cx(q[num[3]],syn)

    qc.measure(syn,c[0])
    qc.h(flag)
    qc.measure(flag,c[1])

def Unflagged_Z_syn(qc,q,num,syn,c):
    # num: 4 length list (corresponding to the syndrome)
    # c: 1
    # syn: 1
    
    qc.reset(syn)
    
    qc.cx(q[num[0]],syn)
    qc.cx(q[num[1]],syn)
    qc.cx(q[num[2]],syn)
    qc.cx(q[num[3]],syn)

    qc.measure(syn,c)

def Flagged_X_syn(qc,q,num,syn,flag,c):
    # num: 4 length list (corresponding to the syndrome)
    # c: 1
    # syn: 1
    qc.reset(syn)
    qc.reset(flag)
    qc.h(flag) # reset it to |+>

    qc.h(q[num[0]])
    qc.cx(q[num[0]],syn)
    qc.h(q[num[0]])
    qc.cx(flag,syn)
    qc.h(q[num[1]])
    qc.cx(q[num[1]],syn)
    qc.h(q[num[1]])
    qc.h(q[num[2]])
    qc.cx(q[num[2]],syn)
    qc.h(q[num[2]])
    qc.cx(flag,syn)
    qc.h(q[num[3]])
    qc.cx(q[num[3]],syn)
    qc.h(q[num[3]])

    qc.measure(syn,c[0])
    qc.h(flag)
    qc.measure(flag,c[1])

def Unflagged_X_syn(qc,q,num,syn,c):
     # num: 4 length list (corresponding to the syndrome)
    # c: 2
    # syn: 1
    # flag: 1
    qc.reset(syn)
    
    qc.h(q[num[0]])
    qc.cx(q[num[0]],syn)
    qc.h(q[num[0]])
    qc.h(q[num[1]])
    qc.cx(q[num[1]],syn)
    qc.h(q[num[1]])
    qc.h(q[num[2]])
    qc.cx(q[num[2]],syn)
    qc.h(q[num[2]])
    qc.h(q[num[3]])
    qc.cx(q[num[3]],syn)
    qc.h(q[num[3]])

    qc.measure(syn,c)

def non_FT_EC(qc,q,syn,csyn):
    # syn: 1
    # c: 6
    Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
    Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
    Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
    Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
    Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
    Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])
    image.png
    
def FT_EC(qc,q,syn,flag,csyn,cflag):
    # syn: |0> total 1
    # flag: |+>=H|0> (reset err + Hadamard gate err) total 1
    # csyn: classic reg for syndrome 6bits
    # cflag: classic reg for flag 1bit

    
    Flagged_Z_syn(qc,q,[3,4,5,6],syn,flag,[csyn[0],cflag])
    with qc.if_test((cflag,1)) as else_f1: # if flagged
        # Possible errors (with single fault) when flagged
        # Possible data error : syndrome (Z[3,4,5,6], Z[1,2,5,6], Z[0,2,4,6], X, X, X) -> reverse 012345
        # IIIZIII : 000100 -> 001000
        # IIIZXII : 101100 -> 001101
        # IIIZYII : 101001 -> 100101
        # IIIZZII : 000001 -> 100000 * 둘이 같음
        # IIIIIIZ : 000111 -> 111000
        # IIIIIXZ : 110111 -> 111011
        # IIIIIYZ : 110001 -> 100011
        # IIIIIZZ : 000001 -> 100000 *
        
        Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
        Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
        Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
        Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
        Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
        Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])
        
        with qc.if_test((csyn,0b001000)): # classical reg 뒤집
            qc.z(q[3])
        with qc.if_test((csyn,0b001101)): 
            qc.z(q[3])
            qc.x(q[4])
        with qc.if_test((csyn,0b100101)):
            qc.z(q[3])
            qc.y(q[4])
        with qc.if_test((csyn,0b100000)): 
            qc.z(q[3])
            qc.z(q[4])
        with qc.if_test((csyn,0b111000)): 
            qc.z(q[6])
        with qc.if_test((csyn,0b111011)): 
            qc.x(q[5])
            qc.z(q[6])
        with qc.if_test((csyn,0b100011)): 
            qc.y(q[5])
            qc.z(q[6])
            
    with else_f1: # not flagged
        with qc.if_test((csyn[0],1)) as else_nf1: # not flagged & syndrome 1
            # 이미 그 전 단계에서 fault가 일어났다는 뜻이니까 나머지 EC에선 fault 없다고 생각
            non_FT_EC(qc,q,syn,csyn)
            
        with else_nf1: # not flagged & syndrome 0
            Flagged_Z_syn(qc,q,[1,2,5,6],syn,flag,[csyn[1],cflag])
            with qc.if_test((cflag,1)) as else_f2: # if the second syndrome flagged
                # Possible errors (with single fault) when flagged
                # Possible data error : syndrome (Z[3,4,5,6], Z[1,2,5,6], Z[0,2,4,6], X, X, X)
                # IZIIIII : 000010 -> 010000
                # IZXIIII : 011010 -> 010110
                # IZYIIII : 011001 -> 100110
                # IZZIIII : 000001 -> 100000 * 둘이 같음
                # IIIIIIZ : 000111 -> 111000
                # IIIIIXZ : 110111 -> 111011
                # IIIIIYZ : 110001 -> 100011
                # IIIIIZZ : 000001 -> 100000 *
                Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
                Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
                Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
                Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
                Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
                Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])

                with qc.if_test((csyn,0b010000)): # classical reg 뒤집
                    qc.z(q[1])
                with qc.if_test((csyn,0b010110)): 
                    qc.z(q[1])
                    qc.x(q[2])
                with qc.if_test((csyn,0b100110)):
                    qc.z(q[1])
                    qc.y(q[2])
                with qc.if_test((csyn,0b100000)): 
                    qc.z(q[1])
                    qc.z(q[2])
                with qc.if_test((csyn,0b111000)): 
                    qc.z(q[6])
                with qc.if_test((csyn,0b111011)): 
                    qc.x(q[5])
                    qc.z(q[6])
                with qc.if_test((csyn,0b100011)): 
                    qc.y(q[5])
                    qc.z(q[6])
                
            with else_f2:
                with qc.if_test((csyn[1],1)) as else_nf2: # not flagged & syndrome 1
                    # 이미 그 전 단계에서 fault가 일어났다는 뜻이니까 나머지 EC에선 fault 없다고 생각
                    non_FT_EC(qc,q,syn,csyn)

                with else_nf2:
                    Flagged_Z_syn(qc,q,[0,2,4,6],syn,flag,[csyn[2],cflag])
                    with qc.if_test((cflag,1)) as else_f3: # if the third syndrome flagged
                        # Possible errors (with single fault) when flagged
                        # Possible data error : syndrome (Z[3,4,5,6], Z[1,2,5,6], Z[0,2,4,6], X, X, X)
                        # ZIIIIII : 000001 -> 100000
                        # ZIXIIII : 011001 -> 100110
                        # ZIYIIII : 011010 -> 010110
                        # ZIZIIII : 000010 -> 010000 * 둘이 같음
                        # IIIIIIZ : 000111 -> 111000
                        # IIIIXIZ : 101111 -> 111101
                        # IIIIYIZ : 101010 -> 010101
                        # IIIIZIZ : 000010 -> 010000 *
                        Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
                        Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
                        Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
                        Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
                        Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
                        Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])

                        with qc.if_test((csyn,0b100000)): # classical reg 뒤집
                            qc.z(q[0])
                        with qc.if_test((csyn,0b100110)): 
                            qc.z(q[0])
                            qc.x(q[2])
                        with qc.if_test((csyn,0b010110)):
                            qc.z(q[0])
                            qc.y(q[2])
                        with qc.if_test((csyn,0b010000)): 
                            qc.z(q[0])
                            qc.z(q[2])
                        with qc.if_test((csyn,0b111000)): 
                            qc.z(q[6])
                        with qc.if_test((csyn,0b111101)): 
                            qc.x(q[4])
                            qc.z(q[6])
                        with qc.if_test((csyn,0b010101)): 
                            qc.y(q[4])
                            qc.z(q[6])
                    with else_f3: # not flagged
                        with qc.if_test((csyn[2],1)) as else_nf3: # not flagged & syndrome 1
                            non_FT_EC(qc,q,syn,csyn)

                        with else_nf3:
                            Flagged_X_syn(qc,q,[3,4,5,6],syn,flag,[csyn[3],cflag])
                            with qc.if_test((cflag,1)) as else_f4: # if the fourth syndrome flagged
                                # Possible errors (with single fault) when flagged
                                # Possible data error : syndrome (Z[3,4,5,6], Z[1,2,5,6], Z[0,2,4,6], X, X, X) -> reverse 012345
                                # IIIXIII : 100000 -> 000001
                                # IIIXXII : 001000 -> 000100 * 둘이 같음
                                # IIIXYII : 001101 -> 101100
                                # IIIXZII : 100101 -> 101001 
                                # IIIIIIX : 111000 -> 000111
                                # IIIIIXX : 001000 -> 000100 *
                                # IIIIIYX : 001110 -> 011100
                                # IIIIIZX : 111110 -> 011111 
                                
                                Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
                                Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
                                Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
                                Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
                                Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
                                Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])
                                
                                with qc.if_test((csyn,0b000001)): # classical reg 뒤집
                                    qc.x(q[3])
                                with qc.if_test((csyn,0b000100)): 
                                    qc.x(q[3])
                                    qc.x(q[4])
                                with qc.if_test((csyn,0b101100)):
                                    qc.x(q[3])
                                    qc.y(q[4])
                                with qc.if_test((csyn,0b101001)): 
                                    qc.x(q[3])
                                    qc.z(q[4])
                                with qc.if_test((csyn,0b000111)): 
                                    qc.x(q[6])
                                with qc.if_test((csyn,0b011100)): 
                                    qc.y(q[5])
                                    qc.x(q[6])
                                with qc.if_test((csyn,0b011111)): 
                                    qc.z(q[5])
                                    qc.x(q[6])
                            with else_f4: # not flagged
                                with qc.if_test((csyn[3],1)) as else_nf4: # not flagged & syndrome 1
                                    non_FT_EC(qc,q,syn,csyn)
                                
                                with else_nf4:
                                    Flagged_X_syn(qc,q,[1,2,5,6],syn,flag,[csyn[4],cflag])
                                    with qc.if_test((cflag,1)) as else_f5: # if the fifth syndrome flagged
                                        # Possible errors (with single fault) when flagged
                                        # Possible data error : syndrome (Z[3,4,5,6], Z[1,2,5,6], Z[0,2,4,6], X, X, X)
                                        # IXIIIII : 010000 -> 000010
                                        # IXXIIII : 001000 -> 000100 * 둘이 같음
                                        # IXYIIII : 001011 -> 110100
                                        # IXZIIII : 010011 -> 110010 
                                        # IIIIIIX : 111000 -> 000111 
                                        # IIIIIXX : 001000 -> 000100 *
                                        # IIIIIYX : 001110 -> 011100
                                        # IIIIIZX : 111110 -> 011111 
                                        Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
                                        Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
                                        Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
                                        Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
                                        Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
                                        Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])

                                        with qc.if_test((csyn,0b000010)): # classical reg 뒤집
                                            qc.x(q[1])
                                        with qc.if_test((csyn,0b000100)): 
                                            qc.x(q[1])
                                            qc.x(q[2])
                                        with qc.if_test((csyn,0b110100)):
                                            qc.x(q[1])
                                            qc.y(q[2])
                                        with qc.if_test((csyn,0b110010)): 
                                            qc.x(q[1])
                                            qc.z(q[2])
                                        with qc.if_test((csyn,0b000111)): 
                                            qc.x(q[6])
                                        with qc.if_test((csyn,0b011100)): 
                                            qc.y(q[5])
                                            qc.x(q[6])
                                        with qc.if_test((csyn,0b011111)): 
                                            qc.z(q[5])
                                            qc.x(q[6])
                                    with else_f5:
                                        with qc.if_test((csyn[4],1)) as else_nf5: # not flagged & syndrome 1
                                            non_FT_EC(qc,q,syn,csyn)
                                        with else_nf5:
                                            Flagged_X_syn(qc,q,[0,2,4,6],syn,flag,[csyn[5],cflag])
                                            with qc.if_test((cflag,1)) as else_f6: # if the sixth syndrome flagged
                                                # Possible errors (with single fault) when flagged
                                                # Possible data error : syndrome (Z[3,4,5,6], Z[1,2,5,6], Z[0,2,4,6], X, X, X)
                                                # XIIIIII : 001000 -> 000100
                                                # XIXIIII : 010000 -> 000010 * 둘이 같음
                                                # XIYIIII : 010011 -> 110010
                                                # XIZIIII : 001011 -> 110100 
                                                # IIIIIIX : 111000 -> 000111
                                                # IIIIXIX : 010000 -> 000010 *
                                                # IIIIYIX : 010101 -> 101010
                                                # IIIIZIX : 111101 -> 101111
                                                Unflagged_Z_syn(qc,q,[3,4,5,6],syn,csyn[0])
                                                Unflagged_Z_syn(qc,q,[1,2,5,6],syn,csyn[1])
                                                Unflagged_Z_syn(qc,q,[0,2,4,6],syn,csyn[2])
                                                Unflagged_X_syn(qc,q,[3,4,5,6],syn,csyn[3])
                                                Unflagged_X_syn(qc,q,[1,2,5,6],syn,csyn[4])
                                                Unflagged_X_syn(qc,q,[0,2,4,6],syn,csyn[5])

                                                with qc.if_test((csyn,0b000100)): # classical reg 뒤집
                                                    qc.x(q[0])
                                                with qc.if_test((csyn,0b000010)): 
                                                    qc.x(q[0])
                                                    qc.x(q[2])
                                                with qc.if_test((csyn,0b110010)):
                                                    qc.x(q[0])
                                                    qc.y(q[2])
                                                with qc.if_test((csyn,0b110100)): 
                                                    qc.x(q[0])
                                                    qc.z(q[2])
                                                with qc.if_test((csyn,0b000111)): 
                                                    qc.x(q[6])
                                                with qc.if_test((csyn,0b101010)): 
                                                    qc.y(q[4])
                                                    qc.x(q[6])
                                                with qc.if_test((csyn,0b101111)): 
                                                    qc.z(q[4])
                                                    qc.x(q[6])
                                            with else_f6:
                                                with qc.if_test((csyn[5],1)) as else_nf6: # not flagged & syndrome 1
                                                    non_FT_EC(qc,q,syn,csyn)
                                                with else_nf6:
                                                    pass
                                                    

                                    
            