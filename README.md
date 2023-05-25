# SBArchOpt: Surrogate-Based Architecture Optimization

SBArchOpt (es-bee-ARK-opt) provides a set of classes and interfaces for applying Surrogate-Based Optimization (SBO)
for system architecture optimization problems:
- Expensive black-box problems: evaluating one candidate architecture might computationally expensive
- Mixed-discrete design variables: categorical architectural decisions mixed with continuous sizing variables
- Hierarchical design variables: decisions can deactivate/activate (parts of) downstream decisions
- Multi-objective: stemming from conflicting stakeholder needs
- Subject to hidden constraints: simulation tools might not converge for all design points

Surrogate-Based Optimization (SBO) aims to accelerate convergence by fitting a surrogate model
(e.g. regression, gaussian process, neural net) to the inputs (design variables) and outputs (objectives/constraints)
to try to predict where interesting infill points lie. Potentially, SBO needs about one or two orders of magnitude less
function evaluations than Multi-Objective Evolutionary Algorithms (MOEA's) like NSGA2. However, dealing with the
specific challenges of architecture optimization, especially in a combination of the challenges, is not trivial.
This library hopes to support in doing this.

The library provides:
- A common interface for defining architecture optimization problems based on [pymoo](https://pymoo.org/)
- Support in using Surrogate-Based Optimization (SBO) algorithms:
  - Implementation of a basic SBO algorithm
  - Connectors to various external SBO libraries
- Analytical and realistic test problems that exhibit one or more of the architecture optimization challenges

## Installation

First, create a conda environment (skip if you already have one):
```
conda create --name opt python=3.9
conda activate opt
```

Then install the package:
```
conda install numpy
pip install sbarchopt
```

Note: there are optional dependencies for the connected optimization frameworks and test problems.
Refer to their documentation for dedicated installation instructions.

## Documentation

Refer to the [documentation](docs/readme.md) for more background on SBArchOpt
and how to implement architecture optimization problems.
Test problem documentation can be found here: [test problems](docs/test_problems.md)

Optimization framework documentation:
- [pymoo](docs/algo_pymoo.md)
- [ArchSBO](docs/algo_arch_sbo.md)
- [BoTorch (Ax)](docs/algo_botorch.md)
- [Trieste](docs/algo_trieste.md)
- [HEBO](docs/algo_hebo.md)
- [TPE](docs/algo_tpe.md)
- [SEGOMOE](docs/algo_segomoe.md)
- [SMARTy](docs/algo_smarty.md)

## Contributing

The project is coordinated by: Jasper Bussemaker (*jasper.bussemaker at dlr.de*)

If you find a bug or have a feature request, please file an issue using the Github issue tracker.
If you require support for using SBArchOpt or want to collaborate, feel free to contact me.

Contributions are appreciated too:
- Fork the repository
- Add your contributions to the fork
  - Update/add documentation
  - Add tests and make sure they pass (tests are run using `pytest`)
- Issue a pull request