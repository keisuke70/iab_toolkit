# ハイブリッド IAB 分類システム

このパッケージは、IAB Content Taxonomy v3.1 分類のための最適化されたハイブリッドアプローチを提供します。このアプローチは、埋め込みベースの Tier 1 検出と LLM ベースの Tier 2 分類を組み合わせたものです。

## 特徴

- **事前計算済み埋め込み**: `.npy`ファイルを使用し、即座に類似度計算を実行
- **日本語コンテンツサポート**: 実際の日本語テキストサンプル（8種類：自動車、美容、技術、ビジネス、健康、キャリア、教育、食品・飲料）で完全にテスト済み
- **包括的なユーザープロファイリング**: 年齢層、ギーク度、コンテンツの洗練度
- **高速処理**: 最適化により従来比2.2倍の高速化を実現
- **包括的CLI**: テキスト分類、ファイル処理、テストスイート実行に対応

## アーキテクチャ

1.  **最適化された Tier 1 検出**: 事前計算された埋め込みとコサイン類似度を使用
2.  **LLM ベースの Tier 2 分類**: 正確なカテゴリ分類のための絞り込まれたタクソノミーサブセット
3.  **ユーザープロファイル分析**: 人口統計学的および行動パターンの推定

## 前提条件とセットアップ

### OpenAI API キーの設定

このシステムは OpenAI API を使用するため、事前に API キーの設定が必要です。

1. **OpenAI API キーの取得**:
   - [OpenAI Platform](https://platform.openai.com/) にアクセス
   - アカウントを作成またはログイン
   - API Keys セクションで新しい API キーを生成

2. **環境変数の設定**:
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # または .env ファイルを作成
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

3. **必要な依存関係**:
   - Python 3.10以上
   - OpenAI API キー
   - インターネット接続（API呼び出し用）

### インストール

```bash
# パッケージのインストール
pip install -e .

# または wheel ファイルから
pip install path/to/iab_toolkit-0.3.0-py3-none-any.whl
```

## クイックスタート

```python
from iab_toolkit import HybridIABClassifier # パッケージ名から直接インポート

# 分類器を初期化
classifier = HybridIABClassifier()

# コンテンツを分類
text_to_classify = "ここに分類したいコンテンツテキストを入力します。例えば、テクノロジーに関するニュース記事やファッションに関するブログ投稿などです。"
result = classifier.classify(text_to_classify)

# 結果へのアクセス
print(f"主要Tier 1ドメイン: {result.primary_tier1_domain}")

print("\nTier 2カテゴリ:")
if result.tier2_categories:
    for cat in result.tier2_categories:
        print(f"  - 名前: {cat.get('name', 'N/A')}") # カテゴリ名
        print(f"    信頼度: {cat.get('confidence', 0.0):.2f}") # 信頼度
else:
    print("  Tier 2カテゴリは見つかりませんでした。")

print("\nユーザープロファイル:")
if result.user_profile:
    print(f"  年齢層: {result.user_profile.age_range}") # 年齢層
    print(f"  ギークレベル: {result.user_profile.geekiness_level}/10") # 技術関心度
    print(f"  コンテンツの洗練度: {result.user_profile.content_sophistication}") # コンテンツの専門性
    print(f"  推定される読者層: {result.user_profile.likely_demographics}") # 推定される読者層
else:
    print("  ユーザープロファイルは生成されませんでした。")

print(f"\n処理時間: {result.processing_time:.3f} 秒") # 処理時間
print(f"使用された手法: {result.method_used}") # 使用された分類手法
```

## パフォーマンスメトリクス

- **処理時間**: 分類あたり約 450ms（従来は約 1000ms）
- **API 効率**: 分類あたり埋め込み呼び出し 1 回 + LLM 呼び出し 1 回
- **精度**: Tier 1 検出 100%、総合精度 80%
- **日本語サポート**: 8種類のサンプルタイプで完全に検証済み（自動車、美容、技術、ビジネス、健康、キャリア、教育、食品・飲料）

## ファイル構成と説明

このプロジェクトは以下の主要なファイルで構成されています。

- `iab_toolkit/`
  - `__init__.py`: `iab_toolkit` パッケージの初期化スクリプト。主要クラスをインポート可能にします。
  - `_config.py`: OpenAI API キーなどの設定情報を管理します。
  - `_embedding.py`: テキストの埋め込みベクトル生成（OpenAI API 利用）と関連ユーティリティを提供します。
  - `_gpt.py`: OpenAI GPT モデルとの連携を担当し、コンテンツ分類やプロファイル生成を行います。
  - `cli.py`: コマンドラインインターフェース（`iab-hybrid`）を提供します。テキスト入力、ファイル入力、テスト実行が可能です。
  - `hybrid_iab_classifier.py`: 中核となる `HybridIABClassifier` クラスを実装し、Tier 1 および Tier 2 の分類処理全体を制御します。
  - `models.py`: 分類結果やユーザープロファイル情報を格納するためのデータクラスを定義します。
  - `optimized_tier1_detector.py`: 事前計算済み埋め込みを利用して高速な Tier 1 ドメイン検出を行う `OptimizedTier1Detector` クラスを実装します。
  - `test_japanese_samples.py`: 日本語サンプルテキストを用いた分類システムのテストスイートです。
  - `test_japanese_samples_client_report.py`: 日本語サンプル分析のクライアント向けレポート生成スクリプトです。
  - `test/`: テスト実行結果の出力フォルダ（ログファイルとレポートファイルを格納）
  - `data/`:
    - `tier1_embeddings.npy`: Tier 1 ドメインの事前計算済み埋め込みベクトル。
    - `tier1_domains.json`: `tier1_embeddings.npy` に対応する Tier 1 ドメイン名の順序付きリスト。
    - `tier1_taxonomy.json`: Tier 1 検出用に最適化・クリーンアップされたタクソノミーデータ。
    - `taxonomy.json`: IAB Content Taxonomy v3.1 の全データ。
    - 各種 `japanese_*.txt`: 日本語のサンプルテキストファイル。
- `pyproject.toml`: プロジェクトのビルド設定、依存関係、CLI のエントリーポイントなどを定義します。
- `README.md`: このファイルです。プロジェクトの概要、使い方、ファイル構成などを説明します。

**事前計算済みデータについて**: `iab_toolkit/data/` ディレクトリ内の事前計算済みファイル（`.npy` や `.json` ファイルなど）は、`pyproject.toml` の設定により、パッケージのビルド時に自動的に組み込まれます。これにより、インストール後すぐに最適化された分類機能を利用できます。

## CLI 利用方法

`iab-hybrid` コマンドを使用して、ターミナルから直接コンテンツ分類システムを利用できます。

### 基本的な使い方

```bash
# 直接テキストを指定して分類
iab-hybrid "ここに分類したいテキストを入力します。"

# ファイルを指定して分類
iab-hybrid --file path/to/your/content.txt

# 日本語サンプルファイルを分類する例
iab-hybrid --file iab_toolkit/data/japanese_automotive_sample.txt

# JSON形式で結果を出力
iab-hybrid --json "テキスト内容"

# 詳細なログを出力（冗長モード）
iab-hybrid --verbose "テキスト内容"
```

### テストスイート実行

```bash
# 技術者向け詳細テスト（ログファイルに出力）
# 全8種類の日本語サンプルをテストし、詳細な技術情報をtest/フォルダにログファイルとして記録
iab-hybrid --test

# クライアント向けレポート生成
# 全8種類の日本語サンプルを分析し、ビジネス向けの読みやすいレポートをtest/フォルダに生成
iab-hybrid --client-report
```

**テスト出力の保存場所:**
- 技術テストログ: `iab_toolkit/test/test_japanese_samples_output_[timestamp].log`
- クライアントレポート: `iab_toolkit/test/japanese_text_analysis_client_report_[timestamp].txt`

### コマンドオプション

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--file` | `-f` | 分類対象のテキストファイルへのパス |
| `--test` | - | 技術者向け詳細テスト：全8種類の日本語サンプルをテストし、技術的な結果を`test/`フォルダにログファイルとして出力 |
| `--client-report` | - | クライアント向けレポート：全8種類の日本語サンプルを分析し、ビジネス向けの読みやすいレポートを`test/`フォルダに生成 |
| `--json` | - | 結果をJSON形式で出力（プログラム処理用） |
| `--verbose` | `-v` | 詳細ログ出力を有効化（デバッグ用） |

### 出力例

**標準出力:**
```
============================================================
IAB HYBRID CLASSIFICATION RESULTS
============================================================
📖 Text Preview: This is a sample text about automotive...
📏 Text Length: 93 characters
🎯 Primary Domain: Automotive
🏷️ Top Tier 2 Categories:
   1. Auto Technology (95.0%)
   2. Auto Type (80.0%)
👤 User Profile:
   Age Range: 30-45
   Tech Level: 7/10
   Sophistication: advanced
   Demographics: tech-savvy professional
⏱️ Processing Time: 4.179 seconds
============================================================
```

**JSON出力:**
```json
{
  "primary_tier1_domain": "Automotive",
  "tier2_categories": [
    {
      "id": "37",
      "name": "Auto Technology",
      "confidence": 0.95,
      "reasoning": "技術関連のコンテンツ分析結果"
    }
  ],
  "user_profile": {
    "age_range": "30-45",
    "geekiness_level": 8,
    "content_sophistication": "advanced",
    "likely_demographics": "tech-savvy professional",
    "confidence": 0.8
  },
  "processing_time": 3.487,
  "method_used": "hybrid_embedding_llm"
}
```

## Wheel ビルドとローカルインストール

配布可能な「wheel」ファイル（.whl）をビルドし、その wheel ファイルを他のプロジェクトにインストールすることができます。

### ビルド手順

1.  `build` パッケージがインストールされていることを確認してください:
    ```bash
    pip install build
    ```
2.  ターミナルで `iab_toolkit` ディレクトリに移動します:
    ```bash
    cd c:\\Users\\Ykeisuke\\Documents\\iab_toolkit
    ```
3.  ビルドコマンドを実行します:
    ```bash
    python -m build
    ```
    これにより、`dist` ディレクトリ内に `.whl` ファイル（例: `iab_toolkit-0.3.0-py3-none-any.whl`）が作成されます。

### 他のプロジェクトへのインストール

作成された `.whl` ファイルを他のプロジェクト（または既知の場所）にコピーし、次のコマンドを実行します:

```bash
pip install path/to/your/iab_toolkit-0.3.0-py3-none-any.whl
```

## データファイル (主要なもの)

- `tier1_embeddings.npy`: Tier 1 ドメインの事前計算済み埋め込みベクトル（39 ドメイン、1536 次元）。
- `tier1_domains.json`: `tier1_embeddings.npy` に対応する Tier 1 ドメイン名の順序付きリスト。
- `tier1_taxonomy.json`: Tier 1 検出用に最適化・クリーンアップされたタクソノミーデータ。問題のあるエントリが除外され、Tier 1 ドメインの説明が子カテゴリ情報を含むように強化されています。
- `taxonomy.json`: IAB Content Taxonomy v3.1 の全データ。Tier 2 以降の分類に使用されます。

## 他のプロジェクトでの利用について

現状の `iab-hybrid` CLI は、主に人間が直接結果を確認することを想定した、読みやすい形式でのテキスト出力を行います。

他のシステムやプロジェクトから本パッケージの分類機能を利用する場合、`HybridIABClassifier` クラスを直接インポートして使用することを推奨します。これにより、分類結果を Python のオブジェクトとして直接取得でき、より柔軟な連携が可能です。クイックスタートのセクションに記載されているコード例を参照してください。

CLI の出力を他のプログラムで直接パースすることも不可能ではありませんが、将来的に CLI の出力形式が変更される可能性も考慮すると、Python クラス経由での利用が最も安定した方法となります。JSON 形式での出力オプション (`--json`) も提供していますが、これも主に人間による確認や簡単なスクリプトでの利用を想定しています。
