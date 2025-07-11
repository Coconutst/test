@echo off
echo ===== 升级智能体工具依赖 =====
echo.

if not exist deepseek_agent_env (
    echo 虚拟环境不存在，请先运行初始安装
    pause
    exit /b 1
)

echo 激活虚拟环境...
call deepseek_agent_env\Scripts\activate.bat

echo 升级pip...
python -m pip install --upgrade pip

echo 安装新的工具依赖...
pip install beautifulsoup4>=4.12.0
pip install duckduckgo-search>=3.9.0
pip install qrcode>=7.4.0
pip install pillow>=10.0.0
pip install psutil>=5.9.0
pip install pandas>=2.0.0
pip install lxml>=4.9.0

echo.
echo 测试工具安装...
python -c "import bs4; print('✓ BeautifulSoup4安装成功')"
python -c "import duckduckgo_search; print('✓ DuckDuckGo搜索安装成功')"
python -c "import qrcode; print('✓ QRCode安装成功')"
python -c "import psutil; print('✓ Psutil安装成功')"
python -c "import pandas; print('✓ Pandas安装成功')"

echo.
echo ===== 工具升级完成 =====
echo 现在可以使用以下命令测试工具：
echo python test_tools.py
echo.
pause
