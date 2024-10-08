# Generated by Django 5.1 on 2024-10-05 08:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Clash",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("faculty_name", models.CharField(max_length=255)),
                ("cluster_number", models.IntegerField()),
                ("students", models.TextField()),
                ("chosen_student", models.CharField(default="nobody", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Deadline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_deadline", models.DateTimeField()),
                ("faculty_deadline", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("teacher_id", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                (
                    "email",
                    models.CharField(
                        default="studentmail.sid0+DN@gmail.com", max_length=100
                    ),
                ),
                ("willingness", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Faculty_log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("faculty_name", models.CharField(max_length=255)),
                ("faculty_id", models.IntegerField(unique=True)),
                (
                    "faculty_log",
                    models.FileField(
                        null=True, upload_to="../logfiles/media/faculty_logs/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FinalAllotment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_roll_no", models.CharField(max_length=255)),
                ("faculty_name", models.CharField(max_length=255)),
                ("cluster_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_id", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("cgpa", models.DecimalField(decimal_places=2, max_digits=4)),
                ("email", models.CharField(max_length=255)),
                ("is_eligible", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Student_log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_name", models.CharField(max_length=255)),
                ("student_rollno", models.CharField(max_length=8, unique=True)),
                (
                    "student_log",
                    models.FileField(
                        null=True, upload_to="../logfiles/media/student_logs/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "teacher_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="OtpToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("otp_code", models.CharField(default="322739", max_length=6)),
                ("tp_created_at", models.DateTimeField(auto_now_add=True)),
                ("otp_expires_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otps",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PreferenceList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("preferences", models.TextField()),
                (
                    "student_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.student"
                    ),
                ),
            ],
        ),
    ]
