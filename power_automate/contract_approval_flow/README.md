# 契約書・申請書の承認ワークフロー自動化フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせた、契約書・申請書の承認フロー例です。

- SharePoint リストに契約・申請が登録されたらクラウドフローが起動し、承認依頼・リマインド・結果記録を自動化します。
- 承認後のデータ転記やオンプレシステム入力は、Power Automate for desktop で記録した UI 操作をサブフローとして呼び出します。
- 接続先 URL やリスト名は環境に合わせて値を変更してください。

## 構成ファイル

| ファイル | 用途 |
| --- | --- |
| `cloud_flow_definition.json` | クラウドフロー本体の定義 (pac CLI でインポート可能な定義)。 |
| `pad_flow_outline.md` | Power Automate for desktop のアクション手順例。クラウドフローからデスクトップフローを起動する前提です。 |

## インポートと設定

1. `cloud_flow_definition.json` を [Power Platform CLI](https://learn.microsoft.com/power-platform/developer/cli/introduction) または Web ポータルの「My flows」→「Import」から読み込みます。
2. インポート時に以下の接続参照を環境の接続にマップしてください。
   - SharePoint, Office 365 Outlook, Microsoft Teams, Approvals, Power Automate for desktop
3. フロー内の下記パラメータを自組織のリスト名・URL に置き換えます。
   - `siteAddress`: 契約書リストを配置している SharePoint サイトの URL。
   - `listName`: 契約書リスト名 (例: `Contracts`)。
   - `documentLibrary`: 契約書ファイルを格納するドキュメント ライブラリ名。
4. Power Automate for desktop 側で `pad_flow_outline.md` の手順を参考に UI フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. SharePoint リストへの新規アイテム追加をトリガーに開始。
2. 添付された契約書ファイルを SharePoint の指定ライブラリにコピーし、ファイルリンクを取得。
3. `Start and wait for an approval` で承認者へ Adaptive Card 付き依頼を送信。
4. 承認待ちで 3 日ごとに Teams でリマインド (承認完了で早期終了)。
5. 承認結果をリストに書き戻し、結果メールを申請者に送信。
6. 承認済みの場合のみデスクトップフローをキューに投入し、オンプレシステムへの転記を自動化。

## 注意点

- 承認待ちのリマインド間隔 (`PT72H`) やリマインド回数 (`3`) は `cloud_flow_definition.json` 内で変更可能です。
- 大量実行時はフローの同時実行数を制限し、PAD 側でリトライと例外スクリーンショット取得を設計してください。
- フロー定義はサンプルです。実導入時はセキュリティ ポリシーや DLP の要件に従って調整してください。
