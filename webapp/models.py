from django.db import models

# Create your models here.
class FoodReviews(models.Model):
    product_id  = models.CharField(max_length=16)
    user_id     = models.CharField(max_length=16)
    name        = models.CharField(max_length=32)
    helpfulness = models.CharField(max_length=8)
    score       = models.DecimalField(max_digits=4, decimal_places=2)
    timestamp   = models.DateTimeField(blank=True, null=True)
    summary     = models.CharField(max_length=256)
    text        = models.TextField()

    def __str__(self):
        return '{} - review by {} ({})'.format(self.product_id, self.name, self.user_id)

    class Meta:
        verbose_name        = 'Food Review'
        verbose_name_plural = 'Food Reviews'
