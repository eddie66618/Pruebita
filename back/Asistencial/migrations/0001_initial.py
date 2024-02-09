# Generated by Django 3.1.1 on 2022-05-20 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ambiente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codAmb', models.CharField(max_length=11)),
                ('descAmb', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='bienpat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codEti', models.CharField(max_length=30, unique=True)),
                ('propBien', models.CharField(default='ESSALUD', max_length=50)),
                ('desBien', models.CharField(max_length=100)),
                ('serBien', models.CharField(max_length=50)),
                ('modBien', models.CharField(max_length=15)),
                ('marBien', models.CharField(max_length=15)),
                ('situBien', models.CharField(default='B', max_length=5)),
                ('valBien', models.IntegerField(default=0)),
                ('estBien', models.CharField(default=1, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='dependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codDep', models.CharField(max_length=20, unique=True)),
                ('descDep', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='maestro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codMaestro', models.CharField(max_length=10)),
                ('descripMaestro', models.CharField(max_length=50)),
                ('detalleMaestro', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_doc', models.CharField(max_length=40)),
                ('num_doc', models.CharField(max_length=15, unique=True)),
                ('ape_pat', models.CharField(max_length=40)),
                ('ape_mat', models.CharField(max_length=50)),
                ('nombres', models.CharField(max_length=50)),
                ('fecha_nac', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(max_length=10, null=True)),
                ('estado', models.CharField(default=1, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dniPer', models.CharField(max_length=8, unique=True)),
                ('apePatPer', models.CharField(max_length=50)),
                ('apeMatPer', models.CharField(max_length=50)),
                ('nomPer', models.CharField(max_length=50)),
                ('sexo', models.CharField(max_length=50)),
                ('fecNacPer', models.DateField(null=True)),
                ('codPlaPer', models.CharField(max_length=50)),
                ('regPer', models.CharField(max_length=50)),
                ('cargoPer', models.CharField(max_length=50)),
                ('nivelPer', models.CharField(max_length=50)),
                ('telefoPer', models.CharField(max_length=50)),
                ('correoPer', models.CharField(max_length=50)),
                ('direcPer', models.CharField(max_length=50)),
                ('estPer', models.CharField(default=1, max_length=5)),
                ('dependencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.dependencia')),
            ],
        ),
        migrations.CreateModel(
            name='proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rucProveedor', models.CharField(max_length=30, unique=True)),
                ('nombreProveedor', models.CharField(max_length=50)),
                ('telefProveedor', models.CharField(max_length=20)),
                ('direcProveedor', models.CharField(max_length=20, null=True)),
                ('estadoProveedor', models.CharField(default=1, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_doc', models.CharField(max_length=15, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('cas', models.CharField(max_length=30)),
                ('usuario', models.CharField(max_length=15, unique=True)),
                ('clave', models.CharField(max_length=20)),
                ('perfil', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='valGlobalSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaEval', models.DateField()),
                ('ganPerPeso', models.CharField(max_length=15)),
                ('camPesoCorp', models.CharField(max_length=15)),
                ('duraDieta', models.CharField(max_length=15)),
                ('resultDieta', models.CharField(max_length=15)),
                ('tipoDieta', models.CharField(max_length=40)),
                ('sintoGastro', models.CharField(max_length=15)),
                ('disfuncion', models.CharField(max_length=15)),
                ('cambioCapFun', models.CharField(max_length=15)),
                ('grasaSubcu', models.CharField(max_length=15)),
                ('atrofiaMusc', models.CharField(max_length=15)),
                ('EdemaTobi', models.CharField(max_length=15)),
                ('edemaSacro', models.CharField(max_length=15)),
                ('ascitis', models.CharField(max_length=15)),
                ('resultadoVGS', models.CharField(max_length=25)),
                ('fechaReg', models.DateField()),
                ('userReg', models.CharField(max_length=20)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='provMaq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usobien', models.CharField(max_length=5)),
                ('bienpat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
            ],
        ),
        migrations.CreateModel(
            name='presAnemia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPres', models.DateField()),
                ('nomNefro', models.CharField(max_length=30)),
                ('medPres', models.CharField(max_length=30)),
                ('dosisPres', models.IntegerField()),
                ('medHiePres', models.CharField(max_length=30)),
                ('dosisHiePres', models.IntegerField()),
                ('viaAdmPres', models.CharField(max_length=10)),
                ('viaAdmHiePres', models.CharField(max_length=10)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='personalVpnAct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=30, null=True)),
                ('usuario', models.CharField(max_length=30)),
                ('clave', models.CharField(max_length=30)),
                ('personalAutoriza', models.CharField(max_length=40)),
                ('fechaHabilita', models.DateField(blank=True, null=True)),
                ('fechaInstalacion', models.DateField(blank=True, null=True)),
                ('observacion', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_reg', models.DateTimeField(auto_now=True)),
                ('dato', models.CharField(max_length=30)),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.personal')),
            ],
        ),
        migrations.CreateModel(
            name='personalCertificado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaSolicita', models.DateField()),
                ('tipoCertificado', models.CharField(max_length=30)),
                ('fechaInstalacion', models.DateField(blank=True, null=True)),
                ('perosnalInstala', models.CharField(blank=True, max_length=40, null=True)),
                ('observacion', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_reg', models.DateTimeField(auto_now=True)),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.personal')),
            ],
        ),
        migrations.CreateModel(
            name='nutricion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turno', models.CharField(max_length=30)),
                ('frecuencia', models.CharField(max_length=30)),
                ('fechaIngreso', models.DateField(null=True)),
                ('fechaEvaluacion', models.DateField(null=True)),
                ('peso', models.CharField(max_length=30)),
                ('talla', models.CharField(max_length=30)),
                ('imc', models.CharField(max_length=30)),
                ('porcentajeCMB', models.CharField(max_length=30)),
                ('porcentajeEPT', models.CharField(max_length=30, null=True)),
                ('albSerica', models.CharField(max_length=30)),
                ('ValGlobalSub', models.CharField(blank=True, max_length=30, null=True)),
                ('ingestaCalorica', models.CharField(max_length=60)),
                ('ingestaProteica', models.CharField(max_length=60)),
                ('diagNutricional', models.CharField(max_length=60)),
                ('interveNutricional', models.CharField(max_length=60)),
                ('fechaReg', models.DateTimeField(auto_now_add=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='movimientoAnemia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaMotivo', models.DateField()),
                ('razonMotivo', models.CharField(max_length=30)),
                ('obserMotivo', models.CharField(max_length=30)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='incidenciaDsi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problema', models.CharField(max_length=200)),
                ('clasiSolu', models.CharField(max_length=50, null=True)),
                ('solucion', models.CharField(max_length=500, null=True)),
                ('userReg', models.CharField(max_length=20)),
                ('fecha_reg', models.DateTimeField(auto_now=True)),
                ('numTicket', models.CharField(max_length=20)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.maestro')),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.personal')),
            ],
        ),
        migrations.CreateModel(
            name='exclusionAnemia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaExclu', models.DateField()),
                ('razonExclu', models.CharField(max_length=30)),
                ('ObservaExclu', models.CharField(max_length=30)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='examen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_exam', models.CharField(max_length=50, null=True)),
                ('archivo_exam', models.FileField(null=True, upload_to='media/')),
                ('estado_lectura', models.CharField(max_length=30, null=True)),
                ('estado', models.CharField(default='1', max_length=5)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('user_reg', models.CharField(max_length=40, null=True)),
                ('fecha_mod', models.DateTimeField(null=True)),
                ('user_mod', models.CharField(max_length=50, null=True)),
                ('fecha_eli', models.DateTimeField(null=True)),
                ('user_eli', models.CharField(max_length=50, null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='bienSoftware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sistemaOperativo', models.CharField(max_length=20)),
                ('ofimatica', models.CharField(max_length=20)),
                ('antivirus', models.CharField(max_length=20)),
                ('bienpat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
            ],
        ),
        migrations.CreateModel(
            name='bienPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bienpat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.personal')),
            ],
        ),
        migrations.CreateModel(
            name='bienImag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='fotos/')),
                ('bienpat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
            ],
        ),
        migrations.CreateModel(
            name='bienHadware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procesador', models.CharField(max_length=20)),
                ('numeroIp', models.CharField(max_length=20)),
                ('numeroMac', models.CharField(max_length=20)),
                ('memoriaRam', models.CharField(max_length=20)),
                ('capAlmacenamiento', models.CharField(max_length=20)),
                ('uso', models.CharField(max_length=20)),
                ('condicion', models.CharField(max_length=20)),
                ('bienpat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
            ],
        ),
        migrations.CreateModel(
            name='bienDetalleMonitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pulgadas', models.CharField(max_length=20)),
                ('bienpat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
            ],
        ),
        migrations.CreateModel(
            name='bienAmbiente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ambiente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.ambiente')),
                ('bienpat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.bienpat')),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.personal')),
            ],
        ),
        migrations.CreateModel(
            name='archivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numHisCli', models.CharField(max_length=30, null=True)),
                ('numBalda', models.CharField(max_length=30, null=True)),
                ('estado', models.CharField(default='1', max_length=5)),
                ('user_reg', models.CharField(max_length=30, null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
            ],
        ),
        migrations.AddField(
            model_name='ambiente',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.dependencia'),
        ),
        migrations.CreateModel(
            name='admiAnemia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaAdmi', models.DateField()),
                ('nomEnfer', models.CharField(max_length=30)),
                ('medAdmi', models.CharField(max_length=30)),
                ('dosisAdmi', models.IntegerField()),
                ('medHieAdmi', models.CharField(max_length=30)),
                ('dosisHieAdmi', models.IntegerField()),
                ('viaAdm', models.CharField(max_length=10)),
                ('viaAdmHierro', models.CharField(max_length=10)),
                ('presAnemia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.presanemia')),
            ],
        ),
    ]