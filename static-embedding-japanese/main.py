from sentence_transformers import SentenceTransformer

model_name = "hotchpotch/static-embedding-japanese"
model = SentenceTransformer(model_name, device="cpu")

query = "美味しいラーメン屋に行きたい"
docs = [
    "素敵なカフェが近所にあるよ。落ち着いた雰囲気でゆっくりできるし、窓際の席からは公園の景色も見えるんだ。",
    "新鮮な魚介を提供する店です。地元の漁師から直接仕入れているので鮮度は抜群ですし、料理人の腕も確かです。",
    "あそこは行きにくいけど、隠れた豚骨の名店だよ。スープが最高だし、麺の硬さも好み。",
    "おすすめの中華そばの店を教えてあげる。とりわけチャーシューが手作りで柔らかくてジューシーなんだ。",
]

embeddings = model.encode([query] + docs)
print(embeddings.shape)
similarities = model.similarity(embeddings[0], embeddings[1:])
for i, similarity in enumerate(similarities[0].tolist()):
    print(f"{similarity:.04f}: {docs[i]}")
