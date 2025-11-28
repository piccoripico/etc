# ユーザアカウント／権限のライフサイクル補助フロー

Power Automate (クラウドフロー) と Power Automate for desktop を組み合わせ、入社・異動・退職の申請を一元化し、Azure AD / M365 権限付与とオンプレ資産への反映を自動化する例です。

- SharePoint リストで申請を受け付け、承認後に Azure AD グループ追加やメールボックス設定、Teams 招待を自動実行します。
- 異動・退職は不要グループの削除や共有リソース権限の整理を行い、関係者へ Teams / メールで結果通知します。
- Power Automate for desktop (PAD) でオンプレ AD やレガシー権限管理ツールへの追加・削除を自動入力し、結果をクラウドフローへ返します。
- 接続先 URL やグループ名は環境に合わせて変更してください。

## 構成ファイル

| ファイル | 用途 |
| --- | --- |
| `cloud_flow_definition.json` | クラウドフロー本体の定義 (pac CLI でインポート可能な定義)。 |
| `pad_flow_outline.md` | Power Automate for desktop のアクション手順例。クラウドフローからデスクトップフローを呼び出すことを前提としています。 |

## インポートと設定

1. `cloud_flow_definition.json` を [Power Platform CLI](https://learn.microsoft.com/power-platform/developer/cli/introduction) または Web ポータルの「My flows」→「Import」から読み込みます。
2. インポート時に以下の接続参照を環境の接続にマップします。
   - SharePoint, Office 365 Outlook, Microsoft Teams, Azure AD, Power Automate for desktop
3. フロー内パラメータを自組織の値に置き換えます。
   - `siteAddress`: 申請リストを配置する SharePoint サイト URL。
   - `requestListName`: 入社/異動/退職を管理するリスト名 (例: `UserLifecycleRequests`)。
   - `teamsChannelId`: 結果を通知する Teams チャネル ID。
   - `defaultLicenses`: 付与する M365 SKU の配列 (例: `ENTERPRISEPACK`)。
   - `baseGroups`: 標準で追加する Azure AD グループの配列。
4. Power Automate for desktop 側で `pad_flow_outline.md` を参考にオンプレシステムへの反映フローを作成し、クラウドフローの **Run a flow built with Power Automate for desktop** アクションから呼び出してください。

## クラウドフローの主な処理

1. SharePoint リストの新規アイテムをトリガーに開始し、申請内容 (氏名、UPN、区分、開始/終了日、所属、マネージャー) を取得します。
2. 区分に応じて以下を実行します。
   - **入社**: Azure AD ユーザの作成または有効化、ライセンス付与、標準グループ追加、Teams への歓迎メッセージ送信。
   - **異動**: 新部署グループへ追加し旧部署グループから削除、共有リソース権限の入替を記録し通知。
   - **退職**: 端末・メールボックスのサインインブロック、ライセンス除去、共有権限とグループを削除、代理人への自動転送設定。
3. PAD を呼び出し、オンプレ AD やレガシー権限管理ツールに同様の変更を自動入力させ、戻り値 (成功/失敗、詳細メッセージ) を受け取ります。
4. 実行結果を SharePoint リストに書き戻し、申請者と管理チームへ Teams メッセージとメールで通知します。
5. すべてのステップでログ (実行時刻、実施操作、PAD 戻り値、通知結果) をリスト列として記録します。

## 注意点

- グループ名やライセンス SKU は `cloud_flow_definition.json` でパラメータ化しています。環境に合わせて変更してください。
- PAD 側では UI 変更に備えてセレクタ安定化、リトライ、スクリーンショット取得を実装してください。
- 本サンプルはテンプレートです。実環境では社内ガバナンスや DLP ポリシーに合わせて調整してください。
