import mechanicalsoup
import sys
import time

if __name__ == '__main__':
    browser = mechanicalsoup.StatefulBrowser()
    searchterms = [ x.strip() for x in open(sys.argv[1]).readlines() ]
    outfile = sys.argv[2]
    for term in searchterms:
        browser.open("https://duckduckgo.com/")
        browser.select_form('#search_form_homepage')
        browser["q"] = term
        browser.submit_selected()

        srch = '-'*5 + ' ' + term + ' ' + '-'*5
        count = 0
        res = []
        for link in browser.get_current_page().select('a.result__a'):
            res.append( link.text + ' -> ' + link.attrs['href'] )
            print( link.text, '->' , link.attrs['href'] )
            count += 1
            if count == 4:
                break
        print('\n')
        with open(outfile,'a') as out:
            out.write(srch + '\n')
            out.write('\n'.join(res))
            out.write('\n\n')
        time.sleep(10.0)
            
