# HyperQwen KVarN K8/V4 runtime image

This is the reproducible runtime used by all three Qwen3.8 single-3090 HyperQwen
profiles. It starts from the immutable HyperQwen `3acb93f` image and adds only the
KVarN K8/V4 registration/launcher hook needed by the high-fidelity profile. The
BF16 and K4/V2 profiles are unchanged by that extension, so one image pin covers
all three profiles.

The image contains **no model weights**. Club-3090 `setup.sh <slug>` downloads the
prepared target and DFlash2 drafter independently from Hugging Face, and the
compose mounts them read-only from `MODEL_DIR`.

Published image:

```text
Docker Hub: vykosx/hyperqwen-vllm:3acb93f-r1
Immutable:  vykosx/hyperqwen-vllm@sha256:11be34eaeac386b418beb98afe78221551f181c6a5726f9cf2dc02fdf92b438c
```

Club-3090 pins the immutable digest. A normal user does not need to build this
image manually: `scripts/setup.sh <slug>` fetches the target + drafter, and
`switch.sh` / `launch.sh` pulls the engine image automatically. For example:

```bash
bash scripts/setup.sh hyperqwen-vllm/qwen38-27b-single-w4a16-k8v4
bash scripts/switch.sh hyperqwen-vllm/qwen38-27b-single-w4a16-k8v4 --force
```

Direct pull / local rebuild:

```bash
docker pull vykosx/hyperqwen-vllm@sha256:11be34eaeac386b418beb98afe78221551f181c6a5726f9cf2dc02fdf92b438c
docker build \
  -t vykosx/hyperqwen-vllm:3acb93f-r1 \
  models/qwen3.8-27b/hyperqwen-vllm/docker/hyperqwen-k8v4
```

The Dockerfile runs a build-time import/configuration self-test and fails if the
K8/V4 geometry is not registered exactly as intended. See `NOTICE.md` for source
and license provenance.
