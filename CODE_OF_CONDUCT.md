# Code of Conduct

## Pledge

Everyone contributing here agrees to three things:

- **Accurate.** A number is a measurement, not an opinion. When something is
  wrong, say so and point at the run that shows it.
- **Traceable.** A benchmark result comes with the script, the settings and the
  hardware. "It felt faster" is not a contribution.
- **Authorised.** The security tools in this repository run against your own
  machine only. A pull request that removes the loopback rail, or adds a target
  that is not self-hosted and deliberately vulnerable, is rejected.

## Scope

Issues, pull requests, discussions and commit messages.

This repository holds a configuration and a benchmark, not a community product.
Most disagreement is "did you hold the settings constant?" or "is that exploit
real?" — technical questions, answered with evidence.

## Behaviour

Acceptable:

- Correcting a number with a reproduction
- Rejecting an addition and writing down why
- Reporting a vulnerability privately (see [`SECURITY.md`](SECURITY.md))

Not acceptable:

- Personal attacks, racism or sexualised harassment
- Adding a measurement you know to be fabricated
- Pointing the security tools at a system you do not own
- Publishing someone's API key or private host

## Enforcement

| Stage | Outcome |
| :--- | :--- |
| 1. Private warning | With a reason |
| 2. Temporary suspension | Reasoned and time-limited |
| 3. Permanent ban | Repeated or severe |

## Reporting

Email `irtibat@mahirfatih.com`. If the matter can be public, an issue is fine.
A reporter's name is not shared beyond the people involved.

## Attribution

These principles follow [Contributor Covenant 2.1](https://www.contributor-covenant.org/),
specialised for a benchmark repository: what matters here is **measurement
honesty** and **authorised use**, which is why those carry the pledge.
