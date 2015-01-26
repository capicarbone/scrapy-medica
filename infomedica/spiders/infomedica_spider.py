from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector, Selector

from infomedica.items import DoctorItem

class DmozSpider(BaseSpider):
	name = "medica"
	allowed_domains = ["info-medica.net"]
	start_urls = [
		"http://info-medica.net"
	]

	archivo = None	

	def parse(self, response):        
		return [FormRequest(url="http://info-medica.net/searchdoctor.php",
			formdata={'city':'2', 'category': '', 'surname':''},
			callback=self.doctors_page)]

	def doctors_page(self, response):  

		s = Selector(response=response)  	
		
		doctors_urls = s.xpath('//section//a/@href').extract()[1:-1]		
			
		requests = []

		if len(doctors_urls) != 0:			
			next_page_url = s.xpath("//div[@class=\"functions\"]/a/@href").extract()[-1]  

			for url in doctors_urls:
				# Se agrega la url de cada doctor
				requests.append(Request(url="http://info-medica.net/" + url, callback=self.take_doctor))

			requests.append(Request(url=next_page_url, callback=self.doctors_page))

			return requests

		return None

	def take_doctor(self, response):	
		s = Selector(response=response)
		
		result = s.css("h4 a::text").extract()

		if (len(result) > 0 ):

			doctor = DoctorItem()
			doctor['correo'] = result[0]			
			doctor['nombre'] = s.css(".info h2::text").extract()[0]			
			doctor['especialidad'] = s.xpath("//h4/text()").extract()[0]

			if self.archivo is None:
				self.archivo = open("docs", 'wb')
			
			self.archivo.write("%s - %s - %s  \n" % (doctor['nombre'].encode('utf-8'), doctor['correo'].encode('utf-8'), doctor['especialidad'].encode('utf-8')))

			#print "%s - %s - %s" % (correo, nombre, especialidad)
			return doctor

		return None
		

		