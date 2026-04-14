# HANDOFF - 2026-04-14

## 完了したタスク
- Phase 1: プロジェクト初期構成（全ドキュメント・設定ファイル・スケルトンコード）
  - CLAUDE.md（ルート / backend / frontend）
  - .claude/settings.json、commands（handoff / test / phase）
  - docs/（ARCHITECTURE / API / ECOSYSTEM / PHASES / STRUCTURE）
  - backend スケルトン（main.py / config.py / schemas.py / routers / services）
  - frontend スケルトン（Vite + React + TS + Tailwind、全コンポーネント）
  - scripts/install.sh、scripts/start.sh
  - .gitignore、.env.example、facefusion.ini
  - GitHub push（main ブランチ）

## 未完了・中断中
- FaceFusion の実際のインストール（scripts/install.sh を実行する必要あり）
- バックエンドの動作確認（conda env "facefusion" がサーバーに存在しない）
- フロントエンドの依存パッケージインストール（npm install 未実施）

## 次セッションで最初にやること（ファイル名・コマンド付き）
1. サーバー (192.168.50.112) にSSH接続
2. `bash scripts/install.sh` を実行してconda環境とFaceFusionをセットアップ
3. `cd backend && conda run -n facefusion uvicorn main:app --reload --port 8010` で起動確認
4. `curl http://192.168.50.112:8010/health` でヘルスチェック
5. `curl -X POST http://192.168.50.112:8010/api/swap/image -F "source_image=@test_face.jpg" -F "target_image=@test_photo.jpg" --output result.png` でスワップ確認

## 判明した問題・注意事項
- FaceFusion 3.6.0 のCLI引数は `python -m facefusion headless-run` を使用
  - `--config-path facefusion.ini` でINIファイルを渡す
  - `--source-paths` と `--target-path` と `--output-path` が必須
- inswapper_128_fp16 モデルは初回にダウンロードが発生する（GitHub / HuggingFace）
- GFPGAN 1.4 も同様に初回ダウンロードが必要
- `download_providers = github huggingface` はfacefusion.iniに設定済み

## 現在のフェーズ
Phase 1 - Foundation（スケルトン完成・サーバーセットアップ待ち / 約50%）

Exit Criteria達成状況：
- [ ] curlで画像スワップが成功すること → **未達成（サーバーセットアップ必要）**
