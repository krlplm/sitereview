################################################################################
#Script to fetch the URL categorization from BlueCoat SiteReviewer API
################################################################################

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import json
import requests
import sys
import os

class SiteReview(object):
    def __init__(self):
        self.baseurl = "http://sitereview.bluecoat.com/rest/categorization"
        self.useragent = {"User-Agent": "Mozilla/5.0"}

    def sitereview(self, url):
        payload = {"url": url}
        
        try:
            self.req = requests.post(
                                    self.baseurl,
                                    headers=self.useragent,
                                    data=payload
                                    )
        except requests.ConnectionError:
            sys.exit("[-] ConnectionError: " \
                     "A connection error occurred")

        return json.loads(self.req.content)

    def check_response(self, response):

        if self.req.status_code != 200:
            sys.exit("[-] HTTP {} returned".format(req.status_code))

        elif "error" in response:
            sys.exit(response["error"])

        else:
            self.category = BeautifulSoup(response["categorization"], "lxml").get_text()
            self.date = BeautifulSoup(response["ratedate"], "lxml").get_text()[0:35]
            self.url = response["url"]



def site(url):
    s = SiteReview()
    response = s.sitereview(url)
    s.check_response(response)
    border = "=" * (len("BlueCoat Site Review") + 2)

    #print "\n{0}\n{1}\n{0}\n".format(border, "Blue Coat Site Review")
    print "URL: {}\n{}\nCategory: {}\n".format(
                                                              s.url,
                                                              s.date,
                                                              s.category
                                                              )

def main(lst):
   with open(os.path.join(lst), 'rb') as f:
    	for url in f:
   		s = SiteReview()
    		response = s.sitereview(url)
    		s.check_response(response)
    		border = "=" * (len("BlueCoat Site Review") + 2)

    		#print "\n{0}\n{1}\n{0}\n".format(border, "Blue Coat Site Review")
    		print "URL: {}\n{}\nCategory: {}\n".format(
                                                              s.url,
                                                              s.date,
                                                              s.category
                                                              )

if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-u", "--url", type=str, help="Submit domain/URL to Blue Coat's Site Review")
    p.add_argument("-l", "--lst", type=str, help="include the list of URLs separated by new line specifying the absolute path")
    args = p.parse_args()
    if args.url:
    	site(args.url)
    elif args.lst:
	main(args.lst)
    else:
	print "\n" + "Note: Please supplement the single url by using switch -u or a list of urls with the path by using switch -l" + "\n"	
else:
    pass
