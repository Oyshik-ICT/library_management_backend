from django.db import models

class CategoryChoice(models.TextChoices):
    FICTION = 'FICTION', 'Fiction'
    NON_FICTION = 'NON_FICTION', 'Non-Fiction'
    SCIENCE = 'SCIENCE', 'Science'
    HISTORY = 'HISTORY', 'History'
    BIOGRAPHY = 'BIOGRAPHY', 'Biography'
    MYSTERY = 'MYSTERY', 'Mystery'
    FANTASY = 'FANTASY', 'Fantasy'
    ROMANCE = 'ROMANCE', 'Romance'
    TECHNOLOGY = 'TECHNOLOGY', 'Technology'
    ART = 'ART', 'Art'
    CHILDRENS = 'CHILDRENS', "Children's Books"
    SELF_HELP = 'SELF_HELP', 'Self-Help'
    TRAVEL = 'TRAVEL', 'Travel'
