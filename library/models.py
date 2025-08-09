import logging

from django.core.validators import MinValueValidator
from django.db import models

from .choices import CategoryChoice

logger = logging.getLogger("__name__")


class Category(models.Model):
    name = models.CharField(max_length=20, choices=CategoryChoice.choices, unique=True)

    def __str__(self):
        return f"Category = {self.name}"


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    bio = models.TextField()

    def __str__(self):
        return f"Author = {self.name}"


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books", db_index=True
    )
    total_copies = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} is written by {self.author.name}"

    def is_available(self):
        """
        Check if the book has available copies
        """
        return self.available_copies > 0

    def decrement_copies(self):
        """
        Reduce availabe copies by 1
        """
        try:
            self.available_copies -= 1
            self.save(update_fields=["available_copies"])
        except Exception as e:
            logger.error(
                f"Error decrementing copies for {self.title} => {e}", exc_info=True
            )
            raise

    def increment_copies(self):
        """
        Increment availabe copies by 1
        """
        try:
            self.available_copies += 1
            self.save(update_fields=["available_copies"])
        except Exception as e:
            logger.error(
                f"Error incrementing copies for {self.title} => {e}", exc_info=True
            )
            raise
