import pytest
import tempfile
import numpy as np
from sb_arch_opt.problems.turbofan_arch import *
from sb_arch_opt.sampling import HierarchicalExhaustiveSampling
from sb_arch_opt.algo.pymoo_interface import get_nsga2
from pymoo.optimize import minimize
from pymoo.core.population import Population
from pymoo.core.initialization import Initialization

check_dependency = lambda: pytest.mark.skipif(not HAS_OPEN_TURB_ARCH, reason='Turbofan arch dependencies not installed')


@check_dependency()
def test_simple_problem():
    problem = SimpleTurbofanArch()
    problem.print_stats()

    assert len(HierarchicalExhaustiveSampling(n_cont=1).do(problem, 0)) == problem._get_n_valid_discrete()

    problem.get_discrete_rates(force=True, show=True)

    _, is_act_all = problem.all_discrete_x
    assert is_act_all is None
    _, is_act_all = problem.design_space.all_discrete_x_by_trial_and_imputation
    assert np.all(problem.is_conditionally_active == np.any(~is_act_all, axis=0))


@pytest.mark.skip('Takes about 1 minute')
@check_dependency()
def test_simple_problem_eval():
    with tempfile.TemporaryDirectory() as tmp_folder:
        problem = SimpleTurbofanArch(n_parallel=2)
        algo = get_nsga2(pop_size=2, results_folder=tmp_folder)

        algo.initialization = Initialization(Population.new(X=np.array([
            [0.00000000e+00, 7.25000000e+00, 1.45000000e+00, 0.00000000e+00,
             5.56433341e+01, 0.00000000e+00, 0.00000000e+00, 2.16132276e+03,
             1.05000000e+04, 1.05000000e+04, 0.00000000e+00, 3.00000000e+00,
             0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
            [1.00000000e+00, 3.24903112e+00, 1.79150862e+00, 1.00000000e+00,
             3.38760525e+00, 1.72941504e-01, 0.00000000e+00, 1.12242658e+04,
             1.52650779e+04, 1.05000000e+04, 1.00000000e+00, 4.93314012e+00,
             1.00000000e+00, 1.00000000e+00, 1.00000000e+00],
        ])))

        result = minimize(problem, algo, termination=('n_eval', 2))
        f, g = result.pop.get('F'), result.pop.get('G')
        assert np.all(np.abs(f[0, :]-np.array([21.9345935])) < 1e-2)
        assert np.all(np.abs(g[0, :]-np.array([0.85551435, -0.9, 40.64333408, -14., -14.])) < 1e-2)
        assert np.isinf(f[1, 0])
        assert np.all(np.isinf(g[1, :]))


@check_dependency()
def test_realistic_problem():
    problem = RealisticTurbofanArch()
    problem.print_stats()

    assert problem._get_n_valid_discrete() == 1163
    # problem.get_discrete_rates(force=True, show=True)  # Takes several minutes

    f_pf = problem.pareto_front()
    x_pf = problem.pareto_set()
    x_pf_corr, is_act_pf = problem.correct_x(x_pf)
    assert np.all(x_pf_corr == x_pf)
    assert not np.all(is_act_pf)

    f_eval = problem.evaluate(x_pf[[0], :], return_as_dictionary=True)['F']
    assert np.all(np.isfinite(f_eval))
    assert np.all(f_eval[0, :] == f_pf[0, :])
