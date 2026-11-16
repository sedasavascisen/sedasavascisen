# Learning-based RIS phase prediction and phase representation (2019–2026), including wideband/OFDM

Scope note: the paper being positioned appears to be the user's own: Savaşçı Şen, "Overcoming the Phase Discontinuity Problem in RIS Optimization: A Robust and Scalable Phase-Aware Deep Regression Framework via Hybrid CNN–LSTM Architecture", Advanced Intelligent Systems, DOI 10.1002/aisy.70460 — [Wiley](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.70460). The publisher page returned HTTP 403 to my fetch. The figure below ("29.9% RMSE improvement", sin/cos pairs with an MSE-type loss) comes only from a search-engine snippet: UNVERIFIED. Check it against the paper itself and `aisy_paket/`.

Method: arXiv full texts (2001.02348, 2002.10072, 2009.13988, 2009.14404, 1904.10136, 2506.22448) and the IEEE Access PDF of Fondo-Ferreiro et al. were downloaded and searched with grep. Anything taken only from a search snippet is marked UNVERIFIED. I did not run Crossref lookups. DOIs are as printed in the papers or on arXiv/publisher pages.

---

## Q1. Which works use sin/cos (or complex-unit) outputs, circular losses, or wrapping-aware losses for RIS/beamforming, and what gains do they report?

### Takeaway
There are three output families in RIS learning:
- **(a) sin/cos encoding with an MSE regression loss.** This is the closest prior art to the target paper. Fondo-Ferreiro et al., IEEE Access 2025, do exactly this, for exactly the stated reason (2π periodicity).
- **(b) Raw angle output passed through e^{jθ} inside a rate-based loss.** Gao et al. 2020 do this. Here wrapping is a non-issue because the loss is 2π-periodic by construction.
- **(c) Real/imaginary outputs.** Some works then add an explicit unit-modulus normalization layer (Jiang/Cheng/Yu JSAC 2021; Huang/Mo/Yuen JSAC 2020). Others use a plain MSE on real/imaginary parts with no normalization (Özdoğan/Björnson 2020).

Outside RIS, circular regression is settled. Biternion and von Mises losses (Prokudin et al., ECCV 2018) reduce to a cosine loss on normalized (cos, sin) outputs. I found no RIS paper that reports a controlled ablation of sin/cos vs raw-angle regression other than the target paper (UNVERIFIED).

### Cited Findings
- **Fondo-Ferreiro, Saghezchi, Gil-Castiñeira, Rodriguez**, "Neural Networks for Phase Shift Optimization of RISs Under Imperfect CSI", IEEE Access 13:53694–53705, 2025, DOI 10.1109/ACCESS.2025.3552065 — [PDF](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf)
  - Encoding: each input and output angle is encoded as θ → (sin θ, cos θ) "to avoid the issues caused by the circular symmetry of the angles (i.e., they have a periodicity of 2π)". Decoding is arctan(y1/y2), written as plain arctan in the text, not atan2.
  - Network and inputs: a fully connected network that takes the angles of the imperfect Tx–RIS and RIS–Rx channel estimates.
  - Labels: the closed-form optimal phase computed from perfect CSI.
  - Reported results: for N ≥ 16, the FCN reaches "nearly optimal throughput and BER", with a gap below 1% to the optimum. The "direct" (unprocessed imperfect-CSI) approach degrades throughput by more than 60%. For N = 4 the FCN degrades by up to 15%. With L = 100 labels, the FCN reaches BER 0.14 against 0.2 for the direct approach (a 30% improvement).
  - Scope of the evidence: the reported gain is from denoising imperfect CSI. The paper does not isolate the effect of the sin/cos encoding itself.
- **Gao, Zhong, Chen, Lin, Zhang**, "Unsupervised Learning for Passive Beamforming", arXiv:2001.02348 (2020) — [arXiv](https://arxiv.org/abs/2001.02348)
  - The network outputs real phases p_pred. A Lambda layer computes θ_pred = e^{j·p_pred} = cos(p_pred) + j·sin(p_pred).
  - The loss is the negative received power, −(1/K)Σ|G_k Θ_k h_kr + h_kd|², which is inherently 2π-periodic in the phase.
  - "unlike the commonly used mean square error in supervised learning systems, the loss function is set to be the negative of the objective function."
- **Jiang, Cheng, Yu**, "Learning to Reflect and to Beamform for IRS with Implicit Channel Estimation", arXiv:2009.14404, IEEE JSAC 2021 — [arXiv](https://arxiv.org/abs/2009.14404)
  - A GNN maps received pilots directly to the configuration.
  - A final normalization layer outputs the real and imaginary parts of the reflection coefficients "while ensuring that the unit modulus constraints" hold. The BS beamformer is Frobenius-normalized to meet the power budget.
  - The loss is −E[Σ_k R_k(v,W)] (sum rate), or −E[min_k R_k] for max-min fairness.
- **Huang, Mo, Yuen**, "RIS Assisted Multiuser MISO Systems Exploiting Deep Reinforcement Learning", arXiv:2002.10072, IEEE JSAC 2020 — [arXiv](https://arxiv.org/abs/2002.10072)
  - DDPG actor with tanh activations.
  - "a normalization layer is employed at the output of the actor network", so that Tr{GG^H} = P_t and |Φ(n,n)|² = 1.
  - Complex quantities are split into real and imaginary parts.
- **Özdoğan, Björnson**, "Deep Learning-based Phase Reconfiguration for IRSs", arXiv:2009.13988, Asilomar 2020 — [arXiv](https://arxiv.org/abs/2009.13988)
  - Supervised training. The output stacks the optimal phases and beamformer, with real and imaginary parts separated (dimension 2(N+M)).
  - The loss is MSE. No unit-modulus layer is described in the method section I read.
- **Ma et al.**, "Unsupervised Learning-Based Joint Resource Allocation and Beamforming Design for RIS-Assisted MISO-OFDMA Systems", arXiv:2506.22448 (2025) — [arXiv](https://arxiv.org/abs/2506.22448)
  - BeamNet uses a sigmoid-based phase mapping, f(φ) = π·sigmoid(β(φ − π)), as a differentiable relaxation for discrete phases.
- **Metasurface (optics, not wireless RIS)** — [arXiv:2504.06069](https://arxiv.org/pdf/2504.06069)
  - A non-trainable normalization layer enforces sin²φ + cos²φ = 1, and the loss is a Euclidean distance in sin/cos space.
  - This is useful as cross-domain precedent but is not a RIS paper. The details come from a snippet: UNVERIFIED.
- **Circular regression (ML)**
  - Prokudin, Gehler, Nowozin, "Deep Directional Statistics: Pose Estimation with Uncertainty Quantification", ECCV 2018, arXiv:1805.03430 — [arXiv](https://arxiv.org/abs/1805.03430), [CVF](https://openaccess.thecvf.com/content_ECCV_2018/papers/Sergey_Prokudin_Deep_Directional_Statistics_ECCV_2018_paper.pdf).
  - That paper builds on biternion networks, which predict (cos, sin) followed by a normalization layer and a cosine loss. It extends them to von Mises likelihoods and von Mises mixtures for uncertainty.
  - The original biternion paper (Beyer et al., GCPR 2015) was not fetched, so its DOI is UNVERIFIED.
- **Von Mises likelihood reduces to a cosine loss.** Maximizing the von Mises log-likelihood with fixed concentration is equivalent to minimizing −cos(y − θ), as used in arXiv:2406.19162 — [arXiv](https://arxiv.org/abs/2406.19162).
- **Image-orientation comparison** — [arXiv:2603.25351](https://arxiv.org/pdf/2603.25351.pdf)
  - A 2026 study compares circular angle regression, binning, unit-vector regression and von Mises losses.
  - It reports that circular losses improve convergence over L1/L2. This is from a snippet: UNVERIFIED.

### Inferences
- **Novelty.** The "remove the ±π discontinuity with sin/cos" contribution is not new to RIS. Fondo-Ferreiro et al. (2025) use the identical encoding with the identical motivation. The circular-regression literature (biternions, 2015; von Mises, 2018) predates both. A positioning paper should cite these and frame its contribution as the architecture plus an empirical ablation, not as the encoding idea.
- **Unsupervised training.** The ±π discontinuity is a property of **supervised angle-regression losses** only. Any rate- or power-based loss computed through e^{jθ} (Gao 2020; Jiang 2021; Huang 2020) is periodic and has no discontinuity. So the sin/cos fix matters only when training against phase labels.
- **Projection.** Plain sin/cos MSE does not force (ŝ, ĉ) onto the unit circle, so decoding with atan2 projects implicitly. The biternion/unit-modulus normalization layer (Prokudin 2018; Jiang 2021; Huang 2020) makes that projection explicit and differentiable.
- **Decoding.** Fondo-Ferreiro's arctan(y1/y2) is quadrant-ambiguous unless it is implemented as atan2. That paper does not say which.

### Gaps
- I found no RIS paper with a controlled ablation (same network, raw-angle vs sin/cos vs unit-modulus layer vs rate loss) that reports rate gains. The 29.9% RMSE figure for the target paper is UNVERIFIED (403 on fetch).
- I found no RIS paper that uses a von Mises likelihood or a learned concentration (uncertainty) for phase outputs.

---

## Q2. How are learned RIS phase predictors evaluated: RMSE vs achievable rate vs effective rate under delay? Any on aged channels or with measured inference latency?

### Takeaway
Most works report **system metrics**: rate, received power or BER as a percentage of an optimization benchmark (SDR, SCA, AO, exhaustive search). They report latency only as **solver runtime**, compared with the iterative baseline on the same CPU or GPU, and usually argue it against the channel coherence time. Per-sample phase MSE/RMSE appears mainly in supervised work (Fondo-Ferreiro). I found **no** paper that evaluates a one-shot RIS phase predictor on an *effective rate under delay*, meaning rate computed on the channel that exists after inference latency has elapsed. The closest are:
- Gao 2020, which compares runtime with coherence time but does not age the channel.
- Taha et al. 2021, which uses an effective achievable rate that includes beam-training overhead.
- Urbinati et al., which measure on-device MCU latency against rate (snippet-level, UNVERIFIED).

### Cited Findings
- **Gao et al. 2020** (arXiv:2001.02348) — [arXiv](https://arxiv.org/abs/2001.02348)
  - The RISBFNN reaches 88.12–96.26% of SDR performance across configurations. Random phases reach 38.77–76.61%.
  - Measured runtimes on the same Intel i7-8700 CPU: 0.0399 / 0.0487 / 0.1167 ms for the NN vs 199.2 / 287.7 / 715.3 ms for SDR (M,N = 2,16 / 4,32 / 8,64).
  - The authors argue SDR is "inapplicable" because coherence time is Tc = 13.77 ms (1.5 m/s at 2.6 GHz). The NN's rate is not evaluated on aged channels.
- **Ma et al. 2025** (arXiv:2506.22448) — [arXiv](https://arxiv.org/abs/2506.22448)
  - At M = 64 (discrete phases), the network reaches 99.93% of the discrete-SCA sum rate in 0.036% of its runtime, on an RTX 3060 GPU and i7-12700 CPU.
  - The speed-up is "mainly attributed to the fact that our algorithm only requires a single forward pass."
- **Fondo-Ferreiro et al. 2025** (DOI 10.1109/ACCESS.2025.3552065) — [PDF](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf)
  - KPIs are BER, throughput, phase-shift estimation MSE, and NN **training** time.
  - The paper motivates using "accurate but less frequent (outdated) CSI", but it models the CSI error as additive Gaussian, not as temporal aging.
  - Per my text search, it reports no inference-latency measurement.
- **Taha, Alrabeiah, Alkhateeb 2021** (IEEE Access, DOI 10.1109/ACCESS.2021.3064073; arXiv:1904.10136) — [arXiv](https://arxiv.org/abs/1904.10136)
  - Evaluation uses achievable rate against an upper bound with perfect CSI.
  - The paper explicitly considers coherence time and beam-training overhead. It refines the k_B beams with the highest predicted rates to trade overhead for rate.
- **Urbinati, Decarli, Guidi, Guerra, Masini, Zanella**, "On-Device Deep Learning for RIS Beamforming", techRxiv / IEEE Access under review — [GitHub](https://ithub.global.ssl.fastly.net/LucaUrbinati44/DL-on-RISC), [ResearchGate](https://www.researchgate.net/publication/404250467_On-Device_Deep_Learning_for_RIS_Beamforming_Design_and_Latency-Rate_Trade-Offs)
  - The work deploys DL codebook selection on MCUs in the RIS controller and maps a latency–rate Pareto frontier.
  - Snippets give sub-millisecond inference for light models and about 10 ms for near-optimal rate (803 µs and 532 µs figures appear garbled). Retraining is repeated periodically under mobility.
  - **UNVERIFIED** numbers: full text not read.
- **Survey runtime figure** (Phase Shift Design survey, arXiv:2204.13372) — [arXiv](https://arxiv.org/abs/2204.13372)
  - The survey cites roughly 11 h of training against roughly 66 µs of inference for one unsupervised method.
  - It also notes that unsupervised methods give "no guarantee of solution quality". Snippet-level: UNVERIFIED as to which paper it refers to.
- **Channel aging handled by separate predictors.** CNN-AR channel prediction robust to aging ([arXiv:2406.07387](https://arxiv.org/pdf/2406.07387)) and velocity-aware re-estimation with outdated CSI ([arXiv:2408.17128](https://arxiv.org/abs/2408.17128)) both treat aging as a channel-prediction problem, not as an evaluation axis for phase predictors. Snippet-level: UNVERIFIED.

### Inferences
- **How latency is handled.** The field's standard latency argument is "NN runtime is far below coherence time, while the iterative solver is not" (Gao 2020; Ma 2025). The rate itself is still computed on the *same* channel the prediction was made from. That leaves a gap for latency-aware evaluation, where rate is computed at t + τ_inference (plus τ_CSI) for both the NN and the classical arm. This is the thesis framing: compute delay as a first-class constraint.
- **Weak baselines.** The usual baseline is a fixed-iteration solver (SDR with 100 randomizations, SCA) timed at full convergence. None of the works I read sweep the classical method's iteration and step budget so that it can match the NN's latency. This is the "weak baseline" pitfall listed in the project CLAUDE.md.
- **RMSE vs rate.** Phase RMSE is a weak proxy for rate. Rate depends on coherent combining, so phase errors on weak-gain elements matter little. No surveyed work reports the RMSE–rate correlation.

### Gaps
- I found no paper that reports effective rate on aged channels for a one-shot learned RIS phase predictor alongside measured inference latency. This absence is notable, but my search was limited (about 25 tool calls).
- The Urbinati latency numbers need the full text.

---

## Q3. Learning-based wideband RIS / OFDM phase design: architectures, evaluation, latency

### Takeaway
The anchor learning-based wideband work is Taha et al. 2021:
- OFDM with K subcarriers and **one reflection vector ψ for all subcarriers**, justified by analog phase shifters.
- A fully connected network regresses the predicted rate of every DFT-codebook beam, using an MSE loss on per-sample max-normalized rates.
- Evaluation is achievable rate vs a perfect-CSI bound. Latency is framed as beam-training overhead, and no inference time is reported.

Other learning work for wideband RIS is DRL (1-bit, OFDM), OFDMA resource allocation (Ma 2025), or THz/near-field schemes that frame the common-phase problem. Model-based wideband designs (beam-squint, common-phase upper-bound maximization) are the classical comparators.

### Cited Findings
- **Taha et al. 2021** (arXiv:1904.10136; DOI 10.1109/ACCESS.2021.3064073) — [arXiv](https://arxiv.org/abs/1904.10136)
  - "the same phase shift will be applied to the signals on all subcarriers, i.e., ψ_k = ψ, ∀k", with [ψ]_m = e^{jφ_m}.
  - "using one interaction vector ψ for all subcarriers, there is no closed" form solution, so the optimum requires exhaustive search over codebook P.
  - The model "output[s] a set of predictions on the achievable rates of every possible reflection beamforming vector in the codebook". It is trained with MSE(r, r̂), and labels are normalized per sample by max_n r(s)_n.
  - The DL input uses only the first K_DL = 64 subcarriers. The data come from the DeepMIMO ray-tracing dataset.
- **Ma et al. 2025** (arXiv:2506.22448) — [arXiv](https://arxiv.org/abs/2506.22448)
  - Unsupervised two-stage BeamNet + AllocationNet for RIS-assisted MISO-OFDMA, covering continuous and discrete phases.
  - Reports 99.93% of SCA rate at 0.036% of runtime.
  - The paper notes that prior works "focused on narrowband frequency-flat fading".
- **Fondo-Ferreiro et al. 2025**: in a 5G link-level (TU Vienna) setting, the method "estimates only a single phase shift value per RIS element" rather than the full response "across all subcarriers" — [PDF](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf)
- **"DRL-Based RIS Phase Shift Design for OFDM Communication Systems"** (IEEE Xplore doc 10037180): DQN designs phases for a 1-bit, column-wise RIS in downlink OFDM to raise spectral efficiency — [IEEE](https://ieeexplore.ieee.org/document/10037180/). Authors, DOI and latency reporting: UNVERIFIED (snippet only).
- **THz hybrid-field RIS deep learning** (Intelligent Computing, DOI 10.34133/icomputing.0065): the abstract names optimizing "a common RIS phase shared by all the subcarriers" as a crucial challenge, and the scheme combines channel extrapolation with DL multiuser beamforming — [SPJ](https://spj.science.org/doi/10.34133/icomputing.0065). UNVERIFIED beyond the snippet.
- **Model-based wideband comparators**
  - Beam-squint mitigation that derives per-frequency optimal phases, then a common phase that maximizes an achievable-rate upper bound — [arXiv:2103.11105](https://arxiv.org/abs/2103.11105).
  - Wideband near-field RIS beamforming — [arXiv:2401.11141](https://arxiv.org/abs/2401.11141).
  - TTD-based THz wideband precoding — [Tsinghua PDF](https://oa.ee.tsinghua.edu.cn/dailinglong/publications/paper/Wideband_Precoding_for_RIS-Aided_THz_Communications.pdf).
  - These are snippet-level as to specifics: UNVERIFIED.
- **Elbir & Mishra survey** of DL architectures for IRS, arXiv:2009.02540 — [arXiv](https://arxiv.org/abs/2009.02540) (not read in full).

### Inferences
- No surveyed learning-based wideband RIS paper reports measured inference latency against a latency-matched classical baseline. Taha 2021 reasons about overhead in beam-training slots. Ma 2025 reports runtime ratios against full-convergence SCA only.
- Taha's design sidesteps phase regression entirely: rate regression over a codebook, effectively classification. So it has no ±π issue, but it pays codebook quantization loss.

### Gaps
- The DQN-OFDM paper (10037180) and the THz hybrid-field paper were not read in full. Their architectures, metrics and latency are unverified.
- I found no learning-based wideband RIS paper that trains with an unsupervised loss averaged over subcarriers for a single common ψ and measures inference latency. Ma 2025 is OFDMA, and how its RIS phases relate to subcarriers was not confirmed in my reading.

---

## Q4. Unsupervised (rate-maximizing) vs supervised (label-based) training for RIS phase networks; pitfalls of label-based training

### Takeaway
Labels come from closed-form optima (single-user), exhaustive search, SDR or AO. The latter are suboptimal and expensive, so a supervised network is capped by its label generator and inherits its errors. Supervised phase regression also brings the ±π / phase-ambiguity problem. Unsupervised training on the negative rate (Gao 2020; Jiang 2021; Ma 2025) avoids labels and wrapping. The cost is no quality guarantee and a non-convex training landscape.

### Cited Findings
- **Gao et al. 2020**: "the main challenge of supervised learning is how to obtain labels. In [14], the optimal labels were obtained via exhaustive search, which is extremely" costly. Unsupervised learning is adopted so that "no labels are required" — [arXiv](https://arxiv.org/abs/2001.02348).
- **Ma et al. 2025**:
  - Supervised learning "requires large volumes of labeled data ... which are difficult to obtain in practical systems and may be as costly to generate as solving the original optimization problem."
  - Semi-supervised and self-supervised alternatives also have limitations.
  - [arXiv](https://arxiv.org/abs/2506.22448)
- **Fondo-Ferreiro et al. 2025**:
  - "Unsupervised approaches seem to be more practical for real-world applications since they do not require labeled data to operate, although they still need labeled data for cross-validation and testing."
  - Their own labels are the closed-form single-user optimum. They concede it is infeasible to obtain perfect CSI in practice, so in a real system the labels would come from exhaustive search or AO, which is "very time-consuming".
  - [PDF](https://pure.southwales.ac.uk/ws/portalfiles/portal/30824250/Neural_Networks_for_Phase_Shift_Optimization_of_Reconfigurable_Intelligent_Surfaces_Under_Imperfect_Channel_State_Information.pdf)
- **Özdoğan & Björnson 2020**: supervised, with labels from the optimal phase/beamformer obtained by alternating optimization, and an MSE loss on real/imaginary parts — [arXiv](https://arxiv.org/abs/2009.13988).
- **Survey arXiv:2204.13372**: unsupervised methods avoid labeling cost but give "no guarantee of solution quality" — [arXiv](https://arxiv.org/abs/2204.13372). Snippet-level: UNVERIFIED wording.
- **Jiang, Cheng, Yu 2021**: end-to-end, label-free training on the sum-rate or min-rate objective directly from pilots, bypassing explicit channel estimation — [arXiv](https://arxiv.org/abs/2009.14404).

### Inferences
- **Labels can be non-unique.** For single-user RIS, the rate is invariant to a common phase rotation of all elements when there is no direct link, and nearly invariant when the direct link is weak. Optimal labels are then non-unique, and MSE against one arbitrary representative penalizes equally good predictions. This is a pitfall separate from the ±π discontinuity, and sin/cos encoding does not fix it. It is my inference from the system model; no surveyed paper states it explicitly.
- **Per-sample metrics can mislead.** A supervised one-shot predictor evaluated by RMSE can look good while losing rate, or the reverse. Rate-based (unsupervised) training aligns the training objective with the system metric. For the positioning paper, comparing against an unsupervised rate-loss network of equal size is the natural ablation.
- **Mobility.** Labels computed on the current channel, given to a predictor that is deployed with latency, are stale by construction. Neither supervised nor unsupervised works in this survey train or evaluate against t + τ channels.

### Gaps
- I found no quantitative head-to-head between supervised and unsupervised training with the same architecture and data for RIS phases in the works I read.
- The classic label-quality ("learning to optimize", WMMSE imitation) literature outside RIS was not fetched in this pass.
