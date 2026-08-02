## An open text, a laboratory archive, and a state-space course are not substitutes

The [Feedback Systems companion](073-cds-101-cds-110.md) and its [open textbook site](https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers) connect modeling, analysis, design, and robustness. It is a companion and archive rather than a currently graded CDS 101/110 offering. The [official MIT 6.302 archive](https://ocw.mit.edu/courses/6-302-feedback-systems-spring-2007) uses Bode plots, root locus, compensation, and motor, thermal, or op-amp laboratories to develop classical frequency-domain judgment. Its syllabus assumes prior linear-systems, circuits, physics, and mathematics work, plus experience in an earlier circuit laboratory; it is not an entry course immediately after calculus. The [Stanford EE 263 archive](068-ee-263.md) enters through linear algebra and state space.

Use [MIT 6.302](067-6-302.md) as the default first pass because it grounds classical feedback judgment in electronic and electromechanical experiments. When a safe laboratory bench is unavailable, use the open Feedback Systems text and companion as the no-lab alternative. Add [MIT 6.241J](069-6-241j.md) or the 2008 EE 263 archive when formal controllability, observability, realization, estimation, robust stability, and robust performance are needed. The courses differ in entry point and evidence, so there is no reason to complete all four in numerical order.

Whichever spine is chosen, keep one physical object through modeling, analysis, and design. Switching to a new example chosen to flatter each method hides the interfaces among coordinates, linearization, and performance specifications.

## One second-order object should survive physical, pole, and experimental explanations

[Signals and systems](../signals-systems/index.md) contributes poles and zeros, convolution, frequency response, sampling, and stability. [Engineering mathematics](../mathematics/index.md) contributes ODEs, eigenvalues, quadratic forms, optimization, and probability. Choose a motor, thermal process, or mass-spring-damper system. Derive a state model from physical quantities, locate an equilibrium, linearize it, obtain a transfer function, and check it through units, energy, and limiting cases.

For the same poles or eigenvalues, distinguish internal, input-output, and asymptotic stability, then predict step-response and Bode features. Design a classical or state-feedback controller and compare two specifications using stability margin, transients, control effort, saturation, and sample-time sensitivity. “The simulation did not diverge” is not a stability proof. A controller plot cannot rescue inconsistent units among state, input, output, and disturbance.

Hand-calculate the direction of change caused by one variation in mass, damping, delay, or sample period. If that direction can only be read from a plot after the run, it is hard to tell whether the simulation is checking the model or the model is being adjusted to fit the simulation.

## An advanced course should answer how the baseline controller breaks

[MIT 6.243J](070-6-243j.md) treats nonlinear stability, Lyapunov methods, backstepping, and adaptive control. [6.245](071-6-245.md) treats MIMO systems, \(H_\infty\), \(\mu\), and LMIs. [6.231](072-6-231.md) treats stochastic decisions and dynamic programming. A pendulum-like system whose linear controller works only locally gives 6.243J a concrete role. A multivariable object that cannot meet stability and performance under uncertainty motivates 6.245. A state containing random resources or scheduling decisions motivates 6.231.

On the same second-order or low-order object, introduce parameter error, delay, noise, or disturbance and study one case that works nominally but breaks after perturbation. Separate model, discretization, measurement, and controller errors and name the uncovered operating region. If a new method cannot identify the nominal assumption it repairs, the added mathematics is hiding the baseline problem.

## The year determines which assignments, tools, and claims belong together

6.302 lacks its primary text notes, and the 1985 videos are not the 2007 classroom. Its motor, thermal, and op-amp labs also need a newly selected safe low-voltage BOM. EE 263 here means the 2008 Linear Dynamical Systems archive. Since Fall 2025, the same number denotes Matrix Methods and SVD, so current Julia work does not belong in the old MATLAB offering. 6.241J has no videos and incomplete solutions, 6.243J lacks a video and laboratory loop, 6.245 has a dated MATLAB and LMI workflow, and the 6 related videos listed by 6.231 are not recordings of that course.

End with a versioned low-order model, one nominal run, and one perturbed run whose solver, tolerance, discretization, and non-equivalent port features are stated. The term that explains the perturbation becomes the next syllabus: a nonlinear region of attraction leads to 6.243J, a multivariable uncertainty bound to 6.245, and a random policy or resource decision to 6.231. If none of those terms is needed to explain the run, the baseline model and controller still deserve another iteration.
