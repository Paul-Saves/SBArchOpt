import pytest
import tempfile
import numpy as np
import unittest
from sb_arch_opt.algo.segomoe_interface import *
from sb_arch_opt.problems.continuous import Branin
from sb_arch_opt.problems.discrete import MDBranin
from sb_arch_opt.problems.md_mo import MOHimmelblau, MDMOHimmelblau
from sb_arch_opt.problems.constrained import (
    ArchCantileveredBeam,
    MDCantileveredBeam,
    ArchWeldedBeam,
    MDWeldedBeam,
)
from sb_arch_opt.problems.hidden_constraints import (
    Mueller01,
    MOHierarchicalRosenbrockHC,
)


def check_dependency():
    return pytest.mark.skipif(
        not HAS_SEGOMOE, reason="SEGOMOE dependencies not installed"
    )


class TestSEGOMOE(unittest.TestCase):

    @check_dependency()
    def test_interface(self):
        with tempfile.TemporaryDirectory() as tmp_folder:
            interface = SEGOMOEInterface(Branin(), tmp_folder, n_init=10, n_infill=1)
            assert interface.x.shape == (0, 2)
            assert interface.n == 0
            assert interface.x_failed.shape == (0, 2)
            assert interface.n_failed == 0
            assert interface.n_tried == 0
            assert interface.y.shape == (0, 1)
            assert interface.f.shape == (0, 1)
            assert interface.g.shape == (0, 0)
            assert interface.h.shape == (0, 0)
            assert len(interface.pop) == 0
            assert len(interface.opt) == 0

    @check_dependency()
    def test_so_cont(self):
        with tempfile.TemporaryDirectory() as tmp_folder:
            interface = SEGOMOEInterface(Branin(), tmp_folder, n_init=10, n_infill=1)
            opt = interface.run_optimization()
            assert interface.x.shape == (11, 2)
            assert interface.n == 11
            assert interface.n_failed == 0
            assert interface.n_tried == 11
            assert interface.y.shape == (11, 1)
            assert interface.f.shape == (11, 1)
            assert interface.g.shape == (11, 0)
            assert interface.h.shape == (11, 0)
            assert len(interface.pop) == 11
            assert len(opt) == 1

            interface2 = SEGOMOEInterface(Branin(), tmp_folder, n_init=10, n_infill=2)
            interface2.initialize_from_previous()
            assert interface2.x.shape == (11, 2)

            interface2.run_optimization()
            assert interface2.x.shape == (12, 2)

    @check_dependency()
    def test_so_cont_constrained(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                ArchCantileveredBeam(), tmp_folder, n_init=10, n_infill=5, use_moe=False
            )
            opt = interface.run_optimization()
            assert interface.f.shape == (15, 1)
            assert interface.g.shape == (15, 2)

            feasible_mask = np.all(interface.g < 0, axis=1)
            assert len(np.where(feasible_mask)[0]) > 0
            assert len(opt) == 1

            pop = interface.pop
            assert np.all(pop.get("feas") == feasible_mask)

            interface2 = SEGOMOEInterface(
                ArchCantileveredBeam(), tmp_folder, n_init=10, n_infill=6
            )
            interface2.run_optimization()
            assert np.all(interface2.g[:-1, :] == interface.g)

    @check_dependency()
    def test_so_mixed(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(MDBranin(), tmp_folder, n_init=10, n_infill=1)
            opt = interface.run_optimization()
            assert interface.x.shape == (11, 4)
            assert interface.y.shape == (11, 1)
            assert interface.f.shape == (11, 1)
            assert interface.g.shape == (11, 0)
            assert interface.h.shape == (11, 0)
            assert len(interface.pop) == 11
            assert len(opt) == 1
            assert np.all(interface.x == MDBranin().correct_x(interface.x)[0])

    @check_dependency()
    def test_so_mixed_constrained(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                MDCantileveredBeam(), tmp_folder, n_init=10, n_infill=2, use_moe=False
            )
            opt = interface.run_optimization()
            assert interface.f.shape == (12, 1)
            assert interface.g.shape == (12, 2)

            feasible_mask = np.all(interface.g < 0, axis=1)
            assert len(np.where(feasible_mask)[0]) > 0
            assert len(opt) == 1

            pop = interface.pop
            assert np.all(pop.get("feas") == feasible_mask)

    @check_dependency()
    def test_so_failing(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                Mueller01(), tmp_folder, n_init=50, n_infill=2, use_moe=False
            )
            interface.run_optimization()
            assert interface.n < 52
            assert interface.n_tried == 52
            assert interface.n + interface.n_failed == 52

            interface2 = SEGOMOEInterface(
                Mueller01(), tmp_folder, n_init=50, n_infill=2, use_moe=False
            )
            interface2.initialize_from_previous()
            assert interface2.n < 52
            assert interface2.n_tried == 52
            assert interface2.n + interface2.n_failed == 52

    @check_dependency()
    def test_mo_cont(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                MOHimmelblau(), tmp_folder, n_init=50, n_infill=1
            )
            opt = interface.run_optimization()
            assert interface.x.shape == (51, 2)
            assert interface.y.shape == (51, 2)
            assert interface.f.shape == (51, 2)
            assert interface.g.shape == (51, 0)
            assert interface.h.shape == (51, 0)
            assert len(interface.pop) == 51
            assert len(opt) > 1

    @check_dependency()
    def test_mo_cont_constrained(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                ArchWeldedBeam(), tmp_folder, n_init=10, n_infill=1
            )
            opt = interface.run_optimization()
            assert interface.x.shape == (11, 4)
            assert interface.y.shape == (11, 6)
            assert interface.f.shape == (11, 2)
            assert interface.g.shape == (11, 4)
            assert interface.h.shape == (11, 0)
            assert len(interface.pop) == 11
            assert len(opt) > 1

    @check_dependency()
    def test_mo_mixed(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                MDMOHimmelblau(), tmp_folder, n_init=10, n_infill=1
            )
            opt = interface.run_optimization()
            assert interface.x.shape == (11, 2)
            assert interface.y.shape == (11, 2)
            assert interface.f.shape == (11, 2)
            assert interface.g.shape == (11, 0)
            assert interface.h.shape == (11, 0)
            assert len(interface.pop) == 11
            assert len(opt) >= 1

    @check_dependency()
    def test_mo_mixed_constrained(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                MDWeldedBeam(), tmp_folder, n_init=10, n_infill=1
            )
            opt = interface.run_optimization()
            assert interface.x.shape == (11, 4)
            assert interface.y.shape == (11, 6)
            assert interface.f.shape == (11, 2)
            assert interface.g.shape == (11, 4)
            assert interface.h.shape == (11, 0)
            assert len(interface.pop) == 11
            assert len(opt) >= 1

    @check_dependency()
    def test_mo_failing(self):
        with tempfile.TemporaryDirectory() as tmp_folder:

            interface = SEGOMOEInterface(
                MOHierarchicalRosenbrockHC(),
                tmp_folder,
                n_init=20,
                n_infill=1,
                use_moe=False,
            )
            interface.run_optimization()
            assert interface.n < 21
            assert interface.n_tried == 21
            assert interface.n + interface.n_failed == 21


if __name__ == "__main__":
    unittest.main()
