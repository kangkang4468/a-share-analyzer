@echo off
chcp 65001 > nul
echo ==================================================
echo  A股智能分析终端 - 实时数据更新
echo ==================================================
echo.
echo 正在拉取全A股最新实盘价格并注入 HTML 页面...
echo.
python "%~dp0get_stocks.py"
echo.
echo 完成！请在浏览器中刷新 stock_analysis.html 查看最新数据。
echo ==================================================
pause
