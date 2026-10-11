# HyperQwen runtime cache fallback

This directory is only the plain `docker compose up` fallback for HyperQwen's
host-mounted `/cache`. Normal Club-3090 launches use the shared engine cache
resolved by the launcher. Generated Triton/Inductor/Hugging Face cache data is
ignored and must never be committed.
