from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class WebscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['title'] = adapter['title'].lower()
        adapter['category'] = adapter['category'].lower()
        adapter['price'] = float(adapter['price'].replace('£', ''))

        stars = adapter['stars'].split(' ')[1]
        if stars == 'One':
            adapter['stars'] = 1
        elif stars == 'Two':
            adapter['stars'] = 2
        elif stars == 'Three':
            adapter['stars'] = 3
        elif stars == 'Four':
            adapter['stars'] = 4
        elif stars == 'Five':
            adapter['stars'] = 5

        is_available = adapter['availability'].split('\n')[2].replace('  ', '')
        if is_available == 'In stock':
            adapter['availability'] = True
        else:
            adapter['availability'] = False
        
        return item 
    
class CsvPipeline:
    def open_spider(self, spider):
        self.file = open('books.csv','wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def process_item(self, item, spider):   
        self.exporter.export_item(item)
        return item
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

