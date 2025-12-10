# 🌐 MAKAR: a Multi-Agent framework based Knowledge-Augmented Reasoning for Grounded Multimodal Named Entity Recognition

> **MAKAR**: Grounded Multimodal Named Entity Recognition (GMNER), which aims to extract textual entities, their types, and corresponding visual regions from image-text data
---

## 📰 News 🔥

🎉 **[August 2025]** We are thrilled to announce that our paper,  
**"MAKAR: A Multi-Agent Framework based Knowledge-Augmented Reasoning for Grounded Multimodal Named Entity Recognition"**,  
has been **accepted by EMNLP 2025**! 🎉

We are currently finalizing the **camera-ready version** and meticulously organizing our experimental code.  
✅ **Code and datasets will be released publicly very soon!**  
🔔 Stay tuned for updates!

---

## 🛠️ Training the MAKAR Model

Follow the instructions below to set up and train the MAKAR model components.

---

### 🧠 Knowledge Enhancement Agent (KEA)

MAKAR is based on AdaSeq, AdaSeq project is based on Python version >= 3.7 and PyTorch version >= 1.8.

Step 1: Installation

```bash
git clone https://github.com/modelscope/adaseq.git
cd adaseq
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
```

Step 2: Copy MAKAR folder into .../adaseq/examples/
```bash
cd MNER_code/AdaSeq
```

Navigate to the KEA directory:

```bash
-adaseq
---|examples
-----|MAKAR
-------|twitter-10000-FMNERG.yaml
-------|twitter-10000-GMNER.yaml
```

Step 3：Replace the original adaseq folder with our adaseq folder

```bash
-adaseq
---|.git
---|.github
---|adaseq   <-- (Use our adaseq replace it)  
---|docs
---|examples
---|scripts
---|tests
---|tools
```

Step 4: Training Model

- For **GMNER**:
  ```bash
  python -m scripts.train -c examples/MAKAR/twitter-10000-GMNER.yaml
  ```

- For **FMNERG**:
  ```bash
  python -m scripts.train -c examples/MAKAR/twitter-10000-FMNERG.yaml
  ```

---

### 🔍 Entity Correction Agent (ECA)

> ⚠️ **Note**: Bing Search has been discontinued.  
> As a **temporary workaround**, we are using **GLM-Search** and **ChromeDriver-based web scraping** for knowledge retrieval.  
> A more robust long-term solution is under active investigation.

```bash
cd Search
```

- **GLM-Search** (via ZhipuAI):
  ```bash
  python zhipu_search.py
  ```

- **Web Scraping (Entity Names)**:
  ```bash
  python web_newsearch_name.py
  ```

- **Web Scraping (Text Queries)**:
  ```bash
  python web_newsearch_text.py
  ```

---

### 🤖 Entity Reasoning Grounding Agent (ERGA)

#### SFT
1. Navigate to the KEA directory:
   ```bash
   cd LLaMA-Factory
   ```

2. Install dependencies:
   ```bash
    pip install -e ".[torch,metrics]"

    pip install "deepspeed>=0.10.0,<=0.16.9"
    ```

3. Train the model:
   ```bash
    FORCE_TORCHRUN=1 llamafactory-cli train examples/train_full/easy_qwen25vl_full_sft_3k.yaml
    ```

#### GRPO

1. Navigate to the ERGA directory and install in development mode:
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

3. Launch training:
   ```bash
   bash examples/3k_qwen2_5_vl_7b_gmner_sft_grpo_easy2hard.sh
   ```

4. Merge model checkpoints (optional):
   ```bash
   python3 scripts/model_merger.py --local_dir checkpoints/easy_r1/3k_qwen2_5_vl_7b_sft_grpo_GMNER_easy2hard/global_step_60/actor
   ```

---

> 💡 **Tip**: Ensure your environment satisfies all dependency requirements before running any scripts.  
> 🚀 **GPU support is strongly recommended** for efficient training and inference.

### 🔗 Pre-trained Models
- [**MAKAR-3B**](https://modelscope.cn/models/soliton110/MAKAR-3B)  
  Lightweight version optimized for resource-constrained environments
- [**MAKAR-7B**](https://modelscope.cn/models/soliton110/MAKAR-7B)  
  Full-capacity version with enhanced reasoning capabilities

---

## 🙏 Acknowledgments

Our implementation builds upon the open-source frameworks **RIVEG** and **PGIM**.  
We sincerely thank the authors for their outstanding contributions to the community!  

Additionally, our multi-stage training framework is built on top of **AdaSeq**, **LLaMA-Factory**, and **EasyR1**, which are powerful and flexible toolkits that greatly accelerated our development and experimentation.

---

> 📬 **Contact**: For questions or collaboration, please reach out via GitHub Issues or email (linxinkui@iie.ac.cn).

