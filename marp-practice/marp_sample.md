---
marp: true
theme: gaia
#theme: default
size: 16:9
paginate: true
#backgroundColor: "#ffffff"
#color: "#000000"
header: ""
footer: "© 2023 Your Name"
#class: invert # タイトルスライドのみ背景色と文字色を反転させる場合に残す（適宜削除）
class:
  - invert
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
---

# タイトルスライド

## サブタイトル

あなたの名前 / 所属

---

# 発表内容

- 箇条書き1
- 箇条書き2
- 箇条書き3

---

# 画像を挿入する

![alt text](your-image.png)

画像のサイズ調整や背景画像として使用することも可能です。

背景画像として使用する例：

![bg right:60%](background-image.jpg)

---

# 上側のゾーン
ここはレイアウトの中で**上側**に位置します！ヘッダーとして使ったり、タイトルなどをつけられます。
<div class="flex sa">
<div style="--fw: 3;">

# 左の子要素
ここは、レイアウトの中で**左側**に位置します！
ここは、レイアウトの中で**左側**に位置します！
ここは、レイアウトの中で**左側**に位置します！
</div>
<div style="--fw: 2;">

# 右の子要素
同じくここは**右側**です！
同じくここは**右側**です！
</div>
</div>

# 下側のゾーン
ここはレイアウトで**下側**に位置します！フッターやまとめの文を挿入できます。

---

# コードブロック

```python
print("Hello, Marp!")