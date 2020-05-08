import re
import requests
from lxml import html
from bs4 import BeautifulSoup


#Packages
from library.package import schedule


class Lectio:

	def __init__(self, Username, Password, schoolId, personType):
		self.Username = Username
		self.Password = Password
		self.SchoolId = schoolId
		self.personType = personType

		LOGIN_URL = "https://www.lectio.dk/lectio/{}/login.aspx".format(self.SchoolId)

		# Start requests session and get eventvalidation key
		session = requests.Session()
		result = session.get(LOGIN_URL)
		# print(result.text)
		tree = html.fromstring(result.text)
		authenticity_token = list(set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

		# Create payload
		payload = {
			"m$Content$username2": self.Username,
			"m$Content$password2": self.Password,
			"m$Content$passwordHidden": self.Password,
			"__EVENTVALIDATION": authenticity_token,
			"__EVENTTARGET": "m$Content$submitbtn2",
			"__EVENTARGUMENT": "",
			"LectioPostbackId": ""
		}

		# Perform login
		result = session.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

		# Getting student id
		dashboard = session.get("https://www.lectio.dk/lectio/{}/forside.aspx".format(self.SchoolId))
		soup = BeautifulSoup(dashboard.text, features="html.parser")
		findID = soup.find("a", {"id": "s_m_HeaderContent_subnavigator_ctl01"}, href=True)

		#Formats the url for person type
		if (self.personType == "Student"):
			self.personId = (findID['href']).replace('/lectio/' + self.SchoolId + '/forside.aspx?elevid=', '')
		elif (self.personType == "Teacher"):
			self.personId = (findID['href']).replace('/lectio/' + self.SchoolId + '/forside.aspx?laererid=', '')
		else:
			print("Error. Cant get the type of person.")
			return

		self.Session = session
	
	def getSchedule(self):
		result = schedule.schedule(self, self.Session, self.SchoolId, self.personType, self.personId)

		return result