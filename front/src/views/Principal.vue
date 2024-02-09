<template>
  <div>
    <NavBar />
    <div>
      <v-container grid-list-md>
        <v-layout row wrap d-flex align-center>
          <v-flex xs12 sm3 v-if="perfil == 0">
            <div>
              <CardModulos
                title="Admision y Citas"
                detalle_titulo="Citas, Cupos relacionados a pacientes"
                img="1"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 1 || perfil == 2 || perfil == 0">
            <div>
              <CardModulos
                title="Consulta Externa"
                detalle_titulo="Todo lo relacionado a la atención del Paciente"
                img="2"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 0">
            <div>
              <CardModulos
                title="Laboratorio"
                detalle_titulo="Ver resultados Masivos relacionados a Laboratorio"
                img="3" 
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 0">
            <div>
              <CardModulos
                title="Escaneados"
                detalle_titulo="Examenes de laboratorio escaneado"
                img="5"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 0">
            <div>
              <CardModulos
                title="Maquinas"
                detalle_titulo="Mantenimientos de maquinas de Hemodialisis"
                img="7"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 3 || perfil == 0">
            <div>
              <CardModulos
                title="Archivo"
                detalle_titulo="Gestion de Archivo, Historias Clinicas Fisicas"
                img="6"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 4 || perfil == 5 || perfil == 6 || perfil == 7 || perfil == 0">
            <div>
              <CardModulos
                title="Bienes Estrategicos"
                detalle_titulo="Gestiona la delegación de Bienes Estrategicos"
                img="8"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 8 || perfil == 9 || perfil == 0">
            <div>
              <CardModulos
                title="Gestión de Cupos"
                detalle_titulo="Gestiona la asignacion de cupos IPRESS Privadas"
                img="9"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 13 || perfil == 0">
            <div>
              <CardModulos
                title="Admisión y Cupos"
                detalle_titulo="Gestiona de Asistencia y Cupos de Pacientes"
                img="12"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 12 || perfil == 0">
            <div>
              <CardModulos
                title="Incidencias"
                detalle_titulo="Registro y Control de Incidencias"
                img="11"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 10 || perfil == 11 || perfil == 0">
            <div>
              <CardModulos
                title="Documentos"
                detalle_titulo="Envio de Archivos al CNSR - Oficina Servicios Contratados"
                img="10"
              />
            </div>
          </v-flex>
          <v-flex xs12 sm3 v-if="perfil == 1 || perfil == 2 || perfil == 3 || perfil == 4 || perfil == 5 || perfil == 6 || perfil == 7 || perfil == 8 || perfil == 9 || perfil == 10 || perfil == 11 || perfil == 12|| perfil == 13 || perfil == 14 || perfil == 0">
            <div>
              <CardModulos
                title="Seguridad"
                detalle_titulo="Gestiona los Accesos al sistema para los usuarios"
                img="4"
              />
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/navbar/NavBar.vue";
import CardModulos from "../components/cards/CardModulos.vue";
import NavBarVertical from "../components/navbar/NavBarVertical.vue";

//require('../../assets/lab.jpg'),
export default {
  data() {
    return {
      dialog: false,
      perfil: "",
      nombre: "",
    };
  },
  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
  },
  created() {
    this.perfil = sessionStorage.getItem("perfil");
    this.nombre = sessionStorage.getItem("nombre");
    //console.log("Perfil", this.perfil);
  },
  methods: {
    actionOut() {
      this.dialog = false;
      this.$router.push("/");
    },
  },
  components: {
    NavBar,
    CardModulos,
    NavBarVertical,
  },
};
</script>