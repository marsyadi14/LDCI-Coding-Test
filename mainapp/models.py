from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser

class Status(models.TextChoices):
    ACTIVE = "ACT", _("Active")
    BANNED = "BAN", _("Banned")

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255)
    display_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    user_status = models.CharField(max_length=3, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.display_name}@{self.username}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def activate(self):
        self.user_status = Status.ACTIVE
        
    def ban(self):
        self.user_status = Status.BANNED
    
    class Meta:
        ordering = ["username"]
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(fields=["username"], name="username_idx"),
        ]
    
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_content = models.CharField(max_length=140, blank=True)
    loc_lon = models.FloatField(blank=True, null=True)
    loc_lat = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_status = models.CharField(max_length=3, choices=Status.choices)
    liker_id = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)
    poster_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="poster"
    )
    repost_id = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="repost"
    )
    
    def __str__(self):
         return f"{self.post_content[:10]}..."
    
    class Meta:
        ordering = ["post_id"]
        verbose_name = "post"
        verbose_name_plural = "posts"
        indexes = [
            models.Index(fields=["post_id"], name="post_id_idx"),
        ]