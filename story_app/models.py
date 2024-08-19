from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from os.path import join


# Create your models here.
def story_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'story_{instance.id}_{current_time}.{ext}'
    return join('media/stories/', filename)


class Story(models.Model):
    title = models.CharField(max_length= 255)
    contributions = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'story_created_by')
    image = models.ImageField(upload_to= story_image_upload_path, blank= True, null= True)

    def __str__(self):
        return self.title
