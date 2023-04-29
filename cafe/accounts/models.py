from django.db import models
from django.utils import timezone
import bcrypt

class Account(models.Model):
    phone = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_authenticated = True

    USERNAME_FIELD = 'phone'

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def get_username(self):
        return self.phone
    
    @property
    def is_staff(self):
        return self.is_admin

