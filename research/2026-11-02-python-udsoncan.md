# python-udsoncan — 2026-11-02

Discovery: recursive GitHub-first follow-up from python-can-isotp. YouTube transcript evidence unavailable; no attribution to playlist content.

Upstream: https://github.com/pylessard/python-udsoncan (Pier-Yves Lessard). License: MIT, LICENSE.txt copyright 2017. No code copied.

Evidence inspected: README.rst, setup.py, LICENSE.txt, Jenkinsfile, top-level udsoncan/ and test/ trees, GitHub release v1.26.1 (2026-06-25), master commit 07d7be1 (2026-10-26). Jenkinsfile configures Python 3.7–3.13 testing, but a passing Jenkins execution was **not** confirmed. GitHub Actions reports zero runs. No local installation or ECU/CAN testing.

Components: udsoncan/client.py (client), connections.py (transports), services/ (UDS service codecs), Request.py and Response.py (message models), j2534.py (adapter), test/client/ and test/test_connection.py (fixtures). Setup declares Python >=3.7; SocketCAN example depends on Linux and an ISO-TP transport.

Gold: VERIFIED (upstream source/release evidence only), A24 = 5 utility + 3 working evidence + 5 reusability + 4 novelty + 4 documentation + 3 maintenance. Do not imply a confirmed CI pass.

Caveat: README demonstrates session change, security access, data writing and ECU reset; these are potentially state-changing actions. Test only with mocked/simulated or expressly authorized equipment. MIT notices must be retained for copies.

Next: verify mocked request/response round trips and negative-response handling; check compatibility against stable python-can-isotp and Python versions; investigate J2534 dependencies and supported OS.
