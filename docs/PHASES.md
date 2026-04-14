# Development Phases - cocoro-face

## Phase 1 - Foundation（現在）
**Goal**: 画像1枚のフェイススワップが動くこと

- [x] リポジトリ初期構成（全ドキュメント・設定ファイル）
- [x] scripts/install.sh（conda環境 + FaceFusion + 依存パッケージ）
- [x] FastAPI骨格 + POST /api/swap/image
- [x] facefusion_service.py（subprocessラッパー）
- [x] 最小フロントエンド（アップロード→スワップ→ダウンロード）
- [x] systemdサービス化（scripts/start.sh）
- [ ] **サーバーへのインストール実施**
- [ ] **動作確認（curlでスワップ成功）**

**Exit Criteria**: `curl`で画像スワップが成功すること

---

## Phase 2 - Video Support
**Goal**: 動画フェイススワップの非同期処理

- [ ] BackgroundTasks + job_id管理（SQLite）
- [ ] GET /api/job/{job_id} ステータスAPI
- [ ] DELETE /api/job/{job_id} 削除API
- [ ] WebSocket進捗通知 (WS /ws/job/{job_id})
- [ ] フロントエンドにプログレスバー追加
- [ ] 動画アップロード対応（target_video）
- [ ] job_service.py SQLite実装

**Exit Criteria**: 30秒動画のスワップがUI上で進捗確認できること

---

## Phase 3 - UI Polish
**Goal**: AKOOLライクなUI完成

- [ ] ドラッグ&ドロップアップロード
- [ ] 複数顔選択UI（face_selector_order）
- [ ] 設定パネル（品質・モデル選択・pixel_boost）
- [ ] 結果履歴（SQLite）
- [ ] 顔プリセット保存
- [ ] レスポンシブデザイン対応
- [ ] ダークモード
- [ ] エラーメッセージのUI改善

**Exit Criteria**: 非エンジニアが迷わず使えること

---

## Phase 4 - Production Hardening（オプション）
**Goal**: 本番運用レベルの安定性

- [ ] systemdサービス定義ファイル（cocoro-face.service）
- [ ] ログローテーション設定
- [ ] ストレージ使用量監視・自動クリーンアップ
- [ ] バックエンドテストカバレッジ90%以上
- [ ] nginx リバースプロキシ設定

**Exit Criteria**: 24時間無人運用でも安定動作すること
