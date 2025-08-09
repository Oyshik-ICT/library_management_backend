import logging

from rest_framework import serializers

from .models import Author, Book, Category

logger = logging.getLogger("__name__")


class PartialUpdateSerializer(serializers.ModelSerializer):
    """
    Base serializer to support partial fields update by changing only the changed fields
    """

    def update(self, instance, validated_data):
        try:
            update_fields = []

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                update_fields.append(attr)

            instance.save(update_fields=update_fields)
            return instance
        except Exception as e:
            logger.error(
                f"Error updating {instance.__class__.__name__}=> {e}", exc_info=True
            )
            raise serializers.ValidationError(
                "An error occure while updating the object"
            )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class AuthorSerializer(PartialUpdateSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "category",
            "total_copies",
            "available_copies",
        ]

        extra_kwargs = {"available_copies": {"read_only": True}}

    def validate(self, attrs):
        """
        Ensure total copy is greater or equal to the available copy
        """
        try:
            total_copies = attrs.get("total_copies")
            available_copies = attrs.get("available_copies")

            if self.instance:
                if total_copies is None:
                    total_copies = self.instance.total_copies
                if available_copies is None:
                    available_copies = self.instance.available_copies

            if total_copies is not None and available_copies is not None:
                if total_copies < available_copies:
                    raise serializers.ValidationError(
                        "Total copies must be greater or equal than available copies"
                    )

            return super().validate(attrs)
        except Exception as e:
            logger.error("Error occure in BookSerializer=> {e}", exc_info=True)

    def create(self, validated_data):
        """
        Set available copies equal to total copies when creating a book
        """
        try:
            validated_data["available_copies"] = validated_data["total_copies"]
            return super().create(validated_data)
        except Exception as e:
            logger.error("Error occure in creating book> {e}", exc_info=True)
            raise serializers.ValidationError("An error occure while creating a book")

    def update(self, instance, validated_data):
        """
        Update a book instance while adjusting available copies if total copies changed
        """
        try:
            if "total_copies" in validated_data:
                extra_copies = validated_data["total_copies"] - instance.total_copies
                validated_data["available_copies"] = (
                    instance.available_copies + extra_copies
                )

            update_fields = []

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                update_fields.append(attr)

            instance.save(update_fields=update_fields)
            return instance
        except Exception as e:
            logger.error("Error occure in updating book> {e}", exc_info=True)
            raise serializers.ValidationError("An error occure while updating book")
