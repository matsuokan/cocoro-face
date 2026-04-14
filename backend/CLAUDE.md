# Backend Rules

- 型アノテーション必須（mypy strict）
- 例外はすべてHTTPExceptionに変換してからraise
- FaceFusion呼び出しは services/facefusion_service.py 経由のみ
- 環境変数は config.py でまとめて管理
- テスト実行: pytest -v --cov=. --cov-report=term-missing
- カバレッジ80%以上を維持
