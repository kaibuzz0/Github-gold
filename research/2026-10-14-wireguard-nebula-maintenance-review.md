# GitHub Gold: networking evidence refresh (2026-10-14)

## Scope
Repository-native follow-up to the existing wireguard-go and Nebula dossiers. Evidence levels below refer to upstream artifacts, not independent execution.

## WireGuard/wireguard-go
- Upstream: https://github.com/WireGuard/wireguard-go
- Evidence: VERIFIED (upstream), provisional S / 28.
- MIT-style root license, notice retention required.
- Go module specifies Go 1.23.1. Reusable modules include device/, conn/, tun/, ipc/, replay/, ratelimiter/, rwcancel/, tai64n/ and tests/.
- The latest inspected upstream commit on 2026-10-06 fixes a handshake-response state issue (2631ce99). A 2026-05-22 commit fixes Linux TUN header state in GRO processing.
- The official README recommends kernel WireGuard for Linux when available.

## slackhq/nebula
- Upstream: https://github.com/slackhq/nebula
- Evidence: VERIFIED (upstream), provisional S / 28.
- Root MIT license; Go module specifies Go 1.26.0.
- Latest inspected stable release v1.11.2, published 2026-09-22.
- Upstream commits on 2026-10-13 address macOS/BSD route correctness.
- Reusable components include lighthouse.go, handshake/, firewall.go, cert/, cmd/, punchy.go, hostmap.go, overlay/ and e2e/.
- CI includes test.yml and smoke workflows. Separate mobile clients need separate licensing review.

## Boundaries and next actions
Neither project was independently built, deployed, benchmarked, or security-audited. No third-party implementation code was copied. Keep both candidates queued until MASTER_LIST.md, catalog/tools.json and catalog/candidate_queue.json can be synchronized. Next inspect Tailscale's WireGuard fork divergence and Nebula's lighthouse and certificate lifecycle.
