<div align="center">

![Text-to-Video Banner](https://images.unsplash.com/photo-1485846234645-a62644f84728?w=1200&auto=format&fit=crop)

# Awesome-Text-To-Video [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated, visually-organized list of **Text-to-Video (T2V)** products, open-source models, research papers, datasets, and benchmarks.

[中文](README_zh.md) | English

</div>

---

## Table of Contents

- [What's New](#whats-new)
- [Commercial Text-to-Video Products](#commercial-text-to-video-products)
  - [Closed-Source Platforms](#closed-source-platforms)
  - [Featured Product Cards](#featured-product-cards)
  - [Related Tools](#related-tools)
- [Open-Source Models & Toolkits](#open-source-models--toolkits)
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

Key trends:
- **Native 4K** and synchronized audio are becoming standard.
- **Open-source models** now rival closed commercial systems.
- **Multi-shot storytelling** and character consistency are the new battlegrounds.
- **Inference acceleration** (sliding tile attention, token carving, caching) makes local generation feasible.

---

## Commercial Text-to-Video Products

### Closed-Source Platforms

| Product | Maker | Best For | Max Output | Highlights | Link |
|---------|-------|----------|------------|------------|------|
| 🎬 **Runway Gen-4 / Gen-4.5** | RunwayML | Professional creators | 1080p (4K upscale) | `@reference` consistency, world-class physics, Aleph editing | [runwayml.com](https://runwayml.com) |
| 🐉 **Kling 3.0** | Kuaishou | Motion-heavy / cinematic | 1080p, 15 s | Best-in-class motion, generous free tier | [klingai.com](https://klingai.com) |
| 🔍 **Veo 3 / Veo 3.1** | Google DeepMind | 4K broadcast production | Native 4K | Scene extension, native audio + lip-sync | [deepmind.google](https://deepmind.google/technologies/veo/) |
| 🌱 **Seedance 2.0** | ByteDance | Multi-shot storytelling | 2K, 60 s multi-shot | 12 mixed inputs, native audio-video joint gen | [seedance.tv](https://www.seedance.tv) |
| ✨ **Luma Dream Machine** | Luma AI | Action / sports / physics | 4K | Realistic motion blur, fluid dynamics | [lumalabs.ai](https://lumalabs.ai) |
| 🎭 **Pika 2.5 / 3.0** | Pika Labs | Social / stylized content | 2K | Fast, cheap, strong style transfer | [pika.art](https://pika.art) |
| 🌀 **Hailuo AI** | MiniMax | Realistic humans / prompt adherence | 1080p, 10 s | Strong physical realism, #1 in China | [hailuoai.video](https://hailuoai.video) |
| 🛠️ **Krea AI** | Krea | Model-agnostic access | Varies | Unified UI for Kling, Hailuo, Luma, Runway, Pika | [krea.ai](https://www.krea.ai) |
| 🔮 **Gemini Omni** | Gemini Omni | Multimodal prompting | 720p–4K | Text/image/video/audio in one prompt, native audio sync | [gemini-omni.pro](https://gemini-omni.pro/) |
| 🧑‍💼 **Synthesia** | Synthesia | Corporate training / avatars | 1080p | 100+ avatars, 130+ languages | [synthesia.io](https://www.synthesia.io) |
| 🎤 **DeepBrain AI** | DeepBrain AI | Hyper-realistic avatars | 1080p | PPT-to-video, chroma key, native AI anchors | [deepbrain.io](https://www.deepbrain.io) |
| ⚠️ ~~**Sora / Sora 2**~~ | ~~OpenAI~~ | ~~Photorealism~~ | ~~1080p–8K~~ | **Consumer app shut down March 2026** | ~~[openai.com/sora](https://openai.com/sora)~~ |

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
  <img src="https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=600&auto=format&fit=crop" width="100%">
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
</table>

</div>

### Related Tools

| Tool | What it does | Link |
|------|--------------|------|
| **TubePrompter** | Converts existing videos into optimized text-to-video prompts for Sora, Veo, Runway, etc. | [tubeprompter.com](https://tubeprompter.com/) |

---

## Open-Source Models & Toolkits

<div align="center">

| Model | Preview | Org | Size | License | Notes |
|-------|---------|-----|------|---------|-------|
| **Wan 2.7** | <img src="https://opengraph.githubassets.com/1/Wan-Video/Wan2.1" width="160"> | Alibaba | 27B (14B active) | Apache 2.0 | MoE DiT; 1.3B runs in ~8 GB VRAM; audio support |
| **HunyuanVideo 1.5** | <img src="https://opengraph.githubassets.com/1/Tencent-Hunyuan/HunyuanVideo" width="160"> | Tencent | 8.3B | Apache 2.0 | 480p I2V in ~75 s on RTX 4090; bilingual |
| **LTX-Video / LTX-2.3** | <img src="https://opengraph.githubassets.com/1/Lightricks/LTX-Video" width="160"> | Lightricks | 22B | Apache 2.0* | Native 4K@50fps + stereo audio; ~8 GB VRAM |
| **CogVideoX** | <img src="https://opengraph.githubassets.com/1/THUDM/CogVideo" width="160"> | THUDM / Zhipu AI | 2B / 5B | Apache 2.0 | Expert transformer; strong ComfyUI/LoRA support |
| **Open-Sora 2.0** | <img src="https://opengraph.githubassets.com/1/hpcaitech/Open-Sora" width="160"> | HPC-AI Tech | 11B | Apache 2.0 | Full training pipeline; $200k training cost claim |
| **Open-Sora-Plan 1.3** | <img src="https://opengraph.githubassets.com/1/PKU-YuanGroup/Open-Sora-Plan" width="160"> | PKU-YuanGroup | — | MIT | Open reproduction of Sora capabilities |
| **Mochi 1** | <img src="https://opengraph.githubassets.com/1/genmoai/mochi" width="160"> | Genmo | 10B | Apache 2.0 | Realistic physics and motion |
| **Step-Video-T2V** | <img src="https://opengraph.githubassets.com/1/stepfun-ai/Step-Video-T2V" width="160"> | StepFun | — | — | Large open-source T2V model series |
| **Stable Video Diffusion** | <img src="https://opengraph.githubassets.com/1/Stability-AI/generative-models" width="160"> | Stability AI | — | — | Image-to-video / video foundation model |
| **AnimateDiff** | <img src="https://opengraph.githubassets.com/1/guoyww/AnimateDiff" width="160"> | Tsinghua / CUHK | — | — | Animate personalized T2I models without tuning |
| **Latte** | <img src="https://opengraph.githubassets.com/1/Vchitect/Latte" width="160"> | Shanghai AI Lab / NTU | — | — | Early DiT-based latent diffusion for video |

</div>

Quick repository links:

[![Wan](https://img.shields.io/badge/GitHub-Wan--Video%2FWan2.1-blue?logo=github)](https://github.com/Wan-Video/Wan2.1)
[![HunyuanVideo](https://img.shields.io/badge/GitHub-Tencent--Hunyuan%2FHunyuanVideo-blue?logo=github)](https://github.com/Tencent-Hunyuan/HunyuanVideo)
[![LTX-Video](https://img.shields.io/badge/GitHub-Lightricks%2FLTX--Video-blue?logo=github)](https://github.com/Lightricks/LTX-Video)
[![CogVideo](https://img.shields.io/badge/GitHub-THUDM%2FCogVideo-blue?logo=github)](https://github.com/THUDM/CogVideo)
[![Open-Sora](https://img.shields.io/badge/GitHub-hpcaitech%2FOpen--Sora-blue?logo=github)](https://github.com/hpcaitech/Open-Sora)
[![Open-Sora-Plan](https://img.shields.io/badge/GitHub-PKU--YuanGroup%2FOpen--Sora--Plan-blue?logo=github)](https://github.com/PKU-YuanGroup/Open-Sora-Plan)
[![Mochi](https://img.shields.io/badge/GitHub-genmoai%2Fmochi-blue?logo=github)](https://github.com/genmoai/mochi)
[![Step-Video](https://img.shields.io/badge/GitHub-stepfun--ai%2FStep--Video--T2V-blue?logo=github)](https://github.com/stepfun-ai/Step-Video-T2V)

---

## Research Papers

### 2026

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

### 2024

- **Sora: A Review on Background, Technology, Limitations, and Opportunities of Large Vision Models**, Yixin Liu et al. [[Paper](https://arxiv.org/abs/2402.17177)]
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
| **VidProM** | — | Large prompt-gallery dataset for video generation | [VidProM](https://vidprom.github.io/) |

### Benchmarks

| Benchmark | Focus | Link |
|-----------|-------|------|
| **VBench / VBench-2.0** | Comprehensive video generation evaluation suite | [Vchitect/VBench](https://github.com/Vchitect/VBench) |
| **T2V-CompBench** | Compositional text-to-video generation | [T2V-CompBench](https://github.com/Karine-Huang/T2V-CompBench) |
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

This list was compiled and updated using information from the following sources:

- [OpenAI Sora](https://openai.com/sora)
- [Google DeepMind Veo](https://deepmind.google/technologies/veo/)
- [Runway Help: Creating with Gen-4 Video](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4-Video)
- [Runway Review 2026: Gen-4.5, Aleph, and the Post-Sora Video AI Landscape](https://aiunpacking.com/review/runway/)
- [Luma Dream Machine](https://lumalabs.ai)
- [Kling AI](https://klingai.com)
- [Hailuo AI](https://hailuoai.video)
- [Pika](https://pika.art)
- [Krea AI](https://www.krea.ai)
- [ByteDance Seedance 2.0 Global Release: 2026 Launch Guide](https://resource.digen.ai/bytedance-seedance-2-0-global-release-2026/)
- [Seedance 2.0 Review: ByteDance Tops AI Video in 2026](https://www.buildfastwithai.com/blogs/seedance-2-bytedance-ai-video-2026)
- [HunyuanVideo GitHub](https://github.com/Tencent-Hunyuan/HunyuanVideo)
- [Wan 2.1 GitHub](https://github.com/Wan-Video/Wan2.1)
- [CogVideo GitHub](https://github.com/THUDM/CogVideo)
- [Open-Sora GitHub](https://github.com/hpcaitech/Open-Sora)
- [Open-Sora-Plan GitHub](https://github.com/PKU-YuanGroup/Open-Sora-Plan)
- [LTX-Video GitHub](https://github.com/Lightricks/LTX-Video)
- [Mochi GitHub](https://github.com/genmoai/mochi)
- [Step-Video-T2V GitHub](https://github.com/stepfun-ai/Step-Video-T2V)
- [AnimateDiff GitHub](https://github.com/guoyww/AnimateDiff)
- [Latte GitHub](https://github.com/Vchitect/Latte)
- [VBench GitHub](https://github.com/Vchitect/VBench)
- arXiv papers cited in the [Research Papers](#research-papers) section.
