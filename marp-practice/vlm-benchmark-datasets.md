---
marp: true
theme: gaia
size: 16:9
paginate: true
header: ""
footer: ""
class: invert
style: |
  .flex{
    display: flex;
    gap: 1em;
  }
  .sa {
    justify-content: space-around;
  }
  .sb {
    justify-content: space-between;
  }
  .sa div,.sb div{
    margin: 0.1em;
    font-size: 0.8em;
  }
  .fw div{
    flex: var(--fw);
  }
  .smaller-font-size {
    font-size: 0.7em !important;
  }
---

# Vision Language Model のベンチマークデータセットに関する論文紹介

Yuya Osujo / CADDi Attribute Team

<!-- 
_footer: "※ このスライドで紹介している画像は元の論文から引用してきたものを含みます"
-->
---

## 今回の内容

Vision & Language Model の学習に使用されるデータセットや評価ベンチマークに関する論文を紹介

- [Visual Instruction Tuning](https://arxiv.org/pdf/2304.08485) (2023.12, NeurIPS 2023)
- [HERON-BENCH: A BENCHMARK FOR EVALUATING VISION LANGUAGE MODELS IN JAPANESE](https://arxiv.org/pdf/2404.07824)
(2024.4)
- [Improved Baselines with Visual Instruction Tuning](https://arxiv.org/pdf/2310.03744) (2024.5, CVPR 2024)

---

## 主要な Vision & Language Model のベンチマーク評価結果

- [Gemini 2.5](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/#enhanced-reasoning)
- [Claude 3.7 sonnet](https://www.anthropic.com/claude/sonnet)
- [DeepSeek-R1](https://arxiv.org/pdf/2501.12948)

---

## Visual Instruction Tuning

命令追従型の生成データセット作成手順とモデル、評価ベンチマーク、評価メトリクスの提案

- データ作成: (画像入力のできない通常の) GPT-4 と既存の画像+キャプションのデータセットを活用
- モデル: 生成したデータセットで E2E 学習された MLLM である LLaVA
- 評価ベンチマーク: LLaVA-Bench (COCO) と LLaVA-Bench (In-the-Wild)
- 評価メトリクス: GPT-4 (Text Only LLM) を用いた方法 (あとで図にする)

---

## 命令追従データの作成 1

背景と課題

- 命令追従型（Instruction Following）のマルチモーダルデータの不足
  - 画像とキャプション (テキスト) のペアはたくさんある (例: CC, LAION)
- なぜか? 人手作業が必要、時間がかかる、定義が曖昧で作成が難しい
  - 💡 GPT-4に質問を作らせて、画像+キャプションを命令形式に拡張すれば良い

---

## 命令追従データの作成 2

シンプルな手法

- 既存の画像＋キャプションデータに対して：
  - GPT に 質問 Xq を生成させる（例：「この画像の人物は何をしていますか？」など）
  - 画像 Xv は <image> などの placeholder を使うか無視 (多分)
  - キャプション Xc を答えとして使う
- 単純な Q&A 形式では多様性・推論性が不足する

---

## 命令追従データの作成 3

提案手法

<div class="smaller-font-size">

- テキストのみを入力として受け付ける GPT に画像を言語化して渡す (記号的表現) 
- 記号的表現: キャプションとバウンディングボックス
- GPT-4 に対して「画像を見たように」感じさせる
- その上で、会話・詳細記述・複雑な推論の3つの形式で質問を自動生成

</div>

できたデータ

<div class="smaller-font-size">

https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K/viewer?row=0

</div>

---

## 命令追従データの作成 4

プロンプト例 (会話応答データ作成)

![w:600](./assets/visual_instruction_tuning_prompt.png)

---

## 命令追従データの作成 5

few-shot sample (画像は渡されない)

![w:400](./assets/illustrate-the-instruction-following-data-exapmle.png)

---

## 評価ベンチマーク

<div class="flex sa">
<div style="--fw: 3;">

  LLaVA-Bench (COCO) と LLaVA-Bench (In-the-Wild) の 2種類

  - LLaVA-Bench (COCO)
    - COCO-Val-2014 からランダムな 30 枚の画像を選択
    - 各画像に対して、提案したデータ生成パイプラインを使用して 3 種類の質問 (会話、詳細な説明、複雑な推論) を合計 90 の質問で生成
  - LLaVA-Bench (In-the-Wild)
    - 極めて詳細に画像を説明するよう手動でアノテーション

</div>
<div style="--fw: 2;">

  ![w:500](./assets/visual_instruction_tuning_llava_bench_in_the_wild_sample.png)

</div>
</div> 

---

## 定量評価方法

次のような 3ステップで評価、スコア（1〜10）が得られる。

<div class="smaller-font-size">

- triplet を用意
  - 画像・質問・その画像に関する「正解テキスト記述」（例：COCOのキャプションなど）

- 2つの回答を準備
  - LLaVA: 画像と質問を元に回答を生成
  - GPT-4 (text-only): 正解テキスト記述と質問を元に「理論上最良」の参照回答を生成

- GPT-4 に評価を依頼
  - 上記2つの回答を、質問と視覚情報（テキスト化された画像情報）とともに GPT-4 に与える
  - GPT-4 が以下の観点で両者を比較し、スコアと説明を返す
  - 有用性、関連性、正確さ、詳細さ

</div> 

---

---

## Improved Baselines with Visual Instruction Tuning

InstructBLIP［9］やQwen-VL［2］とは対照的に、それらは数億～数十億規模の画像と言語のペアデータ上で特別に設計された視覚リサンプラーを訓練しているのに対し、LLaVAはLMMにとって最もシンプルなアーキテクチャ設計を用い、わずか60万の画像-テキストペアに対して単純な全結合射影層を訓練するだけで済む。最終モデルは、単一の8-A100マシンで約1日で学習を完了でき、幅広いベンチマークで最先端の結果を達成している。さらに、Qwen-VL［2］が社内データを学習に使用しているのとは異なり、LLaVAは公開されているデータのみを利用している。

---

## HERON-BENCH

新しい評価ベンチマーク「Japanese Heron-Bench」を紹介
  - 新たに収集された画像と、日本語の文脈に特有の102の質問で構成
  - 日本語におけるVLMの画像記述能力と質問応答能力を評価するため
  - データセット作成とスコアリング方法は LLaVA-Bench に倣う

---

## データの作成方法

パブリックドメインまたはCC BY 2.0ライセンスの日本関連画像21枚を収集し、各画像に以下のアノテーション
- 3つのカテゴリ: 会話, 詳細, 複雑
- 7つのサブカテゴリ: アニメ, アート, 文化, 食べ物, 風景, ランドマーク, 交通
- 質問: 各カテゴリに1つまたは2つの質問で合計 102 個
- コンテキスト: 画像に関する情報をコンテキストとして手動で詳細に記述
  - モデル回答のコンテキストとして使用
---

## スコアリング方法

LLaVA-Bench で提案された方法と同じ
- 画像と質問をVLMに入力して評価し、回答テキストを取得
- 取得した回答、GPT-4の回答、およびコンテキスト（GroundTruth）をGPT-4 APIを用いて評価
- GPT-4 API に、コンテキストに基づいてGPT-4の回答とVLMの回答の両方に10点満点のスコアを割り当て、スコアの理由を説明するように指示
- 最終的なVLMのスコアは、VLMの回答の平均スコアとGPT-4モデルの回答の平均スコアの比によって決定

---


## MMMU(CVPR 2024 Oral), JMMMU(NAACL 2025)

- MMMU
- JMMMU

---

## SEED-Bench

- [SEED-Bench: Benchmarking Multimodal LLMs with Generative Comprehension](https://arxiv.org/pdf/2307.16125) (2023.8)
- [SEED-Bench-2: Benchmarking Multimodal Large Language Models](https://arxiv.org/pdf/2311.17092) (2023.11, CVPR 2024)

---

## GPQA

- [GPQA: A Graduate-Level Google-Proof Q&A Benchmark](https://arxiv.org/pdf/2311.12022) (2023.11)
- A challenging dataset of 448 multiple-choice questions written by domain experts in biology, physics, and chemistry
- GPQA main (448問) と GPQA Diamond (198問) の 2セット
  - 専門家検証者2人の合意と非専門家検証者3人の正答率で難易度分け
- 正答率
  - 専門家 (博士号取得or取得目指す): 65%, 非専門家 (他の分野で博士号取得or取得目指す, Google検索ok): 34%, Random: 25%, GPT-4 (few-shot, CoT, 当時最新): 39%
- データ収集パイプラインも紹介

---

## GPQA のデータ収集パイプライン

<div class="flex sa">
<div style="--fw: 3;">

  3つの step で作成
  - 問題作成
    - 専門家は正答できるが、非専門家は Google検索しても正解できない難易度
  - 専門家検証 & 問題修正
    - 検証専門家1 による検証 → 問題修正(あれば) → 検証専門家2 による検証
  - 非専門家検証
    - 別のドメインで問題作成や専門家検証を実施している専門家
    - Google検索ok, 時間制限なし
</div>
<div style="--fw: 2;">

  ![w:500](./assets/gpqa_data_collect_pipeline.png)

</div>
</div>

---

## コードブロック

```python
print("Hello, Marp!")