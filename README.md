# vmbi
This uses a master inventory list of assets and verifies whether that asset appears in a vulnerability scan report (e.g. Tenable Nessus scan report).  The purpose is to report on whether an asset is reachable by the vulnerability scanner and regularly scanned.

It should result in a data frame per below:

<pre>
Asset, Scan Date 1, Scan Date 2, Scan Date 3
HOSTNAME1, TRUE, FALSE, TRUE
HOSTNAME2, TRUE, TRUE, TRUE
HOSTNAME3, FALSE, FALSE, FALSE
</pre>
