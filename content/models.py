from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class AirlinePolicy(models.Model):
    airline_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    content = RichTextField(default= "Cancellation\nCancellation Fee = Airline's Fee + Ural Tours Fee\nRefund Amount = Paid Amount - Cancellation Fee\nRe-issue\nRe-issue Fee = Airline's Fee + Fare Difference + Ural Tours Fee\n*The airline's fee is indicative and per person. Convenience fee is non-refundable.",
                            config_name='snippet'
    )

    def __str__(self):
        return self.airline_name
    
