# RIS standardization status and wideband channel models for RIS-OFDM evaluation (2021–2026)

Research date: 2026-11-16. Primary documents were read in full text where noted ("read in full"). Anything not verified against a primary source is marked UNVERIFIED.

## Q1. What do ETSI GR RIS documents specify or recommend on reconfiguration time, control latency and evaluation methodology?

### Takeaway
ETSI ISG RIS has published informative Group Reports only (GR RIS 001–005). None of them sets a normative reconfiguration-time number. They give example ranges: reconfiguration rate from "below 1 ms" (up to symbol-level) to "quasi-static, above tens of seconds"; reconfiguration latency "compatible with the scheduler"; and, in GR RIS 004, total RIS system delay "less than 1 ms" for FR1 at 15 kHz SCS. GR RIS 003 defines "RIS control plane latency" as an evaluation KPI. It says system-level simulators should model the latency of setting RIS coefficients with "one suitable parameter". Its own link model assumes one RIS state applies to all subcarriers in a band, i.e. it is frequency-flat per element.

### Cited Findings
**Document set and versions**
- ISG RIS was set up in September 2021. First-phase reports: GR RIS 001 (use cases, deployment scenarios, requirements), GR RIS 002 (technological challenges, architecture, standards impact) and GR RIS 003 (communication models, channel models, channel estimation, evaluation methodology) — [ETSI ISG RIS activity report](https://www.etsi.org/committee-activity/activity-report-ris); [TelecomTV on GR RIS 001](https://www.telecomtv.com/content/6g/etsi-releases-first-report-on-reconfigurable-intelligent-surfaces-communication-and-channel-models-48068/)
- On 25 April 2025 ETSI announced GR RIS 004 V1.1.1 ("Implementation and Practical Considerations") and GR RIS 005 V1.1.1 ("Diversity and Multiplexing of RIS-aided Communications"), plus updated GR RIS 001/002/003 at V1.2.1 — [ETSI press release, 25 Apr 2025](https://www.etsi.org/newsroom/news/2522-etsi-releases-new-reports-on-reconfigurable-intelligent-surfaces/). The V1.2.1 version numbers come from the URLs on that page.
- Versions read in full for these notes: GR RIS 001 V1.1.1 (2023-04), GR RIS 002 V1.2.1 (2025-02), GR RIS 003 V1.1.1 (2023-06), GR RIS 004 V1.1.1 (2025-03) — [GR RIS 003 V1.1.1 PDF](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf); [GR RIS 001 V1.1.1 PDF](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/001/01.01.01_60/gr_RIS001v010101p.pdf); [GR RIS 002 V1.2.1 PDF](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/002/01.02.01_60/gr_RIS002v010201p.pdf); [GR RIS 004 V1.1.1 PDF](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf)
- UNVERIFIED: I could not download GR RIS 001 V1.2.1, GR RIS 003 V1.2.1 or GR RIS 005 V1.1.1 (the ETSI server returned an HTML page). The GR RIS 001/003 quotes below come from the V1.1.1 texts and may have changed in V1.2.1. I found no evidence of a GR RIS 006 or later report, or of any normative ETSI GS.

**Reconfiguration time and rate (GR RIS 001 V1.1.1, clause 7.4, Table 7.4-1)**
- "Reconfigurability rate identifies the time from one triggered configuration to the next one. It can range between being very high, e.g. below 1 ms, and very slow or quasi-static, e.g. above tens of seconds." — [GR RIS 001 V1.1.1 §7.4](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/001/01.01.01_60/gr_RIS001v010101p.pdf)
- Example values in Table 7.4-1 (GR RIS 001 V1.1.1):
  - Configuration flexibility: 1–3 bits phase granularity.
  - Reconfiguration rate: "ranging from quasi-static configuration to symbol-level reconfiguring rate".
  - Reconfiguration latency: "Compatible with the scheduler" ("the delay of applying RIS configuration").
  - Codebook size: 16 (4 bits) as an example.
  - Independently configurable elements: "10 s to more than 1 000", and groups such as column-wise configuration are possible.
  - Source: [GR RIS 001 V1.1.1](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/001/01.01.01_60/gr_RIS001v010101p.pdf)

**Hardware switching speed and total system delay (GR RIS 004 V1.1.1)**
- Unit-cell switching must be fast enough for TDD multi-user operation. Switching is "typically in the region of nanoseconds" for varactors, PIN diodes and FETs, but "in the region of milliseconds" for liquid crystals and MEMS — [GR RIS 004 V1.1.1 §4.x](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf)
- GR RIS 004 writes the total system delay T_T as a sum of terms: switching delay, microcontroller delay (including rise/fall), DAC delay (analogue RIS), the per-logic-gate delays of the M chained logic elements, and per-path propagation delays. Experimentally, T_T is "largely dominated by" the DAC delay in an analogue RIS, so digital RIS switch faster. The requirement "will be dictated by... the 5G NR frame structure". Example: "Assuming FR1 frequency band and 15 kHz SCS, the T_T should be less than 1 ms to prevent packet loss during UE movement." — [GR RIS 004 V1.1.1](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf)
- Serially daisy-chained shift registers make refresh latency grow with RIS size. Row-parallel control, e.g. on an FPGA, gives higher refresh rates — [GR RIS 004 V1.1.1 §4.7.3](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf)

**Control signalling (GR RIS 002 V1.2.1, §7.2)**
- For a 5G network-controlled RIS, existing NR channels can be reused. PDCCH carries dynamic RIS control for one or more RIS. PDSCH carries semi-static/static control with higher-layer configuration. PUSCH/PUCCH carry assistance information such as ACK/NACK and status. Private, non-standardized interfaces are also possible. For a UE-controlled RIS, the options are the Uu air interface or PC5 — [GR RIS 002 V1.2.1 §7.2.2](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/002/01.02.01_60/gr_RIS002v010201p.pdf)
- RIS slot configuration can mirror NR cell-specific and UE-specific TDD UL/DL configuration. The controlling-mode indication (network-controlled, UE-controlled or quasi-autonomous) is "typically not expected to change frequently". The report also notes that "latency and communication overheads of the dynamic RIS control" are a design trade-off — [GR RIS 002 V1.2.1 §7.2.1](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/002/01.02.01_60/gr_RIS002v010201p.pdf)
- Channel measurement timescales: for a facade-mounted fixed RIS, the RIS–BS channel is semi-static and can be measured at longer intervals, while the RIS–UE channel has a shorter coherence time and needs shorter periodicity. A RIS on a train or UAV makes both hops dynamic. Sub-surface-based configuration is suggested for "reduced overhead and low-latency channel measurements" in dynamic scenarios — [GR RIS 002 V1.2.1 §7.3](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/002/01.02.01_60/gr_RIS002v010201p.pdf)

**Evaluation methodology (GR RIS 003 V1.1.1, clauses 6–8 and annex example)**
- KPI clause 8.1.6 defines latency from two perspectives. The first is user-plane latency (end-to-end BS↔UE through the RIS). The second is "RIS control plane latency", "the time duration to (re-)select and (re-)configure RIS, which can be evaluated for different RIS control plane protocols". Overhead (§8.1.8) explicitly "includes the signalling to (re)select, enable, (re-)configure, and control RIS" — [GR RIS 003 V1.1.1 §8.1.6, §8.1.8](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- System-level simulation guidance: "RIS deployment scenarios can have different latency in setting RIS beamforming coefficients, which should be modeled by one suitable parameter in system-level simulations." For near-field, arrays can be split into sub-arrays with spherical wavefronts between sub-arrays and plane waves within each — [GR RIS 003 V1.1.1 §8.x](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- Frequency-flat element assumption: the exemplary system model in §7.2.2.1 uses "a narrowband system, i.e. a subcarrier of an OFDM system". A RIS element state "is assumed to be applicable to all sub-carriers within a certain bandwidth" — [GR RIS 003 V1.1.1 §7.2.2.1](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- Per-hop channel models: GR RIS 003 Table 1 reuses TR 38.901 (V16.1.0) for each hop. BS–RIS uses UMa/UMi or InH/InF/LOS, and RIS–UE uses InH/InF/LOS or UMa/UMi. A "pure LOS channel model is applicable" when the RIS–UE or BS–RIS distance is very small — [GR RIS 003 V1.1.1 §6.2, Table 1](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- Worked link-budget example (Tables 6–7) — [GR RIS 003 V1.1.1 Tables 6–7](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf):
  - Link setup: 28 GHz, 120 kHz SCS, 50 RB (72 MHz), DFT-s-OFDM uplink, 14-symbol PUSCH, 1-symbol DMRS Type A / type 1, MCS 3, practical channel estimation.
  - UE–BS link: CDL-A with 300 ns DS.
  - UE–RIS hop: CDL-E with 30 ns DS (or LOS) and 77.78 Hz Doppler (3 km/h).
  - RIS–BS hop: CDL-A with 300 ns DS, or CDL-E with 30 ns DS.
  - Result: 900 elements (16.1 cm × 16.1 cm) meet the 5 Mbps UL target.
- GR RIS 003 also covers near-field regimes (§5.2.2), near-field path loss (§6.3.1.3), an empirical channel model (§6.4) and channel estimation for unstructured and structured models (§7.3–7.4). These include element-wise, sub-surface and codebook-based estimation, and two-timescale designs where the RIS phase "can be updated at a much lower rate than the fast fading fluctuations" — [GR RIS 003 V1.1.1](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)

### Inferences
- The ETSI documents treat reconfiguration latency as a parameter to model and report, not as a fixed number. A thesis that models control latency explicitly and studies how it changes method rankings fits the methodology GR RIS 003 asks for. The "<1 ms at 15 kHz SCS" figure in GR RIS 004 is the most concrete ETSI number: about one slot at μ=0. It is an example, not a requirement.
- The per-element, frequency-flat assumption in GR RIS 003 (one state for all subcarriers) matches a standard RIS-OFDM evaluation model. Frequency-dependent unit-cell responses fall outside that baseline and would have to be argued separately.

### Gaps
- I could not read the contents of GR RIS 001/003 V1.2.1 or GR RIS 005 V1.1.1 (download blocked), so 2025 changes to reconfiguration-time wording are UNVERIFIED.
- ISG RIS term extension or a third phase after 2025: no source found.

## Q2. Is RIS in 3GPP Rel-19/Rel-20 work items? What happened with NCR, and what control timing does NCR assume?

### Takeaway
RIS has no 3GPP study or work item in Rel-18 or Rel-19. In the Rel-20 6G study (FS_6G_Radio, TR 38.760-x), I found no evidence that RIS has been adopted as of late 2026. It appears only in advocacy contributions. NCR was studied in Rel-18 (TR 38.867) and specified in Rel-18 (WI NR_netcon_repeater, RF in TS 38.106). NCR control uses side-control information over the Uu interface (NCR-MT). Beam and ON/OFF indications are given per time resource at slot or symbol granularity. Forwarding is analog with a latency on the order of tens of ns.

### Cited Findings
- RIS was proposed for Rel-18 and again for Rel-19, but "in both releases, it has been decided not to continue with it as a study-item, and to leave it for possible future specification" — [arXiv:2404.04753, RIS in Cellular Networks – Challenges and Issues](https://arxiv.org/abs/2404.04753)
- "RIS has been excluded from 3GPP Rel-19 and is unlikely to be incorporated into 5G-Advanced". The same survey says Rel-20 "may serve as the final opportunity for RIS" for 6G — [arXiv:2506.19526 (2025 survey)](https://arxiv.org/pdf/2506.19526). This is a secondary source.
- During the Rel-18 NCR study definition there were discussions about including RIS: "it was decided not to include and leave them for possible future releases" — [arXiv:2403.09601, Carvalho et al., "Network-Controlled Repeater – An Introduction", 2024](https://arxiv.org/pdf/2403.09601)
- Rel-18 "Core: NR network-controlled repeaters" is listed among the Rel-18 items closed at RAN#102 (Dec 2023) — [5G-PPP standards tracker, RAN#102 summary](https://standards-tracker.5g-ppp.eu/node/433). A RAN#102 WI summary is RP-232884 — [3GPP draft RP-232884](https://www.3gpp.org/ftp/Email_Discussions/RAN2/%5BRAN2%23124%5D/StatusReports%20for%20RAN%23102/R18%20WI%20NCR/Draft%20RP-232884%20WI%20summary%20for%20NR%20network-controlled%20repeaters_v2.docx) (not opened).
- NCR study TR 38.867 v18.0.0 (Sep 2022) and RF spec TS 38.106 (Mar 2023 version) are cited in [arXiv:2403.09601](https://arxiv.org/pdf/2403.09601). UNVERIFIED: the exact current TS 38.106 title and version.
- NCR architecture and control, from [arXiv:2403.09601](https://arxiv.org/pdf/2403.09601):
  - NCR = NCR-MT plus NCR-Fwd. The NCR-MT receives side control information (SCI) from the gNB over the NR Uu "control link".
  - The Rel-18 WI "mainly focused on specifying the signaling of the SCI for controlling the NCR-Fwd behavior related to beamforming, UL-DL TDD operation and ON-OFF configuration".
  - The NCR is OFF by default and goes ON "only in the time resources with an access link beam indication".
  - "Both slot- and symbol-level granularities are feasible for the time-domain resource indication and determination of the access link beam."
  - Access-link beams can be periodic, semi-persistent or dynamic. Dynamic beams are indicated "as pairs of beam and time resource indices, where the full set of time resources is preconfigured by RRC".
  - "NCRs do not support dynamic TDD".
  - Forwarding is analog, "implying a latency in the order of tens of nanoseconds".
  - The NCR is transparent to the UE.
- NCR-Fwd backhaul-link DL/UL timing follows the NCR-MT's DL/UL frame timing (Rel-18 WI summary, as reported in search results) — [3GPP draft RP-232884](https://www.3gpp.org/ftp/Email_Discussions/RAN2/%5BRAN2%23124%5D/StatusReports%20for%20RAN%23102/R18%20WI%20NCR/Draft%20RP-232884%20WI%20summary%20for%20NR%20network-controlled%20repeaters_v2.docx). UNVERIFIED: not opened directly.
- RAN1#110 (2022) discussed indicating a starting time unit and duration for each beam — [RAN1#110 FL summary 9.8.1 (draft)](https://3gpp.org/ftp/TSG_RAN/WG1_RL1/TSGR1_110/Inbox/drafts/9.8(FS_NR_netcon_repeater)/9.8.1/R1-220xxxx%20FL%20Summary%20of%209.8.1%20on%20Side%20control%20information%20to%20enable%20NCR_v012_CMCC_CTC.docx). Not opened.
- Rel-20 6G study, from [ATIS 3GPP Rel-20 webinar slides, April 2026](https://cdn.atis.org/atis.org/2026/04/16110914/Combined-Slides_3GPP-Webinar-R20_2026.pdf):
  - "Study on 6G Radio" FS_6G_Radio, UID 1080072, lead WG RAN1, target June 2027, 19% complete, WID RP-260282.
  - TRs: 38.960 (RANP), 38.760-1 (RAN1), 38.760-2/-3/-4 (RAN2/3/4).
  - RAN1 interim assessment due at TSG#112 (June 2026) on waveform, numerology, frame structure and bandwidth.
  - 6G KPIs: control-plane latency 20 ms; user-plane latency 4 ms for immersive communication and 1 ms for HRLLC.
  - 6G supports a 3 MHz minimum allocation with 15 kHz SCS.
  - The slides do not mention RIS or repeaters (text search for "RIS", "reconfigurable intelligent" and "repeater" found nothing).
  - The slides label RP-251881 as the 6G study ("FS_6G_RAN_Scen_Req"), which conflicts with the WID RP-260282 / RP-251395 listing on the same slides; the document numbering is inconsistent in the source.
- At RAN#108 (Prague, 9–13 June 2025, where the 6G SID was finalized), more than 30 member organizations led or co-signed 15 RIS-related contributions urging RIS inclusion. This is an advocacy article, so it does not show adoption — [C114 article, 23 Jun 2025](https://m.c114.com.cn/w2934-1291593.html)
- Rel-20 also contains 5G-Advanced items. A Rel-20 overview paper does not list RIS or NCR enhancements (text search for "RIS" and "repeater" found nothing) — [arXiv:2506.11828, "A Tale of Two Mobile Generations"](https://arxiv.org/pdf/2506.11828)

### Inferences
- As of Nov 2026, RIS has no 3GPP normative or study-item status. The closest standardized analogue is the Rel-18 NCR. Its control model is gNB-scheduled, slot- or symbol-granular beam/ON-OFF indication via SCI, with RRC-preconfigured time resources. That model is a reasonable template for "controlled-RIS reconfiguration at slot granularity" in a thesis model.
- The 6G CP latency KPI (20 ms) and UP latency (1 ms HRLLC) give an outer envelope. RIS reconfiguration plus computation that must finish within one slot (1 ms at 15 kHz, 0.125 ms at 120 kHz) is much tighter.

### Gaps
- NCR beam-application time or SCI processing delay (minimum k-offset between DCI and the forwarding beam): not found in a primary source. TS 38.213 NCR clause content is UNVERIFIED.
- Rel-19 NCR enhancement WI: not found. Whether any exists is UNVERIFIED.
- RAN1#124–#126-bis agreements on RIS in TR 38.760-1: not checked. The chair-notes download returned HTML.

## Q3. Which papers extend 38.901 to RIS (cascaded models) and give wideband/delay-domain parameters?

### Takeaway
The usual approach, which ETSI GR RIS 003 also endorses, is to model each hop with a 38.901 GBSM/CDL (BS–RIS, RIS–UE) and cascade them. In the delay domain this is a convolution of the two hops' cluster delays. TR 38.901 itself has no RIS clause up to V19.x. Explicit 38.901-framework RIS extensions with delay modelling exist mainly in arXiv/IEEE work, for example arXiv:2412.07356 (convolutional cascaded GBSM, measured at 6.9 GHz) and the SimRIS line (Basar & Yildirim).

### Cited Findings
- Each RIS hop (BS–RIS, RIS–UE, RIS–RIS) can be modelled with existing TR 38.901 scenario models, as tabulated in GR RIS 003 Table 1 — [ETSI GR RIS 003 V1.1.1 §6.2](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- arXiv:2412.07356 "Cascaded channel modeling and experimental validation for RIS assisted communication system" — [arXiv:2412.07356](https://arxiv.org/abs/2412.07356):
  - Extends a 3GPP-framework GBSM with a convolutional form to describe how sub-channel multipaths cascade (angles, delays, powers from the GBSM).
  - Validated by a 6.9 GHz factory measurement of the Tx–RIS–Rx channel and of each sub-channel.
  - UNVERIFIED: measurement bandwidth.
- arXiv:2412.07336 argues that the 3GPP GBSM needs extension for RIS, and identifies Tx–RIS and RIS–Rx coupling as an open modelling challenge — [arXiv:2412.07336](https://arxiv.org/pdf/2412.07336v2)
- I. Yildirim, E. Basar, "Channel Modeling in RIS Empowered Wireless Communications", in *Intelligent Reconfigurable Surfaces (IRS) for Prospective 6G Wireless Networks*, Wiley-IEEE, 2023, pp. 123–148, doi:10.1002/9781119875284.ch7 (cited as [i.13] in GR RIS 003) — [GR RIS 003 references](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- System-level RIS simulation methodology for industry standards (3GPP-style SLS with RIS) — [arXiv:2409.13405](https://arxiv.org/pdf/2409.13405). Not opened in detail.
- System-level comparison of IAB, NCR and RIS for densification — [arXiv:2410.02415](https://arxiv.org/pdf/2410.02415). Not opened in detail.
- Comparison between NCR and RIS — [arXiv:2211.06974](https://arxiv.org/pdf/2211.06974). Not opened in detail.
- TR 38.901 large-bandwidth/large-array modelling (§7.6.2) applies "only when the bandwidth B is greater than c/D Hz", where D is the maximum antenna aperture. Rays then get individual TOAs per antenna pair. This is relevant for electrically large RIS or wideband cases: for D = 0.5 m, c/D = 600 MHz — [ETSI TR 138 901 V16.1.0 §7.6.2](https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/16.01.00_60/tr_138901v160100p.pdf). The numeric example is my own computation.
- Rel-19 7–24 GHz (FR3) validation of TR 38.901 covers the stochastic channel model only — [arXiv:2603.25927](https://arxiv.org/pdf/2603.25927); see also [arXiv:2602.07623](https://arxiv.org/pdf/2602.07623v1). A draft TR 38.901 V19.x exists — [3GPP draft 38.901 j20](https://www.3gpp.org/ftp/tsg_ran/WG1_Rl1/DRAFT/Draft_versions/draft_38901-j20.docx). A search summary reported that its table of contents has no RIS clause; I did not verify this directly.
- Near-field: GR RIS 003 §5.2.2 covers near-field regimes and multipath/single-path near-field models, including a Fresnel approximation for spherical wavefronts, and near-field path loss in §6.3.1.3 — [GR RIS 003 V1.1.1](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)

### Inferences
- In a cascaded CDL/TDL model, the effective RIS-path delay spread is roughly the combination of both hops' spreads (convolution of power-delay profiles). The RIS path is therefore more frequency-selective than either hop alone. With one frequency-flat phase vector applied across all subcarriers (the GR RIS 003 assumption), wideband phase design is a compromise across subcarriers. This is the point a wideband RIS-OFDM experiment should quantify.

### Gaps
- No peer-reviewed paper was found, within this budget, that publishes a full CDL-style table (cluster delays, powers, angles) specifically for the RIS cascaded channel. The measurement bandwidth and delay parameters of arXiv:2412.07356 are UNVERIFIED.
- Published wideband RIS channel measurements (e.g. RMS delay spread of RIS paths indoors): not collected here.

## Q4. Indoor office (InH) delay spreads in 38.901 and implied coherence bandwidths; NR numerology for pilot overhead and SCS

### Takeaway
TR 38.901 Table 7.5-6 (InH-Office) gives a median DS of about 20 ns (LOS) and 26–39 ns (NLOS, 28 GHz down to ≤6 GHz). The 90th percentile is about 34 ns (LOS) and 47–59 ns (NLOS). The CDL/TDL scaling table gives 10/30/100/300/1000 ns options. The informative indoor-office "normal" profile is 39 ns at 2 GHz and 20 ns at 28 GHz. Using Bc ≈ 1/(5·DS), the 50%-correlation coherence bandwidth indoors is about 5–10 MHz. That is roughly 25–50 RB-widths at 15 kHz, or 3–6 RBs at 120 kHz.

### Cited Findings
- InH-Office lgDS = log10(DS/1 s), from [ETSI TR 138 901 V16.1.0 (3GPP TR 38.901 v16.1.0), Table 7.5-6 Part-2](https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/16.01.00_60/tr_138901v160100p.pdf):
  - LOS: μ = −0.01·log10(1+fc) − 7.692, σ = 0.18.
  - NLOS: μ = −0.28·log10(1+fc) − 7.173, σ = 0.10·log10(1+fc) + 0.055.
  - fc is in GHz. NOTE 6: for InH below 6 GHz, use fc = 6 for frequency-dependent LSPs.
- CDL/TDL delay scaling (Table 7.7.3-1): very short 10 ns, short 30 ns, nominal 100 ns, long 300 ns, very long 1000 ns. Delays are scaled as τ_scaled = τ_model · DS_desired — [TR 38.901 V16.1.0 §7.7.3](https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/16.01.00_60/tr_138901v160100p.pdf)
- Table 7.7.3-2 (informative), indoor office DS_desired [ns], from [TR 38.901 V16.1.0 Table 7.7.3-2](https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/16.01.00_60/tr_138901v160100p.pdf):
  - Short profile: 20 (2 GHz), 16 (6–70 GHz).
  - Normal profile: 39 (2), 30 (6), 24 (15), 20 (28), 18 (39), 16 (60–70).
  - Long profile: 59 (2), 53 (6), 47 (15), 43 (28), 41 (39), 38 (60), 37 (70).
  - "Short" is the LOS median and "normal"/"long" are the NLOS median/90th percentile.
  - For comparison: UMi normal 129/93/66 ns at 2/6/28 GHz; UMa normal 363 ns at 2–6 GHz.
- GR RIS 003's RIS example uses CDL-E with 30 ns DS for the indoor UE–RIS hop and CDL-A with 300 ns for the outdoor hops — [GR RIS 003 V1.1.1 Table 7](https://etsi.org/deliver/etsi_gr/RIS/001_099/003/01.01.01_60/gr_ris003v010101p.pdf)
- 6G study: 3 MHz minimum allocation with 15 kHz SCS; numerology and frame structure under RAN1 study (interim June 2026) — [ATIS Rel-20 slides 2026](https://cdn.atis.org/atis.org/2026/04/16110914/Combined-Slides_3GPP-Webinar-R20_2026.pdf)
- GR RIS 004 points to the SCS table 5.3.2-1 of TS 38.101-1 for deriving RIS timing requirements per FR1/FR2 — [GR RIS 004 V1.1.1](https://www.etsi.org/deliver/etsi_gr/RIS/001_099/004/01.01.01_60/gr_ris004v010101p.pdf)
- NR numerology (3GPP TS 38.211 §4.2–4.3). UNVERIFIED in this session; standard values from the spec, not re-fetched:
  - Δf = 2^μ·15 kHz, with μ = 0…4 in Rel-15 and μ = 5, 6 (480/960 kHz) added in Rel-17 for FR2-2.
  - 14 OFDM symbols per slot with normal CP; extended CP only for μ = 2.
  - Slot length 1 ms / 2^μ: 15 kHz → 1 ms, 30 → 0.5 ms, 60 → 0.25 ms, 120 → 0.125 ms.
  - Normal CP ≈ 4.69 µs·2^−μ: 4.69 / 2.34 / 1.17 / 0.59 µs.
  - RB = 12 subcarriers.
  - DMRS Type 1: comb-2 (6 REs per RB per CDM group per symbol). Type 2: 4 REs per RB per CDM group. 1–4 DMRS symbols per slot.
  - A source to cite is [ETSI TS 138 211](https://www.etsi.org/deliver/etsi_ts/138200_138299/138211/), version still to be fixed.

**Computed values**

These are my own calculations (script-free arithmetic; reproduce before citing). Medians and percentiles come from the Table 7.5-6 lognormal; Bc uses the textbook rules of thumb Bc,0.5 ≈ 1/(5·DS) and Bc,0.9 ≈ 1/(50·DS).

| InH-Office case | Median DS | 90th pct DS | Bc,0.5 | Bc,0.9 |
|---|---|---|---|---|
| LOS, fc ≤ 6 GHz | 19.9 ns | 33.9 ns | ≈ 10 MHz | ≈ 1.0 MHz |
| NLOS, fc ≤ 6 GHz | 38.9 ns | 58.8 ns | ≈ 5.1 MHz | ≈ 0.51 MHz |
| LOS, 28 GHz | 19.7 ns | 33.4 ns | ≈ 10.2 MHz | — |
| NLOS, 28 GHz | 26.2 ns | 47.4 ns | ≈ 7.6 MHz | — |

For the CDL scaling options, Bc,0.5 = 20 / 6.7 / 2 / 0.67 MHz for DS = 10 / 30 / 100 / 300 ns.

### Inferences
- The tabulated 6 GHz "normal" indoor value (30 ns) does not match the median computed from Table 7.5-6 with fc = 6 (38.9 ns), while the 2 GHz value (39 ns) does. Table 7.7.3-2 is probably not consistently using the fc = 6 floor. Cite whichever formula is actually used and state fc.
- All InH CPs (≥ 0.59 µs at 120 kHz) are far above InH delay spreads (tens of ns, about 60 ns at the 90th percentile). Even the 300 ns CDL-A outdoor hop fits inside the 15/30 kHz CP, so ISI is not the issue in RIS-OFDM indoor evaluations. Frequency selectivity across the band is.
- Pilot density: with Bc,0.5 ≈ 5–10 MHz indoors, comb-2 DMRS (every other subcarrier) is heavily oversampled in frequency. The relevant RIS overhead is the number of pilot symbols needed to resolve the N-element cascaded channel, which scales with N or with the number of sub-surfaces (GR RIS 003 §7.3). That count is multiplied by symbol length, which shrinks by 2^μ.
- If the RIS must reconfigure within one slot, the budget is 1 ms at μ=0 and 0.125 ms at μ=3. That is the frame for any "computation latency as a first-class constraint" argument.

### Gaps
- TS 38.211 numerology and DMRS facts were not re-fetched in this session. Verify the clause and version before quoting.
- Coherence bandwidth rules of thumb (1/(5·DS), 1/(50·DS)) are textbook approximations (Rappaport, *Wireless Communications*) and were not re-verified here. The exact Bc depends on the PDP shape. For the thesis, compute it from the actual CDL PDP with a script.
- InH cluster counts and per-cluster DS (Table 7.5-6: InH LOS 15 clusters, NLOS 19, c_DS) were not extracted. UNVERIFIED.
