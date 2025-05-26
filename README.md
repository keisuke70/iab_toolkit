# ハイブリッド IAB 分類システム

このパッケージは、IAB Content Taxonomy v3.1 分類のための最適化されたハイブリッドアプローチを提供します。このアプローチは、埋め込みベースの Tier 1 検出と LLM ベースの Tier 2 分類を組み合わせたものです。

## 特徴

- **2.2 倍のパフォーマンス向上**: Tier 1 検出において、API 呼び出し回数を 40+回から 1 回に削減
- **100%の Tier 1 精度**: 包括的なテストで達成
- **事前計算済み埋め込み**: `.npy`ファイルを使用し、即座に類似度計算を実行
- **日本語コンテンツサポート**: 実際の日本語テキストサンプルで完全にテスト済み
- **包括的なユーザープロファイリング**: 年齢層、ギーク度、コンテンツの洗練度

## アーキテクチャ

1.  **最適化された Tier 1 検出**: 事前計算された埋め込みとコサイン類似度を使用
2.  **LLM ベースの Tier 2 分類**: 正確なカテゴリ分類のための絞り込まれたタクソノミーサブセット
3.  **ユーザープロファイル分析**: 人口統計学的および行動パターンの推定

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
- **日本語サポート**: 5 種類のサンプルタイプで完全に検証済み

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

**基本的な使い方:**

```bash
# 直接テキストを指定して分類
iab-hybrid "ここに分類したいテキストを入力します。"

# ファイルを指定して分類
iab-hybrid --file path/to/your/content.txt

# 日本語サンプルテストを実行 (結果はログファイルに出力されます)
iab-hybrid --test

# 結果をJSON形式で出力
iab-hybrid "テキスト" --json

# 詳細なログを出力 (冗長モード)
iab-hybrid "テキスト" -v
```

**オプション:**

- `text` (引数): 分類対象のテキストコンテンツ。`--file` や `--test` を使用する場合は省略可能です。
- `--file, -f FILE_PATH`: 分類対象のテキストファイルへのパス。
- `--test`: 日本語サンプルテキストを使用したテストスイートを実行します。
- `--json`: 結果を JSON 形式で標準出力します。
- `--verbose, -v`: 詳細なログ（スタックトレースなど）を含む冗長モードを有効にします。

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
