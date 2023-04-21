from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Contact, Product, Factory, RetailsNet, IndiPred


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ("factory", "retails", "indi")

    def validate(self, attrs):
        link_factory = attrs.get("factory")
        link_retails = attrs.get("retails")
        link_indi = attrs.get("indi")

        links_vendor = (link_factory, link_retails, link_indi)

        if sum(map(lambda x: x is not None, links_vendor)) != 1:
            assert ValidationError({"error": "Адрес может быть только у одного поставщика"})

        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("factory", "retails", "indi")


class FactorySerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Factory
        fields = "__all__"

    def create(self, validated_data):
        contact = validated_data.pop("contact")
        products = validated_data.pop("products")

        with transaction.atomic():
            instance = self.Meta.model.objects.create(**validated_data)

            data = {}
            if self.Meta.model is Factory:
                data["factory"] = instance
            elif self.Meta.model is RetailsNet:
                data["retails"] = instance
            elif self.Meta.model is IndiPred:
                data["indi"] = instance
            else:
                raise ValidationError({"error": "Ошибка сохранения поставщика"})

            Contact.objects.create(**contact, **data)

            for product in products:
                item = Product.objects.create(**product)
                instance.products.add(item)

        return instance


class RetailSerializer(FactorySerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = RetailsNet
        fields = "__all__"

    def create(self, validated_data):
        contact = validated_data.pop("contact")

        with transaction.atomic():
            instance = self.Meta.model.objects.create(**validated_data)

            data = {}
            if self.Meta.model is Factory:
                data["factory"] = instance
            elif self.Meta.model is RetailsNet:
                data["retails"] = instance
            elif self.Meta.model is IndiPred:
                data["indi"] = instance
            else:
                raise ValidationError({"error": "Ошибка сохранения поставщика"})

            Contact.objects.create(**contact, **data)

            products = Product.objects.filter(factory=validated_data.get("factory"),
                                              indi=validated_data.get("indi_pred"),
                                              retails=validated_data.get("retails"))

            for product in products:
                instance.products.add(product)

        return instance

    def validate(self, attrs):
        links_vendors = {}

        link_factory = attrs.get("factory")
        links_vendors['factory'] = link_factory

        link_retails = attrs.get("retails_net")
        links_vendors['retails_net'] = link_retails

        link_indi = attrs.get("indi_pred")
        links_vendors['indi_pred'] = link_indi

        if sum(map(lambda x: x is not None, links_vendors.values())) != 1:
            assert ValidationError({"error": "Связь может быть только с одним поставщиком"})

        return attrs


class IndividualSerializer(RetailSerializer):
    class Meta:
        model = IndiPred
        fields = "__all__"
