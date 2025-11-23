SET PYTHONPATH=common
cd src
pyinstaller -w PriceChecker.py --onefile --add-data "common;common"
copy *.json dist
xcopy cs dist\cs /e /i /y
mkdir dist\Log


pause