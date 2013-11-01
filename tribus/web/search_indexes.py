from haystack import indexes
from tribus.web.cloud.models import Package
from django.contrib.auth.models import User

class PackageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    name = indexes.CharField(model_attr='Package')
    auto_name = indexes.EdgeNgramField(model_attr='Package')
    destination = indexes.CharField(model_attr='Package')
    
    def get_model(self):
        return Package
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    
class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    destination = indexes.CharField(model_attr='username')
    user_name = indexes.CharField(model_attr='username')
    last_name = indexes.CharField(model_attr='get_full_name')
    auto_name = indexes.EdgeNgramField(model_attr='get_full_name')
    
    def get_model(self):
        return User
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()