# Power Automate for desktop: オンプレ会計システム転記フロー例

クラウドフローから `Run a flow built with Power Automate for desktop` で呼び出すことを想定した PAD のフロー構成例です。UI は各社システムに合わせて修正してください。

## 変数入力 (クラウドフローから渡す)
- `ContractId`: SharePoint リストのアイテム ID
- `ContractorName`: 契約相手名
- `Amount`: 契約金額
- `ApprovedDate`: 承認日 (yyyy-MM-dd)
- `DocumentLink`: 契約書ファイルの URL

## アクション手順
1. `Launch Excel` (必要なら) で転記済み ID やログを書き出すブックを開く。
2. `Launch application` でオンプレ会計/稟議システムを起動。
3. `Populate text field on window` を使い、以下のフィールドに値を入力。
   - 契約 ID / 案件番号: `ContractId`
   - 取引先: `ContractorName`
   - 金額: `Amount`
   - 承認日: `ApprovedDate`
   - 契約書リンク/備考: `DocumentLink`
4. 必須ドロップダウンやチェックボックスを `Select item in list` / `Set checkbox state` で設定。
5. `Click UI element in window` で保存/登録ボタンをクリック。
6. 正常終了時は `Write to Excel worksheet` でステータス「Posted」、失敗時は `Take screenshot of window` を実行し、`Excel` にエラー内容を記録。
7. `Close window` / `Terminate process` で後処理。

## リトライと例外
- `On block error` で 3 回までリトライするスコープを作成し、失敗ごとに待機 (`Delay 00:00:10`) を挟む。
- エラー時はスクリーンショットファイルを SharePoint のエラーフォルダーに `Upload file to SharePoint` で保存し、クラウドフローにステータスを返す。
