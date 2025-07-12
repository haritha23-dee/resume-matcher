from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# ✅ Resume Model: Stores uploaded resume file
class Resume(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/')  # saved to media/resumes/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ✅ ResumeMatch Model: Stores each role match with score & category
class ResumeMatch(models.Model):
    resume = models.ForeignKey(Resume, related_name='matches', on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.resume.name} → {self.role} ({self.score})"

# ✅ Delete file from storage when Resume is deleted from DB
@receiver(post_delete, sender=Resume)
def delete_resume_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
