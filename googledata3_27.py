import urllib2  # works fine with Python 2.7.9 (not 3.4.+)
import json
import time
 
def fetchPreMarket(ls_symbol, exchange="NASDAQ"):
    
    url = link+"%s:%s" % (exchange, ticker)
    u = urllib2.urlopen(url)
    content = u.read()
    data = json.loads(content[3:])
    info = data[0]
    # print info
    t = str(info["elt"])    # time stamp
    l = float(info["l"])    # close price (previous trading day)
    p = float(info["el"])   # stock price in pre-market (after-hours)
    # print t, l, p
    return (t,l,p)
 
    

if __name__ == '__main__':

    ls_symbol = ["FB", "TSLA"]

    link = "http://finance.google.com/finance/info?client=ig&q="
    for ticker in ls_symbol:
        t,l,p = fetchPreMarket(ls_symbol)

        print "%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (t, l, p, p-l,(p/l-1)*100.)
    

# p0 = 0
# while True:
#     t, l, p = fetchPreMarket("AAPL","NASDAQ")
#     if(p!=p0):
#         p0 = p
#         print("%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (t, l, p, p-l,
#                                                  (p/l-1)*100.))
#     time.sleep(60)