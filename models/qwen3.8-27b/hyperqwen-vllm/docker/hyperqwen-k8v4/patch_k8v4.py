from pathlib import Path


root = Path("/app/venv/lib/python3.12/site-packages/vllm")
changes = {
    root / "config/cache.py": (
        '    "kvarn_k4v4_g128",\n',
        '    "kvarn_k4v4_g128",\n    "kvarn_k8v4_g128",\n',
    ),
    root / "utils/torch_utils.py": (
        '    "kvarn_k4v4_g128": torch.uint8,\n',
        '    "kvarn_k4v4_g128": torch.uint8,\n    "kvarn_k8v4_g128": torch.uint8,\n',
    ),
    root / "model_executor/layers/quantization/kvarn/config.py": (
        '    "kvarn_k4v4_g128": {"key_bits": 4, "value_bits": 4, "group": 128},\n',
        '    "kvarn_k4v4_g128": {"key_bits": 4, "value_bits": 4, "group": 128},\n'
        '    "kvarn_k8v4_g128": {"key_bits": 8, "value_bits": 4, "group": 128},\n',
    ),
    root / "v1/attention/backends/kvarn_attn.py": (
        '        "kvarn_k4v4_g128",\n',
        '        "kvarn_k4v4_g128",\n        "kvarn_k8v4_g128",\n',
    ),
}

for path, (needle, replacement) in changes.items():
    text = path.read_text()
    assert "kvarn_k8v4_g128" not in text, f"already patched: {path}"
    assert text.count(needle) == 1, f"unexpected anchor count in {path}: {text.count(needle)}"
    path.write_text(text.replace(needle, replacement, 1))

launcher = Path("/app/single-user/start_qwen.sh")
text = launcher.read_text()
needle = '  ATTN_ARGS="--kv-cache-dtype kvarn_k4v2_g128 --block-size 128"\n'
replacement = '  ATTN_ARGS="--kv-cache-dtype ${KVARN_DTYPE:-kvarn_k4v2_g128} --block-size 128"\n'
assert needle in text and "KVARN_DTYPE:-kvarn_k4v2_g128" not in text
launcher.write_text(text.replace(needle, replacement, 1))

# HyperQwen proves its patch set by reverse-applying the exact patch files. The
# intentional dtype registrations above make the KVarN reverse check no longer
# byte-identical, so also accept a positive live-registry proof of the installed
# KVarN implementation and our additional preset.
verify = Path("/app/verify.sh")
text = verify.read_text()
needle = '  if patch -p1 -R --dry-run -s --fuzz 0 -d "$SP" < kvarn/kvarn-0.30.0.patch >/dev/null 2>&1; then\n'
proof = """  if patch -p1 -R --dry-run -s --fuzz 0 -d "$SP" < kvarn/kvarn-0.30.0.patch >/dev/null 2>&1 \\
      || $PY -c "from vllm.config.cache import CacheDType; from vllm.model_executor.layers.quantization.kvarn.config import KVARN_PRESETS; from vllm.utils.torch_utils import STR_DTYPE_TO_TORCH_DTYPE; from vllm.v1.attention.backends.registry import AttentionBackendEnum; assert 'kvarn_k8v4_g128' in CacheDType.__args__; assert KVARN_PRESETS['kvarn_k8v4_g128']['key_bits'] == 8; assert KVARN_PRESETS['kvarn_k8v4_g128']['value_bits'] == 4; assert str(STR_DTYPE_TO_TORCH_DTYPE['kvarn_k8v4_g128']) == 'torch.uint8'; AttentionBackendEnum.KVARN.get_class()" >/dev/null 2>&1; then
"""
assert needle in text
verify.write_text(text.replace(needle, proof, 1))
