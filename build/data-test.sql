COPY piggybank(name, broken) FROM stdin;
cochon	FALSE
lapin	FALSE
nounours	TRUE
hippo	FALSE
\.

COPY wealth(piggybank_id, change_id) FROM stdin;
1	7
1	7
1	7
1	7
1	7
1	7
1	12
1	12
4	1
4	2
4	3
4	13
4	13
\.
