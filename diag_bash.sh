#!/bin/bash
# 诊断 bash 环境里的 python 和 playwright
echo "=== which python ==="
which python
echo "=== python executable ==="
python -c "import sys; print(sys.executable)"
echo "=== playwright check ==="
python -c "import playwright; print('playwright OK')" 2>&1
echo "=== exit: $? ==="
echo "=== cdp test ==="
cd /c/Users/Administrator/Desktop/传输/projects/atm-toolbox
python cdp_go_page.py 2>&1 | head -30
echo "=== cdp exit: $? ==="