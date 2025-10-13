set -x

MODEL_PATH="your SFT model"  # replace it with your local file path

python3 -m verl.trainer.main \
    config=examples/config_easy2hard.yaml \
    data.train_files=hard3000@train \
    data.val_files=hard3000@test \
    worker.actor.model.model_path=${MODEL_PATH} \
    worker.rollout.tensor_parallel_size=1 \
    trainer.experiment_name=3k_qwen2_5_vl_7b_sft_grpo_GMNER_easy2hard \
    trainer.n_gpus_per_node=8
