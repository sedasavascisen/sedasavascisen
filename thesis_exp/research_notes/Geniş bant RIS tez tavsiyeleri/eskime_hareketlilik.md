# Channel aging, outdated CSI, mobility/Doppler and CSI staleness in RIS-assisted systems (2019–2026)

Method note: titles, authors, venues and DOIs below were checked against the Crossref API and the arXiv API on 2026-11-16, unless marked UNVERIFIED. Statements about what a paper *does* come from its abstract (arXiv API) or full text when this is noted. Claims marked "(search snippet)" come only from search-engine summaries and should be checked against the paper before anyone quotes them. Searched 2026-11-16; about 15 tool calls; not a systematic review.

## Q1. Which papers study RIS with outdated / aged CSI, how do they model time variation, and what metrics do they use?

### Takeaway
RIS aging work almost always uses the same model: a first-order Gauss-Markov / AR(1) process per link, with correlation ρ = J0(2π f_D τ) (Jakes/Clarke). The BS–RIS link is usually treated as quasi-static and only the RIS–UE and direct links age. The metrics are ergodic or sum SE (deterministic equivalents), secrecy capacity, ABER and outage probability. Delay τ is almost always pilot-to-data delay or feedback delay. It is never the optimizer's own run time.

### Cited Findings
- **Papazafeiropoulos, Krikidis, Kourtessis, "Impact of Channel Aging on RIS Aided Massive MIMO Systems With Statistical CSI", IEEE TVT 2023, DOI 10.1109/TVT.2022.3203796, arXiv 2209.04171.** Models aging in both the uplink training and downlink data phases. Uses MMSE estimation of the effective channels and RZF precoding. Derives a closed-form deterministic-equivalent sum SE that depends only on large-scale statistics, then optimizes the phase shifts and power on it. — [arXiv 2209.04171](https://arxiv.org/abs/2209.04171); DOI verified via [Crossref](https://doi.org/10.1109/TVT.2022.3203796)
- **Song, Shi, Lu, Zhu et al., "Performance Analysis of RIS-Aided MISO Systems with EMI and Channel Aging", IEEE VTC2024-Spring, DOI 10.1109/VTC2024-Spring62846.2024.10683661, arXiv 2405.09200.** The temporal correlation coefficient is the Jakes form ρ_i[n] = J0(2π n f_D T_s) (search snippet). — [arXiv 2405.09200](https://arxiv.org/abs/2405.09200)
- An ICC 2026 follow-up adds URLLC: "Performance Analysis of RIS-Aided MISO URLLC Systems with Channel Aging and EMI", DOI 10.1109/ICC59461.2026.11588182 (Crossref record only; content not checked). — [Crossref](https://doi.org/10.1109/ICC59461.2026.11588182)
- **Haider Shah, Qaraqe, Althunibat, Widmer, "On the Impact of Age of Channel Information on Secure RIS-Assisted mmWave Networks", IEEE VTC2024-Spring, DOI 10.1109/VTC2024-Spring62846.2024.10683291.** Full text read:
  - Builds a Monte Carlo study of how "age of channel information" affects the joint design of transmit beamforming and RIS configuration, in both the near and far field of the RIS.
  - The correlation is driven by the user's velocity and maximum Doppler shift.
  - Metric: secrecy capacity.
  - Conclusion: "adequate secrecy capacity can still be achieved even when channel information is slightly outdated, thus reducing the need for frequent RIS configuration."
  - [IMDEA repository PDF](https://dspace.networks.imdea.org/bitstream/handle/20.500.12761/1804/On%20the%20Impact%20of%20Age%20of%20Channel%20Information%20on%20Secure%20RIS-assisted%20mmWave%20Networks.pdf?sequence=1); [DOI](https://doi.org/10.1109/VTC2024-Spring62846.2024.10683291)
- **Deb & Ghosh, "Time varying channel estimation for RIS assisted network with outdated CSI: Looking beyond coherence time", Computer Communications 2025, DOI 10.1016/j.comcom.2025.108202, arXiv 2408.17128.**
  - Notes that channel-estimation (CE) overhead grows linearly with the number of RIS elements, and that "due to the mobility of the UE and the time consumed during CE, the estimated CSI may become outdated during actual data communication".
  - Proposes setting the time between CE rounds per user, from throughput analysis on outdated CSI (using channel condition and pathloss, not just coherence time).
  - Estimation delays T_d0 (direct link) and T_d (cascaded link) enter through correlation coefficients (search snippet).
  - [arXiv 2408.17128](https://arxiv.org/abs/2408.17128); [DOI](https://doi.org/10.1016/j.comcom.2025.108202)
- **Multi-RIS UAV-V2X under "mobility-aware CSI aging", Sensors 26(11):3355, 2026, DOI 10.3390/s26113355.**
  - Says mobility and feedback delay misalign the RIS phases, so ABER degrades "due to the loss in coherent combining gain".
  - Reports about a 75% ABER reduction for multi-RIS vs single RIS under outdated CSI at 20 dB (search snippet; authors not checked).
  - [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13259205/)
- **Multi-RIS LoRa, outdated + imperfect CSI + discrete phases (Oulu repository, 2025).** Joint BER/outage analysis. Exact venue and DOI not verified, so UNVERIFIED bibliographically. — [Oulu repository](https://oulurepo.oulu.fi/bitstream/handle/10024/54441/nbnfioulu-202503101930.pdf?sequence=1)
- **Liu, He, Zhang, Han et al., "Robust Transmission Design for RIS-Assisted High-Speed Train Communication Coverage Enhancement With Imperfect Cascaded Channels", arXiv 2604.15387 (2026).**
  - Argues that "due to the rapidly time-varying fading channels and feedback delays, achieving perfect CSI at the BS is not feasible in HST scenarios".
  - Uses bounded-error (worst-case rate, S-procedure/LMI) and statistical-error (outage, Bernstein-type inequality) robust designs.
  - Reports that cascaded-channel errors matter much more than direct-link errors (search snippet).
  - [arXiv 2604.15387](https://arxiv.org/abs/2604.15387)
- **Ryu, Choi, Yang, Cioffi, "End-to-End Mobility-Aware Multi-RIS Optimization via Blockage Detection and Closed-Form Riemannian Updates", arXiv 2608.25393 (Aug 2026).** Full text read:
  - Uses "the standard Gauss–Markov channel aging model" with a delay-dependent ρ(Δ) on the direct and RIS–UE links; the BS–RIS link is quasi-static.
  - [arXiv 2608.25393](https://arxiv.org/abs/2608.25393)
- **Doppler and high-mobility RIS:**
  - Basar, "Reconfigurable Intelligent Surfaces for Doppler Effect and Multipath Fading Mitigation", Frontiers in Communications and Networks 2021, DOI 10.3389/frcmn.2021.672857, arXiv 1912.04080. — [arXiv 1912.04080](https://arxiv.org/abs/1912.04080)
  - Huang, Zheng, Zhang, "Transforming Fading Channel from Fast to Slow: IRS-Assisted High-Mobility Communication", ICC 2021, DOI 10.1109/ICC42927.2021.9500699, arXiv 2011.03147. The journal version, "…Intelligent Refracting Surface Aided High-Mobility Communication", is IEEE TWC 2022, DOI 10.1109/TWC.2021.3135685, arXiv 2106.02274.
    - The refracting surface is mounted on the vehicle, so the LoS cascaded component mainly shows Doppler phase rotation across blocks.
    - A two-stage protocol estimates the LoS cascaded channel (Doppler-compensated) and then sets the refraction, which turns fast fading into slow fading.
    - [arXiv 2106.02274](https://arxiv.org/abs/2106.02274)
  - Huang, Zhu, Zhang, "Intelligent Surfaces Aided High-Mobility Communications: Opportunities and Design Issues", arXiv 2310.11309 (overview). — [arXiv 2310.11309](https://arxiv.org/abs/2310.11309)
  - Li, Niu, Wu, Ai, "Throughput Maximization for Intelligent Refracting Surface Assisted mmWave High-Speed Train Communications", IEEE IoT-J, DOI 10.1109/JIOT.2023.3337131, arXiv 2311.18167. Assumes Doppler is removed by a compensation scheme (search snippet). — [arXiv 2311.18167](https://arxiv.org/abs/2311.18167)
  - Hu, An, Gan, Yuen, "Performance Analysis of RIS-Aided High-Mobility Wireless Systems", arXiv 2508.15375. HST MISO with BCD joint optimization; reports about 15 dB average channel-gain improvement. — [arXiv 2508.15375](https://arxiv.org/abs/2508.15375)
  - IRS-aided relaying for high-speed trains, IEEE TWC 2024, DOI 10.1109/TWC.2024.3466555 (authors and content not checked). — [ACM DL](https://dl.acm.org/doi/10.1109/TWC.2024.3466555)

### Inferences
- The thesis's mobility model can cite J0-based Gauss-Markov as the de-facto standard (Song et al. 2024; Ryu et al. 2026; Truong & Heath 2013 for massive MIMO). A geometric or trajectory model, where the AoD/AoA drift of the RIS–UE link is deterministic, is rarer in this literature. It is mainly found in the HST/refracting-surface papers and in position-based predictive control (Q2).
- Every paper above defines staleness as the gap between pilot (or feedback) and data. None of them makes the delay τ depend on which optimizer is used.

### Gaps
- A side-by-side rate-loss-vs-velocity number across these papers was not extracted; most give only figures.
- Jakes vs geometric-model comparisons specifically for the *cascaded* channel were not found.

## Q2. Which works use channel prediction (Kalman, LSTM, transformer) for RIS under mobility, and what do they assume about estimation noise?

### Takeaway
There are prediction methods of all three kinds: Kalman/EKF tracking, CNN-AR and LSTM, and transformers. Most are trained or evaluated with noisy pilot-based estimates but a fixed SNR. No paper found compares Kalman, LSTM and transformer predictors for RIS under the same latency budget, and none counts the predictor's own inference time.

### Cited Findings
- **Liu, Chen, Pan, Pan, "Channel Tracking for RIS-Aided mmWave Communications Under High Mobility Scenarios", IEEE Commun. Lett. 2023, DOI 10.1109/LCOMM.2023.3262646, arXiv 2211.03671.**
  - Tracks the cascaded angles at the RIS rather than the individual angles.
  - Works under non-Gaussian noise.
  - Beats an EKF-based tracking baseline.
  - [arXiv 2211.03671](https://arxiv.org/abs/2211.03671)
- **Ginige, de Sena, Mahmood et al., "Machine Learning-Based Channel Prediction for RIS-Assisted MIMO Systems with Channel Aging", IEEE WCNC 2024, DOI 10.1109/WCNC57260.2024.10570599, arXiv 2406.07387.**
  - CNN integrated with an autoregressive predictor, for correlated fast fading.
  - Claims robustness to aging and lower pilot overhead.
  - [arXiv 2406.07387](https://arxiv.org/abs/2406.07387)
- **Koralege, de Sena, Mahmood, Karim et al., "A Deep-Unfolding Approach to RIS Phase Shift Optimization Via Transformer-Based Channel Prediction", Linköping Electronic Conf. Proc. 212 (2024) 441–447, DOI 10.3384/ecp212.060, arXiv 2502.18280.**
  - Compares DNN, LSTM and transformer predictors; the transformer gives the lowest RMSE.
  - The predicted channel feeds a deep-unfolded phase optimizer.
  - [arXiv 2502.18280](https://arxiv.org/abs/2502.18280)
- **Jiang, Cui, Ng et al. (Dai group), "Accurate Channel Prediction Based on Transformer: Making Mobility Negligible", IEEE JSAC 2022, DOI 10.1109/JSAC.2022.3191334.** Not RIS-specific.
  - Explicitly cites baseband *processing delay* as worsening aging, which motivates multi-frame-ahead prediction.
  - Reports a 2.5 dB / 1 dB NMSE gain over LSTM for near-future frames (search snippet).
  - [PDF](https://oa.ee.tsinghua.edu.cn/dailinglong/publications/paper/Accurate_Channel_Prediction_Based_on_Transformer_Making_Mobility_Negligible.pdf)
- **Mathias, Termehchi, Abrão, Hossain, "Beamforming Control in RIS-Aided Wireless Communications: A Predictive Physics-Based Approach", arXiv 2508.16980 (2025).**
  - States that RIS beamforming control has "multiple latency-inducing factors. As a result, by the time the beamforming is effectively updated, the channel conditions may have already changed."
  - Uses a kinematic observer (speed and acceleration from low-rate position estimates) plus a predictor, so the RIS is configured for a future position.
  - [arXiv 2508.16980](https://arxiv.org/abs/2508.16980)
  - A related closed-loop MPC letter by the same group: Mathias, Martins, Abrão, "A Closed-Loop Model Predictive Control for Beamforming in RIS-Aided Communications", IEEE WCL 2026, DOI 10.1109/LWC.2026.3701340 (Crossref only; content not checked).
- **LSTM-based trajectory prediction for multi-RIS activation and configuration, arXiv 2602.07937 (2026).** Predicts future user positions and reconstructs the geometric channel (search snippet; authors not checked). — [arXiv 2602.07937](https://arxiv.org/abs/2602.07937)
- **LSTM precoding with implicit CSI for RIS mmWave, arXiv 2509.12658.** Maps pilots directly to the RIS configuration (search snippet). — [arXiv 2509.12658](https://arxiv.org/abs/2509.12658)
- **Massive-MIMO origin of prediction-against-aging:** Truong & Heath propose channel prediction to partly recover the aging loss. — [arXiv 1305.6151](https://arxiv.org/abs/1305.6151)

### Inferences
- Deep prediction has a cost that is mostly not reported: inference latency adds to the same delay the predictor is meant to cover. The Dai-group JSAC paper is the only one found that names processing delay as part of the prediction horizon.

### Gaps
- None of the RIS prediction abstracts states whether training used noisy or noise-free past CSI. Clean-trained vs noise-trained comparisons were not found. (This is directly relevant to the thesis's "imperfect CSI: two arms" task.)

## Q3. Is there work on "age of CSI", AoI or staleness in RIS phase control or massive MIMO precoding that links update period or processing delay to performance? In particular, does any work treat the optimizer's own computation time as aging (the "effective rate" idea)?

### Takeaway
"Age of CSI" as a tunable update interval exists: Deng et al. 2017 for massive MIMO; Deb & Ghosh 2025 and Haider Shah et al. 2024 for RIS. RIS-AoI papers mostly optimize the AoI of *data packets*, with RIS phases as a means; that is a different concept. **I found no paper that evaluates each RIS (or MIMO) optimization method on the channel that exists when that method finishes, i.e. with method-dependent delay τ = T_acq + T_compute(method).** The closest are:
- Ryu et al. 2026: a T_sense + T_opt < T_CSI feasibility constraint, with FLOP counts and no wall-clock time.
- Mathias et al. 2025: latency-aware predictive control, with latency treated as given rather than set by the algorithm.
- Zappone et al. 2021: overhead-aware rate, where estimation and feedback time is subtracted from the slot but compute time is not modeled.
- The Dai-group JSAC paper: processing delay is named.

### Cited Findings
- **Deng, Jiang, Zhou, Niu, "How Often Should CSI be Updated for Massive MIMO Systems with Massive Connectivity?", arXiv 1707.09093 (2017).**
  - Analyzes "the influence of the age of CSI on the downlink transmission rate using linear precoders".
  - Shows the CSI updating interval should follow a quasi-periodic distribution, trading CSI accuracy against acquisition overhead by optimizing per-user update frequency.
  - Venue and DOI not verified, so UNVERIFIED (arXiv entry has no DOI); a related GLOBECOM'21 "How often do we need to estimate wireless channels…" PDF exists at NJU but was not checked.
  - [arXiv 1707.09093](https://arxiv.org/abs/1707.09093)
- **Haider Shah et al. VTC2024-Spring (above):** "age of channel information" against secrecy capacity. Concludes that slightly outdated CSI is acceptable, which lowers how often the RIS must be reconfigured. — [DOI](https://doi.org/10.1109/VTC2024-Spring62846.2024.10683291)
- **Deb & Ghosh 2025 (above):** the per-user inter-estimation interval is a design variable chosen from throughput under outdated CSI. Only CE time, not optimizer time, adds to staleness. — [arXiv 2408.17128](https://arxiv.org/abs/2408.17128)
- **Zappone, Di Renzo, Shams, Qian, Debbah, "Overhead-Aware Design of Reconfigurable Intelligent Surfaces in Smart Radio Environments", IEEE TWC 20(1):126–141, 2021, DOI 10.1109/TWC.2020.3023578, arXiv 2003.02538.**
  - Channel-estimation and phase-feedback durations scale with the number of RIS elements and are subtracted from the slot in the rate and energy-efficiency expressions.
  - Computation time of the optimizer is not part of the model, according to the available summaries; the full text was not read.
  - [arXiv 2003.02538](https://arxiv.org/abs/2003.02538); [DOI](https://doi.org/10.1109/TWC.2020.3023578)
- **Ryu, Choi, Yang, Cioffi, arXiv 2608.25393 (2026).** Full text read:
  - Imposes "T_sense(ℓ) + T_opt < T_CSI"; the data phase is shortened by sensing plus optimization time.
  - Channel realizations every 5 ms: weighted sum rate stays stable "as long as the detection–optimization loop can be completed within 5 ms".
  - Compares methods by FLOPs to 99% convergence, e.g. at M=32, K=16: SCRPA 3.867 GFLOP, AO-SPR 0.514 GFLOP, RMO-LS 54.997 GFLOP, WMMSE-GRAD 0.093 GFLOP.
  - No wall-clock times. The text contains a "55 ms budget" that is inconsistent with the 5 ms used elsewhere; probably a typo.
  - The feedback delay Δ is defined separately and T_opt is not explicitly added to the aging lag.
  - [arXiv 2608.25393](https://arxiv.org/abs/2608.25393)
- **Mathias et al. arXiv 2508.16980.** Treats RIS-control and localization latency as the source of mismatch and compensates by prediction. Latency is not tied to the algorithm's complexity (abstract). — [arXiv 2508.16980](https://arxiv.org/abs/2508.16980)
- **Delbari, Neuder, Jiménez-Sáez, Asadi, "Fast Transition-Aware Reconfiguration of Liquid Crystal-based RISs", arXiv 2402.05469 (2024).**
  - Hardware switching time (LC response) is the bottleneck.
  - The phase design minimizes the time to switch between configurations serving mobile TDMA users.
  - This adds another non-negligible deployment delay besides compute.
  - [arXiv 2402.05469](https://arxiv.org/abs/2402.05469)
- **RIS-AoI papers (packet freshness, not CSI freshness):**
  - Samir, Elhattab, Assi et al., "Optimizing Age of Information Through Aerial RIS: A Deep RL Approach", IEEE TVT 2021, DOI 10.1109/TVT.2021.3063953. — [Crossref](https://doi.org/10.1109/TVT.2021.3063953)
  - Muhammad, Elhattab, Arfaoui et al., "Age of Information Optimization in RIS-Assisted Wireless Networks", IEEE TNSM 2024, DOI 10.1109/TNSM.2023.3310790, arXiv 2103.06405. — [arXiv 2103.06405](https://arxiv.org/abs/2103.06405)
  - RIS-NOMA IoT freshness, arXiv 2202.13572. — [arXiv 2202.13572](https://arxiv.org/abs/2202.13572)
  - Qu, Huang, Khabbaz et al., "Optimization of Information Freshness in Multi-RIS Cooperative Assisted Wireless Sensor Network", IEEE TWC 2024, DOI 10.1109/TWC.2024.3439774 (Crossref only). — [Crossref](https://doi.org/10.1109/TWC.2024.3439774)
- **Feng & Yang, "Precoding and Scheduling for AoI Minimization in MIMO Broadcast Channels", arXiv 2009.00171.** Assumes perfect CSI before each transmission; AoI of the data, not of the CSI. — [arXiv 2009.00171](https://arxiv.org/abs/2009.00171)
- **Massive-MIMO aging background:**
  - Truong & Heath, "Effects of channel aging in massive MIMO systems", J. Commun. Netw. 2013, DOI 10.1109/JCN.2013.000065, arXiv 1305.6151. "The analytical results on aging show how capacity is lost due to time variation in the channel." The detailed model (AR with Jakes J0 correlation) is from memory and was not re-read, so UNVERIFIED in detail. — [arXiv 1305.6151](https://arxiv.org/abs/1305.6151)
  - Kong, Zhong, Papazafeiropoulos et al., "Sum-Rate and Power Scaling of Massive MIMO Systems With Channel Aging", IEEE TCOM 2015, DOI 10.1109/TCOMM.2015.2493998. — [Crossref](https://doi.org/10.1109/TCOMM.2015.2493998)
  - Papazafeiropoulos, "Impact of General Channel Aging Conditions on the Downlink Performance of Massive MIMO", arXiv 1605.07661. Doppler and LO phase noise jointly cause aging; deterministic equivalents for MRT and RZF. A GLOBECOM 2015 version has DOI 10.1109/GLOCOM.2015.7417729; the journal version's DOI was not verified. — [arXiv 1605.07661](https://arxiv.org/abs/1605.07661)
  - Zheng, Zhang, Björnson, Ai, "Impact of Channel Aging on Cell-Free Massive MIMO Over Spatially Correlated Channels", IEEE TWC 2021, DOI 10.1109/TWC.2021.3074421, arXiv 2104.11500. — [arXiv 2104.11500](https://arxiv.org/abs/2104.11500)
  - A patent on "adaptive learning aided precoder for channel aging" lists CSI-estimation *processing time* as an aging contributor that grows roughly linearly with the number of antennas (patent, not peer-reviewed). — [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12647165)

### Inferences
- The thesis claim, that compute latency is a first-class design constraint which reorders methods, appears not to be covered as stated. The ingredients exist separately:
  - aging models: Gauss-Markov/J0;
  - overhead-aware rates (Zappone 2021);
  - feasibility constraints on compute time (Ryu 2026, FLOPs only);
  - prediction to cover latency (Mathias 2025; Dai JSAC 2022).
- None of them ranks methods by rate measured on the channel at their own finish time, using measured wall-clock time. This is a gap the thesis can claim, after a further targeted search.
- Ryu et al. 2026 is the closest and most recent competitor. Its comparison is in FLOPs; under a compute-as-aging view, the ranking SCRPA > AO-SPR in converged WSR could reverse once SCRPA's roughly 7.5× higher FLOPs at M=32 are converted into extra staleness. That is a hypothesis, not a measured result.

### Gaps
- No search was done in Google Scholar, IEEE Xplore full text or other indexes, so a "first to consider" claim needs another targeted search: "computation delay" + "channel aging" + "reconfigurable intelligent surface"; "latency-aware" + "WMMSE"; "anytime algorithm beamforming".
- Full text of Zappone 2021 was not read to confirm that compute time is absent.

## Q4. Are there closed-form results for the optimum number of iterations or the update period under channel aging?

### Takeaway
There are closed-form or near-closed-form results for the **pilot spacing / frame size / CSI update interval** under aging, in massive MIMO. **No closed-form optimum number of iterations under aging was found**, in RIS, massive MIMO or adaptive beamforming. RIS papers fix iteration counts or report convergence curves.

### Cited Findings
- **Daei, Fodor, Skoglund, "Exploiting Spatial and Temporal Correlations in Massive MIMO Systems Operating Over Non-Stationary Aging Channels", IEEE TWC 2026, DOI 10.1109/TWC.2025.3637076, arXiv 2405.07882.**
  - Average-SE approximation as a function of pilot spacing, pilot and data powers and beamformers; maximizing it gives the optimal parameters (abstract).
  - Search snippets say the frame size has a closed form that depends mainly on the tagged user's velocity and is robust to channel-variance mismatch. Not confirmed in the full text.
  - [arXiv 2405.07882](https://arxiv.org/abs/2405.07882)
- **Deng et al., arXiv 1707.09093:** optimized per-user CSI update frequency, with a quasi-periodic update interval. — [arXiv 1707.09093](https://arxiv.org/abs/1707.09093)
- **Tentu, Amudala, Chattopadhyay, Budhiraja, "Hardware-Impaired Rician-Faded Cell-Free Massive MIMO Systems With Channel Aging", arXiv 2304.09019.** Closed-form SE under aging; the optimal pilot length is found *numerically* against UE speed (search snippet). — [arXiv 2304.09019](https://arxiv.org/abs/2304.09019)
- **Deb & Ghosh 2025:** adaptive CE interval from throughput under outdated CSI; whether the result is closed-form is not verified. — [arXiv 2408.17128](https://arxiv.org/abs/2408.17128)
- **Iterations vs delay:**
  - Guo, Makki, Svensson, "A Genetic Algorithm-based Beamforming Approach for Delay-constrained Networks", arXiv 1703.03792. A search snippet says the required number of iterations "decreases when the cost of running the algorithm is included" and is almost independent of the channel model. The abstract only mentions end-to-end throughput and lower complexity, so the iteration claim is UNVERIFIED against the full text. The setting is initial-access mmWave beamforming, not aging. — [arXiv 1703.03792](https://arxiv.org/abs/1703.03792)
  - A TechRxiv 2022 preprint on alternating optimization under channel aging and phase noise fixes AO at 3 iterations without optimizing that number (search snippet; authors and DOI not checked, so UNVERIFIED). — [TechRxiv](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.21253446.v1)
  - Ryu et al. 2026 report iterations to 99% of converged WSR (SCRPA ≈ 386, AO-SPR ≈ 47, RMO-LS ≈ 413) but do not optimize the iteration count against aging. — [arXiv 2608.25393](https://arxiv.org/abs/2608.25393)

### Inferences
- A closed-form optimum iteration count k* under aging is easy to state from the pieces:
  - gain curve G(k) = G∞ − c·q^k for a linearly converging method;
  - aging penalty from ρ(τ0 + k·t_iter) = J0(2π f_D (τ0 + k t_iter));
  - effective rate log2(1 + ρ² G(k) SNR / (1 + (1−ρ²) …)).
- It does not appear in the literature found, so it would be an original contribution of the thesis if derived. It must not be presented as previously published.

### Gaps
- Classical adaptive-filtering literature (LMS/RLS tracking: the optimal step size under a random-walk / Gauss-Markov target gives the misadjustment-vs-lag trade-off) is a likely source of closed-form "tracking vs convergence" results. It was not searched here. The standard reference is Haykin, *Adaptive Filter Theory* (book, no DOI), on lag error vs gradient noise; this is from memory, so UNVERIFIED in this session.

## Q5. Two-timescale RIS designs (statistical CSI for the RIS, instantaneous CSI for the precoder): what do they assume about precoder refresh?

### Takeaway
Two-timescale designs assume the precoder is refreshed every coherence block from fresh, or explicitly outdated, effective-channel CSI. The RIS is reconfigured only when the statistics change. Most assume the statistics are quasi-static and the short-timescale precoder is computed instantly. Cao, Lv & Ni (2022) is the exception: it models the per-slot precoder as using *outdated* instantaneous CSI.

### Cited Findings
- **Zhao, Wu, Zhao, Zhang, "Intelligent Reflecting Surface Enhanced Wireless Networks: Two-Timescale Beamforming Optimization", IEEE TWC 2021, DOI 10.1109/TWC.2020.3022297, arXiv 1912.01818.**
  - IRS phases are optimized on statistical CSI (correlated Rician), "which varies much slowly".
  - The AP precoder is "designed to cater to the I-CSI of the users' effective channels with the optimized IRS phase-shifts", which cuts training overhead and passive-beamforming complexity.
  - The precoder is assumed to use the current effective-channel CSI, with no aging stated in the abstract.
  - [arXiv 1912.01818](https://arxiv.org/abs/1912.01818); [DOI](https://doi.org/10.1109/TWC.2020.3022297)
  - Companion with QoS constraints and scheduling: arXiv 2011.02237. — [arXiv 2011.02237](https://arxiv.org/abs/2011.02237)
  - Note: the conference version is SAM 2020, DOI 10.1109/SAM48682.2020.9104346.
- **Cao, Lv, Ni, "Two-Timescale Optimization for IRS-Assisted MIMO Transmission in Fast-Changing Channels", IEEE TWC 2022, DOI 10.1109/TWC.2022.3184000, arXiv 2206.07276.**
  - The IRS is configured infrequently from statistical CSI.
  - The BS precoder and power allocation are updated frequently "based on quickly outdated instantaneous CSI".
  - The optimal small-timescale power allocation under outdated CSI is water-filling.
  - Large-timescale configuration is done by mini-batch PSO, or by model-driven PSO on a lower bound.
  - [arXiv 2206.07276](https://arxiv.org/abs/2206.07276)
- **Zhao, Xu, Cai, Niu et al., "Secrecy Rate Maximization of RIS-assisted SWIPT Systems: A Two-Timescale Beamforming Design Approach", arXiv 2211.16666.** Assumes quasi-static statistical CSI and notes that if the statistics go out of date quickly, statistical-CSI overhead and RIS re-optimization frequency both rise; leaves that to future work (search snippet). — [arXiv 2211.16666](https://arxiv.org/abs/2211.16666)
- **Statistical-only RIS designs under mobility:**
  - Papazafeiropoulos et al. TVT 2023 (above): phases from large-scale statistics, with aging included in the SE. — [arXiv 2209.04171](https://arxiv.org/abs/2209.04171)
  - A mmWave vehicular robust RIS design using only statistical CSI (UiA repository) argues that instantaneous CSI is "rapidly varying and easily outdated" under mobility (search snippet; bibliographic details not checked, so UNVERIFIED). — [UiA PDF](https://uia.brage.unit.no/uia-xmlui/bitstream/handle/11250/3137094/Article.pdf?sequence=1)

### Inferences
- The two-timescale literature shifts the compute-latency problem onto the precoder. The RIS solve is slow but runs rarely; the precoder must run every block. The precoder's compute time is assumed zero, or, in Cao et al. 2022, treated as a given outdatedness.
- For the thesis's framing, two-timescale designs are the main structural alternative to fast per-block RIS optimization. A fair baseline under "effective rate" would include a statistical-CSI RIS with a per-block RZF/MMSE precoder, whose compute time is small.

### Gaps
- None of the two-timescale papers checked reports the wall-clock time of the short-timescale precoder, or analyzes what happens when the statistics drift under user motion. Only Zhao et al. 2211.16666 mentions the latter, as future work.
