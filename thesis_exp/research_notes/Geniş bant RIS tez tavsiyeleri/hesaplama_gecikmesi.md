# Computation-latency-aware beamforming and RIS optimization (2018–2026)

Scope note: about 17 search/fetch calls. Most sources were checked only at the arXiv abstract page or through search snippets, and each entry says which. Any number not confirmed at a primary page is marked UNVERIFIED. Unless an entry says otherwise, DOIs are arXiv-issued (10.48550/arXiv.<id>). I did not check DOIs against Crossref in this pass, so publisher DOIs listed as "from arXiv page" count as reported, not Crossref-verified.

## Q1. Which works define computation-aware, processing-delay-aware or anytime beamforming, and what do they conclude about iteration count vs performance?

### Takeaway
Hardly any wireless paper uses the term "anytime" for beamforming or RIS optimization, and I found none for RIS. The nearest explicit treatment counts the algorithm's running time against the slot's throughput and concludes that a suboptimal beamformer that stops early maximizes end-to-end throughput. Most "real-time" learning papers state the problem (computational delay makes iterative solutions go stale) but do not define a latency-constrained objective.

### Cited Findings
- Guo, Makki, Svensson, "A Genetic Algorithm-based Beamforming Approach for Delay-constrained Networks" (arXiv:1703.03792, 2017). Abstract: the GA scheme reaches "(almost) the same end-to-end throughput as the exhaustive search-based optimal approach" with "considerably less implementation complexity". A search snippet adds that the paper counts algorithm running time inside throughput, finds the best throughput comes from a suboptimal beamformer (the remaining slot time goes to data), and finds the required number of iterations falls once computation cost is counted. The snippet-level claims come from the PDF snippet only and were not seen on the abstract page: UNVERIFIED in detail. This is the closest conceptual precedent for "latency is a design constraint that changes the optimal iteration count". — [arXiv:1703.03792](https://arxiv.org/abs/1703.03792)
- Xia, Zheng, Zhu, Zhang, Wang, Petropulu, "A Deep Learning Framework for Optimization of MISO Downlink Beamforming", IEEE TCOM (DOI 10.1109/TCOMM.2019.2960361, from arXiv page). Its motivation: iterative optimization "introduces high computational delay and is thus not suitable for real-time implementation". It reports performance near WMMSE for sum rate with "significantly reduced computational complexity". The abstract gives no wall-clock numbers. — [arXiv:1901.00354](https://arxiv.org/abs/1901.00354)
- Sun, Chen, Shi, Hong, Fu, Sidiropoulos, "Learning to Optimize: Training Deep Neural Networks for Interference Management", IEEE TSP 66(20):5438–5453, 2018 (DOI 10.1109/TSP.2018.2866382). The DNN approximates WMMSE and claims "orders of magnitude speedup in computational time". The abstract has no specific timing figures. This is the founding "learning to optimize" wireless paper whose argument rests on computation time. — [arXiv:1705.09412](https://arxiv.org/abs/1705.09412)
- RIS staleness from control latency: the paper argues that RIS beamforming control has several latency sources, so "by the time the beamforming is effectively updated, the channel conditions may have already changed". It also says raising the reconfiguration rate can overload the control channel. Its remedy is predictive, physics-based control. — [arXiv:2508.16980](https://arxiv.org/abs/2508.16980) (search snippet / HTML page)
- Latency-aware multi-RIS uplink delay minimization with an online low-overhead heuristic (2026). Seen only in a search snippet: UNVERIFIED in detail. — [arXiv:2602.17198](https://arxiv.org/abs/2602.17198)
- Delay-constrained MU-MIMO beamforming with imperfect CSIT (2013). Per a search snippet, it reports MATLAB computation time per decision slot and says the value-iteration baseline needs more than 10^3 s. Here "delay" means queueing delay, not compute latency. — [arXiv:1305.1012](https://arxiv.org/abs/1305.1012)

### Inferences
- The thesis claim that compute latency is a first-class constraint that reorders methods has one direct precedent (Guo/Makki/Svensson 2017: the optimal iteration count shrinks once runtime is charged against the slot). That work is non-RIS and GA-based. I found no RIS-specific paper that formalizes an anytime or iteration-budgeted objective under mobility, so the niche looks open (absence of evidence, not proof).
- The usual framing in the literature is one-sided: learning is assumed to win because it is "fast", and the comparison is against iterative solvers run to convergence. A classical solver truncated to the same time budget is not used.

### Gaps
- No source uses "anytime beamforming" or "anytime RIS optimization" explicitly. Searches for "anytime" and "early termination" with RIS returned none.
- I could not open the full text of 1703.03792 to quote its iteration-vs-throughput figure.

## Q2. Which deep-unfolding RIS/MIMO papers report measured runtimes, and do they compare against a classical baseline tuned at each time budget?

### Takeaway
Many unfolding papers report runtime speedups, typically 10–25x, but the baseline is almost always the classical algorithm run to convergence or for a fixed iteration count. None of the papers I found tunes the classical baseline's step size or objective at each wall-clock budget. Several compare only on equal iteration or layer counts.

### Cited Findings
- Hu, Cai, Shi, Xu, Yu, Ding, "Iterative Algorithm Induced Deep-Unfolding Neural Networks: Precoding Design for Multiuser MIMO Systems" (arXiv:2006.08099). It unfolds WMMSE with fewer layers than iterations and replaces matrix inversion with element-wise nonlinearity and a first-order Taylor approximation. It claims WMMSE-level performance "with reduced computational complexity". I did not retrieve runtime numbers. The journal is IEEE TWC 2021; the publisher DOI 10.1109/TWC.2020.3033334 is from memory: UNVERIFIED. — [arXiv:2006.08099](https://arxiv.org/abs/2006.08099)
- Pellaco, Bengtsson, Jaldén, "Deep unfolding of the weighted MMSE beamforming algorithm" (arXiv:2006.08448). It replaces inversion, eigendecomposition and bisection with PGD. It "matches or outperforms" WMMSE **with the same number of iterations** in most settings and claims "lower computational load". This is an iteration-matched comparison, not a wall-clock one. — [arXiv:2006.08448](https://arxiv.org/abs/2006.08448)
- Chowdhury, Verma, Swami, Segarra, "Deep Graph Unfolding for Beamforming in MU-MIMO Interference Networks" (UWMMSE, arXiv:2304.00446). A search snippet reports about 54 ms per sample for UWMMSE against about 1.30 s for classical WMMSE (about 24x). The abstract page has no runtime numbers, so the figures are UNVERIFIED (snippet only). — [arXiv:2304.00446](https://arxiv.org/abs/2304.00446)
- Adam et al., "Real-Time and Security-Aware Precoding in RIS-Empowered Multi-User Wireless Networks" (DUNet, arXiv:2401.00192). This is an RIS deep-unfolding paper with an explicit runtime claim: "about 25.6 times faster" than alternating optimization at comparable accuracy. The abstract does not give hardware or timing method. — [arXiv:2401.00192](https://arxiv.org/abs/2401.00192)
- DeepFP (deep-unfolded fractional programming for MIMO beamforming). Per a search snippet: about 0.053 s CPU against about 0.563 s for WMMSE-SC (Nt=64, K=6), reaching about 98.9% of the baseline rate, with the classical baseline higher in rate. UNVERIFIED (snippet). — [arXiv:2601.02822](https://arxiv.org/abs/2601.02822)
- Deep-unfolded fractional optimization for robust throughput (2026). Per a snippet, it reports the lowest single-CPU inference time, with WMMSE the next fastest. UNVERIFIED (snippet). — [arXiv:2602.06062](https://arxiv.org/abs/2602.06062)
- Deep-unfolded THz hybrid beamforming. Per a snippet, about 0.01 s against more than 10 s for MO-AltMin at Nt=128. This is not RIS. UNVERIFIED (snippet). — [arXiv:2302.12041](https://arxiv.org/abs/2302.12041)
- Unfolded PGA for hybrid joint communication and sensing beamforming. Per a snippet, runtime falls by up to 65% against PGA without unfolding, which is a same-algorithm comparison. UNVERIFIED (snippet). — [arXiv:2411.17747](https://arxiv.org/abs/2411.17747)
- RIS-specific PGD unfolding with learnable per-layer step sizes. The paper notes a gradient–phase scale mismatch that can stall updates; I saw no runtime numbers. — [arXiv:2606.17484](https://arxiv.org/abs/2606.17484) (snippet); also SIM unrolled PGD [arXiv:2603.02122](https://arxiv.org/abs/2603.02122) (snippet)
- RIS phase prediction with transformer channel prediction plus deep unfolding. — [arXiv:2502.18280](https://arxiv.org/abs/2502.18280) (title only; runtime not checked)
- Survey context: Balatsoukas-Stimming & Studer, "Deep Unfolding for Communications Systems: A Survey and Some New Directions" — [arXiv:1906.05774](https://arxiv.org/abs/1906.05774); a 2025 review of deep unfolding for next-generation wireless — [arXiv:2502.05952](https://arxiv.org/abs/2502.05952). A snippet from one detection paper says NN-based detectors need "5× to more than 100× higher runtime than a standard LMMSE" detector. The paper and context are UNVERIFIED, and I did not identify the exact source.

### Inferences
- The standard reporting pattern is (a) equal iteration count (Pellaco 2020), or (b) unfolded network against a classical algorithm run to convergence or to a fixed high iteration count, measured on CPU (DUNet, UWMMSE, DeepFP). Neither is an equal-wall-clock comparison against a classical solver whose step size and objective are re-tuned for each budget. The thesis protocol (sweep the classical arm's best setting per latency budget, select on validation, report on test) therefore appears stricter than the published norm. The reported 10–25x speedups would likely shrink under that protocol. This is an inference; none of these papers ran the stricter test.
- Speedups are often reported only per sample at inference, with no hardware, threading or load details. That makes them hard to compare and vulnerable to the measurement-load bias this project has already encountered.

### Gaps
- I could not confirm a single RIS deep-unfolding paper that reports wall-clock against a per-budget-tuned classical baseline. I believe none exists, but my search was not exhaustive.
- I did not extract runtime tables for Hu et al. 2006.08099 or UWMMSE from the full texts.

## Q3. FPGA/real-time RIS controller papers: reconfiguration time, switching speed, controller latency

### Takeaway
Controller and reconfiguration latency spans several orders of magnitude. PIN-diode element switching takes about 1–10 µs (textbook figures). FPGA-driven PIN tiles report full updates below 0.1 ms. Microcontroller or host-software prototypes take ms-scale times per configuration, and liquid-crystal RIS takes tens of ms per array. Few papers report an end-to-end channel-to-phase-update loop time.

### Cited Findings
- Dai et al., "Reconfigurable Intelligent Surface-Based Wireless Communications: Antenna Design, Prototyping, and Experimental Results", IEEE Access 8:45913–45923, 2020, DOI 10.1109/ACCESS.2020.2977772 (DOI from repository record). The prototype has 256 elements with 2-bit PIN-diode phase shifting, gain of 21.7 dBi at 2.3 GHz and 19.1 dBi at 28.5 GHz, and USRP baseband. I found no switching-time figure in the abstract-level sources. — [Southampton ePrints](https://eprints.soton.ac.uk/438298/); [HAL](https://hal-centralesupelec.archives-ouvertes.fr/hal-02944237)
- Computer-vision-aided RIS beam tracking prototype (arXiv:2207.05032). Per snippets: a master/slave cascaded FPGA control board up to 200 MHz (100 MHz reference), a 1.6 Gbps inter-FPGA link, each PIN diode driven individually, and total RIS power under 0.5 W. The excerpts give no measured end-to-end reconfiguration time. UNVERIFIED (snippet). — [arXiv:2207.05032](https://arxiv.org/abs/2207.05032)
- An 8×16 one-bit PIN RIS for privacy-preserving ISAC lists a "RIS switching time of 2 ms" in its experiment table, with an FPGA over Ethernet running Verilog/C++. UNVERIFIED (snippet). — [arXiv:2601.04488](https://arxiv.org/abs/2601.04488)
- A spot-beam/OAM RIS prototype at 10.7 GHz with 2-bit phases and 300 PIN diodes driven by 11 MSP430 MCUs (arXiv:2407.19379). Per a snippet, it takes about 15.4 ms to cycle all codebooks, assuming 1 ms per codebook, and LabVIEW/MATLAB processing adds visible delays. The abstract page gives no latency number, so the timing is UNVERIFIED (snippet). — [arXiv:2407.19379](https://arxiv.org/abs/2407.19379)
- A 16×16 PIN-diode RIS tile (Advanced Electronic Materials, 2026, repository copy) reports an FPGA-controlled update time below 0.1 ms. UNVERIFIED: repository record only, and I could not identify title or DOI. — [repository.adu.ac.ae](https://repository.adu.ac.ae/bitstreams/40fec506-031e-43b9-9b57-04727f594feb/download)
- Liquid-crystal RIS. LiquiRIS (Abanto-Leon, Neuder, Ahmed, Jimenez Saez, Jamali, Asadi; IEEE WoWMoM 2026) measures reconfiguration time on a 120-cell LC-RIS and reports "up to 71.61%" reduction in overall reconfiguration time against conventional schemes. The abstract gives no absolute ms values. — [arXiv:2410.21506](https://arxiv.org/abs/2410.21506). A companion modeling paper finds a larger phase-shift range shortens LC reconfiguration time (snippet) — [arXiv:2504.08352](https://arxiv.org/abs/2504.08352). A TU Delft thesis reports about 0.35 ms per unit cell, or about 35 ms per array refresh for 100 elements. UNVERIFIED (snippet, thesis). — [TU Delft repository](https://repository.tudelft.nl/file/File_3230d9cd-4300-4e09-97a6-3c769a929a55?preview=1)
- Textbook figures (TU Berlin CommIT): PIN-diode switching under 1 µs, with about 10 µs cited in a controller-pipeline context. These are not measured prototype data. — [CommIT, Practical Limitations](https://commit-web.commit.tu-berlin.de/en/book/telecom/chapter/ch28/section/s05)
- "FPGA-accelerated deep learning for RIS configuration" (HTEC industry blog). Marketing, not peer-reviewed; omit or treat as UNVERIFIED. — [htec.com](https://htec.com/?p=21156)

### Inferences
- For the thesis, the hardware switching time of a PIN RIS (µs) is small compared with the optimizer compute times this project measures (ms). Under mobility, the compute latency of the phase optimizer, not the surface's switching time, is likely the dominant term in the staleness budget. LC-RIS is the exception, since its tens of ms per refresh are comparable to or larger than optimizer latency. This ordering is an inference from the figures above.
- Serial shift-register or MCU control and host-side MATLAB/LabVIEW loops add ms-scale overhead in several prototypes. "Controller latency" in prototypes is often dominated by the control path, not the diode.

### Gaps
- I found no prototype that reports a measured end-to-end loop (CSI acquisition, optimizer, phase update, steady state) together with the optimizer's own wall-clock time.
- I did not retrieve switching times for widely cited prototypes such as Pei et al. 2021 (1100-element RIS) or Trichopoulos et al.: UNVERIFIED and absent here.
- I found no GPU/NPU latency reports specific to an RIS phase optimizer.

## Q4. Results showing learned methods losing on wall-clock while winning per iteration

### Takeaway
I found no wireless paper that explicitly reports "wins per iteration, loses per millisecond". The closest wireless evidence is iteration-matched comparisons that never check wall-clock (Pellaco 2020). The general learned-optimizer literature states plainly that learned optimizers had historically not shown wall-clock speedups over tuned hand-designed ones.

### Cited Findings
- Metz et al., "Understanding and correcting pathologies in the training of learned optimizers", ICML 2019 (PMLR v97). Abstract: learned optimizers "have yet to demonstrate wall-clock speedups over hand-designed optimizers". The authors report one CNN-training case reaching target loss in about one fifth of the wall-clock time of tuned first-order methods. This is ML training, not wireless. — [arXiv:1810.10180](https://arxiv.org/abs/1810.10180); [PMLR](https://proceedings.mlr.press/v97/metz19a.html)
- Pellaco et al. 2020 compare unfolded and classical WMMSE at equal iteration count only (see Q2). — [arXiv:2006.08448](https://arxiv.org/abs/2006.08448)
- DeepFP: the classical WMMSE-SC baseline attains higher rate (the snippet table shows about 103% against DeepFP's 98.9%) while being slower. This is a rate–time trade-off, not a per-iteration-vs-wall-clock reversal. UNVERIFIED (snippet). — [arXiv:2601.02822](https://arxiv.org/abs/2601.02822)
- Per a search snippet, one MIMO detection paper notes NN detectors cost 5× to over 100× the runtime of LMMSE. Source attribution is UNVERIFIED (search result set included [arXiv:2212.07816](https://arxiv.org/abs/2212.07816), but I did not confirm it is that paper).

### Inferences
- If the thesis result holds (the learned update rule gains per step, but one learned step costs about 2.7 Adam steps and loses per ms at every budget), it is a rarely reported negative result in wireless. It matches the general warning from Metz et al. that per-step gains of learned optimizers do not translate automatically into wall-clock gains.
- Because the literature mostly reports iteration-matched or converged-baseline comparisons, publication bias toward "unfolding is faster" is plausible. This is an inference and was not measured.

### Gaps
- I found no wireless or RIS paper that explicitly reports a per-iteration win turning into a wall-clock loss. A deeper full-text search of unfolding papers' runtime tables would be needed to confirm none exists.

## Q5. O-RAN near-RT/real-time control loop timing relevant to RIS control

### Takeaway
O-RAN timescales are standard. The non-RT RIC (rApps) runs above 1 s, the near-RT RIC (xApps) runs 10 ms to 1 s, and real-time control below 10 ms (beam management) falls outside the RICs, which motivates DU/CU-hosted dApps (measured loops under 450 µs). RIS-over-O-RAN work places RIS control as xApps (near-RT) or as a two-timescale plan. None of it reports a measured RIS optimizer-to-phase-update loop time.

### Cited Findings
- Near-RT RIC xApps operate on the 10 ms–1 s timescale and non-RT rApps above 1 s. Beam management needs real-time timescales below 10 ms. I/Q-based beam management over E2 exceeds the 10 ms required. — [Lacava et al., dApps: Enabling Real-Time AI-Based Open RAN Control, arXiv:2501.16502](https://arxiv.org/abs/2501.16502) (Computer Networks 2025, per page note)
- dApps run at the DU/CU and achieve control loops under 450 µs in the cited prototype. — [arXiv:2501.16502](https://arxiv.org/abs/2501.16502); original dApps concept: [D'Oro et al., arXiv:2203.02370](https://arxiv.org/abs/2203.02370)
- O-RAN nGRG research report RR-2024-10, "dApps for Real-Time RAN Control: Use Cases and Requirements". It is non-normative, lists beam management as a use case, and notes sub-ms closed-loop latency in an open-source prototype. — [O-RAN nGRG RR-2024-10 (PDF)](https://mediastorage.o-ran.org/ngrg-rr/nGRG-RR-2024-10-dApp%20use%20cases%20and%20requirements.pdf); [dApp architecture report](https://www.o-ran.org/research-reports/dapp-architecture-and-interfaces)
- RIS control as near-RT RIC xApps over E2 with an RIS service model, validated with the GoSimRIS simulator (Ksentini et al., EURECOM; IEEE letter). Venue/DOI UNVERIFIED. — [EURECOM record](https://www.eurecom.fr/en/node/4900116)
- "RIS Meets O-RAN": a multi-user RIS optimization xApp demonstrated on an OpenAirInterface O-RAN testbed (EuCNC 2025 per snippet). — [arXiv:2501.18917](https://arxiv.org/abs/2501.18917)
- DARIO: a two-timescale O-RAN orchestrator in which non-RT computes UE–RIS association and RB plans, near-RT xApps enforce scheduling, and RIS controllers apply precomputed phase states. — [TU Berlin TechRxiv PDF (Drummond et al. 2024)](https://www.tkn.tu-berlin.de/bib/drummond2024empowering-techrxiv/drummond2024empowering-techrxiv.pdf) (venue UNVERIFIED)
- RIS-enabled Open RAN on the Colosseum emulator (Tsampazi et al., "O-RIS-ing") — [TU Berlin PDF](https://www.tkn.tu-berlin.de/bib/tsampazi2025o-ris-ing/tsampazi2025o-ris-ing.pdf) (venue UNVERIFIED); RIS control through stochastic network calculus in O-RAN — [arXiv:2502.18753](https://arxiv.org/abs/2502.18753) (snippet only)

### Inferences
- An RIS phase optimizer whose wall-clock is a few to tens of ms fits only the near-RT RIC (10 ms–1 s) or a dApp at the edge of its budget. Per-slot (sub-ms) RIS reconfiguration would need dApp or DU placement and a sub-ms optimizer. The ms-scale optimizer latencies the thesis measures map directly onto this O-RAN placement question, which is an argument for the thesis framing.
- Any optimizer hosted in the near-RT RIC also carries E2 transport latency on top of compute. Total staleness = E2 + compute + RIS switching, and the compute term is the one the thesis controls.

### Gaps
- I found no measured end-to-end RIS xApp/dApp loop latency (CSI to xApp to E2 to RIS controller to phase applied).
- I did not consult the normative O-RAN WG2/WG3 specs directly. The 10 ms–1 s figure comes from research papers that summarize them.
