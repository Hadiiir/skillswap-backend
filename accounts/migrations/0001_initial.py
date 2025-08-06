# Generated migration for accounts app

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='avatar')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='bio')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='phone number')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='location')),
                ('website', models.URLField(blank=True, verbose_name='website')),
                ('points_balance', models.PositiveIntegerField(default=100, verbose_name='points balance')),
                ('total_earned_points', models.PositiveIntegerField(default=0, verbose_name='total earned points')),
                ('total_spent_points', models.PositiveIntegerField(default=0, verbose_name='total spent points')),
                ('rating', models.DecimalField(decimal_places=2, default=0.00, max_digits=3, verbose_name='rating')),
                ('total_reviews', models.PositiveIntegerField(default=0, verbose_name='total reviews')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
                ('is_premium', models.BooleanField(default=False, verbose_name='is premium')),
                ('premium_expires', models.DateTimeField(blank=True, null=True, verbose_name='premium expires')),
                ('preferred_language', models.CharField(choices=[('en', 'English'), ('ar', 'Arabic')], default='en', max_length=5, verbose_name='preferred language')),
                ('email_notifications', models.BooleanField(default=True, verbose_name='email notifications')),
                ('push_notifications', models.BooleanField(default=True, verbose_name='push notifications')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('last_active', models.DateTimeField(auto_now=True, verbose_name='last active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='skill name')),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], default='beginner', max_length=20, verbose_name='skill level')),
                ('years_of_experience', models.PositiveIntegerField(default=0, verbose_name='years of experience')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='user_skills', to='accounts.user')),
            ],
            options={
                'verbose_name': 'User Skill',
                'verbose_name_plural': 'User Skills',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together={('user', 'name')},
        ),
    ]
