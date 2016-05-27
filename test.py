from HTMLParser import HTMLParser 
from monkeylearn import MonkeyLearn
 
ml = MonkeyLearn('e8eae74a9f2d5f20d01e91ca3bc4bfbfadbe4322')
text_list = ["demoras en el subte", "buen estado del subte"]
module_id = 'cl_9mso8PPo'
res = ml.classifiers.classify(module_id, text_list, sandbox=True)
print 'resultados sentimiento: '
print res.result

class StreamHTMLParser(HTMLParser):
	def handle_data(self, data):
		self.data = data

	def getData(self):
		return self.data;

parser = StreamHTMLParser()
parser.feed(u'<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>')
test = parser.getData();
print 'test: ' + test
