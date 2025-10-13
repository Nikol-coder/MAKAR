# Training the MAKAR Model

Follow the instructions below to set up and train the MAKAR model components.

---

## Knowledge Enhancement Agent (KEA)

1. Navigate to the KEA directory:
   ```bash
   cd MNER_code/AdaSeq
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the model:

   - For **GMNER**:
     ```bash
     python -m scripts.train -c examples/PGIM/twitter-10000-GMNER.yaml
     ```

   - For **FMNERG**:
     ```bash
     python -m scripts.train -c examples/PGIM/twitter-10000-FMNERG.yaml
     ```

---

## Entity Correction Agent (ECA)

> **Note**: Bing Search has been discontinued. As a temporary workaround, we are using **GLM-Search** and **ChromeDriver-based web scraping** as alternative retrieval methods. A more robust long-term solution is under investigation.

---

## Entity Reasoning Grounding Agent (ERGA)

1. Navigate to the ERGA directory and install the package in development mode:
   ```bash
   cd EasyR1
   pip install -e .
   ```

2. Install or upgrade required packages:
   ```bash
   pip install -U transformers
   pip install --upgrade tqdm ray
   pip install transformers==4.51.3
   ```

3. Run the training script:
   ```bash
   bash examples/3k_qwen2_5_vl_7b_gmner_sft_grpo_easy2hard.sh
   ```

4. Merge model checkpoints:
   ```bash
   python3 scripts/model_merger.py --local_dir checkpoints/easy_r1/3k_qwen2_5_vl_7b_sft_grpo_GMNER_easy2hard/global_step_60/actor
   ```

---

> **Tip**: Ensure your environment meets all dependency requirements before running any training scripts. GPU support is recommended for efficient training.