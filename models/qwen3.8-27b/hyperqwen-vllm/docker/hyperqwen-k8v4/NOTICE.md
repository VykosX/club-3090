# HyperQwen KVarN K8/V4 image provenance

This image is a very small derived layer over the immutable HyperQwen image built
from `syv-ai/HyperQwen` commit `3acb93f7acdcdbc3cfe67e2849e27537c0524b0a`.

Base image:

`ghcr.io/syv-ai/hyperqwen@sha256:f761ce93d19e6c5a5dfbfb36d8eb98bf7f52fd09cd456465ed14ffcc673b0ffe`

The Club-3090 layer does not replace KVarN kernels or model math. It only:

1. registers the already-parameterized `kvarn_k8v4_g128` KVarN geometry in the
   vLLM dtype/config tables;
2. lets HyperQwen's single-card launcher select the KVarN dtype through
   `KVARN_DTYPE`, preserving `kvarn_k4v2_g128` as the default; and
3. extends HyperQwen's patch verifier with an equivalent positive runtime-registry
   proof because the intentional dtype registration makes the pristine reverse
   patch check non-byte-identical.

HyperQwen and its bundled vLLM-derived work retain their upstream licenses and
attribution. The small Club-3090 extension is contributed under Apache-2.0 to
match this repository.
