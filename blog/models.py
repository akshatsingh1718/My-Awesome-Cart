from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=60, default='')
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=30000, default='')
    views = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to="blog/images", default="")
    pub_date = models.DateField(auto_now=True)
    ##########################
    # head0 = models.CharField(max_length=500, default="")
    # chead0 = models.CharField(max_length=5000, default="")
    # head1 = models.CharField(max_length=500, default="")
    # chead1 = models.CharField(max_length=5000, default="")
    # head2 = models.CharField(max_length=500, default="")
    # chead2 = models.CharField(max_length=5000, default="")

    def __str__(self):
        return self.title


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    phone = models.IntegerField(default=0)
    desc = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.name}({self.msg_id})'


class BlogpostComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    # self because it is pointing on BlogpostComment obj
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:15] + " by " + self.user.username + "(" + str(self.sno) + ")"
