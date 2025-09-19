from django.db import models

class BridgePhoto(models.Model):
    sfn = models.CharField(max_length=50, help_text="Structure File Number")
    inspection_id = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='bridge_photos/')
    thumbnail = models.ImageField(upload_to='bridge_photos/thumbnails/', blank=True, null=True)

    class Meta:
        # This explicitly sets the table name in the database
        db_table = 'Bridge_Photos'

    def __str__(self):
        return f"Photo for SFN {self.sfn}"
