# Generated by Django 3.0.5 on 2022-03-15 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('django_rds_iam_auth', '0055_auto_20220315_0846'),
    ]

    operations = [
        migrations.RunSQL(sql="DROP POLICY tenant_table_policy ON api_tenant;"),
        migrations.RunSQL(
            sql="""
            CREATE POLICY tenant_table_policy ON api_tenant
                USING (privileged_user_has_tenant(current_user, id) OR user_has_root_tenant(current_user, id))
                WITH CHECK (privileged_user_has_tenant(current_user, id));
        """,
            reverse_sql="drop policy tenant_table_policy on api_tenant;",
        ),
    ]
