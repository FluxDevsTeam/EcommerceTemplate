from django.db import models
from django.core.exceptions import ValidationError

STATE_CHOICES = (
    ("Abia", "Abia"),
    ("Adamawa", "Adamawa"),
    ("Akwa Ibom", "Akwa Ibom"),
    ("Anambra", "Anambra"),
    ("Bauchi", "Bauchi"),
    ("Bayelsa", "Bayelsa"),
    ("Benue", "Benue"),
    ("Borno", "Borno"),
    ("Cross River", "Cross River"),
    ("Delta", "Delta"),
    ("Ebonyi", "Ebonyi"),
    ("Edo", "Edo"),
    ("Ekiti", "Ekiti"),
    ("Enugu", "Enugu"),
    ("Gombe", "Gombe"),
    ("Imo", "Imo"),
    ("Jigawa", "Jigawa"),
    ("Kaduna", "Kaduna"),
    ("Kano", "Kano"),
    ("Katsina", "Katsina"),
    ("Kebbi", "Kebbi"),
    ("Kogi", "Kogi"),
    ("Kwara", "Kwara"),
    ("Lagos", "Lagos"),
    ("Nasarawa", "Nasarawa"),
    ("Niger", "Niger"),
    ("Ogun", "Ogun"),
    ("Ondo", "Ondo"),
    ("Osun", "Osun"),
    ("Oyo", "Oyo"),
    ("Rivers", "Rivers"),
    ("Sokoto", "Sokoto"),
    ("Taraba", "Taraba"),
    ("Yobe", "Yobe"),
    ("Zamfara", "Zamfara"),
    ("FCT - Abuja", "FCT - Abuja"),
)


# had to set default for everything so the application doesn't crash and for better understanding as it is a template
class OrganizationSettings(models.Model):
    singleton = models.BooleanField(default=True, unique=True, editable=False)
    available_states = models.JSONField(default=list, help_text='["Ogun", "Lagos"]')
    warehouse_state = models.CharField(max_length=50, choices=STATE_CHOICES, default="Lagos")
    phone_number = models.CharField(max_length=20, default="+0123456789")
    customer_support_email = models.EmailField(default="suskidee@gmail.com")
    admin_email = models.EmailField(default="suskidee@gmail.com")
    brand_logo = models.ImageField(upload_to="brand_logo/", null=True, blank=True)
    facebook = models.URLField(max_length=100, null=True, blank=True)
    instagram = models.URLField(max_length=100, null=True, blank=True)
    twitter = models.URLField(max_length=100, null=True, blank=True)
    linkedin = models.URLField(max_length=100, null=True, blank=True)
    tiktok = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"organization settings: {self.admin_email}"

    def clean(self):
        if not isinstance(self.available_states, list):
            raise ValidationError("available_states must be a list")
        valid_states = [state[0] for state in STATE_CHOICES]
        invalid_states = [state for state in self.available_states if state not in valid_states]
        if invalid_states:
            raise ValidationError(f"Invalid states: {invalid_states}")

    def save(self, *args, **kwargs):
        self.singleton = True
        super().save(*args, **kwargs)


class DeliverySettings(models.Model):
    singleton = models.BooleanField(default=True, unique=True, editable=False)
    fee_per_km = models.DecimalField(max_digits=10, decimal_places=2, default=150)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=4000)
    weight_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1500)
    size_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1500)

    def __str__(self):
        return "delivery settings"

    def save(self, *args, **kwargs):
        self.singleton = True
        super().save(*args, **kwargs)


class DeveloperSettings(models.Model):
    singleton = models.BooleanField(default=True, unique=True, editable=False)
    brand_name = models.CharField(max_length=200, default="KidsDesignCompany")
    contact_us = models.URLField(max_length=200, default="https://kidsdesigncompany.com/contact-us")
    terms_of_service = models.URLField(max_length=200, default="https://kidsdesigncompany.com/terms-of-service")
    backend_base_route = models.URLField(max_length=200, default="https://api.kidsdesigncompany.com")
    frontend_base_route = models.URLField(max_length=200, default="https://kidsdesigncompany.com")
    order_route_frontend = models.URLField(max_length=200, default="https://api.kidsdesigncompany.com/orders")
    payment_failed_url = models.URLField(max_length=200, default="https://api.kidsdesigncompany.com/order_failed")

    def __str__(self):
        return "developer settings for f{self.brand_name}"

    def save(self, *args, **kwargs):
        self.singleton = True
        super().save(*args, **kwargs)
