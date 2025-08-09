from django.db import models
from user.models import CustomUser
from library.models import Book
from uuid import uuid4
from datetime import date

class Borrow(models.Model):
    borrow_id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"borrow id: {self.borrow_id}, user: {self.user.username}"
    
    def is_overdue(self):
        return date.today()  > self.due_date
    
    def days_late(self):
        return (date.today()  - self.due_date).days
