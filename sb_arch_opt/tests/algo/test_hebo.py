import pytest
from sb_arch_opt.problem import *
from sb_arch_opt.algo.hebo_interface import *
from sb_arch_opt.problems.constrained import ArchCantileveredBeam
from sb_arch_opt.algo.hebo_interface.algo import HEBOArchOptInterface

check_dependency = lambda: pytest.mark.skipif(not HAS_HEBO, reason='HEBO dependencies not installed')


@check_dependency()
def test_design_space(problem: ArchOptProblemBase):
    hebo = HEBOArchOptInterface(problem, n_init=10)
    design_space = hebo.design_space
    assert len(design_space.paras) == problem.n_var


@check_dependency()
def test_simple(problem: ArchOptProblemBase):
    assert HAS_HEBO

    hebo = get_hebo_optimizer(problem, n_init=10)
    hebo.optimize(n_infill=2)

    pop = hebo.pop
    assert len(pop) == 12


@check_dependency()
def test_constrained():
    opt = get_hebo_optimizer(ArchCantileveredBeam(), n_init=10)
    opt.optimize(n_infill=1)
    assert len(opt.pop) == 11


@check_dependency()
def test_simple_failing(failing_problem: ArchOptProblemBase):
    hebo = get_hebo_optimizer(failing_problem, n_init=10)
    hebo.optimize(n_infill=1)

    pop = hebo.pop
    assert len(pop) == 5
