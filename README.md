# LeetCode 練習環境

## 環境安裝

執行以下指令安裝虛擬環境與相依套件：

```sh
uv sync
```

## 專案結構

```
src/
  leetcode/         # LeetCode 解題程式
  loader.py         # 測試資料載入工具
test/
  data/             # 測試資料與答案
  test_main.py      # 測試主程式
  conftest.py       # pytest 設定
```

## 如何新增題目

1. 在 `src/leetcode/` 建立 `{name}.py`，將 LeetCode 上的程式碼複製進來，**檔名與 function 名稱需相同**

   ```py
   class Solution:
       def twoSum(self, nums: list[int], target: int) -> list[int]:
           ...
   ```

2. 在 `test/data/` 建立 `{name}.txt`，依序填入測試輸入與預期答案（每組一行）

   ```
   [2,7,11,15]
   9
   [0,1]
   [3,2,4]
   6
   [1,2]
   ```

## 執行測試

### 執行所有測試

```sh
uv run pytest
```

### 執行特定題目

```sh
uv run pytest --target twoSum
```

### 使用 VS Code 偵錯

開啟目標題目的 `.py` 檔，按 `F5` 啟動偵錯，將自動對當前開啟的檔案執行測試。

## 注意事項

- 測試資料格式使用 JSON，例如陣列寫成 `[1,2,3]`，布林值寫成 `true` / `false`
- 浮點數答案允許 ±10⁻⁵ 的誤差
- `test/data/` 與 `src/leetcode/*.py`（除 `__init__.py` 與 `entry.py`）已加入 `.gitignore`，不會被提交
