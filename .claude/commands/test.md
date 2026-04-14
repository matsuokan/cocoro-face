---
description: バックエンドとフロントエンドのテストを実行する
---
以下の順序でテストを実行してください：

## Backend Tests
```bash
cd backend
pytest -v --cov=. --cov-report=term-missing
```
カバレッジが80%未満の場合はテストを追加してください。

## Frontend Type Check
```bash
cd frontend
npm run typecheck
```
型エラーがある場合はすべて修正してください。

## 結果報告
テスト結果をサマリーしてください：
- バックエンドテスト: PASS/FAIL（カバレッジ%）
- フロントエンド型チェック: PASS/FAIL（エラー数）
