# PROCESS.md
14 операций: desulfurization, softening, mg_rejection_ec, evaporation_concentration,
dle_sorption_li, dle_solvent_extraction_li, dle_electrodialysis_li, nf_membrane,
ro_concentration, electrochemical_br, precipitation_sr, k_recovery, b_recovery,
li_carbonate_finish. Каждая — прозрачная корреляция, привязана к источнику
(см. docstring и LITERATURE.md). Recovery DLE штрафуется высоким Mg/Li.
