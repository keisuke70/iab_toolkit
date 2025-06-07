# ハイブリッド IAB 分類システム

このパッケージは、IAB Content Taxonomy v3.1 分類のための最適化されたハイブリッドアプローチを提供します。このアプローチは、埋め込みベースの Tier 1 検出と LLM ベースの Tier 2 分類を組み合わせたものです。

## 特徴

- **事前計算済み埋め込み**: `.npy`ファイルを使用し、即座に類似度計算を実行
- **日本語コンテンツサポート**: 実際の日本語テキストサンプル（8 種類：自動車、美容、技術、ビジネス、健康、キャリア、教育、食品・飲料）で完全にテスト済み
- **包括的なユーザープロファイリング**: 年齢層、性別、ギーク度、メディア品質
- **高速処理**: 最適化により従来比 2.2 倍の高速化を実現
- **包括的 CLI**: テキスト分類、ファイル処理、テストスイート実行に対応

## アーキテクチャ

1.  **最適化された Tier 1 検出**: 事前計算された埋め込みとコサイン類似度を使用
2.  **LLM ベースの Tier 2 分類**: 正確なカテゴリ分類のための絞り込まれたタクソノミーサブセット
3.  **ユーザープロファイル分析**: 人口統計学的および行動パターンの推定

## 前提条件とセットアップ

### システム要件

- **Python**: 3.10 以上
- **OS**: Windows, macOS, Linux 対応
- **インターネット接続**: OpenAI API 呼び出し用

### OpenAI API キーの設定

このシステムは OpenAI API を使用するため、事前に API キーの設定が必要です。

1. **OpenAI API キーの取得**:

   - [OpenAI Platform](https://platform.openai.com/) にアクセス
   - アカウントを作成またはログイン
   - API Keys セクションで新しい API キーを生成

2. **環境変数の設定**:

   ```powershell
   # Windows (PowerShell)
   $Env:OPENAI_API_KEY="your-api-key-here"
   ```

   ```bash
   # macOS/Linux
   export OPENAI_API_KEY="your-api-key-here"
   ```

   **または .env ファイルを作成**:
   ```powershell
   # プロジェクトルートに .env ファイルを作成
   echo "OPENAI_API_KEY=your-api-key-here" | Out-File -FilePath .env -Encoding utf8
   ```

   **重要:** 本パッケージでは `python-dotenv` が依存関係に含まれており、`iab_toolkit._config` モジュールで自動的に `.env` ファイルが読み込まれます。追加のインストールや設定は不要です。

### インストール

**推奨: 仮想環境の使用**

```powershell
# 1. 仮想環境を作成
python -m venv .venv

# 2. 仮想環境を有効化
.\.venv\Scripts\Activate.ps1

# 3. パッケージをインストール（開発モード）
pip install -e .

# または開発依存関係も含めてインストール
pip install -e ".[dev]"
```

**Wheel ファイルからのインストール**:
```powershell
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
        print(f"    IAB番号: {cat.get('id', 'N/A')}") # IAB番号
        print(f"    信頼度: {cat.get('confidence', 0.0):.2f}") # 信頼度
else:
    print("  Tier 2カテゴリは見つかりませんでした。")

print("\nユーザープロファイル:")
if result.user_profile:
    print(f"  年齢層: {result.user_profile.age_range}") # 年齢層
    print(f"  性別: {result.user_profile.gender}") # 性別
    print(f"  ギークレベル: {result.user_profile.geek_level}/10") # 技術関心度
    print(f"  メディア品質: {result.user_profile.media_quality}") # メディアの質
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
- **日本語サポート**: 8 種類のサンプルタイプで完全に検証済み（自動車、美容、技術、ビジネス、健康、キャリア、教育、食品・飲料）

## プロジェクト構成

```
iab_toolkit/
├── pyproject.toml              # プロジェクト設定、依存関係、ビルド設定
├── README.md                   # このファイル（プロジェクト説明書）
├── .venv/                      # 仮想環境（pip install -e . 実行後に作成）
└── iab_toolkit/                # メインパッケージディレクトリ
    ├── __init__.py             # パッケージ初期化、主要クラスのエクスポート
    ├── _config.py              # 設定管理（OpenAI API キー、.env ファイル読み込み）
    ├── _embedding.py           # テキスト埋め込み生成（OpenAI API利用）
    ├── _gpt.py                 # OpenAI GPT モデル連携
    ├── cli.py                  # CLI インターフェース（iab-hybrid コマンド）
    ├── hybrid_iab_classifier.py # メイン分類器クラス
    ├── models.py               # データクラス定義（結果、プロファイルなど）
    ├── optimized_tier1_detector.py # 高速 Tier 1 検出器
    ├── test_japanese_samples.py # 技術者向けテストスイート
    ├── test_japanese_samples_client_report.py # クライアント向けレポート生成
    ├── test/                   # テスト結果出力フォルダ
    │   ├── *.log              # 技術テストログファイル
    │   └── *.txt              # クライアントレポートファイル
    └── data/                   # データファイル
        ├── tier1_embeddings.npy    # 事前計算済み埋め込み（39ドメイン）
        ├── tier1_domains.json      # Tier 1 ドメイン名リスト
        ├── tier1_taxonomy.json     # 最適化済みタクソノミー
        ├── taxonomy.json           # 完全な IAB タクソノミー v3.1
        └── japanese_*.txt          # 日本語テストサンプル（8種類）
```

### 主要ファイルの説明

**コア分類システム:**
- `hybrid_iab_classifier.py`: メインの分類器。Tier 1（埋め込み）+ Tier 2（LLM）のハイブリッド処理
- `optimized_tier1_detector.py`: 事前計算済み埋め込みによる高速 Tier 1 検出（2.2倍高速化）
- `models.py`: `UserProfile`、`FinalClassificationResult` などのデータ構造定義

**API 連携:**
- `_gpt.py`: OpenAI GPT-4 による Tier 2 分類とユーザープロファイル生成
- `_embedding.py`: OpenAI text-embedding-3-small による埋め込み生成
- `_config.py`: API キー管理、環境変数・.env ファイル自動読み込み

**CLI とテスト:**
- `cli.py`: `iab-hybrid` コマンドの実装（テキスト分類、ファイル処理、テスト実行）
- `test_japanese_samples.py`: 8種類の日本語サンプルでの技術的検証
- `test_japanese_samples_client_report.py`: ビジネス向け分析レポート生成

**最適化データ:**
- `tier1_embeddings.npy`: 39個の Tier 1 ドメインの事前計算済み埋め込み（1536次元）
- `tier1_domains.json`: 埋め込みファイルに対応するドメイン名の順序リスト
- `taxonomy.json`: IAB Content Taxonomy v3.1 完全版（700+ カテゴリ）

## CLI 利用方法

`iab-hybrid` コマンドを使用して、ターミナルから直接コンテンツ分類システムを利用できます。

### 基本的な使い方

```powershell
# 直接テキストを指定して分類
iab-hybrid "ここに分類したいテキストを入力します。"

# ファイルを指定して分類
iab-hybrid --file path/to/your/content.txt

# 日本語サンプルファイルを分類する例
iab-hybrid --file iab_toolkit/data/japanese_text_sample.txt

# JSON形式で結果を出力
iab-hybrid --json "テキスト内容"

# 詳細なログを出力（冗長モード）
iab-hybrid --verbose "テキスト内容"
```

### テストスイート実行

```powershell
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

| オプション        | 短縮形 | 説明                                                                                                                 |
| ----------------- | ------ | -------------------------------------------------------------------------------------------------------------------- |
| `--file`          | `-f`   | 分類対象のテキストファイルへのパス                                                                                   |
| `--test`          | -      | 技術者向け詳細テスト：全 8 種類の日本語サンプルをテストし、技術的な結果を`test/`フォルダにログファイルとして出力     |
| `--client-report` | -      | クライアント向けレポート：全 8 種類の日本語サンプルを分析し、ビジネス向けの読みやすいレポートを`test/`フォルダに生成 |
| `--json`          | -      | 結果を JSON 形式で出力（プログラム処理用）                                                                           |
| `--verbose`       | `-v`   | 詳細ログ出力を有効化（デバッグ用）                                                                                   |

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
   1. Auto Technology (IAB: 37) (95.0%)
   2. Auto Type (IAB: 38) (80.0%)
👤 User Profile:
   Age Range: 30-45
   Gender: neutral
   Geek Level: 7/10
   Media Quality: advanced
   Demographics: tech-savvy professional
⏱️ Processing Time: 4.179 seconds
============================================================
```

**JSON 出力:**

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
    "gender": "neutral",
    "geek_level": 8,
    "media_quality": "advanced",
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
    ```powershell
    pip install build
    ```
2.  ターミナルで `iab_toolkit` ディレクトリに移動します:
    ```powershell
    cd c:\Users\Ykeisuke\Documents\iab_toolkit
    ```
3.  ビルドコマンドを実行します:
    ```powershell
    python -m build
    ```
    これにより、`dist` ディレクトリ内に `.whl` ファイル（例: `iab_toolkit-0.3.0-py3-none-any.whl`）が作成されます。

### 他のプロジェクトへのインストール

作成された `.whl` ファイルを他のプロジェクト（または既知の場所）にコピーし、次のコマンドを実行します:

```powershell
pip install path/to/your/iab_toolkit-0.3.0-py3-none-any.whl
```

## トラブルシューティング

### 一般的な問題と解決方法

**1. OpenAI API キー関連のエラー**
```
Error: OpenAI API key not found
```
**解決方法:**
- PowerShell で環境変数を設定: `$Env:OPENAI_API_KEY="your-key"`
- または `.env` ファイルを作成: `OPENAI_API_KEY=your-key`
- API キーが有効で残高があることを確認

**2. 仮想環境の問題**
```
iab-hybrid: command not found
```
**解決方法:**
- 仮想環境を有効化: `.\.venv\Scripts\Activate.ps1`
- パッケージを再インストール: `pip install -e .`

**3. 依存関係の問題**
```
ModuleNotFoundError: No module named 'openai'
```
**解決方法:**
- 仮想環境内で依存関係を再インストール: `pip install -e .`
- 必要に応じて `pip install --upgrade pip`

**4. 日本語ファイルの文字化け**
```
UnicodeDecodeError
```
**解決方法:**
- ファイルが UTF-8 エンコーディングで保存されていることを確認
- `--file` オプション使用時にファイルパスが正しいことを確認

### サポートとフィードバック

問題が解決しない場合は、以下の情報を含めてお問い合わせください：
- Python バージョン (`python --version`)
- パッケージバージョン (`pip show iab-toolkit`)
- エラーメッセージの全文
- 実行したコマンド

## データファイル (主要なもの)

- `tier1_embeddings.npy`: Tier 1 ドメインの事前計算済み埋め込みベクトル（39 ドメイン、1536 次元）。
- `tier1_domains.json`: `tier1_embeddings.npy` に対応する Tier 1 ドメイン名の順序付きリスト。
- `tier1_taxonomy.json`: Tier 1 検出用に最適化・クリーンアップされたタクソノミーデータ。問題のあるエントリが除外され、Tier 1 ドメインの説明が子カテゴリ情報を含むように強化されています。
- `taxonomy.json`: IAB Content Taxonomy v3.1 の全データ。Tier 2 以降の分類に使用されます。

## 他のプロジェクトでの利用について

現状の `iab-hybrid` CLI は、主に人間が直接結果を確認することを想定した、読みやすい形式でのテキスト出力を行います。

他のシステムやプロジェクトから本パッケージの分類機能を利用する場合、`HybridIABClassifier` クラスを直接インポートして使用することを推奨します。これにより、分類結果を Python のオブジェクトとして直接取得でき、より柔軟な連携が可能です。クイックスタートのセクションに記載されているコード例を参照してください。

CLI の出力を他のプログラムで直接パースすることも不可能ではありませんが、将来的に CLI の出力形式が変更される可能性も考慮すると、Python クラス経由での利用が最も安定した方法となります。JSON 形式での出力オプション (`--json`) も提供していますが、これも主に人間による確認や簡単なスクリプトでの利用を想定しています。
