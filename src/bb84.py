import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from typing import Tuple


def bb84(alice_bits: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    a = np.array([int(elem) for elem in alice_bits])
    assert a.ndim == 1
    num_qubits = a.size
    b = np.random.randint(0, 2, size=(num_qubits))
    b_prime = np.random.randint(0, 2, size=(num_qubits))

    #bases stubs
    # b = np.array([0, 0, 1, 1, 0, 0, 1, 1])
    # b_prime = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    #bases stubs end


    matching_bases = np.where(b == b_prime)[0]

    qc = QuantumCircuit(num_qubits)

    for i in range(num_qubits):
        if a[i] == 1:
            qc.x(i)
    qc.barrier()

    for i in range(num_qubits):
        if b[i] == 1:
            qc.h(i)
    qc.barrier()

    for i in range(num_qubits):
        if b_prime[i] == 1:
            qc.h(i)
    qc.barrier()

    qc.measure_all()
    # print(qc.draw())

    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc, shots=1)
    counts = job.result().get_counts()

    bob_bits = "".join([key for key in counts.keys()])

    return b, b_prime, matching_bases, bob_bits, a

if __name__ == "__main__":
    result = np.array([], dtype=bool)
    for i in range(10000):
        key_length = np.random.randint(10, 150)
        # key_length = 10
        alice_bits  = ''.join(np.random.randint(0, 2, size=(key_length)).astype('str'))
        b, bp, mb, bob_bits, a = bb84(alice_bits)

        alice_matching_bits = [alice_bits[i] for i in mb]
        bob_matching_bits = ([bob_bits[len(alice_bits) - i - 1] for i in mb])

        # print(f"a:   {a}")
        # print(f"b:   {b}")
        # print(f"b':  {bp}")
        # print(f"Matching bases: {mb}")

        # print(f"bob: {bob_bits}")

        # print(f"alice_bits:  {alice_matching_bits}")
        # print(f"bob_bits:    {bob_matching_bits}")
        # print(alice_matching_bits == bob_matching_bits)

        result = np.append(result, alice_matching_bits == bob_matching_bits)

    print(np.all(result))