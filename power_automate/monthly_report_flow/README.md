# 月次レポート作成・配信フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせた、月次レポートの集計・配信テンプレートです。

- SharePoint リストや Excel テーブルのデータを月次で取得し、HTML テーブルとファイルとして保存します。
- Teams への配信と Outlook でのメール送信を同時に行い、共有リンクまたは添付でレポートを配布します。
- オンプレ BI / 会計システムからの追加データ取得や PDF 化を Power Automate for desktop 側で補完する想定です。

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
   - `siteAddress`: データ/出力を保存する SharePoint サイトの URL。
   - `sourceListName`: 集計元のリスト名 (例: `MonthlyData`)。
   - `reportLibrary`: レポートを保存するドキュメント ライブラリ (例: `Shared Documents`)。
   - `teamsChannelId`: 配信先 Teams チャネル ID (`19:xxxxx@thread.tacv2` 形式)。
4. Power Automate for desktop 側で `pad_flow_outline.md` の手順を参考に UI フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. 毎月 1 日 9:00 (日本時間) に定期トリガーで開始。
2. 集計期間の開始/終了日を算出し、SharePoint リストから対象期間のデータを取得。
3. 取得データを HTML テーブル化し、SharePoint ドキュメント ライブラリにレポート ファイルとして保存。
4. Teams チャネルへ報告メッセージとレポート リンクを投稿し、Outlook メールで HTML 本文＋添付を送信。
5. オンプレソースの追加データが必要な場合はデスクトップフローを起動し、完了結果をログ リストに記録。

## 注意点

- 集計期間の算出ロジックやフィルター条件は `cloud_flow_definition.json` 内の式を調整してください。
- 大量データを扱う場合は SharePoint のしきい値に注意し、件数制限やページングを併用してください。
- レポートの PDF 化や外部システム抽出は PAD 側で実装し、クラウドフローから渡すパラメータと戻り値を統一してください。
