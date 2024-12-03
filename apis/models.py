from datetime import timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , null=True , blank=True , on_delete=models.CASCADE )
    f_name = models.CharField(max_length=11,null=True , blank=True)
    l_name = models.CharField(max_length=11,null=True , blank=True)
    email = models.EmailField(max_length=30,null=True , blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="images/user", 
                                  default="images/user.png")

    # to show the name of the tag instead of the number of the obj
    def __str__(self):
        name = str(self.f_name)
        if self.l_name:
            name += ' ' + str(self.l_name)
        return name

class Tags(models.Model):
    name = models.CharField(max_length= 20 , blank=True )

    # to show the name of the tag instead of the number of the obj
    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return 'should be name there'
    
class ProjectPost(models.Model):
    zkzk = User.objects.get(username = 'zkzk')
    user = models.ForeignKey(User , default=zkzk.id , on_delete=models.CASCADE , null=True , blank=True )
    title = models.CharField(str('headLine') , max_length=30 , null=True , blank=True)
    sub_headline = models.CharField(max_length=150, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="images/Project_post", 
                                  default="images/placeholder.png")
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    # to show the name of the tag instead of the number of the obj
    def __str__(self):
        return str(self.title)
    
    # auto save slug
    def save(self , *args , **kwargs):
        if self.slug == None:
            slug = slugify(self.title)

            has_slug = ProjectPost.objects.filter(slug = slug).exists()
            counter = 1 

            while(has_slug):
                counter += 1
                slug = slugify(self.title) + '-' + str(counter) 
                has_slug = ProjectPost.objects.filter(slug=slug).exists()

            self.slug = slug
        
        super().save(*args , **kwargs)

class post_comment(models.Model):
    post = models.ForeignKey(ProjectPost , null=True , blank=True , on_delete= models.CASCADE)
    user = models.ForeignKey(User ,  null=True , blank=True , on_delete= models.CASCADE)
    comment = models.CharField(max_length=100 , null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        if self.user.last_name:
            return name
        elif self.user.first_name and not self.user.last_name:
            return self.user.first_name
        elif not self.user:
            return 'Anonymes'
    @property
    def created_dynamic(self):
        now = timezone.now()
        return now
    

class notify_user(models.Model):
    notify_post = models.ForeignKey(ProjectPost , on_delete=models.CASCADE , null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE ,null=True, blank=True)
    text = models.TextField(null=True , blank=True)