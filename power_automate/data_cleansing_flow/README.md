# データクレンジング・マスタ同期フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせた、SharePoint/Excel リストの品質チェックとマスタ同期テンプレートです。

- SharePoint リストの重複・欠損・形式不備を検知し、候補値とともに Teams / Outlook へ通知します。
- クレンジング結果を SharePoint に反映し、必要に応じて PAD 経由でオンプレミスのマスタシステムへ同期します。
- 処理ログを別リストに保存し、後続の監査や可視化に活用できます。

## 構成ファイル

| ファイル | 用途 |
| --- | --- |
| `cloud_flow_definition.json` | クラウドフロー本体の定義 (pac CLI でインポート可能な定義)。 |
| `pad_flow_outline.md` | Power Automate for desktop のアクション手順例。クラウドフローからデスクトップフローを起動する前提です。 |

## インポートと設定

1. `cloud_flow_definition.json` を [Power Platform CLI](https://learn.microsoft.com/power-platform/developer/cli/introduction) または Web ポータルの「My flows」→「Import」から読み込みます。
2. インポート時に以下の接続参照を環境の接続にマップしてください。
   - SharePoint, Office 365 Outlook, Microsoft Teams, Power Automate for desktop
3. フロー内のパラメータを自組織の値に置き換えます。
   - `siteAddress`: データとログを保存する SharePoint サイトの URL。
   - `sourceListName`: クレンジング対象のリスト名 (または Excel テーブル名)。
   - `logListName`: 検出結果と同期状況を記録するリスト名。
   - `teamsChannelId`: 通知先 Teams チャネル ID (`19:xxxxx@thread.tacv2` 形式)。
   - `dedupField`: 重複判定に利用する列の内部名 (例: `Title` または `Email`).
4. Power Automate for desktop 側で `pad_flow_outline.md` の手順を参考に UI フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. 平日 8:00 (日本時間) に定期トリガーで開始し、対象リストを取得。
2. 必須列の欠損、メール形式不備、日付の将来/過去許容範囲外をチェックし、修正候補を生成。
3. 重複判定列 (`dedupField`) に基づき、重複レコードを検出して代表行を提案。
4. 検出内容をまとめた HTML テーブルを作成し、Teams と Outlook へ通知。
5. PAD を起動し、修正済みデータをオンプレミスのマスタへ同期 (必要な場合)。
6. フロー実行結果と同期ステータスをログリストへ記録。

## 注意点

- 必須列やメール/日付の検証条件は `cloud_flow_definition.json` の式を調整してください。
- 大量データの場合はページングやフィルター クエリを併用し、処理件数を制御してください。
- PAD 側での同期処理では、UI 変更に備えたセレクタ管理やリトライ設計を行ってください。
