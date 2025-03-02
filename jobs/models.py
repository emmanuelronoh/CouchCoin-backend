from django.db import models
from django.utils.timezone import now
from users.models import User
from django.core.validators import MinValueValidator

class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('web_dev', 'Web Development'),
        ('ui_ux', 'UI/UX Design'),
        ('ai_ml', 'AI & Machine Learning'),
        ('writing', 'Content Writing'),
        ('marketing', 'Digital Marketing'),
        ('data_analysis', 'Data Analysis'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255, db_index=True)  # Indexed for search
    description = models.TextField()
    budget = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],  # Ensures no negative budgets
        help_text="Budget for the job in USD"
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='other', 
        help_text="Category of the job"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posted_jobs', 
        help_text="Client who posted the job"
    )
    freelancer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs',
        help_text="Freelancer assigned to the job"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='open', db_index=True
    )
    created_at = models.DateTimeField(default=now)  # Default timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto timestamp for updates
    status_updated_at = models.DateTimeField(auto_now=True)  # Tracks status changes
    is_active = models.BooleanField(default=True, help_text="Soft delete functionality")

    def soft_delete(self):
        """Soft delete a job instead of removing it from the database."""
        self.is_active = False
        self.save()

    def restore(self):
        """Restore a soft-deleted job."""
        self.is_active = True
        self.save()

    def __str__(self):
        return f"{self.title} - {self.status}"

    class Meta:
        ordering = ['-created_at']  # Show newest jobs first
        verbose_name = "Job Listing"
        verbose_name_plural = "Job Listings"
