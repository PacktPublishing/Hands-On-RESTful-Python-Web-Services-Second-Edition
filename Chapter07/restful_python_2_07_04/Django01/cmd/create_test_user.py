from django.contrib.auth.models import User
user = User.objects.create_user('gaston-hillar', 'testuser@example.com', 'FG$gI^76q#yA3v') 
user.save()
