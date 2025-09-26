import os
import sys
import time
from datetime import datetime,timedelta
from pprint import pprint
from openpyxl import load_workbook

from common.Grids import CustomGrid, GRIDS as gr
from common.Chrome import Scraper
from common.Log import Log

def main():
    def OKClick(cg):
        excel_path = cg.getValue("inExcel")
        workbook = load_workbook(excel_path)


        # シートを取得
        sheet = workbook.active  # 現在のアクティブなシート
        urls = [cell.value for cell in sheet['L']]
        chrome1 = os.getenv('APPDATA') + '\\Chrome'
        print(chrome1)
        scraper = Scraper(chrome1)
        cnt = 0
        for r in range(1,len(urls)):
            cnt = cnt + 1
        cg.start_progress_bar("progress1", cnt)
        n = 0
        for r in range(1,len(urls)):
            if (urls[r].startswith("https://www.loewe.com")):
                price = scraper.get_text_by_class('capds-product__price--active')
                print(price)
                n = n + 1
                scraper.open(urls[r])
                cg.set_progress("progress1", n)
                cg.update_idletasks()

        scraper.quit()

    def CancelClick(cg):
        print("cancel")

    def ExitClick(cg):
        print("exit")
        sys.exit()

    settings = {
        "title":"価格チェックツール",
        "width":600,
        "height":500,
        "grids":[
            {
                "type":gr.LABEL,
                "caption":"価格チェックツール"
            },
            {
                "type":gr.FILE_OPEN,
                "name":"inExcel",
                "label":"定義Excel",
                "title":"定義Excelファイルを選択してください",
                "init":"",
                "file_type":[("定義Excel", "*.xlsx")]
            },
            {
                "type":gr.INPUT,
                "name":"outCSV",
                "label":"出力CSV",
                "init":"",
                "check":{
                }
            },
            {
                "type":gr.PROGRESS_BAR,
                "name":"progress1",
            },
            {
                "type":gr.BUTTONS,
                "buttons":[
                    {
                       "caption":"実行",
                        "callback":OKClick
                    },
                    {
                        "caption":"Cancel",
                        "callback":CancelClick
                    },
                    {
                        "caption":"終了",
                        "callback":ExitClick
                    },
                ]
            },
            {
                "type":gr.MESSAGE,
                "name":"message",
                "lines":6,
            }
        ]
    }
    cg = CustomGrid(settings)

if __name__ == '__main__':
    main()
    