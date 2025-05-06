import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from typing import Tuple


def bb84(alice_bits: str, eavesdropping_prc: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, str, np.ndarray]:
    a = np.array([int(elem) for elem in alice_bits])
    assert a.ndim == 1
    num_qubits = a.size
    b = np.random.randint(0, 2, size=(num_qubits))      # Alice's bases
    b_prime = np.random.randint(0, 2, size=(num_qubits))  # Bob's bases

    matching_bases = np.where(b == b_prime)[0]

    qc = QuantumCircuit(num_qubits)

    # Alice encodes her bits
    for i in range(num_qubits):
        if a[i] == 1:
            qc.x(i)
    for i in range(num_qubits):
        if b[i] == 1:
            qc.h(i)

    # Eve intercepts with a certain probability
    # eve_counter = 0
    for i in range(num_qubits):
        if np.random.rand() < eavesdropping_prc / 100:
            # eve_counter += 1
            eve_basis = np.random.randint(0, 2)
            eve_qc = QuantumCircuit(1, 1)
            
            # Recreate Alice's state
            if a[i] == 1:
                eve_qc.x(0)
            if b[i] == 1:
                eve_qc.h(0)
            
            # Eve applies her basis
            if eve_basis == 1:
                eve_qc.h(0)
            eve_qc.measure(0, 0)

            backend = Aer.get_backend('qasm_simulator')
            job = backend.run(eve_qc, shots=1)
            result = job.result()
            eve_bit = int(list(result.get_counts().keys())[0])

            # Replace the qubit in the main circuit (qc) with Eve's prepared qubit
            # Reset by applying identity sequence: measure + recreate
            if eve_basis == 1:
                qc.h(i)
            if eve_bit == 1:
                qc.x(i)
            if eve_basis == 1:
                qc.h(i)
    # print(f'Eve % = {eve_counter} / {num_qubits} = {eve_counter/num_qubits}')

    # Bob applies his basis
    for i in range(num_qubits):
        if b_prime[i] == 1:
            qc.h(i)

    qc.measure_all()

    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc, shots=1)
    counts = job.result().get_counts()

    bob_bits = "".join([key for key in counts.keys()])
    alice_bits = "".join([str(key) for key in a])

    return b, b_prime, matching_bases, bob_bits, alice_bits


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