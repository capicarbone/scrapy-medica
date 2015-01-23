from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector, Selector

class DmozSpider(BaseSpider):
	name = "medica"
	allowed_domains = ["info-medica.net"]
	start_urls = [
		"http://info-medica.net"
	]

	archivo = None
	cont = 0

	def parse(self, response):        
		return [FormRequest(url="http://info-medica.net/searchdoctor.php",
			formdata={'city':'0', 'category': '', 'surname':''},
			callback=self.doctors_page)]

	def doctors_page(self, response):  

		s = Selector(response=response)  	
		
		doctors_urls = s.xpath('//section//a/@href').extract()[1:-1]

		if self.archivo is None:
			self.archivo = open("docs", 'wb')

		for doctor_elem in doctors_urls:
			self.cont = self.cont + 1    		
			
		requests = []

		if len(doctors_urls) != 0:			
			next_page_url = s.xpath("//div[@class=\"functions\"]/a/@href").extract()[-1]
			self.log("Iria a la pagina " + next_page_url, level=log.DEBUG)       

			for url in doctors_urls:
				# Se agrega la url de cada doctor
				requests.append(Request(url="http://info-medica.net/" + url, callback=self.take_doctor))

			requests.append(Request(url=next_page_url, callback=self.doctors_page))

			return requests

		return None

	def take_doctor(self, response):		
		#nombre = doctor.select("h2/text()").extract()[0]
		#especialidad = doctor.select("h3/text()").extract()[0]
		#self.archivo.write(nombre.encode('utf-8') + " - " + especialidad.encode('utf-8') + "\n")

		return None
		

		