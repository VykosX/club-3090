FROM ghcr.io/syv-ai/hyperqwen@sha256:f761ce93d19e6c5a5dfbfb36d8eb98bf7f52fd09cd456465ed14ffcc673b0ffe

COPY patch_k8v4.py /tmp/patch_k8v4.py
RUN /app/venv/bin/python /tmp/patch_k8v4.py \
    && rm -f /tmp/patch_k8v4.py \
    && /app/venv/bin/python - <<'PY'
from vllm.config.cache import CacheDType
from vllm.model_executor.layers.quantization.kvarn.config import KVARN_PRESETS, KVarNConfig
from vllm.utils.torch_utils import STR_DTYPE_TO_TORCH_DTYPE

assert "kvarn_k8v4_g128" in CacheDType.__args__
assert KVARN_PRESETS["kvarn_k8v4_g128"] == {"key_bits": 8, "value_bits": 4, "group": 128}
assert str(STR_DTYPE_TO_TORCH_DTYPE["kvarn_k8v4_g128"]) == "torch.uint8"
cfg = KVarNConfig.from_cache_dtype("kvarn_k8v4_g128", 256)
assert cfg.tile_bytes_aligned == 51456
assert cfg.tile_bytes_aligned // cfg.group == 402
print("K8/V4 registration OK:", cfg)
PY

LABEL org.opencontainers.image.title="HyperQwen vLLM KVarN K8/V4 for Club-3090" \
      org.opencontainers.image.description="Immutable HyperQwen 3acb93f runtime plus the minimal KVarN K8/V4 registration used by the Club-3090 Qwen3.8 single-3090 profiles" \
      org.opencontainers.image.source="https://github.com/noonghunna/club-3090" \
      org.opencontainers.image.revision="3acb93f7acdcdbc3cfe67e2849e27537c0524b0a+club3090-k8v4-r1" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.base.name="ghcr.io/syv-ai/hyperqwen@sha256:f761ce93d19e6c5a5dfbfb36d8eb98bf7f52fd09cd456465ed14ffcc673b0ffe" \
      org.club3090.hyperqwen.source="https://github.com/syv-ai/HyperQwen/tree/3acb93f7acdcdbc3cfe67e2849e27537c0524b0a" \
      org.club3090.kvarn.dtype="kvarn_k8v4_g128"
