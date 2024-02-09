<template>
  <div>
    <v-bottom-navigation :value="value" class="" color="primary" horizontal>
      <v-container class="">
        <v-row>
          <v-col v-if="urlCas.split('/')[4] == 1" cols="12" sm="6" md="3">
            <v-autocomplete
              v-model="editedItem.sala"
              :rules="[rules.required, rules.counter]"
              :items="itemsSala"
              dense
              label="SALA"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-autocomplete
              v-model="editedItem.turno"
              :rules="[rules.required, rules.counter]"
              :items="itemsTurno"
              dense
              label="TURNO"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-autocomplete
              v-model="editedItem.frecuencia"
              :rules="[rules.required, rules.counter]"
              :items="itemsFrecuencia"
              dense
              label="FRECUENCIA"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-btn @click="ejecutarTurno">
              <span>EJECUTAR</span>
              <v-icon>mdi-checkbox-marked-circle</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-bottom-navigation>

    <v-dialog v-model="dialogDataApi" hide-overlay persistent width="300">
      <v-card color="#1973a5" dark>
        <v-card-text>
          Cargando Datos
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAsistenciCorrecta"
      persistent
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡Se Grabo Correctamente La asistencia del Paciente!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAsistenciCorrecta = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogEditAsistenciCorrecta"
      persistent
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">¡Se Editó el Registro Correctamente!</div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogEditAsistenciCorrecta = false"
            >cerrar</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAsistenciNula"
      persistent
    >
      <v-card>
        <v-toolbar color="#EF5350" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡Ya se registro la asistencia para el paciente!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAsistenciNula = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogNoEdit"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">¡No se puede editar, estado inactivo!</div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogNoEdit = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAcredita"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡Lo sentimos, el paciente {{ nombrePacienteDialog }} no esta
            acreditado!, Vigencia de Seguro Hasta {{ fechaVigencia }}
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            v-if="
              (new Date().getDay() == 2 ||
                new Date().getDay() == 4 ||
                new Date().getDay() == 6) &
                (frecuenciaPac == 'MAR-JUE-SAB') ||
              (new Date().getDay() == 1 ||
                new Date().getDay() == 3 ||
                new Date().getDay() == 5) &
                (frecuenciaPac == 'LUN-MIE-VIE')
            "
            style="border: 1px; background-color: #1973a5; color: #ffffff"
            text
            @click="
              dialogAsistenciaSinAcred = true;
              dialogAcredita = false;
            "
            >Registrar Asistencia sin Acreditación</v-btn
          >
          <v-btn
            style="border: 1px; background-color: #df013a; color: #ffffff"
            text
            @click="dialogAcredita = false"
            >cerrar</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- DESPLEGABLE DE ASISTENCIA SIN ACREDITACION -->
    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      persistent
      v-model="dialogAsistenciaSinAcred"
    >
      <v-card>
        <v-toolbar color="#F78181" dark>
          REGISTRAR SOLO SI SE CUENTA CON AUTORIZACIÓN FORMAL ESSALUD (OSPE/DAR)
          DE REGULARIZACIÓN
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Registrar Asistencia de paciente: {{ nombrePacienteDialog }}
        </v-toolbar>
        <v-toolbar color="#F78181" dark>
          Seguro Vigente Hasta: {{ fechaVigencia }} - ¡Atención! - Paciente Sin
          Acreditación
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Tipo de Seguro: {{ tipoDeSeguro }}
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Tipo de Asegurado: {{ tipoAsegurado }}
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Cas Origen: {{ desCentro }}
        </v-toolbar>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-container class="mt-5">
            <v-row>
              <v-col cols="12" sm="12" md="12">
                <v-radio-group
                  v-if="
                    (new Date().getDay() == 2 ||
                      new Date().getDay() == 4 ||
                      new Date().getDay() == 6) &
                      (frecuenciaPac == 'MAR-JUE-SAB') ||
                    (new Date().getDay() == 1 ||
                      new Date().getDay() == 3 ||
                      new Date().getDay() == 5) &
                      (frecuenciaPac == 'LUN-MIE-VIE')
                  "
                  @change="validAsistencia"
                  v-model="editedItem.estado"
                  row
                >
                  <v-radio label="Asistió" value="ASISTIO"></v-radio>
                  <v-radio label="Falto" value="FALTO"></v-radio>
                </v-radio-group>
                <v-toolbar v-else>
                  !NO PUEDE REGISTRAR LA ASISTENCIA - LA FRECUENCIA NO
                  CORRESPONDE AL DÍA DE HOY¡
                </v-toolbar>
              </v-col>
              <v-col
                v-if="editedItem.estado == 'FALTO'"
                cols="12"
                sm="12"
                md="12"
              >
                <v-autocomplete
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsObserva"
                  dense
                  label="MOTIVO FALTA"
                ></v-autocomplete>
              </v-col>
              <v-col
                v-if="editedItem.estado == 'ASISTIO'"
                cols="12"
                sm="12"
                md="12"
              >
                <!-- DESPLEGABLE ASISTENCIA -->
                <v-autocomplete
                  v-if="
                    (new Date().getDay() == 2 ||
                      new Date().getDay() == 4 ||
                      new Date().getDay() == 6) &
                      (frecuenciaPac == 'MAR-JUE-SAB') ||
                    (new Date().getDay() == 1 ||
                      new Date().getDay() == 3 ||
                      new Date().getDay() == 5) &
                      (frecuenciaPac == 'LUN-MIE-VIE')
                  "
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsAsistencia"
                  dense
                  label="OBSERVACIONES"
                ></v-autocomplete>
                <!-- DESPLEGABLE ASISTENCIA -->
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions class="justify-end">
          <v-btn
            text
            @click="grabarAsistenciaSinAcredita"
            v-if="
              (new Date().getDay() == 2 ||
                new Date().getDay() == 4 ||
                new Date().getDay() == 6) &
                (frecuenciaPac == 'MAR-JUE-SAB') ||
              (new Date().getDay() == 1 ||
                new Date().getDay() == 3 ||
                new Date().getDay() == 5) &
                (frecuenciaPac == 'LUN-MIE-VIE')
            "
            >Aceptar</v-btn
          >
          <v-btn text @click="dialogAsistenciaSinAcred = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- DESPLEGABLE DE ASISTENCIA SIN ACREDITACION -->

    <!-- MENSAJE DE NO REGISTRAR ASISTENCIA POR NO TENER AUTORIZACION -->

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAsistSinAuth"
    >
      <v-card>
        <v-toolbar color="#EF5350" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            No puede registrar Asistencia sin Autorizacion de Essalud (OSPE/DAR)
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAsistSinAuth = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- MENSAJE DE NO REGISTRAR ASISTENCIA POR NO TENER AUTORIZACION -->
    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogErrorRegistrado"
    >
      <v-card>
        <v-toolbar color="#EF5350" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡El Paciente ya tiene La Asistencia Registrada!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogErrorRegistrado = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!--EDITAR ASISTENCIA-->
    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      persistent
      v-model="dialogEditRegAsistencia"
    >
      <v-card>
        <v-card v-if="validEditarAsistencia == ''">
          <v-toolbar color="#EF5350" dark>¡Aviso Importante!</v-toolbar>
          <v-card-text>
            <div class="text-h4 pa-5">
              ¡El Paciente ya tiene La Asistencia Registrada!
            </div>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              style="border: 1px; background-color: #1973a5; color: #ffffff"
              text
              @click="validEditarAsistencia = 'change'"
              >EDITAR ASISTENCIA</v-btn
            >
            <v-btn
              style="border: 1px; background-color: #df013a; color: #ffffff"
              text
              @click="dialogEditRegAsistencia = false"
              >cerrar</v-btn
            >
          </v-card-actions>
        </v-card>
        <v-toolbar
          v-if="validEditarAsistencia == 'change'"
          color="#1973a5"
          dark
        >
          Registrar Asistencia de paciente: {{ nombrePacienteDialog }}
        </v-toolbar>
        <v-toolbar
          v-if="validEditarAsistencia == 'change'"
          color="#1973a5"
          dark
        >
          Seguro Vigente Hasta: {{ fechaVigencia }}
        </v-toolbar>
        <v-toolbar
          v-if="validEditarAsistencia == 'change'"
          color="#1973a5"
          dark
        >
          Cas Origen: {{ desCentro }}
        </v-toolbar>
        <v-form
          v-if="validEditarAsistencia == 'change'"
          ref="form"
          v-model="valid"
          lazy-validation
        >
          <v-container class="mt-5">
            <v-row>
              <v-col cols="12" sm="12" md="12">
                <v-radio-group
                  @change="validAsistencia"
                  v-model="editedItem.estado"
                  row
                >
                  <v-radio label="Asistió" value="ASISTIO"></v-radio>
                  <v-radio label="Falto" value="FALTO"></v-radio>
                </v-radio-group>
              </v-col>
              <v-col
                v-if="editedItem.estado == 'FALTO'"
                cols="12"
                sm="12"
                md="12"
              >
                <v-autocomplete
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsObserva"
                  dense
                  label="MOTIVO FALTA"
                ></v-autocomplete>
              </v-col>
              <v-col
                v-if="editedItem.estado == 'ASISTIO'"
                cols="12"
                sm="12"
                md="12"
              >
                <!-- DESPLEGABLE ASISTENCIA -->
                <v-autocomplete
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsAsistencia"
                  dense
                  label="OBSERVACIONES"
                ></v-autocomplete>
                <!-- DESPLEGABLE ASISTENCIA -->
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions
          v-if="validEditarAsistencia == 'change'"
          class="justify-end"
        >
          <v-btn text @click="editarAsistencia">EDITAR</v-btn>
          <v-btn text @click="dialogEditRegAsistencia = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      persistent
      v-model="dialogRegAsistencia"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>
          Registrar Asistencia de paciente: {{ nombrePacienteDialog }}
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Seguro Vigente Hasta: {{ fechaVigencia }}
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Tipo de Seguro: {{ tipoDeSeguro }}
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Tipo de Asegurado: {{ tipoAsegurado }}
        </v-toolbar>
        <v-toolbar color="#1973a5" dark>
          Cas Origen: {{ desCentro }}
        </v-toolbar>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-container class="mt-5">
            <v-row>
              <v-col cols="12" sm="12" md="12">
                <v-radio-group
                  v-if="
                    (new Date().getDay() == 2 ||
                      new Date().getDay() == 4 ||
                      new Date().getDay() == 6) &
                      (frecuenciaPac == 'MAR-JUE-SAB') ||
                    (new Date().getDay() == 1 ||
                      new Date().getDay() == 3 ||
                      new Date().getDay() == 5) &
                      (frecuenciaPac == 'LUN-MIE-VIE')
                  "
                  @change="validAsistencia"
                  v-model="editedItem.estado"
                  row
                >
                  <v-radio label="Asistió" value="ASISTIO"></v-radio>
                  <v-radio label="Falto" value="FALTO"></v-radio>
                </v-radio-group>
                <v-toolbar v-else>
                  !NO PUEDE REGISTRAR LA ASISTENCIA - LA FRECUENCIA NO
                  CORRESPONDE AL DÍA DE HOY¡
                </v-toolbar>
              </v-col>
              <v-col
                v-if="editedItem.estado == 'FALTO'"
                cols="12"
                sm="12"
                md="12"
              >
                <v-autocomplete
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsObserva"
                  dense
                  label="MOTIVO FALTA"
                ></v-autocomplete>
              </v-col>
              <v-col
                v-if="editedItem.estado == 'ASISTIO'"
                cols="12"
                sm="12"
                md="12"
              >
                <!-- DESPLEGABLE ASISTENCIA -->
                <v-autocomplete
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsAsistencia"
                  dense
                  label="OBSERVACIONES"
                ></v-autocomplete>
                <!-- DESPLEGABLE ASISTENCIA -->
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions class="justify-end">
          <v-btn
            text
            @click="grabarAsistenciaPac"
            v-if="
              (new Date().getDay() == 2 ||
                new Date().getDay() == 4 ||
                new Date().getDay() == 6) &
                (frecuenciaPac == 'MAR-JUE-SAB') ||
              (new Date().getDay() == 1 ||
                new Date().getDay() == 3 ||
                new Date().getDay() == 5) &
                (frecuenciaPac == 'LUN-MIE-VIE')
            "
            >Aceptar</v-btn
          >
          <v-btn text @click="dialogRegAsistencia = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      persistent
      v-model="dialogRegFalta"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>
          Registrar Motivo de Inasistencia
        </v-toolbar>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-container class="mt-5">
            <v-row>
              <v-col cols="12" sm="12" md="12">
                <v-autocomplete
                  v-model="editedItem.observaFalta"
                  :rules="[rules.required]"
                  :items="itemsObserva"
                  dense
                  label="MOTIVO FALTA"
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions class="justify-end">
          <v-btn text @click="grabarFaltaPac">Aceptar</v-btn>
          <v-btn text @click="dialogRegFalta = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-row>
        <v-col
          :key="indice"
          v-for="(contadorRes, indice) in contadorConf"
          cols="12"
          sm="3"
          md="3"
        >
          <v-card class="mx-auto" max-width="350">
            <v-card-text>
              <div>PUESTO {{ contadorRes.datosPueto.numeroPuesto }}</div>
              <p class="text-h5 text--primary">
                {{ contadorRes.datosPueto.tipoPuesto }}
              </p>

              {{ contadorRes.datosPaciente.datosMaestro.descripMaestro }} :
              {{ contadorRes.datosPaciente.num_doc }}

              <div>
                {{
                  contadorRes.datosPaciente.ape_pat +
                  " " +
                  contadorRes.datosPaciente.ape_mat +
                  " " +
                  contadorRes.datosPaciente.nombres
                }}
              </div>
            </v-card-text>
            <v-card-actions
              style="display: flex; justify-content: space-between"
            >
              <v-btn
                v-if="urlCas.split('/')[4] == '1'"
                @click="configItem(contadorRes)"
                text
                color="deep-purple accent-4"
                elevation="2"
              >
                Asistencia
              </v-btn>
              <v-btn
                v-else
                @click="configItem(contadorRes)"
                text
                color="deep-purple accent-4"
                elevation="2"
              >
                Asistencia
              </v-btn>
              <div v-if="urlCas.split('/')[4] == '1'">
                <v-icon
                  large
                  @click="asistenciaPacienteICon(contadorRes)"
                  style="color: #004d40"
                  >mdi-check-circle</v-icon
                >
                <v-icon
                  large
                  @click="faltaPacienteICon(contadorRes)"
                  style="color: #ef5350"
                  >mdi-close-circle</v-icon
                >
              </div>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
export const RUTA_SERVIDOR = process.env.VUE_APP_RUTA_API;
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
export const RUTA_CENTRAL = process.env.VUE_APP_CENTRAL;
export const USUARIO_CENTRAL = process.env.VUE_APP_CENTRAL_USERNAME;
export const PASSWORD_CENTRAL = process.env.VUE_APP_CENTRAL_PASSWORD;

export default {
  data: () => ({
    datosContadorRes: null,
    //value
    value: 1,
    dialogAsistenciCorrecta: false,
    dialogAsistenciNula: false,
    dialogRegFalta: false,
    dialogAsistenciaSinAcred: false,
    dialogAsistSinAuth: false,
    //cupos
    itemsTurno: ["TURNO 1", "TURNO 2", "TURNO 3", "TURNO 4"],
    itemsFrecuencia: ["LUN-MIE-VIE", "MAR-JUE-SAB"],
    itemsSala: ["SALA1", "SALA2", "SALA3", "SALA4"],
    itemsEstado: ["true", "false"],
    itemsPuesto: ["NORMAL", "ESPECIAL"],
    itemsObserva: [
      "FALLECIDO",
      "HOSPITALIZACION",
      "PACIENTE TRANSFERIDO",
      "NO ACUDIO A SESION DE HEMODIALISIS",
    ],
    itemsAsistencia: [
      "ASISTIO EN TURNO DIFERENTE POR CITA MEDICA",
      "DIALISIS FRUSTRA",
      "SIN OBSERVACION",
    ],
    itemsAsistSinAcred: [
      "SE CUENTA CON AUTORIZACION FORMAL ESSALUD (OSPE/DAR) DE REGULARIZACION",
      "SIN AUTORIZACION",
    ],
    //JALAR DATA DE USER
    datosEditPuesto: "",
    //perfil data
    perfil: "",
    nombre: "",
    url: "",
    usuario: "",
    //Datos de formulario
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    editedItem: {
      //Cupos
      turno: "",
      frecuencia: "",
      sala: "",
      capacidad: Number,
      tipoPuesto: "",
      estado: null,
      numeroPuesto: null,
      observaFalta: "",
    },
    // SIN ACREDITACION
    autorizacion: "",
    // SIN ACREDI
    headers: [],
    desserts: [],
    editedIndex: -1,
    dataex: "",
    defaultItem: {
      turno: "",
      frecuencia: "",
      sala: "",
      capacidad: Number,
      tipoPuesto: "",
      estado: null,
      numeroPuesto: null,
      observaFalta: "",
    },
    dialog: false,
    dialogEdit: false,
    formAdmi: false,
    dialogDelete: false,
    dialogEditAdm: false,
    dialogNoEdit: false,
    dialogDataApi: false,
    dialogRegAsistencia: false,
    dialogAcredita: false,
    dialogErrorRegistrado: false,
    dialogEditRegAsistencia: false,
    dialogEditAsistenciCorrecta: false,
    vista: "",
    valid: true,
    datosEdit: "",
    actionBoton: "AGREGAR",
    contadorConf: [],
    nombrePacienteDialog: "",
    urlPacienteAsistencia: "",
    urlAsigCuposPac: "",
    frecuenciaPac: "",
    tipoDeSeguro: "",
    tipoAsegurado: "",
    fechaVigencia: "",
    desCentro: "",
    urlEditAsistencia: "",
    validEditarAsistencia: "",
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },
  methods: {
    validAsistencia(e) {
      // console.log(e.target.value)
      if (e != "") {
        this.editedItem.observaFalta = "";
      }
      // if (e == "ASISTIO") {
      //   this.editedItem.observaFalta = "";
      // }
    },

    grabarFaltaPac() {
      if (!this.editedItem.observaFalta) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_API + "/asisPacDiario/",
                {
                  asigCuposPac: this.datosContadorRes.url,
                  estadoAsistencia: "FALTO",
                  estadoAcredi: "ACREDITADO",
                  observaFalta: this.editedItem.observaFalta,
                  usuario_reg: this.usuario + "|" + this.nombre,
                  validacionAsistencia:
                    new Date(
                      Date.now() - new Date().getTimezoneOffset() * 60000
                    )
                      .toISOString()
                      .substr(0, 10) +
                    "|" +
                    this.datosContadorRes.datosPaciente.url.split("/")[4],
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dialogRegFalta = false;
                this.dialogAsistenciCorrecta = true;
                setTimeout(() => {
                  this.dialogAsistenciCorrecta = false;
                }, 1000);
              })
              .catch((res) => {
                console.log("res", res);
                this.dialogAsistenciNula = true;
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
    },
    //
    faltaPacienteICon(contadorRes) {
      this.editedItem.observaFalta = "";
      this.dialogRegFalta = true;
      this.datosContadorRes = contadorRes;
    },
    //Aistencia con icono check
    asistenciaPacienteICon(contadorRes) {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .post(
              RUTA_API + "/asisPacDiario/",
              {
                asigCuposPac: contadorRes.url,
                estadoAsistencia: "ASISTIO",
                usuario_reg: this.usuario + "|" + this.nombre,
                validacionAsistencia:
                  new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
                    .toISOString()
                    .substr(0, 10) +
                  "|" +
                  contadorRes.datosPaciente.url.split("/")[4],
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              /*console.log("exito", res.status);
              this.editedItem.estado = "";
              this.editedItem.observaFalta = "";
              this.dialogRegAsistencia = false;*/
              this.dialogAsistenciCorrecta = true;
              setTimeout(() => {
                this.dialogAsistenciCorrecta = false;
              }, 1000);
            })
            .catch((res) => {
              /*this.dialogErrorRegistrado = true;
              this.dialogRegAsistencia = false;
              this.editedItem.estado = "";
              this.editedItem.observaFalta = "";
              console.log("Error:", res);*/
              console.log("res", res);
              this.dialogAsistenciNula = true;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },
    //Grabar Asistencia de paciente
    grabarAsistenciaPac() {
      if (this.editedItem.estado == "FALTO" && !this.editedItem.observaFalta) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_API + "/asisPacDiario/",
                {
                  asigCuposPac: this.urlAsigCuposPac,
                  estadoAsistencia: this.editedItem.estado,
                  observaFalta: this.editedItem.observaFalta,
                  estadoAcredi: "ACREDITADO",
                  casAsd: this.desCentro,
                  vigSeguro: this.fechaVigencia,
                  usuario_reg: this.usuario + "|" + this.nombre,
                  validacionAsistencia:
                    new Date(
                      Date.now() - new Date().getTimezoneOffset() * 60000
                    )
                      .toISOString()
                      .substr(0, 10) +
                    "|" +
                    this.urlPacienteAsistencia.split("/")[4],
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.editedItem.estado = "";
                this.editedItem.observaFalta = "";
                this.dialogRegAsistencia = false;
                this.dialogAsistenciCorrecta = true;
              })
              .catch((res) => {
                this.dialogErrorRegistrado = true;
                this.dialogRegAsistencia = false;
                this.editedItem.estado = "";
                this.editedItem.observaFalta = "";
                console.log("Error:", res);
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
    },

    grabarAsistenciaSinAcredita() {
      this.dialogAsistenciaSinAcred = true;

      if (this.editedItem.estado == "FALTO" && !this.editedItem.observaFalta) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_API + "/asisPacDiario/",
                {
                  asigCuposPac: this.urlAsigCuposPac,
                  estadoAsistencia: this.editedItem.estado,
                  observaFalta: this.editedItem.observaFalta,
                  estadoAcredi: "SIN ACREDITACIÓN",
                  casAsd: this.desCentro,
                  vigSeguro: this.fechaVigencia,
                  usuario_reg: this.usuario + "|" + this.nombre,
                  validacionAsistencia:
                    new Date(
                      Date.now() - new Date().getTimezoneOffset() * 60000
                    )
                      .toISOString()
                      .substr(0, 10) +
                    "|" +
                    this.urlPacienteAsistencia.split("/")[4],
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.editedItem.estado = "";
                this.editedItem.observaFalta = "";
                this.dialogRegAsistencia = false;
                this.dialogAsistenciCorrecta = true;
                this.dialogAsistenciaSinAcred = false;
              })
              .catch((res) => {
                this.dialogErrorRegistrado = true;
                this.dialogRegAsistencia = false;
                this.editedItem.estado = "";
                this.editedItem.observaFalta = "";
                this.dialogAsistenciaSinAcred = false;
                console.log("Error:", res);
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
    },

    cambioPuesto() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_API +
                "/parameCentroPuesto/" +
                this.datosEditPuesto.split("/")[4] +
                "/",
              {
                tipoPuesto: this.editedItem.tipoPuesto,
                estado: this.editedItem.estado,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.dialogDataApi = true;
              console.log("exito", res.status);
              //this.close();
              this.dialogRegAsistencia = false;
              this.ejecutarTurno();
              this.ParameCentroPuestoInit();
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.dialog = false;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },

    configItem(item) {
      //this.dialogDataApi = true;
      console.log("item", item);
      this.validEditarAsistencia = "";
      this.urlEditAsistencia = "";
      this.nombrePacienteDialog = "";
      this.fechaVigencia = "";
      this.desCentro = "";
      this.editedItem.estado = "";
      this.editedItem.observaFalta = "";
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_API +
                "/asisPacDiario/?search=" +
                new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
                  .toISOString()
                  .substr(0, 10) +
                "|" +
                item.datosPaciente.url.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("respuesta", item.datosPaciente.tipo_doc.split("/")[4]);
              if (res.data.length == 0) {
                axios
                  .post(RUTA_API + "/api/token/", {
                    username: USUARIO,
                    password: PASSWORD,
                  })
                  .then((response) => {
                    this.auth = "Bearer " + response.data.access;
                    axios
                      .post(
                        RUTA_API + "/users/",
                        {
                          codOpcion: "1",
                          codTipDoc:
                            item.datosPaciente.tipo_doc.split("/")[4] == 5
                              ? "1"
                              : "2",
                          numDoc: item.datosPaciente.num_doc,
                          fecNacimiento:
                            item.datosPaciente.fecha_nac.split("-")[2] +
                            "/" +
                            item.datosPaciente.fecha_nac.split("-")[1] +
                            "/" +
                            item.datosPaciente.fecha_nac.split("-")[0],
                        },
                        {
                          headers: { Authorization: this.auth },
                        }
                      )
                      .then((response) => {
                        console.log(response.data);
                        if (
                          response.data.vDataItem[0].flagIndicadorActivo == "1"
                        ) {
                          console.log(
                            "esta acreditado:",
                            response.data.vDataItem[0].fecVigHasta +
                              "|" +
                              item.url
                          );
                          this.urlPacienteAsistencia = item.datosPaciente.url;
                          this.nombrePacienteDialog =
                            item.datosPaciente.ape_pat +
                            " " +
                            item.datosPaciente.ape_mat +
                            " " +
                            item.datosPaciente.nombres;
                          this.tipoDeSeguro =
                            response.data.vDataItem[0].desTipoSeg;
                          this.fechaVigencia =
                            response.data.vDataItem[0].fecVigHasta;
                          this.desCentro = response.data.vDataItem[0].desCentro;
                          this.dialogRegAsistencia = true;
                          this.urlAsigCuposPac = item.url;
                          this.frecuenciaPac = item.datosPueto.frecuencia;
                        } else {
                          this.nombrePacienteDialog =
                            item.datosPaciente.ape_pat +
                            " " +
                            item.datosPaciente.ape_mat +
                            " " +
                            item.datosPaciente.nombres;
                          this.tipoDeSeguro =
                            response.data.vDataItem[0].desTipoSeg;
                          this.fechaVigencia =
                            response.data.vDataItem[0].fecVigHasta;
                          this.frecuenciaPac = item.datosPueto.frecuencia;
                          this.urlAsigCuposPac = item.url;
                          this.desCentro = response.data.vDataItem[0].desCentro;
                          this.urlPacienteAsistencia = item.datosPaciente.url;
                          this.dialogAcredita = true;
                          console.log(
                            "no esta acreditado:",
                            response.data.vDataItem[0].fecVigHasta
                          );
                        }
                        //servicio nuevo de Acreditación
                        axios
                          .post(
                            RUTA_API + "/seguro/",
                            {
                              tpdoc:
                                item.datosPaciente.tipo_doc.split("/")[4] == 5
                                  ? "01"
                                  : "04",
                              nrdoc: item.datosPaciente.num_doc,
                              codcentro: "401",
                            },
                            {
                              headers: { Authorization: this.auth },
                            }
                          )
                          .then((resS004) => {
                            this.tipoDeSeguro = resS004.data.data.tipoSeguro;
                            this.tipoAsegurado =
                              resS004.data.data.tipoAsegurado;
                            this.dialogDataApi = false;
                          })
                          .catch((error) => {
                            console.log("Error on Authentication", error);
                          });
                        //fin de nuevo servicio de acreditación
                      })
                      .catch((error) => {
                        console.log("Error on Authentication", error);
                      });
                  })
                  .catch((response) => {
                    response === 404
                      ? console.warn("lo sientimos no tenemos servicios")
                      : console.warn("Error:", response);
                  });
              } else {
                console.log("Editar Registro", res.data[0].url.split("/")[4]);
                this.dialogEditRegAsistencia = true;
                this.nombrePacienteDialog =
                  item.datosPaciente.ape_pat +
                  " " +
                  item.datosPaciente.ape_mat +
                  " " +
                  item.datosPaciente.nombres;
                this.fechaVigencia = res.data[0].vigSeguro;
                this.desCentro = res.data[0].casAsd;
                this.editedItem.estado = res.data[0].estadoAsistencia;
                this.editedItem.observaFalta = res.data[0].observaFalta;
                this.urlEditAsistencia = res.data[0].url;
              }
            })
            .catch((res) => {
              console.log("algo salio mal", res);
            });
        })
        .catch((response) => {
          console.log("error servicio", response);
        });
    },

    editarAsistencia() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_API +
                "/asisPacDiario/" +
                this.urlEditAsistencia.split("/")[4] +
                "/",
              {
                estadoAsistencia: this.editedItem.estado,
                observaFalta: this.editedItem.observaFalta,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("Listo Editado", res);
              this.dialogEditRegAsistencia = false;
              this.dialogEditAsistenciCorrecta = true;
            })
            .catch((res) => {
              console.log("Error de Consulta", res);
            });
        })
        .catch((response) => {
          console.log("Error Servicio", response);
        });
    },

    ejecutarTurno() {
      if (this.urlCas.split("/")[4] == "1") {
        if (this.editedItem.sala == "SALA1") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.datosPueto.turno == this.editedItem.turno &&
              e.datosPueto.frecuencia == this.editedItem.frecuencia &&
              e.datosPueto.numeroPuesto > 0 &&
              e.datosPueto.numeroPuesto <= 10
          );
          resultTurno.sort((a, b) =>
            a.datosPaciente.ape_pat.localeCompare(b.datosPaciente.ape_pat)
          );
          /*resultTurno.sort(
            (x, y) => x.datosPueto.numeroPuesto - y.datosPueto.numeroPuesto
          );*/
          this.contadorConf = resultTurno;
        }
        if (this.editedItem.sala == "SALA2") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.datosPueto.turno == this.editedItem.turno &&
              e.datosPueto.frecuencia == this.editedItem.frecuencia &&
              e.datosPueto.numeroPuesto > 10 &&
              e.datosPueto.numeroPuesto <= 20
          );
          resultTurno.sort((a, b) =>
            a.datosPaciente.ape_pat.localeCompare(b.datosPaciente.ape_pat)
          );
          /*resultTurno.sort(
            (x, y) => x.datosPueto.numeroPuesto - y.datosPueto.numeroPuesto
          );*/
          this.contadorConf = resultTurno;
        }
        if (this.editedItem.sala == "SALA3") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.datosPueto.turno == this.editedItem.turno &&
              e.datosPueto.frecuencia == this.editedItem.frecuencia &&
              e.datosPueto.numeroPuesto > 20 &&
              e.datosPueto.numeroPuesto <= 30
          );
          resultTurno.sort((a, b) =>
            a.datosPaciente.ape_pat.localeCompare(b.datosPaciente.ape_pat)
          );
          /*resultTurno.sort(
            (x, y) => x.datosPueto.numeroPuesto - y.datosPueto.numeroPuesto
          );*/
          this.contadorConf = resultTurno;
        }
        if (this.editedItem.sala == "SALA4") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.datosPueto.turno == this.editedItem.turno &&
              e.datosPueto.frecuencia == this.editedItem.frecuencia &&
              e.datosPueto.numeroPuesto > 30 &&
              e.datosPueto.numeroPuesto <= 40
          );
          resultTurno.sort((a, b) =>
            a.datosPaciente.ape_pat.localeCompare(b.datosPaciente.ape_pat)
          );
          /*resultTurno.sort(
            (x, y) => x.datosPueto.numeroPuesto - y.datosPueto.numeroPuesto
          );*/
          this.contadorConf = resultTurno;
        }
      } else {
        const resultTurno = this.desserts.filter(
          (e) =>
            e.datosPueto.turno == this.editedItem.turno &&
            e.datosPueto.frecuencia == this.editedItem.frecuencia
        );
        resultTurno.sort((a, b) =>
          a.datosPaciente.ape_pat.localeCompare(b.datosPaciente.ape_pat)
        );
        /*resultTurno.sort(
            (x, y) => x.datosPueto.numeroPuesto - y.datosPueto.numeroPuesto
          );*/
        this.contadorConf = resultTurno;
      }
    },

    initialize() {
      this.desserts = [];
    },

    editItem(item) {
      console.log("item", item);
      this.editedItem.turno = item.turno;
      this.editedItem.frecuencia = item.frecuencia;
      this.editedItem.capacidad = item.capacidad;
      this.editedItem.estado = item.estado;
      this.datosEdit = item.url;
      if (item.estado == true) {
        this.dialogEdit = true;
      } else {
        this.dialogNoEdit = true;
      }
    },

    deleteItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {},

    closeFormAdmin() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    edit() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_API + "/parameCentro/" + this.datosEdit.split("/")[4] + "/",
              {
                estado: false,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.dialogDataApi = true;
              console.log("exito", res.status);
              this.close();
              this.ParameCentroPuestoInit();
              this.dialogEdit = false;
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.dialog = false;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeEdit() {
      this.dialogEdit = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      console.log("click");
      if (
        !this.editedItem.turno ||
        !this.editedItem.frecuencia ||
        !this.editedItem.capacidad
      ) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_API + "/parameCentro/",
                {
                  cas: this.urlCas,
                  turno: this.editedItem.turno,
                  frecuencia: this.editedItem.frecuencia,
                  capacidad: this.editedItem.capacidad,
                  estado: true,
                  usuario_reg: this.usuario + "|" + this.nombre,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                //console.log(this.editedItem);
                this.ParameCentroPuestoInit();
              })
              .catch((res) => {
                console.log("Error:", res);
                this.dialog = false;
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
      //console.log('holaaaaaaaa',this.editedItem)
    },

    nutricion() {
      console.log("nutricion");
    },

    cabezeraParameCentro() {
      this.headers = [
        { text: "Turno", value: "turno" },
        {
          text: "Frecuencia",
          align: "start",
          sortable: false,
          value: "frecuencia",
        },
        { text: "Capacidad", value: "capacidad" },
        { text: "Estado", value: "estado" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    ParameCentroPuestoInit() {
      this.dialogDataApi = true;
      this.cabezeraParameCentro();
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_API +
                "/parameCentroPuesto/?search=true," +
                this.urlCas.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              axios
                .get(
                  RUTA_API +
                    "/asigCuposPac/?search=" +
                    this.urlCas.split("/")[4] +
                    ",true",
                  {
                    headers: { Authorization: this.auth },
                  }
                )
                .then((resCuposAsig) => {
                  this.dialogDataApi = false;
                  console.log("dessert", this.desserts);
                  console.log("resCuposAsig", resCuposAsig.data);
                  this.desserts = resCuposAsig.data;
                })
                .catch((res) => {
                  console.warn("Error:", res);
                  this.dialog = false;
                });
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.dialog = false;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },
  },

  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
  },

  created() {
    this.perfil = sessionStorage.getItem("perfil");
    this.nombre = sessionStorage.getItem("nombre");
    this.url = sessionStorage.getItem("url");
    this.usuario = sessionStorage.getItem("usuario");
    this.urlCas = sessionStorage.getItem("urlCas");
    console.log("Url", this.url);
    console.log("Perfil", this.perfil);
    console.log("Nombre", this.nombre);
    console.log("urlCas", this.urlCas);
    //INICIO DE CONSULTA
    this.ParameCentroPuestoInit();
  },

  components: {},
};
</script>