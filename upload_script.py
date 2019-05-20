import arrow #loads time feature
import csv #loads csv reading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

chrome_options = webdriver.ChromeOptions() #Make sure chromedriver.exe is in the same directory as the script or this gets ugly)
chrome_options.add_argument("--disable-infobars")
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("<page>") # Opens webpage

#login block
user = driver.find_element_by_id("usid") #Login Request For = id control_1		
user.send_keys("<username>")
password = driver.find_element_by_id("pwid")
password.send_keys("<password>")
driver.find_element_by_id("btnSubmit").click()

f = open('Printer_List.csv') # assigns variable to the csv
reader = csv.DictReader(f) #tells python to read that variable

for row in reader: #for loop to comb dataset
	
	time.sleep(2) #lets server catch its breath

	driver.find_element_by_id("option-admin").click() #clicks admin tab
	driver.find_element_by_id("btnAddConfig").click() #clicks add dropdown button

	#BASICS TAB

	#Column A/VPSXID section, must be done before clicking anything!
	vpsid = driver.find_element_by_id("vpsname")
	vpsid.send_keys("TSTVPS02") #identifies instance

	#Columns B, C, D
	pname = driver.find_element_by_id("prtname")
	pname.send_keys(row['Printer Name'])
	plname = driver.find_element_by_id("prtlname")
	plname.send_keys(row['Printer Long Name'])
	gname = driver.find_element_by_id("grpname")
	gname.send_keys(row['Group Name'])

	#Column E / driver and location selection block
	driver.find_element_by_id("btnOpenDriverSelection").click() 
	driver.find_element_by_css_selector("[data-drv='HP Universal Printing PCL 6 <+> Version (08/23/2017,61.210.01.22695)']").click()
	driver.find_element_by_id("btnDriverSelectionSelect").click()
	#driver.find_element_by_id("btnOpenLocationPicker").click() <<< Need to parse locations
	locus = driver.find_element_by_id("location")
	locus.send_keys(row['Branch'])

	#Column F 
	driver.find_element_by_id("option-commtype-pjl").click()

	#Column G
	ipadd = driver.find_element_by_id("tcphost")
	ipadd.send_keys(row['TCP Host'])
	#rport = driver.find_element_by_id("tcprport")
	#rport.send_keys("9100")

	#Retain Time
	retention = driver.find_element_by_id("rtime")
	retention.send_keys("72")

	#FILTERS TAB
	#need to expand the Filter 1 area first
	driver.find_element_by_id("filters-tab-wrapper").click() #clicking filters tab
    # the three fields
	dtype = driver.find_element_by_id("ftype1")
	dtype.send_keys("PDF")
	expand = driver.find_element_by_xpath("//*[text()='Filter 1']").click()
	cmd = driver.find_element_by_id("filter1")
	cmd.send_keys("/opt/lrs/convert1/lrscvdr")
	args = driver.find_element_by_id("farg1") 
	args.send_keys("PDF2PS &KEYPDF2PS -i &infile -type PDF -o &outfile -type PS -logdir &TMPDIR -logfile &PRINTER")

	#exit iteration
	driver.find_element_by_id("btnUpdate").click()


