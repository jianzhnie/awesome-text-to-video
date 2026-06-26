<div align="center">

![Text-to-Video Banner](https://images.unsplash.com/photo-1485846234645-a62644f84728?w=1200&auto=format&fit=crop)

# Awesome-Text-To-Video [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated, visually-organized list of **Text-to-Video (T2V)** products, open-source models, research papers, datasets, and benchmarks.

</div>

---

## Table of Contents

- [What's New](#whats-new)
- [Commercial Text-to-Video Products](#commercial-text-to-video-products)
  - [Generative Text-to-Video Models](#generative-text-to-video-models)
  - [AI Avatar / Presenter Tools](#ai-avatar--presenter-tools)
  - [All-in-One Creative Platforms](#all-in-one-creative-platforms)
  - [Discontinued / Historical](#discontinued--historical)
  - [Featured Product Cards](#featured-product-cards)
  - [Related Tools](#related-tools)
  - [How to Choose](#how-to-choose)
- [Open-Source Models & Toolkits](#open-source-models--toolkits)
  - [Quick Start](#quick-start)
- [Research Papers](#research-papers)
  - [2026](#2026)
  - [2025](#2025)
  - [2024](#2024)
  - [2023](#2023)
  - [2022](#2022)
  - [Before 2021](#before-2021)
- [Datasets & Benchmarks](#datasets--benchmarks)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

---

## What's New

> **2026 Update**: The T2V landscape has shifted dramatically. OpenAI discontinued the consumer Sora app in early 2026, while open-source models (Wan 2.7, HunyuanVideo 1.5, LTX-2.3) and commercial alternatives (Runway Gen-4.5, Seedance 2.0, Kling 3.0, Veo 3.1) now dominate.
>
> *Data collected as of June 2026. Prices, features, and availability change quickly — always check the official website before making a decision.*

Key trends:
- **Native 4K** and synchronized audio are becoming standard.
- **Open-source models** now rival closed commercial systems.
- **Multi-shot storytelling** and character consistency are the new battlegrounds.
- **Inference acceleration** (sliding tile attention, token carving, caching) makes local generation feasible.

---

## Commercial Text-to-Video Products

### Closed-Source Platforms

#### Generative Text-to-Video Models

| Product | Maker | Best For | Max Output | Highlights | Link |
|---------|-------|----------|------------|------------|------|
| 🎬 **Runway Gen-4 / Gen-4.5** | RunwayML | Professional creators | 1080p (4K upscale) | `@reference` consistency, world-class physics, Aleph editing | [runwayml.com](https://runwayml.com) |
| 🐉 **Kling 3.0** | Kuaishou | Motion-heavy / cinematic | 1080p, 15 s | Best-in-class motion, generous free tier | [klingai.com](https://klingai.com) |
| 🔍 **Veo 3 / Veo 3.1** | Google DeepMind | 4K broadcast production | Native 4K | Scene extension, native audio + lip-sync | [deepmind.google](https://deepmind.google/technologies/veo/) |
| 🌱 **Seedance 2.0** | ByteDance | Multi-shot storytelling | 2K, 60 s multi-shot | 12 mixed inputs, native audio-video joint gen | [seedance.tv](https://www.seedance.tv) |
| ✨ **Luma Dream Machine** | Luma AI | Action / sports / physics | 4K | Realistic motion blur, fluid dynamics | [lumalabs.ai](https://lumalabs.ai) |
| 🎭 **Pika 2.5 / 3.0** | Pika Labs | Social / stylized content | 2K | Fast, cheap, strong style transfer | [pika.art](https://pika.art) |
| 🌀 **Hailuo AI** | MiniMax | Realistic humans / prompt adherence | 1080p, 10 s | Strong physical realism, #1 in China | [hailuoai.video](https://hailuoai.video) |
| 🎬 **PixVerse V6** | PixVerse | Anime / stylized content | 1080p, 15 s | Character consistency engine, 20+ camera controls, native audio | [pixverse.ai](https://pixverse.ai/) |
| 🎥 **Vidu Q1/Q2** | Shengshu / Tsinghua | Highly consistent T2V | 1080p, 16 s | U-ViT backbone, subject consistency, 1080p generation | [vidu.com](https://www.vidu.com/) |
| 🔬 **Lumiere** | Google DeepMind | Research T2V / I2V / editing | 720p | Space-time U-Net, single-pass temporal generation | [lumiere-video.github.io](https://lumiere-video.github.io/) |

#### AI Avatar / Presenter Tools

| Product | Maker | Best For | Max Output | Highlights | Link |
|---------|-------|----------|------------|------------|------|
| 🧑‍💼 **Synthesia** | Synthesia | Corporate training / avatars | 1080p | 100+ avatars, 130+ languages | [synthesia.io](https://www.synthesia.io) |
| 🎤 **DeepBrain AI** | DeepBrain AI | Hyper-realistic avatars | 1080p | PPT-to-video, chroma key, native AI anchors | [deepbrain.io](https://www.deepbrain.io) |
| 🎥 **HeyGen** | HeyGen | AI avatars / translation | 1080p | 100+ avatars, multilingual voice clone, video translation | [heygen.com](https://www.heygen.com/) |
| 🏢 **Colossyan** | Colossyan | Corporate training / e-learning | 1080p | SCORM export, branching quizzes, dual-avatar scenes | [colossyan.com](https://www.colossyan.com/) |
| ⚡ **Elai.io** | Elai | Document-to-video automation | 1080p | URL/PPTX-to-video, 100+ languages, ~1.5 min rendering | [elai.io](https://elai.io/) |
| 🖼️ **D-ID** | D-ID | Talking photos / short outreach | 1080p | Animate any photo, live streaming API, cheapest entry | [d-id.com](https://www.d-id.com/) |
| 📺 **Hour One** | Hour One | Enterprise presentations | 1080p | Broadcast-ready virtual presenters, clean UI | [hourone.ai](https://hourone.ai/) |
| 🧑‍🏫 **Vidnoz AI** | Vidnoz | Budget avatar videos / training | 1080p | Cheap avatar generation, multilingual voiceovers | [vidnoz.com](https://www.vidnoz.com/) |
| 🎨 **Steve.AI** | Steve.AI | Animated explainer videos | 4K | Multiple animation styles, character library | [steve.ai](https://www.steve.ai/) |

#### All-in-One Creative Platforms

| Product | Maker | Best For | Max Output | Highlights | Link |
|---------|-------|----------|------------|------------|------|
| 🛠️ **Krea AI** | Krea | Model-agnostic access | Varies | Unified UI for Kling, Hailuo, Luma, Runway, Pika | [krea.ai](https://www.krea.ai) |
| 🌀 **Morphic / Morph Studio** | Morph Studio | All-in-one creative platform | Varies | 15+ models, canvas editing, custom model training | [morphic.com](https://www.morphic.com/) |
| ✂️ **InVideo AI** | InVideo | Social media / marketing | 1080p | 5000+ templates, AI script-to-video workflow | [invideo.io](https://invideo.io/) |
| 🎩 **Magic Hour** | Magic Hour | Multi-format creative suite | 1080p | Face swap, talking photos, headshots, clothes swapper | [magichour.ai](https://magichour.ai/) |
| 🛒 **Creatify** | Creatify | UGC-style ad generation | 1080p | E-commerce focused, ad performance tracking | [creatify.ai](https://creatify.ai/) |
| 🎞️ **Pixo** | Pixo | Story-driven / storyboard-to-film | Varies | Story idea → storyboard → scene-by-scene generation → finished video, agent-assisted editing | [pixo.video](https://pixo.video/) |

#### Discontinued / Historical

| Product | Maker | Best For | Max Output | Highlights | Link |
|---------|-------|----------|------------|------------|------|
| ⚠️ ~~**Sora / Sora 2**~~ | ~~OpenAI~~ | ~~Photorealism~~ | ~~1080p–8K~~ | **Consumer app shut down March 2026** | ~~[openai.com/sora](https://openai.com/sora)~~ |
| ⚠️ ~~**Haiper**~~ | ~~Haiper~~ | ~~Fast creator clips~~ | ~~1080p~~ | **Consumer product shut down in 2026** | ~~[haiper.ai](https://haiper.ai/)~~ |

### Featured Product Cards

<div align="center">

<table>
<tr>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1536240478700-b869070f9279?w=600&auto=format&fit=crop" width="100%">
  <h3>Runway Gen-4.5</h3>
  <p>Ranked #1 on Artificial Analysis T2V benchmark (1,247 Elo). Native text-to-video with character-locking <code>@reference</code>.</p>
  <a href="https://runwayml.com">Try Runway →</a>
</td>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1514525253440-b393452e3723?w=600&auto=format&fit=crop" width="100%">
  <h3>Kling 3.0</h3>
  <p>Best-in-class motion quality, 66 free credits/day, and strong temporal consistency for cinematic content.</p>
  <a href="https://klingai.com">Try Kling →</a>
</td>
</tr>
<tr>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=600&auto=format&fit=crop" width="100%">
  <h3>Veo 3.1</h3>
  <p>First true native 4K T2V model with scene extension to 60+ seconds and synchronized lip-sync audio.</p>
  <a href="https://deepmind.google/technologies/veo/">Try Veo →</a>
</td>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1515634928627-2a4e0dae3ddf?w=600&auto=format&fit=crop" width="100%">
  <h3>Seedance 2.0</h3>
  <p>ByteDance's multi-shot native audio-video generator. Up to 12 mixed inputs, 60 fps, timeline prompting.</p>
  <a href="https://www.seedance.tv">Try Seedance →</a>
</td>
</tr>
<tr>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&auto=format&fit=crop" width="100%">
  <h3>Colossyan</h3>
  <p>SCORM-compliant corporate training with branching quizzes, dual-avatar conversations, and 80+ languages.</p>
  <a href="https://www.colossyan.com/">Try Colossyan →</a>
</td>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=600&auto=format&fit=crop" width="100%">
  <h3>Magic Hour</h3>
  <p>Creative multi-format suite: face swap, talking photos, headshots, and clothes swapper for social content.</p>
  <a href="https://magichour.ai/">Try Magic Hour →</a>
</td>
</tr>
<tr>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1563089145-599997674d42?w=600&auto=format&fit=crop" width="100%">
  <h3>PixVerse V6</h3>
  <p>Specialized in anime and stylized content with character consistency, 20+ camera controls, and native audio.</p>
  <a href="https://pixverse.ai/">Try PixVerse →</a>
</td>
<td width="50%" align="center">
  <img src="https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?w=600&auto=format&fit=crop" width="100%">
  <h3>Morphic / Morph Studio</h3>
  <p>All-in-one creative platform with 15+ models, canvas-based editing, and custom model training for teams.</p>
  <a href="https://www.morphic.com/">Try Morphic →</a>
</td>
</tr>
</table>

</div>

### Related Tools

| Tool | What it does | Link |
|------|--------------|------|
| **TubePrompter** | Converts existing videos into optimized text-to-video prompts for Sora, Veo, Runway, etc. | [tubeprompter.com](https://tubeprompter.com/) |
| **Vadoo AI** | AI shorts automation platform for faceless channels and social clips. | [vadoo.tv](https://vadoo.tv/) |

---

### How to Choose

| Your Goal | Recommended Tool | Why |
|-----------|------------------|-----|
| Professional filmmaking / VFX | **Runway Gen-4.5** | Best creative control, reference consistency, Aleph editing |
| Best motion realism on a budget | **Kling 3.0** | Top-tier motion, generous free tier, native audio |
| 4K broadcast / cinematic scenes | **Veo 3.1** | Native 4K, scene extension, lip-sync audio |
| Multi-shot storytelling | **Seedance 2.0** | Unified audio-video generation, timeline prompting |
| Anime / stylized content | **PixVerse V6** | Character consistency, camera controls, native audio |
| Corporate training / LMS | **Synthesia / Colossyan** | SCORM, avatars, quizzes, multilingual |
| Avatar marketing videos | **HeyGen / D-ID** | Expressive avatars, fast generation, API access |
| Real-time creative exploration | **Krea AI** | 64+ models, sub-50ms feedback |
| Local / open-source deployment | **Wan 2.7 / HunyuanVideo 1.5** | Apache 2.0, consumer GPU friendly |

---

## Open-Source Models & Toolkits

<div align="center">

| Model | Preview | Org | Size | License | Min VRAM | Best For |
|-------|---------|-----|------|---------|----------|----------|
| **Wan 2.7** | <img src="https://opengraph.githubassets.com/1/Wan-Video/Wan2.1" width="160"> | Alibaba | 27B (14B active) | Apache 2.0 | ~8 GB (1.3B) | Best overall open-source, bilingual, audio support |
| **HunyuanVideo 1.5** | <img src="https://opengraph.githubassets.com/1/Tencent-Hunyuan/HunyuanVideo" width="160"> | Tencent | 8.3B | Apache 2.0 | ~14 GB | Fast iteration, efficient quality, bilingual |
| **LTX-Video / LTX-2.3** | <img src="https://opengraph.githubassets.com/1/Lightricks/LTX-Video" width="160"> | Lightricks | 22B | Apache 2.0* | ~8 GB | Real-time / 4K generation with native audio |
| **CogVideoX** | <img src="https://opengraph.githubassets.com/1/THUDM/CogVideo" width="160"> | THUDM / Zhipu AI | 2B / 5B | Apache 2.0 | ~16 GB | ComfyUI ecosystem, LoRA support, beginners |
| **Open-Sora 2.0** | <img src="https://opengraph.githubassets.com/1/hpcaitech/Open-Sora" width="160"> | HPC-AI Tech | 11B | Apache 2.0 | ~24 GB | Full training pipeline, commercial-level quality |
| **Open-Sora-Plan 1.3** | <img src="https://opengraph.githubassets.com/1/PKU-YuanGroup/Open-Sora-Plan" width="160"> | PKU-YuanGroup | — | MIT | Varies | Open reproduction of Sora capabilities |
| **Mochi 1** | <img src="https://opengraph.githubassets.com/1/genmoai/mochi" width="160"> | Genmo | 10B | Apache 2.0 | ~24 GB | Realistic physics and motion |
| **Step-Video-T2V** | <img src="https://opengraph.githubassets.com/1/stepfun-ai/Step-Video-T2V" width="160"> | StepFun | — | — | High | Large open-source T2V model series |
| **Stable Video Diffusion** | <img src="https://opengraph.githubassets.com/1/Stability-AI/generative-models" width="160"> | Stability AI | — | — | ~16 GB | Image-to-video / video foundation model |
| **AnimateDiff** | <img src="https://opengraph.githubassets.com/1/guoyww/AnimateDiff" width="160"> | Tsinghua / CUHK | — | Apache 2.0 | ~12 GB | Animate personalized T2I models without tuning |
| **Latte** | <img src="https://opengraph.githubassets.com/1/Vchitect/Latte" width="160"> | Shanghai AI Lab / NTU | — | Apache 2.0 | ~16 GB | Early DiT-based latent diffusion for video |
| **SkyReels V1 / V2** | <img src="https://opengraph.githubassets.com/1/SkyworkAI/SkyReels-V2" width="160"> | SkyworkAI | 1.3B / 14B | — | ~16 GB | Human-centric V1; V2 uses diffusion-forcing for infinite-length film |
| **MAGI-1** | <img src="https://opengraph.githubassets.com/1/SandAI-org/MAGI-1" width="160"> | Sand AI | 4.5B / 24B | — | Varies | Autoregressive chunk-based generation, up to 4M tokens context |
| **Waver 1.0** | <img src="https://opengraph.githubassets.com/1/FoundationVision/Waver" width="160"> | ByteDance | 12B | — | ~24 GB | Unified T2V/I2V/T2I, 1080p, Cascade Refiner |
| **VideoCrafter2** | <img src="https://opengraph.githubassets.com/1/AILab-CVC/VideoCrafter" width="160"> | Tencent AI Lab / CUHK | — | — | ~16 GB | High-quality T2V/I2V diffusion models |
| **ModelScope T2V** | <img src="https://opengraph.githubassets.com/1/ali-vilab/VGen" width="160"> | Alibaba / DAMO | — | — | ~16 GB | Early open diffusion T2V model (UNet3D) |
| **Allegro / Allegro-TI2V** | <img src="https://opengraph.githubassets.com/1/rhymes-ai/Allegro" width="160"> | Rhymes AI | ~3B | Apache 2.0 | ~9 GB (offload) | Apache 2.0 commercial use, Diffusers integration |
| **DynamiCrafter** | <img src="https://opengraph.githubassets.com/1/Doubiiu/DynamiCrafter" width="160"> | CUHK / Tencent AI Lab | — | Apache 2.0 | ~16 GB | (Text-)Image-to-video animation from still images |
| **I2VGen-XL** | <img src="https://opengraph.githubassets.com/1/ali-vilab/i2vgen-xl" width="160"> | Alibaba / DAMO | — | — | ~16 GB | High-fidelity image-to-video with semantic understanding |
| **VideoComposer** | <img src="https://opengraph.githubassets.com/1/ali-vilab/videocomposer" width="160"> | Alibaba / DAMO | — | Apache 2.0 | ~16 GB | Compositional video synthesis with motion controllability |
| **Lumiere (unofficial)** | <img src="https://opengraph.githubassets.com/1/lucidrains/lumiere-pytorch" width="160"> | lucidrains | — | MIT | N/A | PyTorch implementation of Google DeepMind's Lumiere |

</div>

Quick repository links with stars:

[![Wan](https://img.shields.io/github/stars/Wan-Video/Wan2.1?style=social)](https://github.com/Wan-Video/Wan2.1)
[![HunyuanVideo](https://img.shields.io/github/stars/Tencent-Hunyuan/HunyuanVideo?style=social)](https://github.com/Tencent-Hunyuan/HunyuanVideo)
[![LTX-Video](https://img.shields.io/github/stars/Lightricks/LTX-Video?style=social)](https://github.com/Lightricks/LTX-Video)
[![CogVideo](https://img.shields.io/github/stars/THUDM/CogVideo?style=social)](https://github.com/THUDM/CogVideo)
[![Open-Sora](https://img.shields.io/github/stars/hpcaitech/Open-Sora?style=social)](https://github.com/hpcaitech/Open-Sora)
[![Open-Sora-Plan](https://img.shields.io/github/stars/PKU-YuanGroup/Open-Sora-Plan?style=social)](https://github.com/PKU-YuanGroup/Open-Sora-Plan)
[![Mochi](https://img.shields.io/github/stars/genmoai/mochi?style=social)](https://github.com/genmoai/mochi)
[![Step-Video](https://img.shields.io/github/stars/stepfun-ai/Step-Video-T2V?style=social)](https://github.com/stepfun-ai/Step-Video-T2V)
[![SkyReels](https://img.shields.io/github/stars/SkyworkAI/SkyReels-V2?style=social)](https://github.com/SkyworkAI/SkyReels-V2)
[![MAGI-1](https://img.shields.io/github/stars/SandAI-org/MAGI-1?style=social)](https://github.com/SandAI-org/MAGI-1)
[![Waver](https://img.shields.io/github/stars/FoundationVision/Waver?style=social)](https://github.com/FoundationVision/Waver)
[![VideoCrafter](https://img.shields.io/github/stars/AILab-CVC/VideoCrafter?style=social)](https://github.com/AILab-CVC/VideoCrafter)
[![VGen](https://img.shields.io/github/stars/ali-vilab/VGen?style=social)](https://github.com/ali-vilab/VGen)
[![Allegro](https://img.shields.io/github/stars/rhymes-ai/Allegro?style=social)](https://github.com/rhymes-ai/Allegro)
[![DynamiCrafter](https://img.shields.io/github/stars/Doubiiu/DynamiCrafter?style=social)](https://github.com/Doubiiu/DynamiCrafter)
[![I2VGen-XL](https://img.shields.io/github/stars/ali-vilab/i2vgen-xl?style=social)](https://github.com/ali-vilab/i2vgen-xl)
[![VideoComposer](https://img.shields.io/github/stars/ali-vilab/videocomposer?style=social)](https://github.com/ali-vilab/videocomposer)
[![Lumiere PyTorch](https://img.shields.io/github/stars/lucidrains/lumiere-pytorch?style=social)](https://github.com/lucidrains/lumiere-pytorch)

### Quick Start

Get started with the most popular open-source models:

**Wan 2.1**
```bash
git clone https://github.com/Wan-Video/Wan2.1
cd Wan2.1
pip install -r requirements.txt
```

**HunyuanVideo 1.5**
```bash
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo
cd HunyuanVideo
# Follow the official guide for sampling and I2V inference
```

**CogVideoX**
```bash
git clone https://github.com/THUDM/CogVideo
cd CogVideo
pip install -r requirements.txt
```

For detailed inference configs, LoRA fine-tuning, and ComfyUI workflows, see each repository's README.

---

## Research Papers

### 2026

- **Efficient Video Diffusion Models: Advancements and Challenges**, Shitong Shao. [[Paper](https://arxiv.org/abs/2604.15911)]
  - First comprehensive survey focused on efficient video diffusion: step distillation, efficient attention, model compression, caching/trajectory optimization.
- **Controllable Video Generation: A Survey** [[Paper](https://arxiv.org/abs/2507.16869)]
  - Systematic review of pose-guided, structure-controlled, and other conditional video generation methods.
- **Survey of Video Diffusion Models: Foundations, Implementations, and Applications**, Yimu Wang et al. [[Paper](https://arxiv.org/abs/2504.16081)]
  - Comprehensive taxonomy of diffusion-based video generation, evaluation metrics, industry solutions, and training engineering.
- **UNIC: Unified In-Context Video Editing** [[Paper](https://arxiv.org/abs/2506.04216)]
- **BRITE: A Benchmark for Reliable and Interpretable T2V Evaluation on Implausible Scenarios** [[Paper](https://arxiv.org/abs/2605.00873)]
- **Runway Gen-4.5 Technical Report** — Runway (2026) [[Runway Help](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4-Video)]
- **ByteDance Seedance 2.0** — Global launch April 2026 [[Overview](https://resource.digen.ai/bytedance-seedance-2-0-global-release-2026/)]
- **LTX-2.3: Native 4K Video + Audio Generation** — Lightricks (March 2026) [[Project](https://github.com/Lightricks/LTX-Video)]
- **Wan 2.7: Mixture-of-Experts Video Generation** — Alibaba (April 2026) [[arXiv](https://arxiv.org/abs/2503.20314)] [[Code](https://github.com/Wan-Video/Wan2.1)]

### 2025

- **Bridging Text and Video Generation: A Survey**, Nilay Kumar et al. [[Paper](https://arxiv.org/abs/2510.04999)]
  - Comprehensive survey on T2V evolution, DiT architectures, datasets, training recipes, and benchmarks.
- **Wan: Open and Advanced Large-Scale Video Generative Models**, Alibaba. [[Paper](https://arxiv.org/abs/2503.20314)] [[Code](https://github.com/Wan-Video/Wan2.1)]
- **Training a Commercial-Level Video Generation Model in $200k** (Open-Sora 2.0) [[Paper](https://arxiv.org/abs/2503.09642)] [[Code](https://github.com/hpcaitech/Open-Sora)]
- **Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model**, Guoqing Ma et al. [[Paper](https://arxiv.org/abs/2502.10248)] [[Code](https://github.com/stepfun-ai/Step-Video-T2V)]
- **HunyuanVideo: A Systematic Framework For Large Video Generative Models**, Weijie Kong et al. [[Paper](https://arxiv.org/abs/2412.03603)] [[Code](https://github.com/Tencent-Hunyuan/HunyuanVideo)]
- **Fast Video Generation with Sliding Tile Attention**, Peiyuan Zhang et al. [[Paper](https://arxiv.org/abs/2502.04507)]
- **Training-Free Efficient Video Generation via Dynamic Token Carving** [[Paper](https://arxiv.org/abs/2505.16864)]
- **FastCar: Cache Attentive Replay for Fast Auto-Regressive Video Generation on the Edge** [[Paper](https://arxiv.org/abs/2505.14709)]
- **On-Device Sora: Enabling Training-Free Diffusion-Based Text-to-Video Generation for Mobile Devices** [[Paper](https://arxiv.org/abs/2502.04363)]
- **SkyReels-A2: Compose Anything in Video Diffusion Transformers** [[Paper](https://arxiv.org/abs/2504.02436)]
- **MotionCanvas: Cinematic Shot Design with Controllable Image-to-Video Generation** [[Paper](https://arxiv.org/abs/2502.04299)]
- **EasyControl: Adding Efficient and Flexible Control for Diffusion Transformer** [[Paper](https://arxiv.org/abs/2503.07027)]
- **MUG-V 10B: High-efficiency Training Pipeline for Large Video Generation Models** [[Paper](https://arxiv.org/abs/2510.17519)]
- **VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness** [[Paper](https://arxiv.org/abs/2503.21755)] [[Code](https://github.com/Vchitect/VBench)]
- **Kandinsky 5.0: A Family of Foundation Models for Image and Video Generation** [[Paper](https://arxiv.org/abs/2511.14993)]
- **ARLON: Boosting Diffusion Transformers with Autoregressive Models for Long Video Generation** [[Paper](https://arxiv.org/abs/2410.20502)]
- **T2VTextBench: A Human Evaluation Benchmark for Textual Control in Video Generation Models** [[Paper](https://arxiv.org/abs/2505.04946)]
- **A Survey of AI-Generated Video Evaluation** [[Paper](https://arxiv.org/abs/2410.19884)]

### 2024

- **Movie Gen: A Cast of Media Foundation Models**, Meta. [[Paper](https://arxiv.org/abs/2410.13720)]
- **Lumiere: A Space-Time Diffusion Model for Video Generation**, Google DeepMind. [[Paper](https://arxiv.org/abs/2401.12945)] [[Project](https://lumiere-video.github.io/)] [[Code](https://github.com/lucidrains/lumiere-pytorch)]
- **Vidu: A Highly Consistent, Dynamic and Skilled Text-to-Video Generator with Diffusion Models**, Shengshu / Tsinghua. [[Paper](https://arxiv.org/abs/2405.04233)] [[Code](https://github.com/shengshu-ai/vidu-skills)]
- **Allegro: Open the Black Box of Commercial-Level Video Generation Model**, Rhymes AI. [[Paper](https://arxiv.org/abs/2410.15458)] [[Code](https://github.com/rhymes-ai/Allegro)]
- **DynamiCrafter: Animating Open-domain Images with Video Diffusion Priors**, CUHK / Tencent AI Lab. [[Paper](https://arxiv.org/abs/2310.08465)] [[Code](https://github.com/Doubiiu/DynamiCrafter)]
- **Sora: A Review on Background, Technology, Limitations, and Opportunities of Large Vision Models**, Yixin Liu et al. [[Paper](https://arxiv.org/abs/2402.17177)]
- **VideoCrafter2: Overcoming Data Limitations for High-Quality Video Diffusion Models**, Haoxin Chen et al. [[Paper](https://arxiv.org/abs/2401.09047)] [[Code](https://github.com/AILab-CVC/VideoCrafter)]
- **CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer**, Zhuoyi Yang et al. [[Paper](https://arxiv.org/abs/2408.06072)] [[Code](https://github.com/THUDM/CogVideo)]
- **Latte: Latent Diffusion Transformer for Video Generation**, Xin Ma et al. [[Paper](https://arxiv.org/abs/2401.03048)] [[Code](https://github.com/Vchitect/Latte)]
- **VideoTetris: Towards Compositional Text-to-Video Generation** [[Paper](https://arxiv.org/abs/2406.04277)]
- **MagicTime: Time-lapse Video Generation Models as Metamorphic Simulators** [[Paper](https://arxiv.org/abs/2404.05014)]
- **T2V-CompBench: A Comprehensive Benchmark for Compositional Text-to-Video Generation** [[Paper](https://arxiv.org/abs/2407.14505)]
- **CPA: Camera-pose-awareness Diffusion Transformer for Video Generation** [[Paper](https://arxiv.org/abs/2412.01429)]
- **Open-Sora: Democratizing Efficient Video Production for All** [[Project](https://github.com/hpcaitech/Open-Sora)]
- **Open-Sora-Plan: Open-Source Reproduction of Sora** [[Project](https://github.com/PKU-YuanGroup/Open-Sora-Plan)]

### 2023

- **Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets**, Andreas Blattmann et al. [[Paper](https://arxiv.org/abs/2311.15127)]
- **ModelScope Text-to-Video Technical Report**, Jiayu Wang et al. [[Paper](https://arxiv.org/abs/2308.06571)]
- **I2VGen-XL: High-Quality Image-to-Video Synthesis via Cascaded Diffusion Models**, Alibaba / DAMO. [[Paper](https://arxiv.org/abs/2311.04145)] [[Code](https://github.com/ali-vilab/i2vgen-xl)]
- **AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning**, Yuwei Guo et al. [[Paper](https://arxiv.org/abs/2307.04725)] [[Code](https://github.com/guoyww/AnimateDiff)]
- **Scalable Diffusion Models with Transformers (DiT)**, William Peebles & Saining Xie. [[Paper](https://arxiv.org/abs/2212.09748)] — Foundation for diffusion-transformer architectures used in Sora and successors.
- **Video Generation Models as World Simulators**, OpenAI (Sora technical report). [[Report](https://openai.com/index/video-generation-models-as-world-simulators/)]
- **Text-To-4D Dynamic Scene Generation**, Uriel Singer et al. [[Paper](https://arxiv.org/abs/2301.11280)] [[Project](https://make-a-video3d.github.io/)]

### 2022

- **Tune-A-Video: One-Shot Tuning of Image Diffusion Models for Text-to-Video Generation**, Jay Zhangjie Wu et al. [[Paper](https://arxiv.org/abs/2212.11565)] [[Project](https://tuneavideo.github.io/)] [[Code](https://github.com/showlab/Tune-A-Video)]
- **MagicVideo: Efficient Video Generation With Latent Diffusion Models**, Daquan Zhou et al. [[Paper](https://arxiv.org/abs/2211.11018)] [[Project](https://magicvideo.github.io/)]
- **Phenaki: Variable Length Video Generation From Open Domain Textual Description**, Ruben Villegas et al. [[Paper](https://arxiv.org/abs/2210.02399)]
- **Imagen Video: High Definition Video Generation with Diffusion Models**, Jonathan Ho et al. [[Paper](https://arxiv.org/abs/2210.02303)] [[Project](https://imagen.research.google/video/)]
- **Text-driven Video Prediction**, Xue Song et al. [[Paper](https://arxiv.org/abs/2210.02872)]
- **Make-A-Video: Text-to-Video Generation without Text-Video Data**, Uriel Singer et al. [[Paper](https://arxiv.org/abs/2209.14792)] [[Project](https://makeavideo.studio/)] [[Code](https://github.com/lucidrains/make-a-video-pytorch)]
- **StoryDALL-E: Adapting Pretrained Text-to-Image Transformers for Story Continuation**, Adyasha Maharana et al. [[Paper](https://arxiv.org/abs/2209.06192)] [[Code](https://github.com/adymaharana/storydalle)]
- **Word-Level Fine-Grained Story Visualization**, Bowen Li et al. [[Paper](https://arxiv.org/abs/2208.02341)] [[Code](https://github.com/mrlibw/Word-Level-Story-Visualization)]
- **CogVideo: Large-scale Pretraining for Text-to-Video Generation via Transformers**, Wenyi Hong et al. [[Paper](https://arxiv.org/abs/2205.15868)] [[Code](https://github.com/THUDM/CogVideo)]
- **Show Me What and Tell Me How: Video Synthesis via Multimodal Conditioning**, Yogesh Balaji et al. [[Paper](https://arxiv.org/abs/2203.02573)] [[Code](https://github.com/snap-research/MMVID)] [[Project](https://snap-research.github.io/MMVID/)]
- **Video Diffusion Models**, Jonathan Ho et al. [[Paper](https://arxiv.org/abs/2204.03458)] [[Project](https://video-diffusion.github.io/)]

### Before 2021

- **Transcript to Video: Efficient Clip Sequencing from Texts**, Ligong Han et al. [[Paper](https://arxiv.org/abs/2107.11851)] [[Project](http://www.xiongyu.me/projects/transcript2video/)]
- **GODIVA: Generating Open-DomaIn Videos from nAtural Descriptions**, Chenfei Wu et al. [[Paper](https://arxiv.org/abs/2104.14806)]
- **Text2Video: Text-driven Talking-head Video Synthesis with Phonetic Dictionary**, Sibo Zhang et al. [[Paper](https://arxiv.org/abs/2104.14631)]
- **TiVGAN: Text to Image to Video Generation With Step-by-Step Evolutionary Generator**, Doyeon Kim et al. [[Paper](https://ieeexplore.ieee.org/document/9171240)]
- **Conditional GAN with Discriminative Filter Generation for Text-to-Video Synthesis**, Yogesh Balaji et al. [[Paper](https://www.ijcai.org/Proceedings/2019/0276.pdf)] [[Code](https://github.com/minrq/CGAN_Text2Video)]
- **IRC-GAN: Introspective Recurrent Convolutional GAN for Text-to-video Generation**, Kangle Deng et al. [[Paper](https://www.ijcai.org/Proceedings/2019/0307.pdf)]
- **StoryGAN: A Sequential Conditional GAN for Story Visualization**, Yitong Li et al. [[Paper](https://ojs.aaai.org/index.php/AAAI/article/view/12233)] [[Code](https://github.com/yitong91/StoryGAN)]
- **Video Generation From Text**, Yitong Li et al. [[Paper](https://ojs.aaai.org/index.php/AAAI/article/view/12233)]
- **To create what you tell: Generating videos from captions**, Yingwei Pan et al. [[Paper](https://dl.acm.org/doi/10.1145/3123266.3127905)]

---

## Datasets & Benchmarks

### Datasets

| Dataset | Scale | Highlights | Link |
|---------|-------|------------|------|
| **WebVid-10M** | 10.7M clips | Large-scale text-video pairs scraped from the web | [m-bain/webvid](https://github.com/m-bain/webvid) |
| **InternVid** | 7M+ clips | High-quality video-text dataset with multimodal annotations | [OpenGVLab/InternVid](https://github.com/OpenGVLab/InternVid) |
| **HD-VILA-100M** | 100M clips | High-resolution long-form videos with dense captions | [microsoft/HQD](https://github.com/microsoft/HQD) |
| **Panda-70M** | 70M clips | Large dataset of high-quality video-caption pairs | [snap-research/Panda-70M](https://github.com/snap-research/Panda-70M) |
| **Vript** | 420K clips | Ultra-detailed captions (~145 words), shot type and camera movement | [Vript](https://github.com/mbzuai-oryx/Vript) |
| **MiraData** | 798K clips | Long-duration videos (avg 72s), 1080p, 318-word captions | [MiraData](https://github.com/mira-space/MiraData) |
| **OpenVid-1M** | 1M clips | High-quality, diverse scenarios, ~98-word captions | [OpenVid-1M](https://github.com/NJU-PCALAB/OpenVid-1M) |
| **CI-VID** | 1M clips / 717K seqs | Coherent interleaved text-video dataset | [CI-VID](https://github.com/I2-Multimedia-Lab/CI-VID) |
| **HD-VG-130M** | 130M clips | High-definition, watermark-free video-text pairs | [HD-VG-130M](https://github.com/daooshee/HD-VG-130M) |
| **VidProM** | — | Large prompt-gallery dataset for video generation | [VidProM](https://vidprom.github.io/) |

### Benchmarks

| Benchmark | Focus | Link |
|-----------|-------|------|
| **VBench / VBench-2.0** | Comprehensive video generation evaluation suite | [Vchitect/VBench](https://github.com/Vchitect/VBench) |
| **T2V-CompBench** | Compositional text-to-video generation | [T2V-CompBench](https://github.com/KaiyueSun98/T2V-CompBench) |
| **T2VTextBench** | Human evaluation of textual control in video generation | [T2VTextBench](https://github.com/T2VTextBench/T2VTextBench) |
| **ChronoMagic-Bench** | Metamorphic / time-lapse text-to-video evaluation | [ChronoMagic-Bench](https://github.com/PKU-YuanGroup/ChronoMagic-Bench) |
| **BRITE** | Reliable T2V evaluation on implausible scenarios | [arXiv:2605.00873](https://arxiv.org/abs/2605.00873) |
| **VideoEval** | Low-cost evaluation of video foundation models | [VideoEval](https://github.com/FlagOpen/FlagEval/tree/master/video) |

---

## Contributing

Contributions are welcome! Please open a pull request to add new products, papers, models, datasets, or benchmarks. Keep entries concise and include both a paper link and a code/project link when available.

If you have any questions, feel free to contact [jianzhnie](https://github.com/jianzhnie).

---

## License

`Awesome-Text-To-Video` is released under the Apache 2.0 license.

---

## References

This list was compiled and updated using information from the following sources.

### Product Websites

- [OpenAI Sora](https://openai.com/sora)
- [Google DeepMind Veo](https://deepmind.google/technologies/veo/)
- [Runway](https://runwayml.com) • [Runway Help: Creating with Gen-4 Video](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4-Video) • [Runway Review 2026](https://aiunpacking.com/review/runway/)
- [Luma Dream Machine](https://lumalabs.ai)
- [Kling AI](https://klingai.com)
- [Hailuo AI](https://hailuoai.video)
- [Pika](https://pika.art)
- [Krea AI](https://www.krea.ai)
- [ByteDance Seedance](https://www.seedance.tv) • [Seedance 2.0 Global Release Guide](https://resource.digen.ai/bytedance-seedance-2-0-global-release-2026/) • [Seedance 2.0 Review](https://www.buildfastwithai.com/blogs/seedance-2-bytedance-ai-video-2026)
- [PixVerse](https://pixverse.ai/)
- [Morphic / Morph Studio](https://www.morphic.com/)
- [Hedra](https://www.hedra.com/)
- [Vidnoz AI](https://www.vidnoz.com/)
- [Steve.AI](https://www.steve.ai/)
- [Vidu](https://www.vidu.com/)
- [Lumiere Project Page](https://lumiere-video.github.io/)
- [Synthesia](https://www.synthesia.io)
- [HeyGen](https://www.heygen.com/)
- [DeepBrain AI](https://www.deepbrain.io)
- [Colossyan](https://www.colossyan.com/)
- [Elai.io](https://elai.io/)
- [D-ID](https://www.d-id.com/)
- [Hour One](https://hourone.ai/)
- [Creatify](https://creatify.ai/)
- [InVideo AI](https://invideo.io/)
- [Magic Hour](https://magichour.ai/)

### Open-Source Repositories

- [Wan 2.1](https://github.com/Wan-Video/Wan2.1)
- [HunyuanVideo](https://github.com/Tencent-Hunyuan/HunyuanVideo)
- [CogVideo](https://github.com/THUDM/CogVideo)
- [Open-Sora](https://github.com/hpcaitech/Open-Sora)
- [Open-Sora-Plan](https://github.com/PKU-YuanGroup/Open-Sora-Plan)
- [LTX-Video](https://github.com/Lightricks/LTX-Video)
- [Mochi](https://github.com/genmoai/mochi)
- [Step-Video-T2V](https://github.com/stepfun-ai/Step-Video-T2V)
- [SkyReels-V2](https://github.com/SkyworkAI/SkyReels-V2)
- [MAGI-1](https://github.com/SandAI-org/MAGI-1)
- [Waver](https://github.com/FoundationVision/Waver)
- [VideoCrafter](https://github.com/AILab-CVC/VideoCrafter)
- [VGen / ModelScope T2V](https://github.com/ali-vilab/VGen)
- [Allegro](https://github.com/rhymes-ai/Allegro)
- [DynamiCrafter](https://github.com/Doubiiu/DynamiCrafter)
- [I2VGen-XL](https://github.com/ali-vilab/i2vgen-xl)
- [VideoComposer](https://github.com/ali-vilab/videocomposer)
- [Lumiere PyTorch](https://github.com/lucidrains/lumiere-pytorch)
- [AnimateDiff](https://github.com/guoyww/AnimateDiff)
- [Latte](https://github.com/Vchitect/Latte)

### Datasets, Benchmarks & Surveys

- [VBench](https://github.com/Vchitect/VBench)
- [T2V-CompBench](https://github.com/KaiyueSun98/T2V-CompBench)
- [T2VTextBench](https://arxiv.org/abs/2505.04946)
- [ChronoMagic-Bench](https://github.com/PKU-YuanGroup/ChronoMagic-Bench)
- [VideoEval](https://github.com/FlagOpen/FlagEval/tree/master/video)
- arXiv papers cited in the [Research Papers](#research-papers) section.
