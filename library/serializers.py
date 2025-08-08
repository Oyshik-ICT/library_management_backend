from rest_framework import serializers
from .models import Category, Author, Book

class PartialUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(PartialUpdateSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

    
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "description", "author", "category", "total_copies", "available_copies"]

        extra_kwargs = {
            "available_copies": {"read_only": True}
        }

    def validate(self, attrs):
        total_copies = attrs.get("total_copies")
        available_copies = attrs.get("available_copies")

        if self.instance:
            if total_copies is None:
                total_copies = self.instance.total_copies
            if available_copies is None:
                available_copies = self.instance.available_copies

        if total_copies is not None and available_copies is not None:
            if total_copies < available_copies:
                raise serializers.ValidationError("Total copies must be greater or equal than available copies")
            
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data["available_copies"] = validated_data["total_copies"]
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "total_copies" in validated_data:
            extra_copies = validated_data["total_copies"] - instance.total_copies
            validated_data["available_copies"] = instance.available_copies + extra_copies

        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)
        return instance
    
