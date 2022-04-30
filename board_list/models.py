from djongo import models
from mongoengine import Document, fields
# Create your models here.

class Post(models.Model):
    uid = models.CharField(max_length=256, verbose_name='objectID'),
    title = models.CharField(max_length=256, verbose_name='제목'),
    link = models.URLField(max_length=512, verbose_name='링크'),
    site = models.CharField(max_length=32, verbose_name="사이트"),
    date = models.DateTimeField(max_length=256, verbose_name="작성일"),
    # date_get = models.DateTimeField(max_length=256, verbose_name="몇분전"),
    viewers = models.IntegerField(max_length=32, verbose_name="조회수"),
    writer = models.CharField(max_length=64, verbose_name="작성자"),
    comments = models.IntegerField(null=True, max_length=64, verbose_name="댓글"),
    createdAt = models.DateTimeField(max_length=256, verbose_name="createdAt")


    def __str__(self):
        return self.title

    class Meta:
        db_table = "커뮤니티 List"
        verbose_name = "커뮤니티 List"
        verbose_name_plural = "커뮤니티 List"

#리스트
#번호  제목  글쓴이    작성일                 조회수       사이트
#no  title  writer   date, date_Get      viewers      site