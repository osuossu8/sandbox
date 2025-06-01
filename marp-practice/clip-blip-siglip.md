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

# CLIP BLIP SigLIP - Vision Language Model を支える VisionEncoder の紹介

Yuya Osujo / CADDi Attribute Team

<!-- 
_footer: "※ このスライドで紹介している画像は元の論文から引用してきたものを含みます"
-->
---

## 今回の内容

Vision & Language Model を Vision& にしている VisionEncoder を紹介します

- [CLIP]()
- [BLIP]()
- [SigLIP](https://arxiv.org/pdf/2303.15343)(2023, ICCV2023)

---

## Vision & Language Model の仕組み (ざっくり)

- [LLaVA](https://arxiv.org/pdf/2304.08485) ()

- 画像-テキストの mapping 表現を学習している画像エンコーダ → Projector (MLP) → LLM (図にする、gemini などに出してもらう)

---

---

## 企業で使用されている事例

企業でも色々使われている

- CLIP
  - recruit [[1]](https://blog.recruit.co.jp/data/articles/japanese-clip/)

- BLIP
  - 

- SigLIP
  - mercari [[1]](https://speakerdeck.com/yadayuki/vision-language-modelwohuo-yong-sita-merukarinolei-si-hua-xiang-rekomendonoxing-neng-gai-shan?slide=15) [[2]](https://engineering.mercari.com/blog/entry/20241104-similar-looks-recommendation-via-vision-language-model/)
  - cyberagent [[1]](https://huggingface.co/cyberagent/llava-calm2-siglip)
---

## How to apply in CADDi ?

---

## 参考

- https://techblog.exawizards.com/entry/2023/05/10/055218

---
