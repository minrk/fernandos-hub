import ollama
from mlx_lm.manage import scan_cache_dir

c = get_config()  # noqa

ai_cfg = c.JupyternautExtension

# set api_base on all mlx models
mlx_url = "http://127.0.0.1:8080"
mlx_parameters = {"api_base": mlx_url}

mlx_models = [repo.repo_id for repo in scan_cache_dir().repos]

ai_cfg.model_parameters = {}
for model_id in mlx_models:
    ai_cfg.model_parameters[f"hosted_vllm/{model_id}"] = mlx_parameters

# the default model

# mlx is way faster, but gpt-oss doesn't quite work yet
# (needs harmony deserialization)
ai_cfg.initial_language_model = "ollama/gpt-oss:120b"

for model in ollama.list().models:
    ai_cfg.model_parameters[f"ollama/{model.model}"] = {}

# embeddings and completions?
