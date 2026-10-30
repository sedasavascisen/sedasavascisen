# RIS-MU — multi-user, geometry-based extension

Successor to `RIS-Phase-Discontinuity-Dataset`. The phase-aware sin/cos output
representation of the original work is kept **unchanged** throughout; what
changes is the channel the models are trained on, the number of users, the
training signal, and the architecture.

The point of the repository is not to produce a better number. It is to
establish, with controlled experiments, *which* parts of the original design
are doing the work, and what has to change before a claim about architecture
can be made at all.

---

## Summary of findings

**1. The legacy channel generator has no spatial structure.** It drew an
independent Rayleigh coefficient for every RIS element, inside the element
loop. A half-wavelength-spaced aperture cannot behave that way.

**2. On that channel, no architecture can beat an element-independent model.**
For a single user the optimal phase is `theta_n = -angle(F_n) - angle(G_n)`,
which depends on element *n* alone. A 6.6k-parameter MLP applied
independently to each element reaches 2.14°, matching the best large model.
Convolution and recurrence have nothing to exploit.

**3. The published accuracy is set by the output head, not the body.**
Holding the body fixed and replacing the dense bottleneck with a width-1
convolution changes RMSE by a factor of ~20. The published re-implementation
could not be made to reach its reported figure under either input
normalisation scheme.

**4. Spatial processing earns its place only when the channel is correlated
*and* the CSI is imperfect.** Both conditions are necessary; the legacy
dataset satisfies neither.

**5. Multi-user is where the architecture question becomes real,** because the
closed-form label does not exist and the users couple through one surface.

---

## Step 1 — the channel generator

`RIS_dataset_large_2D.m` lines 83-84, inside `for n = 1:N`:

```matlab
f0 = (randn+1j*randn)/sqrt(2) * exp(-1j*kwave*d_tx) / d_tx;
```

A fresh complex Gaussian per element. In `ris_mu/channel.py` each propagation
path instead carries **one** complex gain, and the per-element variation comes
from exact geometry (distance + `cos^q` element pattern). Added: Rician
K-factor, LoS blockage, correlated log-normal shadowing, and a scatterer
realisation **shared across users** so that nearby users see correlated
channels.

Measured on 1500 realisations, N = 32:

| model | \|rho\|@1d | \|rho\|@2d | eff. rank | cond [dB] | ramp-loss [dB] |
|-------|-----------|-----------|-----------|-----------|----------------|
| legacy       | 0.048 | 0.047 | 30.50 | 5.0  | 12.24 |
| geom/randBS  | 0.316 | 0.252 | 14.75 | 28.9 | 3.11 |
| geom/fixedBS | 0.351 | 0.257 | 14.80 | 28.2 | 4.55 |

*eff. rank* — entropy-based effective rank of the spatial covariance, upper
bound N = 32. *ramp-loss* — power lost when the optimal phase profile is
replaced by the best linear phase ramp; a physical channel keeps most of its
gain, an i.i.d. one does not.

`|rho|@1d = 0.35` is an **ensemble** average over all user positions, so
different arrival directions pull it down; conditioned on one geometry the
correlation is far higher. Quote it with that caveat.

### Two scenario errors inherited from the legacy setup

Both were found by checking the link budget rather than by inspection, and
both silently invalidate any RIS result built on them:

- **The panel faced away from the transmitter.** The legacy geometry placed a
  horizontal panel at `z = 3` with its normal pointing down, and the BS at
  `z = 4` — behind the surface, where a passive element radiates nothing.
  `make_scenario()` now builds matched panel/BS geometry and refuses a BS
  inside the Fraunhofer distance.
- **The RIS cascade was overestimated.** Applying a full path-loss formula to
  each hop double-counts the free-space constant and ignores the element
  aperture. The cascade now uses the physical two-hop model
  `Pr/Pt = Gt Gr Ge dx dy lambda^2 / ((4 pi)^3 d1^2 d2^2)` and takes only the
  *excess* loss from 3GPP TR 38.901 InH-Office.

With that fixed and the direct link blocked — the reason an RIS is deployed at
all — the scenario is healthy: cascade SNR median 30 dB, RIS gain 23 dB.

---

## Step 2 — where the published accuracy comes from

Crossing body against head on the legacy dataset, 40 000 samples:

| body | head | params | RMSE | SR@5° |
|---|---|---|---|---|
| none (element-local) | local | 6 626 | **2.14°** | 98.12% |
| CNN | dense | 583 296 | 50.19° | 10.43% |
| CNN | local | 17 730 | 2.46° | 96.14% |
| CNN-LSTM | dense | 822 976 | 28.62° | 16.92% |
| CNN-LSTM | local | 257 410 | **2.00°** | 97.64% |

The head accounts for essentially all of the variation. With a local head the
body is worth 7% (2.14° → 2.00°) for 39× the parameters — consistent with the
theory, since on this channel the task *is* element-local.

The published dense head ends in a 64-unit layer feeding 2N outputs. At
N = 32 those are equal; at N = 256 it must push 512 numbers through 64 units.
If the original work's degradation with surface size has the same cause, it is
a property of the head and not of the problem.

**Reproduction note.** A faithful re-implementation of the published
architecture reaches 27.97°, not the reported 2.77°. The gap is not explained
by input normalisation: per-feature standardisation, as in the original
`train_cnn_lstm.py`, gives 61.00° against 51.58° for per-sample normalisation
on the same model. The public repository does not contain the preprocessing
script (`theta_NN_multioutput.m`) that produced the training matrices, so the
discrepancy cannot be resolved from the published artefacts alone.

---

## Step 3 — when spatial processing earns its place

CSI error applied to the model input only; labels from the true channel. All
models use the local head, so the comparison isolates the body.

| channel | sigma | element-local | local mixing | global mixing |
|---|---|---|---|---|
| legacy | 0.00 | **3.52°** | 4.91° | 4.91° |
| legacy | 0.10 | **15.90°** | 16.23° | 16.40° |
| legacy | 0.25 | **33.39°** | 33.59° | 33.75° |
| geometric | 0.00 | **2.76°** | 5.10° | 5.86° |
| geometric | 0.10 | **11.14°** | 11.68° | 11.89° |
| geometric | 0.25 | 24.53° | 23.34° | **22.94°** |

On the legacy channel mixing never wins, at any noise level: neighbouring
elements are independent, so there is nothing to borrow. On the geometric
channel the ordering reverses once the CSI is poor enough — the only cell in
the table where convolution and recurrence pay for themselves.

This is the experiment that ties the realism contribution to the architecture
contribution. Without a correlated channel there is no argument for a spatial
model; with perfect CSI there is none either.

---

## Step 4 — multi-user, trained without labels

`theta_n = -angle(F_n) - angle(G_n)` is optimal for one user only. With U
users sharing one surface no closed form exists, so there is nothing to
regress onto — and a network trained to imitate a numerical solver cannot beat
it. Training runs directly on the system metric instead.

Single-antenna BS, users in orthogonal slots, surface fixed over the block:
one phase vector must serve everyone, so the objective is max-min rate
(smoothed, see `losses.py`).

U = 4, N = 32, 16 000 scenarios, max-min rate in b/s/Hz:

| method | min rate | sum rate | % of PGA | ms/sample | params |
|---|---|---|---|---|---|
| no RIS | 0.689 | 13.861 | 10.3% | - | - |
| random phase | 2.616 | 23.911 | 39.2% | - | - |
| **SU closed form** | **5.733** | 33.766 | **86.0%** | - | - |
| PGA max-min (reference) | 6.666 | 34.700 | 100.0% | 2.318 | - |
| MU-CNN-LSTM | 5.304 | 32.602 | 79.6% | 0.172 | 263 554 |
| Equivariant | 5.659 | 33.827 | 84.9% | 0.760 | 130 242 |
| Equiv + residual | 5.351 | 32.727 | 80.3% | 0.846 | 130 435 |

Two things to report honestly. The equivariant model beats the concatenated
extension of the published architecture by 6.7% with half the parameters —
that comparison is the architectural result. But **at U = 4 neither learned
model beats the single-user closed form**, which reaches 86% of the iterative
reference for the cost of one arctangent per element plus U objective
evaluations. One forward pass is not enough to beat a well-chosen heuristic at
this user count; see step 5 for where that changes.

The residual variant (which starts from a weighted circular mean of the
per-user alignments and learns a correction) converges to a worse optimum than
training from scratch. It reaches its reference quickly and then stops
improving — a warm start is not free here.

Baselines in `ris_mu/baselines.py`: no-RIS, random phase, single-user closed
form applied to the best user, and projected gradient ascent on the smooth
max-min objective (the classical reference, 300 iterations × 3 restarts).

---

## Step 5 — what the symmetries buy

The surface serves a *set* of users: a model whose output changes when the
users are relabelled is fitting an artefact, and a model that fixes U in its
first layer cannot be deployed where U varies. `EquivariantRIS` is invariant
to user permutation and equivariant to element permutation by construction
(verified to 2e-07), and accepts any U.

**Relabelling the users** (same 3000 scenarios, 8 permutations):

| model | min rate | spread over permutations |
|---|---|---|
| MU-CNN-LSTM | 5.5522 ± 0.0117 | 0.0316 |
| Equivariant | 5.9714 ± 0.0000 | **0.0000** |

**User counts never seen in training** (trained at U = 4), and the effect of
training across U ∈ {2..6} instead:

| U | trained U=4 | trained mixed | SU closed form | PGA | mixed % of PGA |
|---|---|---|---|---|---|
| 2 | 7.756 | 7.957 | 7.482 | 8.465 | 94.0% |
| 3 | 6.640 | 6.712 | 6.419 | 7.383 | 90.9% |
| 4 | 5.850 | 5.899 | 5.782 | 6.719 | 87.8% |
| 6 | 4.923 | 4.940 | 5.104 | 6.005 | 82.3% |
| 8 | 4.081 | 4.117 | 4.474 | 5.350 | 77.0% |

Margin over the single-user closed form:

| U | trained U=4 | trained mixed |
|---|---|---|
| 2 | +3.7% | **+6.4%** |
| 3 | +3.4% | **+4.6%** |
| 4 | +1.2% | **+2.0%** |
| 6 | −3.6% | −3.2% |
| 8 | −8.8% | −8.0% |

The learned model wins at U ≤ 4 and loses at U ≥ 6. Mixed-U training improves
it at every user count but does not move the crossover. The reason the
baseline strengthens with U is worth stating: "align to the best user" is a
search over U candidates scored on the true objective, so it gets more
candidates as U grows — it is a one-step search, not a free formula.

Being defined for any U buys applicability, not accuracy. That distinction is
the result of this step.

---

---

## Verification of the two load-bearing claims

Both conclusions were re-tested adversarially before being written up.

**The head claim.** The objection is that the dense models were undertrained.
Giving the dense head a lower learning rate, no dropout and 70 epochs changes
nothing (49.75° against 50.19°). Widening only the final hidden layer from 64
to 512 units takes it to 3.77°, which identifies the cause directly: it is the
width of the layer feeding the 2N outputs, not tuning and not the body.

| variant | params | RMSE | what it shows |
|---|---|---|---|
| A — dense, published settings | 583 296 | 50.19° | starting point |
| B — dense, tuned (lr 3e-4, no dropout, 70 ep) | 583 296 | 49.75° | not a tuning artefact |
| C — dense, bottleneck widened 64 → 512 | 1 620 672 | 3.77° | **this is the cause** |
| D — local head | 17 730 | 2.46° | same job, 1% of the parameters |

**The crossover claim.** Step 3 measured the decisive cell once. Repeating it
over four seeds — each redrawing both the channel and the initialisation —
puts the effect an order of magnitude outside the noise.

| channel | element-local | spatial mixing | advantage | seeds where mixing won |
|---|---|---|---|---|
| legacy | 33.28 ± 0.09 | 33.57 ± 0.07 | +0.9 ± 0.1% | **0 / 4** |
| geometric | 24.90 ± 0.11 | 23.41 ± 0.20 | −6.0 ± 0.5% | **4 / 4** |

```bash
python scripts/verify_head_claim.py --n 40000
python scripts/verify_crossover.py --n 12000 --seeds 4
```

---

## Resolving the reproduction gap

The published MATLAB script and the repository's Python script are **different
architectures**. `theta_NN_multioutput_UPDATED.m` ends in

```matlab
lstmLayer(128,'OutputMode','sequence')
lstmLayer(64, 'OutputMode','sequence')
dropoutLayer(0.3)
fullyConnectedLayer(2)        % output size 2, not 2N
```

With a `sequenceInputLayer`, MATLAB applies a fully connected layer at every
time step independently, so the published model emits (sin, cos) per element
through one shared 64→2 map — a width-1 convolution, i.e. the local head of
this study. The repository's `train_cnn_lstm.py` instead flattens the LSTM
output and squeezes it through a 64-unit dense bottleneck. It is not a port of
the MATLAB model.

Rebuilding the MATLAB stack exactly and training it on the same data:

| architecture | RMSE | SR@5° | params |
|---|---|---|---|
| published figure (paper) | 2.77° | — | 727,360 (claimed) |
| **MATLAB stack, re-run here** | **2.11°** | 98.18% | **162,562** |
| repo `train_cnn_lstm.py` (dense head) | 27.97° | 17.59% | 822,976 |

Two consequences. The published result is reproducible, and the head analysis
above is confirmed from the opposite direction. The parameter count in the
paper does not match the architecture: the MATLAB stack has 162,562 trainable
parameters, not 727,360.

The complexity claim also depends on which file is read. With a per-element
head the model is genuinely O(N); the repository's dense head makes it O(N²)
through the N·64 → 256 matmul.

```bash
python scripts/verify_matlab_architecture.py --n 40000 --epochs 50
```

## Layout

```
ris_mu/geometry.py    RIS panel, element positions, cos^q pattern
ris_mu/pathloss.py    3GPP TR 38.901 InH-Office / InF-SL parameters
ris_mu/channel.py     MultiUserRISChannel, make_scenario, legacy_generate
ris_mu/features.py    input construction and labels
ris_mu/models.py      SharedMLP, FCDNN, CNNOnly, CNNLSTM, MUCNNLSTM, EquivariantRIS
ris_mu/losses.py      phase-aware MSE, rate objectives, metrics
ris_mu/baselines.py   no-RIS, random, closed form, PGA max-min
ris_mu/train.py       shared training harness

scripts/diagnose_realism.py      step 1 channel diagnostics
scripts/step1_control.py         element-independent control experiment
scripts/step1b_head_ablation.py  body x head ablation
scripts/step3_csi_transfer.py    channel x CSI-error x model sweep
scripts/step4_multiuser.py       unsupervised multi-user training
scripts/step4b_residual.py       residual variant
scripts/step4c_equiv_long.py     extended training of the equivariant model
scripts/step5_generalisation.py  symmetry and user-count generalisation
scripts/compile_results.py       collects every JSON into the final tables
scripts/verify_head_claim.py     adversarial re-test of the head conclusion
scripts/verify_crossover.py      multi-seed re-test of the crossover conclusion
scripts/verify_matlab_architecture.py  faithful port of the published MATLAB stack
```

## Run

```bash
python scripts/diagnose_realism.py --n 2000
python scripts/step1b_head_ablation.py --n 40000 --epochs 35
python scripts/step3_csi_transfer.py --n 12000 --epochs 22
python scripts/step4_multiuser.py --n 16000 --epochs 40 --users 4
python scripts/step5_generalisation.py --n 4000
python scripts/compile_results.py
```

## Requirements

`numpy`, `scipy`, `matplotlib`, `torch` (CPU is sufficient; every result here
was produced on two cores).
