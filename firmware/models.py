    
#################################################################################
############################################################################################################
###################### CREATED BY OMER AYDEMIR https://github.com/omeraydemirr #############################
############################################################################################################
#################################################################################

from multiselectfield import MultiSelectField
from django.contrib.contenttypes.models import *
from django.db.models import *
import os


class Firmware(models.Model):
    vendor = models.CharField("Vendor",max_length = 120)
    device = models.CharField("Device",max_length = 120)
    model = models.CharField("Model",max_length = 120)
    operating_system = models.CharField("OS",max_length = 120)
    series = models.CharField("Series",max_length = 120)
    file = models.FileField (verbose_name = 'File', upload_to = '')
    def filename(self):
        return os.path.basename (self.file.name)
