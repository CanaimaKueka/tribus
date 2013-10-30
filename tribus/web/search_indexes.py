from haystack import indexes
from tribus.web.packages.models import Package

class PackageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    name = indexes.CharField(model_attr='Package')
    auto_name = indexes.EdgeNgramField(model_attr='Package')
    
    def get_model(self):
        return Package
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()