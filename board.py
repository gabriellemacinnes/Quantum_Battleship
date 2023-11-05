import random
import pandas
import numpy as np
import qiskit
from qiskit import QuantumCircuit, QuantumRegister,ClassicalRegister, transpile, execute, Aer

from qiskit.visualization import plot_bloch_multivector
from qiskit.tools.visualization import plot_histogram

#returns a generated board of qubits
def generate_board(dim, ships, boards):
    b = [[0 for _ in range(dim)] for _ in range(dim)]
    target = ships*boards
    current = 0
    m = []
    for i in range(dim*dim):
        random_number = random.uniform(0, min(boards - boards/3 , target - current ))
        m.append(random_number / boards)
        current += random_number
    random.shuffle(m)
    print(m)
    print(len(m))
    print(sum(m))
    for i in range(dim):
        for j in range(dim):
            prob_0 = m[i*dim + j]
            amplitude_0 = np.sqrt(1 - prob_0)
            amplitude_1 = np.sqrt(prob_0)
            qr = QuantumRegister(1, 'q')
            cr = ClassicalRegister(1, 'c')
            circuit = QuantumCircuit(qr, cr)
            circuit.initialize([amplitude_0, amplitude_1], qr[0])
            b[i][j] = circuit
    return b


 