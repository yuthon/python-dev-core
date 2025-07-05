# python-dev-core

Python開発のためのコアユーティリティパッケージ

## 概要

`python-dev-core`はPython開発における共通的な機能を提供するコアパッケージです。自動ロギング機能やユーティリティ関数など、開発効率を向上させるツールを提供します。

## 特徴

- **自動ロギング**: メタクラスとデコレータによる自動ログ計装
- **開発効率化**: 汎用的なヘルパー関数とユーティリティ
- **型安全**: Python 3.13以降の最新型ヒント機能を活用
- **高品質コード**: 厳格なlintとテストによる品質保証

## インストール

### pipでのインストール

```bash
pip install python-dev-core
```

### 開発環境のセットアップ

```bash
git clone https://github.com/yourusername/python-dev-core.git
cd python-dev-core
uv sync
```

## 使用方法

### 自動ロギング

#### クラスの自動計装

```python
from python_dev_core import AutoLogMeta

class MyService(metaclass=AutoLogMeta):
    def process_data(self, data: list[str]) -> dict[str, int]:
        # メソッドの開始/終了が自動的にログ出力される
        result = {}
        for item in data:
            result[item] = len(item)
        return result

# 使用例
service = MyService()
service.process_data(["hello", "world"])
# DEBUG: MyService.process_data called with args=(['hello', 'world'],), kwargs={}
# DEBUG: MyService.process_data returned {'hello': 5, 'world': 5} (0.0001 s)
```

#### モジュール/関数の自動計装

```python
from python_dev_core import instrument
import my_module

# モジュール全体を計装
instrument(my_module)

# 個別の関数を計装
@instrument
def calculate_sum(numbers: list[int]) -> int:
    return sum(numbers)
```

### ログレベルの制御

環境変数`LOG_LEVEL`でログレベルを制御できます。

```bash
export LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
python your_script.py
```

## 開発

### 必要環境

- Python 3.13以上
- uv (パッケージマネージャー)

### 開発コマンド

```bash
# コードフォーマット
make format

# リント
make lint

# 型チェック
make typecheck

# テスト実行
make test

# すべてのチェック実行
make check
```

## プロジェクト構造

```
python-dev-core/
├── src/
│   └── python_dev_core/
│       ├── __init__.py
│       ├── core/           # コアロジック
│       └── utils/          # ユーティリティ
│           ├── __init__.py
│           ├── helpers.py
│           └── logging/    # ロギング機能
├── tests/                  # テストコード
├── pyproject.toml         # プロジェクト設定
├── Makefile              # 開発タスク
└── README.md             # このファイル
```

## ライセンス

MIT License

## 作者

Hashimoto

## 貢献

バグ報告や機能要望は、GitHubのissueにて受け付けています。

プルリクエストを送る際は：
- `make format`,`make lint`,`make typecheck`を実行してすべてのチェックが通ることを確認
- 新機能にはテストを追加
- ドキュメントを更新