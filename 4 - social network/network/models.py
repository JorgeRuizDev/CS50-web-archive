from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    following = models.ManyToManyField("self", blank=True, symmetrical=False)



class Post(models.Model):
    user = models.ForeignKey(User, related_name="user_op", on_delete=models.CASCADE)
    users_liking = models.ManyToManyField(User,related_name="users_liking", blank=True)
    body = models.CharField(blank=False, null=False, max_length=4000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.date}: {self.body}"

    def like_count(self):
        return len(self.users_liking.all())

class Comment(models.Model):
    body = models.CharField(blank=False, null=False, max_length=4000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Test(models.Model):
    following = models.ManyToManyField(User)