import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/go',
    name: 'Go',
    component: () => import('../views/Principal.vue')
  },
  {
    path: '/ayudadiag',
    name: 'AyudaDiag',
    component: () => import('../views/AyudaDiag.vue')
  },
  {
    path: '/consultaexterna/',
    name: 'ConsultaExterna',
    component: () => import('../views/ConsultaExterna.vue')
  },
  {
    path: '/escaneados',
    name: 'Escaneados',
    component: () => import('../views/Escaneados.vue')
  },
  {
    path: '/archivo',
    name: 'Archivo',
    component: () => import('../views/Archivo.vue')
  },
  {
    path: '/atencion/:id',
    name: 'Atencion',
    component: () => import('../views/ConsultaExterna.vue')
  },
  {
    path: '/seguridad',
    name: 'Seguridad',
    component: () => import('../views/Seguridad.vue')
  },
  {
    path: '/bienes',
    name: 'Bienes',
    component: () => import('../views/DelegacionesBE.vue')
  },
  {
    path: '/cupos',
    name: 'Cupos',
    component: () => import('../views/MenuCupos.vue')
  },
  {
    path: '/cuposIpress',
    name: 'CuposIpress',
    component: () => import('../views/MenuCuposIpress.vue')
  },
  {
    path: '/listaEspera',
    name: 'ListaEspera',
    component: () => import('../views/ListaEspera.vue')
  },
  {
    path: '/prueba',
    name: 'Prueba',
    component: () => import('../views/prueba.vue')
  },
  {
    path: '/docuContratados',
    name: 'DocuContratados',
    component: () => import('../views/DocuContratados.vue')
  },
  {
    path: '/incidencias',
    name: 'Incidencias',
    component: () => import('../views/AdmIncidencias.vue')
  },
  {
    path: '/cuposAsignacion',
    name: 'CuposAsignacion',
    component: () => import('../views/CuposAsignacion.vue')
  },
  {
    path: '/cuposAsignacionCnsr',
    name: 'CuposAsignacionCnsr',
    component: () => import('../views/CuposAsignacionCnsr.vue')
  },
  {
    path: '/cuposRecord',
    name: 'CuposRecord',
    component: () => import('../views/CuposRecord.vue')
  },
  {
    path: '/reporteClinicaAcre',
    name: 'ReporteClinicaAcre',
    component: () => import('../views/ReporteClinicaAcre.vue')
  },
  {
    path: '/liberarCupos',
    name: 'LiberarCupos',
    component: () => import('../views/CuposLiberarCupos.vue')
  }, 
  {
    path: '/encuestaAdm',
    name: 'EncuestaAdm',
    component: () => import('../views/encuestas/EncuestaAdm.vue')
  },
  {
    path: '/cuposReportGraficos',
    name: 'CuposReportGraficos',
    component: () => import('../views/CuposReportGraficos.vue')
  },
  {
    path:'/censo',
    name:'encc',
    component: () => import('@/views/encuestas/EncuestaCenso.vue')
  },
  {
    path:'/censo/:id',
    name:'datos',
    props:true,
    component: ()=> import('@/views/encuestas/DetallesPacienteRegistro.vue')
  },
  {
    path:'/censoLogin',
    name:'CensoLogin',
    component: ()=>import('@/views/Login.vue')    
  },
  {
    path:'/cuposMovPac',
    name:'CuposMovPac',
    component: ()=>import('@/views/CuposMovPac.vue')    
  },
]

const router = new VueRouter({
  routes,
  //mode: 'history',
  //base: '/hisar/',
})

export default router
