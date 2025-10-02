from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from lunch_service.apps.menus.models import Menu

User = get_user_model()


class Vote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'votes'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ['user', 'date']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} voted for {self.menu.restaurant.name} on {self.date}"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)


class VotingResult(models.Model):

    date = models.DateField(unique=True)
    results = models.JSONField()  
    total_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voting_results'
        verbose_name = 'Voting Result'
        verbose_name_plural = 'Voting Results'
        ordering = ['-date']

    def __str__(self):
        return f"Voting results for {self.date} ({self.total_votes} votes)"

    @classmethod
    def get_or_create_for_date(cls, date):

        try:
            return cls.objects.get(date=date)
        except cls.DoesNotExist:
            votes = Vote.objects.filter(date=date)
            results = {}
            total_votes = votes.count()
            
            for vote in votes:
                restaurant_name = vote.menu.restaurant.name
                if restaurant_name not in results:
                    results[restaurant_name] = {
                        'restaurant_id': vote.menu.restaurant.id,
                        'votes': 0,
                        'percentage': 0
                    }
                results[restaurant_name]['votes'] += 1
            
            for restaurant_data in results.values():
                if total_votes > 0:
                    restaurant_data['percentage'] = round(
                        (restaurant_data['votes'] / total_votes) * 100, 2
                    )
            
            return cls.objects.create(
                date=date,
                results=results,
                total_votes=total_votes
            )
