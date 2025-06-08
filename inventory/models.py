from django.db import models
from fernet_fields import EncryptedCharField
from django.contrib.auth import get_user_model

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Device(models.Model):
    DEVICE_TYPES = [
        ('PC', 'Računar'),
        ('LAP', 'Laptop'),
        ('TEL', 'Telefon'),
        ('SRV', 'Server'),
        ('NET', 'Mrežna oprema'),
        ('PRN', 'Printer/MFP'),
        ('OTH', 'Ostalo'),
    ]
    type = models.CharField(max_length=4, choices=DEVICE_TYPES)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    inv_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('active','U upotrebi'),('service','Na servisu'),('retired','Rashodovan')])
    purchase_date = models.DateField()
    warranty_expiry = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} {self.brand} {self.model}"

class Software(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    licence_type = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} {self.version}"

class Licence(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='licences')
    purchase_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to='licences/', blank=True, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.software}"

class Maintenance(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE, null=True, blank=True, related_name='maintenance')
    software = models.ForeignKey('Software', on_delete=models.CASCADE, null=True, blank=True, related_name='maintenance')
    date_signing_contract = models.DateField()
    date_expire_contract = models.DateField()
    description = models.TextField()
    document = models.FileField(upload_to='maintenance/', blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        if self.device:
            return f"Odrzavanje uređaja {self.device}"
        elif self.software:
            return f"Odrzavanje softvera {self.software} - {self.date_expire_contract}"
        else:
            return f"Odrzavanje {self.date}"

class Credential(models.Model):
    name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100)
    password = EncryptedCharField(max_length=255)
    description = models.TextField(blank=True)
    last_changed = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.username})"

class Documentation(models.Model):
    DOC_TYPES = [
        ('CONFIG', 'Konfiguracija'),
        ('PROCEDURE', 'Procedura'),
        ('MANUAL', 'Uputstvo'),
        ('ARCH', 'Arhitektura/shema'),
        ('OTHER', 'Ostalo'),
    ]
    title = models.CharField(max_length=200)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    related_device = models.ForeignKey('Device', null=True, blank=True, on_delete=models.SET_NULL)
    related_software = models.ForeignKey('Software', null=True, blank=True, on_delete=models.SET_NULL)
    upload = models.FileField(upload_to='documentation/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title