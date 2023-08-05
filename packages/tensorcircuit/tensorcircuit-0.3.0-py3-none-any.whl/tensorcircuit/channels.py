"""
Some common noise quantum channels.
"""

import sys
from typing import Any, Sequence, Union
from operator import and_
from functools import reduce
from functools import partial
import numpy as np

from . import cons
from . import interfaces
from .cons import backend, dtypestr
from . import gates


thismodule = sys.modules[__name__]

Gate = gates.Gate
Tensor = Any
Matrix = Any


def _sqrt(a: Tensor) -> Tensor:
    r"""
    Return the square root of Tensor with default global dtype

    .. math::
        \sqrt{a}

    :param a: Tensor
    :type a: Tensor
    :return: Square root of Tensor
    :rtype: Tensor
    """
    a = backend.convert_to_tensor(a)
    a = backend.cast(a, cons.rdtypestr)
    return backend.cast(backend.sqrt(a), dtype=cons.dtypestr)


def _safe_sqrt(perfect_square: int) -> int:
    square_root = int(np.sqrt(perfect_square) + 1e-9)
    if square_root**2 != perfect_square:
        raise ValueError("The input must be a square number.")
    return square_root


def depolarizingchannel(px: float, py: float, pz: float) -> Sequence[Gate]:
    r"""
    Return a Depolarizing Channel

    .. math::
        \sqrt{1-p_x-p_y-p_z}
        \begin{bmatrix}
            1 & 0\\
            0 & 1\\
        \end{bmatrix}\qquad
        \sqrt{p_x}
        \begin{bmatrix}
            0 & 1\\
            1 & 0\\
        \end{bmatrix}\qquad
        \sqrt{p_y}
        \begin{bmatrix}
            0 & -1j\\
            1j & 0\\
        \end{bmatrix}\qquad
        \sqrt{p_z}
        \begin{bmatrix}
            1 & 0\\
            0 & -1\\
        \end{bmatrix}

    :Example:

    >>> cs = depolarizingchannel(0.1, 0.15, 0.2)
    >>> tc.channels.single_qubit_kraus_identity_check(cs)

    :param px: :math:`p_x`
    :type px: float
    :param py: :math:`p_y`
    :type py: float
    :param pz: :math:`p_z`
    :type pz: float
    :return: Sequences of Gates
    :rtype: Sequence[Gate]
    """
    # assert px + py + pz <= 1
    i = Gate(_sqrt(1 - px - py - pz) * gates.i().tensor)  # type: ignore
    x = Gate(_sqrt(px) * gates.x().tensor)  # type: ignore
    y = Gate(_sqrt(py) * gates.y().tensor)  # type: ignore
    z = Gate(_sqrt(pz) * gates.z().tensor)  # type: ignore
    return [i, x, y, z]


def generaldepolarizingchannel(
    p: Union[float, Sequence[Any]], num_qubits: int = 1
) -> Sequence[Gate]:
    r"""
    Return a Depolarizing Channel for 1 qubit or 2 qubits

    :Example:

    >>> cs = tc.channels.generaldepolarizingchannel([0.1,0.1,0.1],1)
    >>> tc.channels.kraus_identity_check(cs)
    >>> cs = tc.channels.generaldepolarizingchannel(0.02,2)
    >>> tc.channels.kraus_identity_check(cs)


    :param p: parameter for each Pauli channel
    :type p: Union[float, Sequence]
    :param num_qubits: number of qubits, 1 and 2 are avaliable, defaults 1
    :type num_qubits: int, optional
    :return: Sequences of Gates
    :rtype: Sequence[Gate]
    """

    if num_qubits == 1:

        if isinstance(p, float):

            assert p > 0 and p < 1 / 3, "p should be >0 and <1/3"
            probs = [1 - 3 * p] + 3 * [p]

        elif isinstance(p, list):

            assert reduce(
                and_, [pi > 0 and pi < 1 for pi in p]
            ), "p should be >0 and <1"
            probs = [1 - sum(p)] + p  # type: ignore

        elif isinstance(p, tuple):

            p = list[p]  # type: ignore
            assert reduce(
                and_, [pi > 0 and pi < 1 for pi in p]
            ), "p should be >0 and <1"
            probs = [1 - sum(p)] + p  # type: ignore

        else:
            raise ValueError("p should be float or list")

    elif num_qubits == 2:

        if isinstance(p, float):

            assert p > 0 and p < 1, "p should be >0 and <1/15"
            probs = [1 - 15 * p] + 15 * [p]

        elif isinstance(p, list):

            assert reduce(
                and_, [pi > 0 and pi < 1 for pi in p]
            ), "p should be >0 and <1"
            probs = [1 - sum(p)] + p  # type: ignore

        elif isinstance(p, tuple):

            p = list[p]  # type: ignore
            assert reduce(
                and_, [pi > 0 and pi < 1 for pi in p]
            ), "p should be >0 and <1"
            probs = [1 - sum(p)] + p  # type: ignore

        else:
            raise ValueError("p should be float or list")

    if num_qubits == 1:
        tup = [gates.i().tensor, gates.x().tensor, gates.y().tensor, gates.z().tensor]  # type: ignore
    if num_qubits == 2:
        tup = [
            gates.ii().tensor,  # type: ignore
            gates.ix().tensor,  # type: ignore
            gates.iy().tensor,  # type: ignore
            gates.iz().tensor,  # type: ignore
            gates.xi().tensor,  # type: ignore
            gates.xx().tensor,  # type: ignore
            gates.xy().tensor,  # type: ignore
            gates.xz().tensor,  # type: ignore
            gates.yi().tensor,  # type: ignore
            gates.yx().tensor,  # type: ignore
            gates.yy().tensor,  # type: ignore
            gates.yz().tensor,  # type: ignore
            gates.zi().tensor,  # type: ignore
            gates.zx().tensor,  # type: ignore
            gates.zy().tensor,  # type: ignore
            gates.zz().tensor,  # type: ignore
        ]

    Gkarus = []
    for pro, paugate in zip(probs, tup):
        Gkarus.append(Gate(_sqrt(pro) * paugate))

    return Gkarus


def amplitudedampingchannel(gamma: float, p: float) -> Sequence[Gate]:
    r"""
    Return an amplitude damping channel.
    Notice: Amplitude damping corrspondings to p = 1.

    .. math::
        \sqrt{p}
        \begin{bmatrix}
            1 & 0\\
            0 & \sqrt{1-\gamma}\\
        \end{bmatrix}\qquad
        \sqrt{p}
        \begin{bmatrix}
            0 & \sqrt{\gamma}\\
            0 & 0\\
        \end{bmatrix}\qquad
        \sqrt{1-p}
        \begin{bmatrix}
            \sqrt{1-\gamma} & 0\\
            0 & 1\\
        \end{bmatrix}\qquad
        \sqrt{1-p}
        \begin{bmatrix}
            0 & 0\\
            \sqrt{\gamma} & 0\\
        \end{bmatrix}

    :Example:

    >>> cs = amplitudedampingchannel(0.25, 0.3)
    >>> tc.channels.single_qubit_kraus_identity_check(cs)

    :param gamma: the damping parameter of amplitude (:math:`\gamma`)
    :type gamma: float
    :param p: :math:`p`
    :type p: float
    :return: An amplitude damping channel with given :math:`\gamma` and :math:`p`
    :rtype: Sequence[Gate]
    """
    # https://cirq.readthedocs.io/en/stable/docs/noise.html
    # https://github.com/quantumlib/Cirq/blob/master/cirq/ops/common_channels.py

    g00 = Gate(np.array([[1, 0], [0, 0]], dtype=cons.npdtype))
    g01 = Gate(np.array([[0, 1], [0, 0]], dtype=cons.npdtype))
    g10 = Gate(np.array([[0, 0], [1, 0]], dtype=cons.npdtype))
    g11 = Gate(np.array([[0, 0], [0, 1]], dtype=cons.npdtype))
    m0 = _sqrt(p) * (g00 + _sqrt(1 - gamma) * g11)
    m1 = _sqrt(p) * (_sqrt(gamma) * g01)
    m2 = _sqrt(1 - p) * (_sqrt(1 - gamma) * g00 + g11)
    m3 = _sqrt(1 - p) * (_sqrt(gamma) * g10)
    return [m0, m1, m2, m3]


def resetchannel() -> Sequence[Gate]:
    r"""
    Reset channel

    .. math::
        \begin{bmatrix}
            1 & 0\\
            0 & 0\\
        \end{bmatrix}\qquad
        \begin{bmatrix}
            0 & 1\\
            0 & 0\\
        \end{bmatrix}

    :Example:

    >>> cs = resetchannel()
    >>> tc.channels.single_qubit_kraus_identity_check(cs)

    :return: Reset channel
    :rtype: Sequence[Gate]
    """
    m0 = Gate(np.array([[1, 0], [0, 0]], dtype=cons.npdtype))
    m1 = Gate(np.array([[0, 1], [0, 0]], dtype=cons.npdtype))
    return [m0, m1]


def phasedampingchannel(gamma: float) -> Sequence[Gate]:
    r"""
    Return a phase damping channel with given :math:`\gamma`

    .. math::
        \begin{bmatrix}
            1 & 0\\
            0 & \sqrt{1-\gamma}\\
        \end{bmatrix}\qquad
        \begin{bmatrix}
            0 & 0\\
            0 & \sqrt{\gamma}\\
        \end{bmatrix}

    :Example:

    >>> cs = phasedampingchannel(0.6)
    >>> tc.channels.single_qubit_kraus_identity_check(cs)

    :param gamma: The damping parameter of phase (:math:`\gamma`)
    :type gamma: float
    :return: A phase damping channel with given :math:`\gamma`
    :rtype: Sequence[Gate]
    """
    g00 = Gate(np.array([[1, 0], [0, 0]], dtype=cons.npdtype))
    g11 = Gate(np.array([[0, 0], [0, 1]], dtype=cons.npdtype))
    m0 = 1.0 * (g00 + _sqrt(1 - gamma) * g11)  # 1* ensure gate
    m1 = _sqrt(gamma) * g11
    return [m0, m1]


def _collect_channels() -> Sequence[str]:
    r"""
    Return channels names in this module.

    :Example:

    >>> tc.channels._collect_channels()
    ['amplitudedamping', 'depolarizing', 'phasedamping', 'reset']

    :return: A list of channel names
    :rtype: Sequence[str]
    """
    cs = []
    for name in dir(thismodule):
        if name.endswith("channel"):
            n = name[:-7]
            cs.append(n)
    return cs


channels = _collect_channels()
# channels = ["depolarizing", "amplitudedamping", "reset", "phasedamping"]


def kraus_identity_check(kraus: Sequence[Gate]) -> None:
    r"""
    Check identity of Kraus operators.

    .. math::
        \sum_{k}^{} K_k^{\dagger} K_k = I


    :Examples:

    >>> cs = resetchannel()
    >>> tc.channels.kraus_identity_check(cs)

    :param kraus: List of Kraus operators.
    :type kraus: Sequence[Gate]
    """

    dim = backend.shape_tuple(kraus[0].tensor)
    dim2 = int(2 ** (len(dim) / 2))
    shape = (dim2, dim2)
    placeholder = backend.zeros(shape)
    placeholder = backend.cast(placeholder, dtype=cons.dtypestr)
    for k in kraus:
        k = Gate(backend.reshape(k.tensor, [dim2, dim2]))
        placeholder += backend.conj(backend.transpose(k.tensor, [1, 0])) @ k.tensor
    np.testing.assert_allclose(placeholder, np.eye(int(shape[0])), atol=1e-5)


single_qubit_kraus_identity_check = kraus_identity_check  # backward compatibility


def kraus_to_super_gate(kraus_list: Sequence[Gate]) -> Tensor:
    r"""
    Convert Kraus operators to one Tensor (as one Super Gate).

    .. math::
        \sum_{k}^{} K_k \otimes K_k^{*}

    :param kraus_list: A sequence of Gate
    :type kraus_list: Sequence[Gate]
    :return: The corresponding Tensor of the list of Kraus operators
    :rtype: Tensor
    """
    kraus_tensor_list = [k.tensor for k in kraus_list]
    k = kraus_tensor_list[0]
    u = backend.kron(k, backend.conj(k))
    for k in kraus_tensor_list[1:]:
        u += backend.kron(k, backend.conj(k))
    return u


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def kraus_to_super(kraus_list: Sequence[Matrix]) -> Matrix:
    r"""
    Convert Kraus operator representation to Louivile-Superoperator representation.

    In the col-vec basis, the evolution of a state :math:`\rho` in terms of tensor components
    of superoperator :math:`\varepsilon` can be expressed as

    .. math::
        \rho'_{mn} = \sum_{\mu \nu}^{} \varepsilon_{nm,\nu \mu} \rho_{\mu \nu}

    The superoperator :math:`\varepsilon` must make the dynamic map from :math:`\rho` to :math:`\rho'` to
    satisfy hermitian-perserving (HP), trace-preserving (TP), and completely positive (CP).

    We can construct the superoperator from Kraus operators by

    .. math::
        \varepsilon = \sum_{k} K_k^{*} \otimes K_k


    :Examples:

    >>> kraus = resetchannel()
    >>> tc.channels.kraus_to_super(kraus)

    :param kraus_list: A sequence of Gate
    :type kraus_list: Sequence[Gate]
    :return: The corresponding Tensor of Superoperator
    :rtype: Matrix
    """
    k = kraus_list[0]
    u = backend.kron(backend.conj(k), k)
    for k in kraus_list[1:]:
        u += backend.kron(backend.conj(k), k)
    return u


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def super_to_choi(superop: Matrix) -> Matrix:
    r"""
    Convert Louivile-Superoperator representation to Choi representation.

    In the col-vec basis, the evolution of a state :math:`\rho` in terms of Choi
    matrix :math:`\Lambda` can be expressed as

    .. math::
        \rho'_{mn} = \sum_{\mu,\nu}^{} \Lambda_{\mu m,\nu n} \rho_{\mu \nu}

    The Choi matrix :math:`\Lambda` must make the dynamic map from :math:`\rho` to :math:`\rho'` to
    satisfy hermitian-perserving (HP), trace-preserving (TP), and completely positive (CP).

    Interms of tensor components we have the relationship of Louivile-Superoperator representation
    and Choi representation

    .. math::
        \Lambda_{mn,\mu \nu} = \varepsilon_{\nu n,\mu m}


    :Examples:

    >>> kraus = resetchannel()
    >>> superop = tc.channels.kraus_to_super(kraus)
    >>> tc.channels.super_to_choi(superop)


    :param superop: Superoperator
    :type superop: Matrix
    :return: Choi matrix
    :rtype: Matrix
    """

    return reshuffle(superop, (3, 1, 2, 0))


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def reshuffle(op: Matrix, order: Sequence[int]) -> Matrix:
    """
    Reshuffle the dimension index of a matrix.

    :param op: Input matrix
    :type op: Matrix
    :param order: required order
    :type order: Tuple
    :return: Reshuffled matrix
    :rtype: Matrix
    """
    dim = backend.shape_tuple(op)
    input_dim = _safe_sqrt(dim[0])
    output_dim = _safe_sqrt(dim[1])
    shape = (output_dim, output_dim, input_dim, input_dim)

    return backend.reshape(
        backend.transpose(backend.reshape(op, shape), order),
        (shape[order[0]] * shape[order[1]], shape[order[2]] * shape[order[3]]),
    )


# TODO(@yutuer21): check jit able and ad
@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def choi_to_kraus(choi: Matrix, atol: float = 1e-5) -> Matrix:
    r"""
    Convert the Choi matrix representation to Kraus operator representation.

    This can be done by firstly geting eigen-decomposition of Choi-matrix

    .. math::
        \Lambda = \sum_k \gamma_k  \vert \phi_k \rangle \langle \phi_k \vert

    Then define Kraus operators

    .. math::
        K_k = \sqrt{\gamma_k} V_k

    where :math:`\gamma_k\geq0` and :math:`\phi_k` is the col-val vectorization of :math:`V_k` .


    :Examples:


    >>> kraus = tc.channels.phasedampingchannel(0.2)
    >>> superop = tc.channels.kraus_to_choi(kraus)
    >>> kraus_new = tc.channels.choi_to_kraus(superop)


    :param choi: Choi matrix
    :type choi: Matrix
    :return: A list of Kraus operators
    :rtype: Sequence[Matrix]
    """
    dim = backend.shape_tuple(choi)
    input_dim = _safe_sqrt(dim[0])
    output_dim = _safe_sqrt(dim[1])

    if is_hermitian_matrix(choi, atol=atol):
        # Get eigen-decomposition of Choi-matrix
        e, v = backend.eigh(choi)

        # CP-map Kraus representation
        kraus = []
        for val, vec in zip(backend.real(e), backend.transpose(v)):
            if val > atol:
                k = backend.sqrt(backend.cast(val, dtypestr)) * backend.transpose(
                    backend.reshape(vec, [output_dim, input_dim]), [1, 0]
                )
                kraus.append(k)

        if not kraus:
            kraus.append(backend.zeros([output_dim, input_dim], dtype=dtypestr))
        return kraus

    raise ValueError("illegal Choi matrix")


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def kraus_to_choi(kraus_list: Sequence[Matrix]) -> Matrix:
    """
    Convert from Kraus representation to Choi representation.

    :param kraus_list: A list Kraus operators
    :type kraus_list: Sequence[Matrix]
    :return: Choi matrix
    :rtype: Matrix
    """
    superop = kraus_to_super(kraus_list)
    return super_to_choi(superop)


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def choi_to_super(choi: Matrix) -> Matrix:
    """
    Convert from Choi representation to Superoperator representation.

    :param choi: Choi matrix
    :type choi: Matrix
    :return: Superoperator
    :rtype: Matrix
    """
    return super_to_choi(choi)


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def super_to_kraus(superop: Matrix) -> Matrix:
    """
    Convert from Superoperator representation to Kraus representation.

    :param superop: Superoperator
    :type superop: Matrix
    :return: A list of Kraus operator
    :rtype: Matrix
    """
    choi = super_to_choi(superop)
    return choi_to_kraus(choi)


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0],
    gate_to_tensor=True,
)
def is_hermitian_matrix(mat: Matrix, rtol: float = 1e-8, atol: float = 1e-5):
    """
    Test if an array is a Hermitian matrix

    :param mat: Matrix
    :type mat: Matrix
    :param rtol: _description_, defaults to 1e-8
    :type rtol: float, optional
    :param atol: _description_, defaults to 1e-5
    :type atol: float, optional
    :return: _description_
    :rtype: _type_
    """

    if len(backend.shape_tuple(mat)) != 2:
        return False
    return np.allclose(
        mat, backend.conj(backend.transpose(mat, [1, 0])), rtol=rtol, atol=atol
    )


def krausgate_to_krausmatrix(kraus_list: Sequence[Gate]) -> Sequence[Matrix]:
    """
    Convert Kraus of Gate form to Matrix form.

    :param kraus_list: A list of Kraus
    :type kraus_list: Sequence[Gate]
    :return: A list of Kraus operators
    :rtype: Sequence[Matrix]
    """

    if isinstance(kraus_list[0], Gate):
        dim = backend.shape_tuple(kraus_list[0].tensor)
        dim2 = int(2 ** (len(dim) / 2))
        return [backend.reshape(k.tensor, [dim2, dim2]) for k in kraus_list]
    else:
        return kraus_list


def krausmatrix_to_krausgate(kraus_list: Sequence[Matrix]) -> Sequence[Gate]:
    """
    Convert Kraus of Matrix form to Gate form.

    :param kraus_list: A list of Kraus
    :type kraus_list: Sequence[Matrix]
    :return: A list of Kraus operators
    :rtype: Sequence[Gate]
    """
    if isinstance(kraus_list[0], Gate):
        return kraus_list

    newkraus = [backend.reshape2(k) for k in kraus_list]

    return [Gate(k) for k in newkraus]


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0, 1],
    gate_to_tensor=True,
)
def evol_kraus(density_matrix: Matrix, kraus_list: Sequence[Matrix]) -> Matrix:
    r"""
    The dynamic evolution according to Kraus operators.

    .. math::
        \rho' = \sum_{k} K_k \rho K_k^{\dagger}

    :Examples:

    >>> density_matrix = np.array([[0.5,0.5],[0.5,0.5]])
    >>> kraus = tc.channels.phasedampingchannel(0.2)
    >>> evol_kraus(density_matrix,kraus)


    :param density_matrix: Initial density matrix
    :type density_matrix: Matrix
    :param kraus_list: A list of Kraus operator
    :type kraus_list: Sequence[Matrix]
    :return: Final density matrix
    :rtype: Matrix
    """

    final_density_matrix = 0
    for k in kraus_list:
        mid = k @ density_matrix @ backend.conj(backend.transpose(k, [1, 0]))
        final_density_matrix += mid
    return final_density_matrix


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0, 1],
    gate_to_tensor=True,
)
def evol_superop(density_matrix: Matrix, superop: Matrix) -> Matrix:
    """
    The dynamic evolution according to Superoperator.

    :Examples:

    >>> density_matrix = np.array([[0.5,0.5],[0.5,0.5]])
    >>> kraus = tc.channels.phasedampingchannel(0.2)
    >>> superop = kraus_to_super(kraus)
    >>> evol_superop(density_matrix,superop)


    :param density_matrix: Initial density matrix
    :type density_matrix: Matrix
    :param superop: Superoperator
    :type superop: Sequence[Matrix]
    :return: Final density matrix
    :rtype: Matrix
    """

    dim = backend.shape_tuple(density_matrix)

    density_vec = backend.reshape(density_matrix, [dim[0] ** 2, 1])

    superoprow = reshuffle(superop, (1, 0, 3, 2))
    final_density_vec = superoprow @ density_vec

    return backend.reshape(final_density_vec, dim)


@partial(
    interfaces.args_to_tensor,  # type: ignore
    argnums=[0, 1],
    gate_to_tensor=True,
)
def check_rep_transformation(
    kraus: Sequence[Gate], density_matrix: Matrix, verbose: bool = False
):
    """
    Check the convertation between those representations.

    :param kraus: A sequence of Gate
    :type kraus: Sequence[Gate]
    :param density_matrix: Initial density matrix
    :type density_matrix: Matrix
    :param verbose: Whether print Kraus and new Kraus operators, defaults to False
    :type verbose: bool, optional
    """

    # from kraus to choi
    choi = kraus_to_choi(kraus)

    # from choi to kraus2
    # choi = backend.convert_to_tensor(choi)
    kraus2 = choi_to_kraus(choi)

    # from kraus2 to choi2
    choi2 = kraus_to_choi(kraus2)

    if verbose:
        print("kraus:", kraus)
        print("kraus_new", kraus2)

    print("test identity from kraus/choi to superop")
    superop = kraus_to_super(kraus)
    superop2 = choi_to_super(choi)
    np.testing.assert_allclose(superop, superop2, atol=1e-5)

    # cheack kraus2 satisfy identity
    print("test normaliztion of kraus_new")
    krausg = krausmatrix_to_krausgate(kraus2)
    kraus_identity_check(krausg)

    # cheack choi2 equals to choi
    print("test identity of choi and choi_new")
    np.testing.assert_allclose(choi, choi2, atol=1e-5)

    # cheack evolution
    print("test evolution identity of kraus and kraus_new")
    density_matrix1 = evol_kraus(density_matrix, kraus)
    density_matrix2 = evol_kraus(density_matrix, kraus2)
    np.testing.assert_allclose(density_matrix1, density_matrix2, atol=1e-5)

    print("test evolution identity of kraus and superop")
    density_matrix3 = evol_superop(density_matrix, superop)
    np.testing.assert_allclose(density_matrix1, density_matrix3, atol=1e-5)
