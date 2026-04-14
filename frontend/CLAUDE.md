# Frontend Rules

- React関数コンポーネントのみ（クラスコンポーネント禁止）
- default export禁止（named exportのみ）
- Tailwindのみでスタイリング（別途CSSファイル作成禁止）
- API呼び出しは src/api/client.ts 経由のみ
- 変更後に必ず npm run typecheck を実行
