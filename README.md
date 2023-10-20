# Site Review
Blue Coat/Symantec Site Review Checker

## Description

This script can be used without a Bluecoat/Symantec sitereview API. 

This script makes use of selenium framework to fetch the categorization details. 

## Pre-requisites:

- Python 3.7+
- Download Chrome Driver compatible with the Browser version you run from https://chromedriver.chromium.org/downloads
  * Unzip and move to /usr/local/bin (MAC OS/Linux) 
  * On Windows, you may place it in any location and configure the path to chromedriver.exe under config.py
- For chrome versions 115 and newer, you will have to download the drivers from https://googlechromelabs.github.io/chrome-for-testing/#stable

## Package Dependencies:

- Install Selenium by running as below,  
```pip install selenium```

Most other package dependencies are by default available with the python installation.

## Usage

Sitereview.py simply takes Optional Arguments, url or lst, and submits it to the Site Review service:

```
How to Run:
sitereview.py [-c] [-l]

Arguments:
  -c cmd, --cmd <domain/ip>       Submit single domain/ip/url to Blue Coat's Site Review
  -l lst, --lst <path_to_file>    Include the list of domains/ip addresses/URLs separated by new line specifying the absolute path
  
Examples:
- python sitereview.py -c google.com
- python sitereview.py -c 8.8.8.8
- python sitereview.py -c https://www.test.com
- python sitereview.py -l domains.txt

Note: The list can be a combination of domains/ip addresses/URLs as well!

```
## Results
- The results are shown in the console and also written to the file results.csv

## Gotchas:

- In the event, the Site Review page prompts the captcha window, open up a new tab and enter the capctha manually.
- Due to time crunch, I haven't handled Capctha in my code but definitely on the feature list

## Benchmarking:

- Currently, I've tested like 200 domains in a list which are handled by the site review with out any issues. 
- However, most of my runs have seen the captcha prompt in between 200-220.
- Following the above hack may be of help but may impact 3-5 IOCs while you perform this.

