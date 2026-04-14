# cocoro-face

ローカル完全動作のフェイススワップWebアプリ。
AKOOLライクなUI/UXを持ち、プライバシー最優先・オフライン動作が絶対条件。

## Stack
- Engine  : FaceFusion 3.6.0 + InsightFace inswapper_128_fp16
- Backend : FastAPI (Python 3.12 / conda env "facefusion")
- Frontend: React + TypeScript + Tailwind CSS (Vite)
- GPU     : RTX PRO 6000 / VRAM 94.96GB / CUDA 12.8
- Server  : 192.168.50.112 (Debian 13, user: mdl)

## Commands
```bash
# Backend
cd backend && uvicorn main:app --reload --port 8010

# Frontend
cd frontend && npm run dev

# Test
cd backend && pytest
cd frontend && npm run typecheck
```

## Absolute Rules
1. 応急処置禁止・根本修正のみ。try/exceptでエラーを握りつぶさない
2. FaceFusionコアは直接編集しない。services/facefusion_service.py経由のみ
3. 新ファイル作成時は必ずdocs/ARCHITECTURE.mdを更新する
4. セッション終了前に必ず/handoffを実行する
5. 1タスク = 1コミット（prefix: feat/fix/refactor/docs）
6. 秘密情報はすべて.envで管理。ハードコード禁止
7. docs/STRUCTURE.mdに記載された凍結ファイルは構造変更禁止

## References
- アーキテクチャ詳細 : @docs/ARCHITECTURE.md
- API仕様            : @docs/API.md
- データスキーマ      : @docs/ECOSYSTEM.md
- 現在の作業状態      : @docs/HANDOFF.md
- フェーズ計画        : @docs/PHASES.md
- 構造凍結リスト      : @docs/STRUCTURE.md
