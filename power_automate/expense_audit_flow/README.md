# 経費・精算処理の自動チェック フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせ、経費申請の自動チェック・差戻し・会計システムへの転記を行う例です。

- Forms で申請された経費データを SharePoint リストへ集約し、領収書画像を AI Builder の「領収書」モデルで読み取り、ポリシー違反を自動判定します。
- 違反時は差戻しコメントを Teams / メールで通知し、再申請用リンクを自動付与します。
- 承認対象の申請は Power Automate for desktop でオンプレ会計システムへ入力し、結果を SharePoint と申請者へフィードバックします。
- 接続先 URL やリスト名は環境に合わせて変更してください。

## 構成ファイル

| ファイル | 用途 |
| --- | --- |
| `cloud_flow_definition.json` | クラウドフロー本体の定義 (pac CLI でインポート可能な定義)。 |
| `pad_flow_outline.md` | Power Automate for desktop のアクション手順例。クラウドフローからデスクトップフローを呼び出すことを前提としています。 |

## インポートと設定

1. `cloud_flow_definition.json` を [Power Platform CLI](https://learn.microsoft.com/power-platform/developer/cli/introduction) または Web ポータルの「My flows」→「Import」から読み込みます。
2. インポート時に以下の接続参照を環境の接続にマップします。
   - Microsoft Forms, SharePoint, Office 365 Outlook, Microsoft Teams, AI Builder, Power Automate for desktop
3. フロー内パラメータを自組織の値に置き換えます。
   - `siteAddress`: 経費申請リストを配置する SharePoint サイト URL。
   - `expenseListName`: 経費申請リスト名 (例: `ExpenseRequests`)。
   - `receiptLibrary`: 領収書ファイルを格納するドキュメント ライブラリ名。
   - `formsId`: 申請元の Microsoft Forms ID。
   - `teamsChannelId`: 通知を送る Teams チャネル ID。
4. Power Automate for desktop 側で `pad_flow_outline.md` を参考に会計システム入力フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. Microsoft Forms の新規応答をトリガーに開始し、応答詳細を取得します。
2. SharePoint リストへ申請データを登録し、添付された領収書画像/ファイルをドキュメント ライブラリに保存します。
3. AI Builder 領収書モデルで金額・日付・店舗名を抽出し、申請内容と照合してポリシー違反を検出します (上限超過・休日利用・重複申請など)。
4. 違反がある場合は差戻しコメントを生成し、Teams メッセージとメールで通知。SharePoint にステータスを更新します。
5. クリアした申請は PAD を呼び出して会計システムへ入力し、戻り値 (成功/失敗、伝票番号) を SharePoint と通知先に反映します。
6. すべてのステップでログ (実行時刻、AI 解析結果、PAD 戻り値、通知結果) を SharePoint リスト列として記録します。

## 注意点

- ポリシー条件 (`maxAmount`, `holidayCheck`, `duplicateDays`) は `cloud_flow_definition.json` でパラメータ化しています。
- PAD 側では UI 変更に備えてセレクタの安定化、リトライ、スクリーンショット取得を実装してください。
- 本サンプルはテンプレートです。実環境では社内規程や DLP ポリシーに合わせて調整してください。
