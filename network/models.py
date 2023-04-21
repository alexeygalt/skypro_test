from django.core.validators import MinValueValidator
from django.db import models


class Vendor(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=50)
    indebtedness = models.DecimalField(decimal_places=2,
                                       max_digits=25,
                                       default=0.00,
                                       validators=([MinValueValidator(0)]))
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Factory(Vendor):
    indebtedness = models.Empty()

    class Meta:
        verbose_name = "Завод"
        verbose_name_plural = "Заводы"


class RetailsNet(Vendor):
    factory = models.ForeignKey("Factory",
                                on_delete=models.PROTECT,
                                related_name="retailers",
                                blank=True,
                                null=True)

    indi_pred = models.ForeignKey("IndiPred",
                                  on_delete=models.PROTECT,
                                  related_name="retailers",
                                  blank=True,
                                  null=True)

    class Meta:
        verbose_name = "Розничная сеть"
        verbose_name_plural = "Розничные сети"


class IndiPred(Vendor):
    factory = models.ForeignKey("Factory",
                                on_delete=models.PROTECT,
                                related_name="individuates",
                                blank=True,
                                null=True)

    retails_net = models.ForeignKey("RetailsNet",
                                    on_delete=models.PROTECT,
                                    related_name="individuates",
                                    blank=True,
                                    null=True)

    class Meta:
        verbose_name = "Индивидуальный предприниматель"
        verbose_name_plural = "Индивидуальный предприниматели"


class Contact(models.Model):
    email = models.EmailField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.PositiveSmallIntegerField()

    factory = models.OneToOneField("Factory", on_delete=models.CASCADE, null=True, blank=True)
    retails = models.OneToOneField("RetailsNet", on_delete=models.CASCADE, null=True, blank=True)
    indi = models.OneToOneField("IndiPred", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.email


class Product(models.Model):
    title = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    factory = models.ManyToManyField("Factory", blank=True, related_name="products")
    retails = models.ManyToManyField("RetailsNet", blank=True, related_name="products")
    indi = models.ManyToManyField("IndiPred", blank=True, related_name="products")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title
