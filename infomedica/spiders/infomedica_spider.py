from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector

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
        	callback=self.despues_post)]

    def despues_post(self, response):    	

    	hxs = HtmlXPathSelector(response)
    	doctores = hxs.select("//article")

    	if self.archivo is None:
    		self.archivo = open("docs", 'wb')

    	for doctor in doctores:
    		self.cont = self.cont + 1
    		nombre = doctor.select("h2/text()").extract()[0]
    		especialidad = doctor.select("h3/text()").extract()[0]
    		self.archivo.write(nombre.encode('utf-8') + " - " + especialidad.encode('utf-8') + "\n")

    	if len(doctores) != 0:
    		sig_url = hxs.select("//div[@class=\"functions\"]/a/@href").extract()[-1]
    		self.log("Iria a la pagina " + sig_url, level=log.DEBUG)

    		return [Request(url=sig_url, callback=self.despues_post)]

    	