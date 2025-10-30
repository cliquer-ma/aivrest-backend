from django.db import models

from core.models import (
    BaseModel
)

class Post(BaseModel):
    user            = models.TextField(default="")
    content         = models.TextField(default="")
    attachements    = models.JSONField(default=list)

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(Post, 10)
        super().save(*args, **kwargs)

class PostLike(BaseModel):
    post        = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    user        = models.TextField(default="")

    def __str__(self):
        return self.reference
    
    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(PostLike, 10)
        super().save(*args, **kwargs)
        
class PostComment(BaseModel):
    post        = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    user        = models.TextField(default="")
    content     = models.TextField(default="")
    
    def __str__(self):
        return self.reference
    
    def save(self, *args, **kwargs):
        if self.pk is None :
            self.reference = generate_reference(PostComment, 10)
        super().save(*args, **kwargs)

