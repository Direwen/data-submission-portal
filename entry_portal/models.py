from django.db import models

class DataEntry(models.Model):
    TEXT_CATEGORY = 'T'
    IMAGE_CATEGORY = 'I'
    CATEGORY_CHOICES = [
        (TEXT_CATEGORY, 'Text'),
        (IMAGE_CATEGORY, 'Image'),
    ]
    
    content = models.TextField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=TEXT_CATEGORY)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
    
    def __str__(self):
        return self.content
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_reviewed']),
        ]