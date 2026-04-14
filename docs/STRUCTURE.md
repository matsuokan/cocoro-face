# Structure Freeze List - cocoro-face

このファイルに記載されたファイル・ディレクトリは、**構造（ファイル名・パス・エクスポート名）を変更禁止**。
変更が必要な場合は、このファイルを更新して理由をコメントとして記録すること。

## 凍結ファイル一覧

### Configuration
| File | Frozen Since | Reason |
|---|---|---|
| `CLAUDE.md` | 2026-04-14 | Claude Code自動読み込みパス |
| `.claude/settings.json` | 2026-04-14 | Claude Code権限設定 |
| `facefusion.ini` | 2026-04-14 | FaceFusion設定ファイルパス |
| `.env` / `.env.example` | 2026-04-14 | 環境変数の統一管理 |

### Backend Entry Points
| File | Frozen Since | Reason |
|---|---|---|
| `backend/main.py` | 2026-04-14 | FastAPI app entry point |
| `backend/config.py` | 2026-04-14 | 全環境変数の単一管理点 |
| `backend/services/facefusion_service.py` | 2026-04-14 | FaceFusion唯一の呼び出し口 |

### Frontend Entry Points
| File | Frozen Since | Reason |
|---|---|---|
| `frontend/src/api/client.ts` | 2026-04-14 | 全APIコールの単一管理点 |

### Scripts
| File | Frozen Since | Reason |
|---|---|---|
| `scripts/install.sh` | 2026-04-14 | CI/CDやドキュメントから参照 |
| `scripts/start.sh` | 2026-04-14 | systemdから参照 |

### Docs
| File | Frozen Since | Reason |
|---|---|---|
| `docs/HANDOFF.md` | 2026-04-14 | /handoffコマンドのターゲット |
| `docs/STRUCTURE.md` | 2026-04-14 | このファイル自身 |

## 変更禁止の定義
- ファイルの**移動・リネーム・削除**禁止
- **エクスポート名**の変更禁止（関数名・クラス名・変数名）
- ファイルの**内容追加・修正**は許可（構造が変わらない範囲で）

## 凍結解除手順
1. このファイルの該当行を削除または更新
2. `docs/ARCHITECTURE.md` の関連セクションを更新
3. `git commit -m "refactor: unfreeze <filename> - <reason>"` でコミット
