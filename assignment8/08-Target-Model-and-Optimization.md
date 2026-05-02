# Assignment 8 — Target Model and Optimization

## 1. Objective of the Assignment

The purpose of this assignment is to implement and rigorously evaluate the primary (target) model that constitutes the central technical contribution of the thesis.

At this stage, the student must demonstrate:

* Ability to extend beyond baseline modeling
* Controlled optimization and tuning strategy
* Awareness of overfitting and generalization limits
* Capacity to justify increased model complexity

This is the point at which the thesis transitions from methodological correctness (baseline validation) to engineering contribution (performance improvement, robustness, or analytical insight).

The primary model must be justified by:

* Literature (Assignment 2)
* Research hypothesis (Assignment 1)
* Empirical baseline results (Assignment 7)

## 2. Scope of Work to Be Delivered

The student must submit:

* Implemented primary model integrated into the existing pipeline
* Structured optimization strategy
* Comparative evaluation results
* Analytical discussion (3–5 pages)

The submission must contain the following components:

### A. Justification of Model Selection

The student must clearly explain:

* Why this model represents the core methodological contribution
* How it addresses the research gap identified earlier
* What limitations of baseline models it aims to overcome

The justification must connect:

* Literature review findings
* Observations from baseline results
* Hypothesis and research question

Model choice must be conceptually grounded, not trend-driven.

### B. Model Architecture and Configuration

Provide a formal description of:

* Model structure (layers, components, ensemble structure, etc.)
* Input-output interface
* Core hyperparameters

The description must focus on:

* Architectural rationale
* Design trade-offs
* Expected behavior under given data constraints

Code-level detail is not required; design-level clarity is mandatory.

### C. Optimization Strategy

Describe and justify:

* Hyperparameter search approach (grid search, random search, Bayesian optimization, etc.)
* Search space boundaries
* Computational constraints
* Early stopping or regularization mechanisms

Explicitly confirm:

* Validation strategy is consistent with Assignment 3
* Test data remains untouched during tuning
* Overfitting detection mechanisms are implemented

The student must demonstrate awareness that optimization must not compromise evaluation fairness.

### D. Generalization and Overfitting Analysis

This section is critical.

The student must analyze:

* Training vs. validation performance
* Learning curves (if applicable)
* Stability across folds
* Sensitivity to hyperparameter changes

Discuss:

* Whether performance gains are robust
* Whether improvements are statistically or practically meaningful
* Whether increased complexity leads to diminishing returns

Engineering maturity is demonstrated through critical restraint, not maximal tuning.

### E. Comparative Evaluation Against Baselines

Present results in:

* Comparative tables
* Metric-consistent reporting
* Optional visual comparison (e.g., performance curves)

The comparison must:

* Use identical preprocessing
* Use identical splits
* Use identical metrics

The student must explicitly state:

* Absolute improvement
* Relative improvement
* Computational cost difference

Improvement must be contextualized, not merely reported.

### F. Interpretation in Relation to Research Question

Conclude by explicitly answering:

* Does the primary model support the research hypothesis?
* Does it meaningfully outperform the baseline?
* What does this imply about the identified research gap?

The interpretation must avoid exaggerated claims. The focus must remain aligned with the original research problem defined in Assignment 1.

## 3. Academic Expectations for an Engineering Thesis

At the engineering level, the primary model stage must demonstrate:

* Controlled experimentation
* Transparent optimization
* Measured and critical interpretation
* Methodological integrity

The thesis is expected to:

* Improve upon baseline performance OR
* Provide deeper analytical insight OR
* Demonstrate robustness under defined constraints

It is not required to:

* Achieve state-of-the-art global benchmarks
* Implement highly complex architectures without justification

Excessive complexity without measurable gain is considered a methodological weakness.

## 4. Quality Evaluation Criteria

Assignment 8 will be evaluated based on:

1. Conceptual justification of the primary model
2. Rigor of optimization methodology
3. Fairness and transparency of comparison
4. Depth of generalization analysis
5. Alignment with research question and hypothesis

Approval of this assignment confirms completion of the core experimental phase.

## 5. Position Within the Seminar Continuum

* Assignment 7 established empirical baselines.
* Assignment 8 introduces and validates the core methodological contribution.
* Assignments 9–12 will shift focus from implementation to analytical synthesis, scientific interpretation, and formal thesis writing.

At this stage:

* The practical component should be functionally complete.
* Further changes must be incremental and justified.
* Experimental instability must be resolved before moving forward.

The thesis now transitions from experimentation to scientific articulation.
