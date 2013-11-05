from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from tribus.web.cloud.models import Package
from django.contrib.auth.models import User

class PackageIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    autoname = indexes.EdgeNgramField(model_attr='Package')
    description = indexes.CharField(model_attr='Description', null = True)
    
    def get_model(self):
        return Package
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
class UserIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    username = indexes.CharField(model_attr='username')
    autoname = indexes.EdgeNgramField(model_attr='get_full_name', use_template = True)
    description = indexes.CharField(model_attr='description', null = True)
    
    def get_model(self):
        return User
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()