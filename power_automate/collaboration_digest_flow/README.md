# コラボ情報統合通知フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせて、Planner/SharePoint/Outlook の情報を 1 つの朝会メッセージにまとめるテンプレートです。

- 毎朝の定期トリガーで、期限が近い Planner タスク、新着 SharePoint ページ/ドキュメント、当日の予定を集約します。
- 集約結果を Teams チャネルとメールに配信し、必要に応じてデスクトップフローでオンプレ会議室管理や来訪者受付システムへの登録を補完します。
- 重要な期限や新着更新に気づき漏れしないことを目的としたサマリー通知です。

## 構成ファイル

| ファイル | 用途 |
| --- | --- |
| `cloud_flow_definition.json` | クラウドフロー本体の定義 (pac CLI でインポート可能な定義)。 |
| `pad_flow_outline.md` | Power Automate for desktop のアクション手順例。クラウドフローからデスクトップフローを起動する前提です。 |

## インポートと設定

1. `cloud_flow_definition.json` を [Power Platform CLI](https://learn.microsoft.com/power-platform/developer/cli/introduction) または Web ポータルの「My flows」→「Import」から読み込みます。
2. インポート時に以下の接続参照を環境の接続にマップしてください。
   - Microsoft Planner, SharePoint, Office 365 Outlook, Microsoft Teams, Power Automate for desktop
3. フロー内のパラメータを自組織の値に置き換えます。
   - `siteAddress`: SharePoint サイト URL (更新情報を取得する元)。
   - `newsListName`: 新着ページ/お知らせのリストまたはライブラリ名。
   - `libraryName`: 新着ドキュメントを確認するドキュメントライブラリ。
   - `teamsChannelId`: 通知先 Teams チャネル ID (`19:xxxxx@thread.tacv2` 形式)。
   - `plannerPlanId` / `plannerGroupId`: 期限が近いタスクを取得する Planner の Plan/Group ID。
4. Power Automate for desktop 側で `pad_flow_outline.md` の手順を参考に UI フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. 平日 8:00 (日本時間) に定期トリガーで開始し、当日 0:00〜翌日 0:00 の時間帯を計算します。
2. Planner の未完了タスクから期日が当日または翌日以内のものを抽出し、担当者/期限で整形します。
3. SharePoint で直近 24 時間に更新されたページ/ニュース、および新規ファイルを取得し、タイトルとリンクを抽出します。
4. Outlook の予定表から当日の予定を取得して件名・開始時刻をまとめます。
5. これらを HTML テーブル化して 1 つのメッセージ本文にまとめ、Teams チャネル投稿とメール送信を行います。
6. オンプレ会議室・受付システムへの同期が必要な場合、デスクトップフローを起動し、結果を Teams に返信します。

## 注意点

- Planner のタスク取得 API によるフィルターが不足する場合、`Filter array` アクションで期日と完了状態を判定してください。
- SharePoint のリスト/ライブラリが大きい場合は件数上限や期間条件を調整し、必要に応じてページングを有効化します。
- HTML テーブルをメール本文に埋め込む場合は `IsHtml` フラグを必ず `true` に設定してください。
- PAD 側に渡すパラメータ (会議室 ID、来訪者リストなど) と戻り値のスキーマをクラウドフローと合わせておくと、トラッキングが容易です。
