# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Descrição')),
                ('weight', models.DecimalField(decimal_places=2, default=100.0, max_digits=8, verbose_name='Peso líquido (ml ou g)')),
                ('energy', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Energia (kcal)')),
                ('carbohydrates', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Carboidratos (g)')),
                ('total_fat', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Gorduras Totais (g)')),
                ('poly_fat', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Gorduras Poli (g)')),
                ('mono_fat', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Gorduras Mono (g)')),
                ('sat_fat', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Gorduras Saturadas (g)')),
                ('protein', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Proteínas (g)')),
                ('total_fibers', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Fibras Totais (g)')),
                ('sol_fibers', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Fibras Solúveis (g)')),
                ('insol_fibers', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Fibras Insolúveis (g)')),
                ('cholesterol', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Colesterol (mg)')),
                ('retinol', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Retinol (Vit A) (mg)')),
                ('ac_ascorbic', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Ácido Ascórbico (Vit C) (mg)')),
                ('tiamine', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Tiamina (Vit B1) (mg)')),
                ('riboflavin', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Riboflavina (Vit B2) (mg)')),
                ('pyridoxine', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Piridoxina (Vit B6) (mg)')),
                ('cobalamin', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Cobalamina (Vit B12) (mcg)')),
                ('dvitamin', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Vitamina D (mcg)')),
                ('niacin', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Niacina (Vit B3)(mg)')),
                ('ac_folic', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Ácido fólico (Vit B9)(mcg)')),
                ('ac_pant', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Ácido pantotênico (Vit B5)(mg)')),
                ('tocopherol', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Tocoferol (Vit E)(mg)')),
                ('iodine', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Iodo (mcg)')),
                ('sodium', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Sódio (mg)')),
                ('calcium', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Cálcio (mg)')),
                ('magnesium', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Magnésio (mg)')),
                ('zinc', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Zinco (mg)')),
                ('manganese', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Manganês (mg)')),
                ('potassium', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Potássio (mg)')),
                ('phosphor', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Fósforo (mg)')),
                ('iron', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Ferro (mg)')),
                ('copper', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Cobre (mg)')),
                ('selenium', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Selênio (mcg)')),
            ],
            options={
                'verbose_name': 'Alimento',
                'verbose_name_plural': 'Alimentos',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.CharField(choices=[('CAFÉ DA MANHÃ', 'Café da Manhã'), ('LANCHE I', 'Lanche I'), ('ALMOÇO', 'Almoço'), ('LANCHE II', 'Lanche II'), ('JANTAR', 'Jantar'), ('CEIA', 'Ceia')], default=None, max_length=40, null=True, verbose_name='Refeição')),
                ('home_measure', models.CharField(blank=True, max_length=255, null=True, verbose_name='Med. Caseira')),
                ('weight', models.DecimalField(decimal_places=2, default=100.0, max_digits=8, verbose_name='Peso líquido (ml ou g)')),
            ],
        ),
        migrations.CreateModel(
            name='UploadSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Descrição da Tabela')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('path', models.FileField(blank=True, null=True, upload_to='upload/table', verbose_name='Tabela')),
            ],
        ),
    ]
