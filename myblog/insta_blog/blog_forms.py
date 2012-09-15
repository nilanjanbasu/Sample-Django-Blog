from django.forms import ModelForm
from myblog.insta_blog.models import Article

class ArticleForm(ModelForm):
	class Meta:
		model=Article
		exclude = ('time_posted','author',)
