[WEB API](https://telegra.ph/api)


# 創建賬戶

使用此方法創建的 Telegraph。大多數人只需要一個帳戶，因此每個新用戶都提供，以便每個保存和作者都需要管理員的通道access_token。

## short_name
（字符串，1-32 個字符）當前屬性。帳戶名稱，幫助多個用戶記住他們使用的帳戶。在Telegra.ph上的“編輯/”發布給用戶健康顯示，其他用戶看這個名字。

## author_name
( String, 0-128 characters )
創建新文章時使用的默認作者姓名。

## author_url
（字符串，0-512 個字符）
默認個人資料鏈接，當用戶點擊標題欄的作者時打開。可以是任何姓名，重點是 Telegram 個人資料或頻道。

---
##### https://api.telegra.ph/createAccount?short_name=kevin&author_name=kevin01.BRI
> {"ok":true,"result":{"short_name":"kevin","author_name":"kevin01.BRI","author_url":"","access_token":"0385b0c00e1fa2cb6d4589788b0431d87a6d0199c689c3924a7882a35a9c","auth_url":"https:\/\/edit.telegra.ph\/auth\/QMFRoL5ahOwmAYG2L8Wr2QvADWpJaXw0I9R6SUgaIL"}}
---

# 編輯賬戶信息

使用此方法更新有關電報帳戶的信息。提交編輯的參數。成功時，返回默認字段的帳戶對象。

## access_token ( String )
必須是。Telegraph帳戶的訪問令牌。

## short_name（字符串，1-32 個字符）
新帳戶名稱。

## author_name ( String, 0-128 characters )
創建新文章時使用的新默認作者姓名。

## author_url ( String, 0-512 characters )
新的默認個人資料鏈接，當用戶點擊標題的作者姓名時打開。可以是任何鏈接，或者是 Telegram 個人資料頻道。

---
##### https://api.telegra.ph/editAccountInfo?access_token=0385b0c00e1fa2cb6d4589788b0431d87a6d0199c689c3924a7882a35a9c&short_name=kevin&author_name=kevin01.BRI



