from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

# Create your models here.
class NewUserManager(BaseUserManager):
#     ordering = ('email')
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



from django.core.validators import MaxValueValidator, MinValueValidator
class NewUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_phonenumber = models.CharField(max_length=15, null=True)
    influencercode=models.TextField(max_length=10)
    influencername = models.CharField(max_length=20, null=True)
    influencerinstagram = models.CharField(max_length=20, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = NewUserManager()

STATE_CHOICES = (
   ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
   ("Andhra Pradesh","Andhra Pradesh"),
   ("Arunachal Pradesh","Arunachal Pradesh"),
   ("Assam","Assam"),
   ("Bihar","Bihar"),
   ("Chhattisgarh","Chhattisgarh"),
   ("Chandigarh","Chandigarh"),
   ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
   ("Daman and Diu","Daman and Diu"),
   ("Delhi","Delhi"),
   ("Goa","Goa"),
   ("Gujarat","Gujarat"),
   ("Haryana","Haryana"),
   ("Himachal Pradesh","Himachal Pradesh"),
   ("Jammu and Kashmir","Jammu and Kashmir"),
   ("Jharkhand","Jharkhand"),
   ("Karnataka","Karnataka"),
   ("Kerala","Kerala"),
   ("Ladakh","Ladakh"),
   ("Lakshadweep","Lakshadweep"),
   ("Madhya Pradesh","Madhya Pradesh"),
   ("Maharashtra","Maharashtra"),
   ("Manipur","Manipur"),
   ("Meghalaya","Meghalaya"),
   ("Mizoram","Mizoram"),
   ("Nagaland","Nagaland"),
   ("Odisha","Odisha"),
   ("Punjab","Punjab"),
   ("Pondicherry","Pondicherry"),
   ("Rajasthan","Rajasthan"),
   ("Sikkim","Sikkim"),
   ("Tamil Nadu","Tamil Nadu"),
   ("Telangana","Telangana"),
   ("Tripura","Tripura"),
   ("Uttar Pradesh","Uttar Pradesh"),
   ("Uttarakhand","Uttarakhand"),
   ("West Bengal","West Bengal"),
)

CATEGORY_CHOICES = (
        ('T', 'T-shirts'),
        ('TW', 'Top Wear'),
        ('BW', 'Bottom Wear'),
        ('MTH', 'Mens T-Shirts and Hoodies'),
        ('MSC', 'Mens Shirts & Coats'),
        ('MPS', 'Mens Pants & Shorts'),
        ('MSI', 'Mens Sportswear and innerwear'),
        ('MTT', 'Mens Tamil Traditional wears'),
        ('GTTS', 'Girls Tops, T-Shirts & Shirts'),
        ('GJP', 'Girl Jeans & Pants'),
        ('GSS', 'Girls Skirts & Shorts'),
        ('GSI', 'Girls Sportswear and innerwear'),
        ('GS', 'Girls Sleepwear'),
        ('GTS', 'Girls Tights & Leggings'),
        ('GTT', 'womens Tamil Traditional wears'),
        ('b1', 'boy(0-1)'),
        ('b2', 'boy(1-2)'),
        ('b3', 'boy(3 or 3+)'),
        ('g1', 'girl(0-1)'),
        ('g2', 'girl(1-2)'),
        ('g3', 'girl(3 or 3+)'),
    )

STATUS_CHOICES = (
     ('Accepted', 'Accepted'),
     ('Packed', 'Packed'),
     ('On The Way', 'On The Way'),
     ('Delivered', 'Delivered'),
     ('Cancel', 'Cancel')
)   



class Size(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
        user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)
        title = models.CharField(max_length=100)
        selling_price = models.FloatField()
        discounted_price = models.FloatField(null=True, blank=True)
        description = models.TextField( null=True, blank=True)
        brand = models.CharField(max_length=100, null=True, blank=True)
        category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, null=True, blank=True)
        product_image = models.ImageField(upload_to='producting', null=True, blank=True, default='producting/not.png')
        product_image2 = models.ImageField(upload_to='producting', null=True, blank=True, default='producting/not.png')
        product_image3 = models.ImageField(upload_to='producting', null=True, blank=True, default='producting/not.png')
        factory = models.CharField(max_length=100, null=True, blank=True)
        commission = models.IntegerField(null=True, blank=True)
        size_choices = (
        ('N', 'None'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        # Add more choices as needed
        )

        color_choices = (
        ('N', 'None'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        # Add more choices as needed
        )
        # size = models.CharField(max_length=40,null=True, choices=size_choices)
        # color = models.CharField(max_length=255,null=True, choices=color_choices)

        size = models.ManyToManyField(Size, null=True, blank=True)
        colors = models.ManyToManyField(Color, null=True, blank=True)
        save_entry = models.BooleanField(default=True)


        def __str__(self):
             return str(self.id)
        def save(self, *args, **kwargs):
        # Check if save_entry is True before saving the entry
         if self.save_entry:
            super().save(*args, **kwargs)
         else:
            # If save_entry is False, do not save the entry
            pass
        
class Influencerinfo(models.Model):
    influencer_name=models.CharField(max_length=30)
    influencer_phone=models.IntegerField()
    influencer_email=models.EmailField()
    influencer_code=models.TextField(max_length=10)
    password=models.TextField()
    def __str__(self):
        return self.influencer_name

class Customer(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
     user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)
     color = models.CharField(max_length=255, null=True, choices=Product.color_choices)
     size = models.CharField(max_length=40, null=True, choices=Product.size_choices)


     def __str__(self):
          return str(self.id)
     
     @property
     def total_cost(self):
          return self.quantity*self.product.discounted_price
     

class OrderPlaced(models.Model):
     user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.PositiveBigIntegerField(default=1)
     ordered_date = models.DateTimeField(auto_now_add=True)
     color = models.CharField(max_length=255, null=True, choices=Product.color_choices)
     size = models.CharField(max_length=40, null=True, choices=Product.size_choices)
     status = models.CharField(choices=STATUS_CHOICES, default="Pending", max_length=30)
     influencercode=models.TextField(max_length=10, null=True)


     @property
     def total_cost(self):
          return self.quantity*self.product.discounted_price

     
class InfluencerCart(models.Model):
     user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     #quantity = models.PositiveIntegerField(default=1)
     code = models.CharField(max_length=10)

     def __str__(self):
          return str(self.id)

class Return(models.Model):
     user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     reason = models.CharField(max_length=255) 
     Returned_date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return str(self.id)

     


     
    