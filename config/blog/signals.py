from .models import Article
# from .models import ArticleHistory
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
@receiver(post_save, sender=Article)
def Post_SaveArticleHistoryCreator(sender, instance, created, **kwargs):
    article = instance

    ArticleHistory.objects.create(
        article = article,
        title = article.title,
        slug = article.slug,
        category = article.category,
        description = article.description,
        thumbnail = article.thumbnail,
        creation_date = article.creation_date,
        publish_date = article.publish_date,
        update_date = article.update_date,
        status = article.status,
    )
"""