from collections import namedtuple
from datetime import datetime
import numpy as np

from csm.calculations.basic_calculations import create_rotation_matrix, check_perm_cycles, \
    check_perm_structure_preservation
from csm.calculations.constants import MINDOUBLE
from csm.input_output.formatters import silent_print
from csm.molecule.molecule import Molecule
from csm.molecule.normalizations import de_normalize_coords


class CSMState(namedtuple('CSMState', ['molecule',
                                       'op_order',
                                       'op_type',
                                       'csm',
                                       'perm',
                                       'dir',
                                       'perm_count',
                                       'num_invalid'])):
    pass


CSMState.__new__.__defaults__ = (None,) * len(CSMState._fields)


def get_chain_perm_string(molecule, perm):
    chain_perm = []
    chain_str = ""
    for origin_chain in molecule.chains:
        sample_atom = molecule.chains[origin_chain][0]
        permuted_index = perm[sample_atom]
        destination_chain = molecule.atoms[permuted_index].chain
        chain_perm.append(destination_chain)
        origin_name = molecule.chains.index_to_name(origin_chain)
        destination_name = molecule.chains.index_to_name(destination_chain)
        chain_str += origin_name + "->" + destination_name + ", "

    chain_str = chain_str[:-2]  # remove final comma and space
    return chain_perm, chain_str

class Operation:
    def __init__(self, op, sn_max=8, init=True):
        self.op_code = op
        if init:
            op = self._get_operation_data(op)
            self.type = op.type
            self.order = op.order
            if op.type == "CH":
                self.order = sn_max
            self.name = op.name

    def _get_operation_data(self, opcode):
        """
        Returns data about an operation based on the opcode
        Args:
            opcode: c2, s4, etc...

        Returns:
            And OperationCode object, with type, order and name
        """
        OperationCode = namedtuple('OperationCode', ('type', 'order', 'name'))
        _opcode_data = {
            "cs": ('CS', 2, "MIRROR SYMMETRY"),
            "ci": ('CI', 2, "INVERSION (S2)"),
            "ch": ('CH', 2, "CHIRALITY"),
            "c2": ('CN', 2, "C2 SYMMETRY"),
            'c3': ('CN', 3, "C3 SYMMETRY"),
            'c4': ('CN', 4, "C4 SYMMETRY"),
            'c5': ('CN', 5, "C5 SYMMETRY"),
            'c6': ('CN', 6, "C6 SYMMETRY"),
            'c7': ('CN', 7, "C7 SYMMETRY"),
            'c8': ('CN', 8, "C8 SYMMETRY"),
            'c10': ('CN', 10, "C10 SYMMETRY"),
            's1': ('CS', 2, "MIRROR SYMMETRY (S1)"),
            's2': ('SN', 2, "S2 SYMMETRY"),
            's4': ('SN', 4, "S4 SYMMETRY"),
            's6': ('SN', 6, "S6 SYMMETRY"),
            's8': ('SN', 8, "S8 SYMMETRY"),
            's10': ('SN', 8, "S10 SYMMETRY")
        }

        def isint(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        opcode = opcode.lower()
        if opcode[0] == 'c' and isint(opcode[1:]):
            return OperationCode(type='CN', order=int(opcode[1:]), name=opcode.upper() + ' SYMMETRY')
        if opcode[0] == 's' and isint(opcode[1:]):
            if opcode[1:] == '1':
                data = _opcode_data[opcode.lower()]
                return OperationCode(type=data[0], order=data[1], name=data[2])
            if int(opcode[1:]) % 2 != 0:
                raise ValueError("SN values must be even")
            return OperationCode(type='SN', order=int(opcode[1:]), name=opcode.upper() + ' SYMMETRY')
        try:
            data = _opcode_data[opcode.lower()]
        except KeyError:
            raise
        return OperationCode(type=data[0], order=data[1], name=data[2])

    def to_dict(self):
        return {
            "name": self.name,
            "order": self.order,
            "type": self.type
        }

    @staticmethod
    def from_dict(in_dict):
        # make an arbitrary operation
        o = Operation("C2", init=False)
        # overwrite values
        o.type = in_dict["type"]
        o.name = in_dict["name"]
        o.order = in_dict["order"]
        return o


class Result:
    def __repr__(self):
        return_string = "{} CSM: {} Molecule: {}".format(self.__class__.__name__, self.csm,
                                                         self.molecule.metadata.appellation())
        return return_string


class CSMResult(Result):
    def __init__(self, state, operation, overall_stats={}, ongoing_stats={}):
        self.failed = False
        # input
        self.molecule = state.molecule.copy()  # not yet denormalized
        self._normalized_molecule_coords = np.array(self.molecule.Q)
        self.molecule.de_normalize()
        self.operation = operation
        self.op_type = state.op_type
        self.op_order = state.op_order

        # result
        self.csm = state.csm
        self.dir = state.dir
        self.perm = state.perm
        self._normalized_symmetric_structure = self.create_symmetric_structure(self.molecule_coords(normalized=True),
                                                                              self.perm, self.dir, self.op_type,
                                                                              self.op_order)
        self._symmetric_structure = de_normalize_coords(list(self._normalized_symmetric_structure),
                                                       self.molecule.norm_factor)
        self.formula_csm = self.get_CSM_by_formula(self.molecule, self._symmetric_structure)

        # stats
        self.overall_statistics = overall_stats
        self.ongoing_statistics = ongoing_stats

        falsecount, num_invalid, cycle_counts, bad_indices = check_perm_cycles(self.perm, operation)
        self.overall_statistics["# bad cycles"] = falsecount
        self.overall_statistics["% bad cycles"] = num_invalid / len(self.molecule)
        try:
            self.overall_statistics["% structure"] = check_perm_structure_preservation(self.molecule, self.perm)
        except ValueError:
            self.overall_statistics["% structure"] = "n/a"

        if self.operation.name == "CHIRALITY":
            if self.op_type == 'CS':
                self.overall_statistics["best chirality"] = "CS"
            else:
                self.overall_statistics["best chirality"] = "S%d" % (self.op_order)

        self.overall_statistics["formula CSM"] = self.formula_csm

        self.chain_perm, self.chain_perm_string=get_chain_perm_string(self.molecule, self.perm)

    def symmetric_structure(self, normalized=False):
        if normalized:
            return self._normalized_symmetric_structure
        else:
            return self._symmetric_structure

    def molecule_coords(self, normalized=False):
        if normalized:
            return self._normalized_molecule_coords
        else:
            return np.array(self.molecule.Q)

    def get_coords(self, symmetric=False, normalized=False):
        if symmetric:
            return self.symmetric_structure(normalized)
        else:
            return self.molecule_coords(normalized)

    @property
    def d_min(self):
        return 1.0 - (self.csm / 100 * self.operation.order / (self.operation.order - 1))

    @property
    def local_csm(self):
        return self.compute_local_csm(self.molecule.Q, self.operation, self.dir)

    def create_symmetric_structure(self, molecule_coords, perm, dir, op_type, op_order):
        # print('create_symmetric_structure called')

        cur_perm = np.arange(len(perm))  # array of ints...
        size = len(perm)
        m_pos = molecule_coords
        symmetric = np.copy(m_pos)

        normalization = 1 / op_order

        ########calculate and apply transform matrix#########
        ###for i<OpOrder
        for i in range(1, op_order):
            # get rotation
            rotation_matrix = create_rotation_matrix(i, op_type, op_order, dir)
            # print("Rotation matrix:\n")
            # print(rotation_matrix)
            # rotated_positions = m_pos @ rotation_matrix

            # set permutation
            cur_perm = [perm[cur_perm[j]] for j in range(size)]

            # add correct permuted rotation to atom in outAtoms
            for j in range(len(symmetric)):
                symmetric[j] += rotation_matrix @ m_pos[cur_perm[j]]
                # print("Symmetric: ", symmetric)

        # apply normalization:
        symmetric *= normalization

        return symmetric

    def get_CSM_by_formula(self, molecule, symmetric_structure):
        Q = molecule.Q
        # step one: get average of all atoms
        init_avg = np.mean(Q, axis=0)
        # step two: distance between intial and actual: initial - actual, squared
        # step three: normal: distance between initial and initial average, (x-x0)^2 + (y-y0)^2 + (z-z0)^2
        # step four: sum of distances between initial and actual, and then sum of x-y-z
        # step five: sum of normal
        distance = np.array([0.0, 0.0, 0.0])
        normal = 0.0
        for i in range(len(Q)):
            distance += (np.square(Q[i] - symmetric_structure[i]))  # square of difference
            normal += (np.sum(np.square(Q[i] - init_avg)))
        distance = np.sum(distance)
        # print("yaffa normal =", normal)
        # step six: 100 * step four / step five
        result = 100 * distance / normal
        return result

    def compute_local_csm(self, molecule_coords, operation, dir):
        size = len(molecule_coords)
        cur_perm = [i for i in range(size)]
        local_csm = np.zeros(size)
        m_pos = molecule_coords

        for i in range(operation.order):
            rot = create_rotation_matrix(i, operation.type, operation.order, dir)

            # set permutation
            cur_perm = [self.perm[cur_perm[j]] for j in range(size)]

            # apply rotation to each atoms
            rotated = rot @ m_pos[cur_perm[i]]
            difference = rotated - m_pos[i]
            square = np.square(difference)
            sum = np.sum(square)
            local_csm[i] = sum * (100.0 / (2 * operation.order))
        return local_csm

    def print_summary(self, legacy_output=False):
        try:
            percent_structure = check_perm_structure_preservation(self.molecule, self.perm)
            silent_print("The permutation found maintains " +
                         str(round(percent_structure * 100, 2)) + "% of the original molecule's structure")

        except ValueError:
            silent_print(
                "The input molecule does not have bond information and therefore conservation of structure cannot be measured")

        falsecount, num_invalid, cycle_counts, bad_indices = check_perm_cycles(self.perm, self.operation)
        silent_print(
            "The permutation found contains %d invalid %s. %.2lf%% of the molecule's atoms are in legal cycles" % (
                falsecount, "cycle" if falsecount == 1 else "cycles",
                100 * (len(self.molecule) - num_invalid) / len(self.molecule)))

        for cycle_len in sorted(cycle_counts):
            valid = cycle_len == 1 or cycle_len == self.operation.order or (
                    cycle_len == 2 and self.operation.type == 'SN')
            count = cycle_counts[cycle_len]
            silent_print("There %s %d %s %s of length %d" % (
                "is" if count == 1 else "are", count, "invalid" if not valid else "",
                "cycle" if count == 1 else "cycles",
                cycle_len))
        if len(self.molecule.chains) > 1:
            silent_print("\nChain perm: " + self.chain_perm_string)

        if self.operation.name == "CHIRALITY":
            silent_print("Minimum chirality was found in", self.overall_statistics["best chirality"])

        if legacy_output:
            silent_print("%s: %.4lf" % (self.operation.name, abs(self.csm)))
            silent_print("CSM by formula: %.4lf" % (self.formula_csm))

        else:
            silent_print("%s: %.6lf" % (self.operation.name, abs(self.csm)))
            silent_print("CSM by formula: %.6lf" % (self.formula_csm))

    def to_dict(self):
        return_dict= {
                "molecule": self.molecule.to_dict(),
                "normalized_molecule_coords": [list(i) for i in self.molecule_coords(normalized=True)],
                "operation": self.operation.to_dict(),

                "csm": self.csm,
                "perm": self.perm,
                "dir": list(self.dir),

                "normalized_symmetric_structure": [list(i) for i in self.symmetric_structure(normalized=True)],
                "symmetric_structure": [list(i) for i in self.symmetric_structure()],
                "formula_csm": self.formula_csm,

                #"overall stats": self.overall_statistics,
                #"ongoing stats": self.ongoing_statistics
            }
        return return_dict

    @staticmethod
    def from_dict(result_dict):
        print('TYPE OF RESULT_DICT:')
        print(type(result_dict))
        print('RESULT_DICT:')
        print(result_dict)
        molecule = Molecule.from_dict(result_dict["molecule"])
        molecule.normalize()
        operation = Operation.from_dict(result_dict["operation"])
        state = CSMState(molecule, operation.order, operation.type, result_dict["csm"], result_dict["perm"],
                         result_dict["dir"])
        result = CSMResult(state, operation, result_dict["overall stats"], result_dict["ongoing stats"])
        return result


class FailedResult(Result):
    def __init__(self, failed_reason, molecule, **kwargs):
        self.failed = True
        self.failed_reason = failed_reason


        self.molecule = molecule.copy()  # not yet denormalized
        self._normalized_molecule_coords = np.array(self.molecule.Q)
        self.molecule.de_normalize()
        self.operation = kwargs["operation"]
        self.op_type = self.operation.type
        self.op_order = self.operation.order
        silent_print(molecule.metadata.appellation() + "_"+ self.operation.op_code +" failed")
        # result
        self.csm = "n/a"
        self.dir = ["n/a", "n/a", "n/a"]
        self.perm = ["n/a"]
        self._normalized_symmetric_structure = []  # [["n/a"] for i in range(len(molecule))]
        self._symmetric_structure = []  # [[0,0,0] for i in range(len(molecule))]
        self.formula_csm = "n/a"

        self.overall_statistics = {
            "failed": "FAILED",
            "reason for failure": self.failed_reason
        }

        self.ongoing_statistics = {}
    def symmetric_structure(self, normalized=False):
        return []

    def molecule_coords(self, normalized=False):
        return []

    def get_coords(self, symmetric=False, normalized=False):
        if not symmetric and not normalized:
            return np.array(self.molecule.Q)
        return []

    def print_summary(self, legacy_output=False):
        pass
    def __repr__(self):
        return super(FailedResult, self).__repr__() + "\tFailure: " + self.failed_reason

class BaseCalculation:
    '''
    A base class for calculations that handles some shared logic, particularly chirality
    '''
    def __init__(self, operation, molecule, **kwargs):
        self.operation=operation
        self.molecule=molecule

    def chirality(self, timeout):
        # First CS
        op = Operation('cs')
        best_result = self._calculate(op, timeout)
        if best_result.csm > MINDOUBLE:
            # Try the SN's
            for op_order in range(2, self.operation.order + 1, 2):
                op = Operation("S" + str(op_order))
                result = self._calculate(op, timeout)
                if result.csm < best_result.csm:
                    best_result = result
                if best_result.csm < MINDOUBLE:
                    break
        return best_result
    def calculate(self, timeout=300):
        self.start_time = datetime.now()
        if self.operation.type == 'CH':  # Chirality
            # sn_max = op_order
            # First CS
            best_result=self.chirality(timeout)
        else:
            best_result = self._calculate(self.operation, timeout=timeout)
        return best_result

    def _calculate(self, operation, timeout):
        raise NotImplementedError

