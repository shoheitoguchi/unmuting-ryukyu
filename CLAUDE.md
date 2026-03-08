# Unmuting Ryukyu — CLAUDE.md

## プロジェクト概要
**Unmuting Ryukyu** は、渡口翔平（Shohei Toguchi）による沖縄の歴史・文化・アイデンティティを世界に発信するドキュメンタリーサイトです。
YouTubeチャンネル [@letsgokinawa](https://www.youtube.com/@letsgokinawa) と連動しています。

## 技術スタック
- **フレームワーク**: Astro v5（SSG）
- **TypeScript**: strict モード（`astro/tsconfigs/strict` を継承）
- **モジュール**: ESM（`"type": "module"`）
- **スタイル**: インラインスタイル（CSS-in-JSなし、外部CSSファイルなし）

## ディレクトリ構造
```
src/
├── pages/
│   ├── index.astro       # トップページ（ヒーロー・ミッション・サービス）
│   ├── about.astro       # 渡口翔平について
│   ├── videos.astro      # 動画一覧
│   ├── services.astro    # 動画制作サービス
│   ├── contact.astro     # お問い合わせ
│   └── blog/
│       ├── index.astro          # ブログ一覧
│       ├── battle-of-okinawa.astro
│       ├── sanshin-legend.astro
│       ├── three-reasons-okinawa.astro
│       └── uchinaanchu-in-hawaii.astro
├── layouts/
│   └── Layout.astro      # 共通レイアウト（ナビ・フッター含む）
└── assets/               # 画像・静的ファイル
```

## デザインシステム（カラー・フォント）
### カラー
| 変数名（概念） | 値 | 用途 |
|---|---|---|
| Crimson Red | `#8B1D25` | アクセント・CTAボタン・装飾ライン |
| Navy Blue | `#1C2C4F` | 見出し・ダークセクション背景 |
| Warm Cream | `#F0EBE3` | 明るいセクション背景・白テキスト代替 |
| Gold | `#C8A86A` | サブタイトル・装飾文字 |
| Light Beige | `#E8E2D8` | セクション区切り背景 |
| Border | `#D0C5BA` | 罫線・カード境界 |
| Body Text | `#4A3F3B` | 本文テキスト（明るい背景上） |
| Muted Text | `#A8B8C8` | 説明文（暗い背景上） |

### フォント
| 用途 | フォント |
|---|---|
| 見出し（日英） | `'Shippori Mincho', 'Noto Serif JP', serif` |
| 本文（日英） | `'Noto Serif JP', serif` |
| UI・ラベル | `'Noto Sans JP', sans-serif` |

## コーディングルール

### TypeScript
- `any` 型の使用禁止
- 型アサーション（`as`）は最小限に
- コンポーネントのpropsは必ず型定義する

### Astro
- 新しいページは `src/pages/` に `.astro` ファイルで作成
- ブログ記事は `src/pages/blog/` に追加
- 共通レイアウトは必ず `Layout.astro` を使う
- スタイルは既存のインラインスタイル方式に合わせる（新たにCSSファイルを作らない）

### コンテンツ
- 言語: **英語メイン**（グローバル向け発信）
- トーン: ドキュメンタリー的・重厚・誠実
- 沖縄・琉球の歴史的事実は正確に扱う

## よく使うコマンド
```bash
npm run dev      # 開発サーバー起動（localhost:4321）
npm run build    # 本番ビルド
npm run preview  # ビルド結果のプレビュー
```

## 新しいブログ記事を追加する時のテンプレート
```astro
---
import Layout from '../../layouts/Layout.astro';
---

<Layout title="記事タイトル | Unmuting Ryukyu">
  <!-- 記事コンテンツ -->
</Layout>
```

## 関連リソース
- YouTube: https://www.youtube.com/@letsgokinawa
- 2nd-Brainのコンテキスト: `/Desktop/2nd-Brain/00_システム/00_UserProfile/00_マスター(Master_Context).md`
- プロジェクトノート: `/Desktop/2nd-Brain/01_プロジェクト/`
