from django.shortcuts import render
from Asistencial.models import correos,solicitud,movimientoPaciente,pacienteLocalizacion,pacienteGeoTem,ubigeo,asisPacDiarioAdicional,examenLaboratorio,dpDiario,loginAppHisar,serologiaPaciente,baseDatosProduccion,asisPacDiario,asigCuposPac,parameCentroPuesto,parameCentro,docuContratados,listaEspera,parNuticion,maestroMatSap,delegacionBienesEstra, cas, usuario, paciente, examen, archivo, bienAmbiente, bienImag, presAnemia,admiAnemia, exclusionAnemia, movimientoAnemia, bienPersonal, bienpat, dependencia, ambiente, personal, proveedor, provMaq, incidenciaDsi, maestro, bienHadware, bienSoftware, bienDetalleMonitor, nutricion, personalVpn, personalCertificado, valGlobalSub
from Asistencial.serializers import correosSerializer,solicitudSerializer,movimientoPacienteSerializer,pacienteLocalizacionSerializer,pacienteGeoTemSerializer,ubigeoSerializer,asisPacDiarioAdicionalSerializer,examenLaboratorioSerializer,dpDiarioSerializer,loginAppHisarSerializer,serologiaPacienteSerializer,baseDatosProduccionSerializer,asisPacDiarioSerializer,asigCuposPacSerializer,parameCentroPuestoSerializer,parameCentroSerializer,docuContratadosSerializer,listaEsperaSerializer,parNuticionSerializer,maestroMatSapSerializer,delegacionBienesEstraSerializer, casSerializer ,usuarioSerializer, PacienteSerializer, ExamenSerializer, ArchivoSerializer, presAnemiaSerializer, admiAnemiaSerializer, exclusionAnemiaSerializer, movimientoAnemiaSerializer, bienAmbienteSerializer, bienImagSerializer, bienPersonalSerializer, bienpatSerializer, dependenciaSerializer, ambienteSerializer, personalSerializer, proveedorSerializer, provMaqSerializer, incidenciaDsiSerializer, maestroSerializer, bienHadwareSerializer, bienSoftwareSerializer, bienDetalleMonitorSerializer, nutricionSerializer, personalVpnSerializer, personalCertificadoSerializer, valGlobalSubSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
#servicios externos
from django.http import HttpResponse,JsonResponse
import requests
import json
from decouple import config
# Create your views here.
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import IsAuthenticated

from django.core.mail import EmailMessage
from django.conf import settings

@api_view(['POST'])
@permission_required([IsAuthenticated])
def enviar_correo_con_adjunto(request):
    # Crear un objeto EmailMessage
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    subject = result.get("asunto")
    message = result.get("mensaje")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [result.get("destinatario")]
    #adjunto = result.get("adjunto")
    msg = EmailMessage(subject, message, from_email, recipient_list)
    msg.content_subtype = 'html'
    msg.body = html_message=result.get("html")
    # Adjuntar un archivo
    # archivo = 'D:\Proyectos2023/HISAR/codigo/back/media/media/imgOriSal/docu.pdf'  # Ruta al archivo que deseas adjuntar
    # msg.attach_file(archivo)
    # Enviar el correo
    msg.send()
    return HttpResponse("Correo enviado exitosamente.")   
##########
@api_view(['POST'])
@permission_required([IsAuthenticated])
def UsersViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.post(config('URL'),auth = (config('USER'), config('PASSWORD')) ,  json = {
                        "codOpcion": result.get("codOpcion"),
                        "codTipDoc": result.get("codTipDoc"),
                        "numDoc": result.get("numDoc"),
                        "fecNacimiento":result.get("fecNacimiento")
                      })
    users = response.json()
    #print(type(result))
    #print(result.get("codOpcion"))

    return JsonResponse(users)
##########

##########
@api_view(['POST'])
@permission_required([IsAuthenticated])
def SeguroViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.get(config('URLS004')+'?tpdoc='+result.get("tpdoc")+'&nrdoc='+result.get("nrdoc")+'&codcentro='+result.get("codcentro")+'&login='+config('LOGINS004')+'&user='+config('USERS004')+'&pass='+config('PASSWORD004'))
    Seguro = response.json()
    #print("algo",Seguro)
    return JsonResponse(Seguro)
##########

# Pacientes geolocalizados Temporalmente

class pacienteGeoTemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = pacienteGeoTem.objects.all()
    serializer_class = pacienteGeoTemSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dni']


# Tablas Generales

class ubigeoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ubigeo.objects.all()
    serializer_class = ubigeoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=ubigeo_reniec']

class casViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = cas.objects.all()
    serializer_class = casSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=tipoCas','^estado','=distrito']


class usuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=usuario','=id']

# Create your views here.
class maestroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = maestro.objects.all()
    serializer_class = maestroSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=codMaestro']

class PacienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=num_doc']

class serologiaPacienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = serologiaPaciente.objects.all()
    serializer_class = serologiaPacienteSerializer()
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__num_doc']
    
class ExamenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = examen.objects.all().order_by('-id')
    serializer_class = ExamenSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['tipo_exa']

class ArchivoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = archivo.objects.all().order_by('-id')
    serializer_class = ArchivoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id']

class presAnemiaViewSet(viewsets.ModelViewSet):
    queryset = presAnemia.objects.all().order_by('-id')
    serializer_class = presAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id','=usuario__cas__codCas']

class admiAnemiaViewSet(viewsets.ModelViewSet):
    queryset = admiAnemia.objects.all().order_by('-id')
    serializer_class = admiAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=presAnemia__paciente__id','=usuario__cas__codCas']

class exclusionAnemiaViewSet(viewsets.ModelViewSet):
    queryset = exclusionAnemia.objects.all().order_by('-id')
    serializer_class = exclusionAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id','=usuario__cas__codCas']

class movimientoAnemiaViewSet(viewsets.ModelViewSet):
    queryset = movimientoAnemia.objects.all().order_by('-id')
    serializer_class = movimientoAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id']

class nutricionViewSet(viewsets.ModelViewSet):
    queryset = nutricion.objects.all().order_by('-id')
    serializer_class = nutricionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id','=usuario__cas__codCas','=pacNuevo']

class valGlobalSubViewSet(viewsets.ModelViewSet):
    queryset = valGlobalSub.objects.all().order_by('-id')
    serializer_class = valGlobalSubSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id']


class bienpatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienpat.objects.all()
    serializer_class = bienpatSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['codEti']

class dependenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = dependencia.objects.all()
    serializer_class = dependenciaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['codDep']

class ambienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ambiente.objects.all()
    serializer_class = ambienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dependencia__id']

class personalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = personal.objects.all()
    serializer_class = personalSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dniPer']

class bienImagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienImag.objects.all()
    serializer_class = bienImagSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=bienpat__id']

class bienPersonalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienPersonal.objects.all()
    serializer_class = bienPersonalSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=bienpat__id']

class bienAmbienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienAmbiente.objects.all()
    serializer_class = bienAmbienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=bienpat__id']

class bienHadwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienHadware.objects.all()
    serializer_class = bienHadwareSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class bienSoftwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienSoftware.objects.all()
    serializer_class = bienSoftwareSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class bienDetalleMonitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienDetalleMonitor.objects.all()
    serializer_class = bienDetalleMonitorSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class proveedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = proveedor.objects.all()
    serializer_class = proveedorSerializer
    permission_classes = [permissions.IsAuthenticated]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['=rucProveedor']

class provMaqViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = provMaq.objects.all()
    serializer_class = provMaqSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']

class incidenciaDsiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = incidenciaDsi.objects.all().order_by('-id')
    serializer_class = incidenciaDsiSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=personal__dniPer','=estado__descripMaestro']

class personalVpnViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = personalVpn.objects.all().order_by('-id')
    serializer_class = personalVpnSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=personal__dniPer']

class personalCertificadoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = personalCertificado.objects.all().order_by('-id')
    serializer_class = personalCertificadoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=personal__dniPer']

class delegacionBienesEstraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = delegacionBienesEstra.objects.all().order_by('-id')
    serializer_class = delegacionBienesEstraSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class maestroMatSapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = maestroMatSap.objects.all().order_by('-id')
    serializer_class = maestroMatSapSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=codSap']

class parNuticionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = parNuticion.objects.all().order_by('-id')
    serializer_class = parNuticionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    #filter_fields = ['=edad','=sexo']
    search_fields = ['=edad','^sexo']

class listaEsperaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = listaEspera.objects.all().order_by('-id')
    serializer_class = listaEsperaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=distrito','=estado']

class docuContratadosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = docuContratados.objects.all().order_by('-id')
    serializer_class = docuContratadosSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=cas__id','^estado']

class parameCentroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = parameCentro.objects.all().order_by('-id')
    serializer_class = parameCentroSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=cas__id','^estado']

class parameCentroPuestoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = parameCentroPuesto.objects.all().order_by('-id')
    serializer_class = parameCentroPuestoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=cas__id','^estado']

class asigCuposPacViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = asigCuposPac.objects.all().order_by('-id')
    serializer_class = asigCuposPacSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=parameCentroPuesto__cas__id','=paciente__num_doc','^estado']

class asisPacDiarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = asisPacDiario.objects.all().order_by('-id')
    serializer_class = asisPacDiarioSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=asigCuposPac__parameCentroPuesto__cas__id','=validacionAsistencia']

class asisPacDiarioAdicionalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = asisPacDiarioAdicional.objects.all().order_by('-id')
    serializer_class = asisPacDiarioAdicionalSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=estadoAsistencia','^cas__id','^fecha_reg']


class baseDatosProduccionViewSet(viewsets.ModelViewSet):
    queryset = baseDatosProduccion.objects.all().order_by('-id')
    serializer_class = baseDatosProduccionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

#BACK PARA APLICATIVOS MOVIL

class loginAppHisarViewSet(viewsets.ModelViewSet):
    queryset = loginAppHisar.objects.all().order_by('-id')
    serializer_class = loginAppHisarSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=paciente__num_doc']

class dpDiarioViewSet(viewsets.ModelViewSet):
    queryset = dpDiario.objects.all().order_by('-id')
    serializer_class = dpDiarioSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=paciente__num_doc']

class examenLaboratorioViewSet(viewsets.ModelViewSet):
    queryset = examenLaboratorio.objects.all().order_by('-id')
    serializer_class = examenLaboratorioSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class pacienteLocalizacionViewSet(viewsets.ModelViewSet):
    queryset = pacienteLocalizacion.objects.all().order_by('-id')
    serializer_class = pacienteLocalizacionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=userReg']

class movimientoPacienteViewSet(viewsets.ModelViewSet):
    queryset = movimientoPaciente.objects.all().order_by('-id')
    serializer_class = movimientoPacienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=cas__id']

class solicitudViewSet(viewsets.ModelViewSet):
    queryset = solicitud.objects.all().order_by('-id')
    serializer_class = solicitudSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__num_doc','=respuesta','^cas__id']

class correosViewSet(viewsets.ModelViewSet):
    queryset = correos.objects.all().order_by('-id')
    serializer_class = correosSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]