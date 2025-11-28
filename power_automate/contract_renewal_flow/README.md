# 契約・更新期限リマインダー & 自動交渉下準備フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせ、契約更新期限の検知と通知、交渉準備の自動化を行うテンプレートです。

- 契約台帳 (SharePoint リスト/Excel) を定期スキャンし、30/14/7日前にリマインドを送信します。
- 期限に応じたテンプレートメッセージを Teams / Outlook へ送付し、関連資料を SharePoint に集約します。
- 仕入先ポータルや見積取得などの前処理を Power Automate for desktop で自動実行する想定です。

## 構成ファイル

| ファイル | 用途 |
| --- | --- |
| `cloud_flow_definition.json` | クラウドフロー本体の定義 (pac CLI でインポート可能な定義)。 |
| `pad_flow_outline.md` | Power Automate for desktop のアクション手順例。クラウドフローからデスクトップフローを起動する前提です。 |

## インポートと設定

1. `cloud_flow_definition.json` を [Power Platform CLI](https://learn.microsoft.com/power-platform/developer/cli/introduction) または Power Automate ポータルの「My flows」→「Import」から読み込みます。
2. インポート時に以下の接続参照を環境の接続にマップしてください。
   - SharePoint, Office 365 Outlook, Microsoft Teams, Power Automate for desktop
3. フロー内のパラメータを自組織の値に置き換えます。
   - `siteAddress`: 契約台帳と資料を保存する SharePoint サイト URL。
   - `contractListName`: 契約台帳のリスト名 (例: `Contracts`)。
   - `documentLibrary`: 契約書/見積を格納するドキュメント ライブラリ (例: `Shared Documents`)。
   - `teamsChannelId`: 通知先 Teams チャネル ID (`19:xxxxx@thread.tacv2` 形式)。
   - `noticeOffsets`: リマインド送信のオフセット日数 (例: `30,14,7`)。
4. Power Automate for desktop 側で `pad_flow_outline.md` の手順を参考に UI フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. 毎朝 7:00 (日本時間) に定期トリガーで開始。
2. `noticeOffsets` で指定した日数分だけ更新期限が近い契約を SharePoint から取得。
3. 契約ごとに通知テンプレート (30/14/7日前で出し分け) を生成し、Teams と Outlook に送信。
4. 関連資料リンクを添付し、既存の見積/稟議ファイルをドキュメント ライブラリへ整理。
5. 仕入先ポータルからの見積取得や更新条件確認が必要な場合はデスクトップフローを起動し、結果をリストに記録。

## 注意点

- フィルター条件や通知メッセージは `cloud_flow_definition.json` 内の式を調整してください。
- 契約台帳の期限フィールド名 (`RenewalDate` など) を実データに合わせて変更してください。
- 仕入先ポータルの UI 変更に備え、PAD 側ではセレクタの再学習やリトライ (WAIT/RETRY) を設定してください。
