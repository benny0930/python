
import crawler.stock as stock
import sys, os


try:
    # aStockInfo = stock.start('0052')
    aStockInfo = stock.start('6488')
    print(aStockInfo)

    # for key in aStockInfo:
    #     print(key + " = " + aStockInfo[key][0])
    #     exit()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
