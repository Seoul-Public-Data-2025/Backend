from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openapi', '0002_safetyfacility_safetyservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_type', models.CharField(choices=[('001', '경찰서'), ('002', 'CCTV'), ('003', '안전시설물'), ('004', '안전지킴이집')], max_length=10)),
                ('lat', models.DecimalField(decimal_places=8, max_digits=11)),
                ('lot', models.DecimalField(decimal_places=8, max_digits=11)),
                ('addr', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='safetyfacility',
            name='facility_type',
            field=models.CharField(choices=[('301', '안심벨'), ('302', 'CCTV'), ('303', '안내표지판 (전주 표기 포함)'), ('304', '노면표기'), ('305', '보안등'), ('306', '안심귀갓길 서비스 안내판'), ('307', '112 위치 신고 안내판'), ('308', '기타(안심반사경 등)')], default='301', max_length=10),
        ),
    ]
