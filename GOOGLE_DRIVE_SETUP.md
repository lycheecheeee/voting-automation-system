## 設定 Google Drive 認證

### 步驟 1：取得 Google API 認證

1. 訪問 https://console.cloud.google.com/
2. 建立新項目
3. 啟用 **Google Drive API**
4. 建立 **OAuth 2.0 Desktop Application** 認證
5. 下載 `credentials.json`
6. 放到 `voting-automation/` 資料夾

### 步驟 2：首次執行認證

執行應用時，會自動打開瀏覽器要求授權：
- 選擇你的 Google 帳號
- 授予存取 Google Drive 的權限
- 系統會自動生成 `token.pickle` 檔案

### 步驟 3：共享 Google Drive 資料夾

你的 Drive 資料夾：
```
https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH
```

資料夾 ID：`1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH`

系統會自動在此資料夾下建立 `投票_YYYYMMDD` 子資料夾，存放：
- CSV 報告
- JSON 數據
- 5 張投票圖片

---

## 自動功能

每次點擊「生成新議題」，系統會：

1. ✅ 生成 5 張投票圖片（PNG，1200x675px）
2. ✅ 生成 CSV 報告（所有文案）
3. ✅ 生成 JSON 數據
4. ✅ 自動上傳到你的 Google Drive
5. ✅ 建立週資料夾整理

---

## 圖片內容

每張圖片包含：
- 投票題號
- 主問題
- 4 個投票選項
- 分類標籤
- 生成日期

設計適合社交媒體分享。

---

## 故障排除

### 如果出現 "認證失敗"

1. 檢查 `credentials.json` 是否存在
2. 刪除 `token.pickle`，重新執行（會重新授權）
3. 確保 Google 帳號有該資料夾的編輯權限

### 如果無法上傳到 Drive

1. 檢查網絡連接
2. 確保資料夾 ID 正確
3. 檢查 Google Drive API 是否啟用

---

## 自訂設定

編輯 `app.py`：

```python
# 修改 Google Drive 資料夾 ID
GOOGLE_DRIVE_FOLDER_ID = "1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH"
```

編輯 `image_generator.py`：

```python
# 修改圖片尺寸
width, height = 1200, 675  # 改為你想要的尺寸

# 修改顏色
bg_color = (245, 247, 250)
title_color = (102, 126, 234)
```

---

## API 端點

```
POST /api/generate          # 生成 + 上傳到 Drive
GET  /api/image/<id>       # 取得投票圖片
GET  /api/upload-status    # 檢查上傳狀態
```
