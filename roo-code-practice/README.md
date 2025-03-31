# Roo Code Practice

roo code の練習
claude-3-7-sonnet-20250219 に以下のプロンプトを実行した結果をそのまま保存

```
タスク
ddd や clean architecture を踏まえて python の fastapi で webapi を作成してください。複数の local vlm とプロンプトを引数にとって、引数に応じて別の vlm を call するようなエンドポイントを作成してください。このプロジェクトは local-vln-server という  dir を新しく作成して、ライブラリは uv で作成してください。pytest でテストも作成し、vlm の通信部分はモックを採用してください。
表示を減らす
トークン:
124
25.6k
コンテキストウィンドウ:
44.5k
200.0k
キャッシュ:
+42.6k
647.5k
APIコスト:
$0.7382
```

---

# Local VLM Server

DDDとClean Architectureを採用したFastAPIベースのローカルVLMサーバー。

## 概要

このプロジェクトは、複数のローカル大規模言語モデル（VLM）とプロンプトを引数にとり、引数に応じて異なるVLMを呼び出すWebAPIを提供します。

## アーキテクチャ

このプロジェクトは以下のアーキテクチャパターンに基づいています：

- **ドメイン駆動設計（DDD）**: ビジネスドメインを中心に設計
- **クリーンアーキテクチャ**: 依存関係を内側に向けて、外部の詳細から内部のビジネスロジックを保護

### レイヤー構成

1. **ドメイン層**: VLMに関するエンティティ、値オブジェクト、ドメインサービス
2. **アプリケーション層**: ユースケースの実装、インターフェースの定義
3. **インフラストラクチャ層**: 外部VLMとの通信実装
4. **インターフェース層**: FastAPIのエンドポイント、スキーマ定義

## 開発環境のセットアップ

```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Linuxの場合
venv\Scripts\activate  # Windowsの場合

# uvを使用した依存関係のインストール
pip install uv
uv pip install -e ".[dev]"
```

## 使用方法

```bash
# サーバーの起動
uvicorn src.local_vlm_server.interface.main:app --reload
```

APIドキュメントは http://localhost:8000/docs で確認できます。

## テスト

```bash
# テストの実行
pytest