<template>
  <div>
    <!-- CONSULTA SOLICITUDES-->
    <!-- <v-dialog v-model="dialogCorreo" max-width="600px" persistent>
      <v-card class="mx-auto">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="mt-4 mx-auto container">
            <v-col cols="12" sm="12" md="12">
              <h3 class="text-center mb-3">Solicitud de cambio de turno de paciente</h3>
              <p>Escriba su correo electronico para enviar constancia de envio de solicitud.</p>
              <v-text-field v-model="correo" label="Correo electronico"></v-text-field>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" @click="enviarCorreo" text> ACEPTAR </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog> -->
    <v-dialog v-model="dialogConfirmacion" max-width="600px">
      <v-card class="mx-auto">
        <!-- <v-icon class="">mdi-close-circle</v-icon> -->
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="mx-auto container">
            <v-col></v-col>
            <v-flex justify-center>
              <p></p>
              <v-icon color="green" large>mdi-checkbox-marked-circle</v-icon>
            </v-flex>
            <v-col cols="12" sm="12" md="12">
              <p class="text-center my-0">{{ mensaje }}</p>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-flex justify-center>
              <v-btn outlined color="blue darken-1" @click="dialogConfirmacion = false"> ACEPTAR
              </v-btn>
            </v-flex>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogoEliminacion" max-width="600px" persisten>
      <v-card class="mx-auto">
        <!-- <v-icon class="">mdi-close-circle</v-icon> -->
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="mt-4 mx-auto container">
            <v-col cols="12" sm="12" md="12">
              <h3 class="text-center mb-3">
                Solicitud de cambio de turno de paciente
              </h3>
              <p class="text-center">
                ¿Esta seguro de eliminar la solicitud de cambio del paciente?
              </p>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" @click="dialogoEliminacion = false" text>
              CANCELAR
            </v-btn>
            <v-btn color="blue darken-1" @click="eliminarSolicitud" text>
              ACEPTAR
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <v-container>
      <v-card class="mx-auto my-5" max-width="1000">
        <v-system-bar color="#1973a5" dark>
          <v-flex>
            <center>CONSULTAR ESTADO DE SOLICITUD</center>
          </v-flex>
        </v-system-bar>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="mt-4 container align-baseline">
            <!-- CAJA DE TEXTO DE DOCUMENTO-->
            <v-col cols="6" sm="6" md="6">
              <v-text-field v-model="editedItem.documento2" :rules="[rules.required]" label="Buscar por documento"
                :maxlength="8">
              </v-text-field>
            </v-col>
            <!-- BOTON DE CONSULTA DOCUMENTO-->
            <v-col cols="3" sm="3" md="3">
              <v-btn color="primary" @click="listarSolicitudes" outlined>
                <span>Buscar</span>
                <v-icon>mdi-checkbox-marked-circle</v-icon>
              </v-btn>
            </v-col>
            <!-- BOTON DE AGREGAR SOLICITUD-->
            <v-btn color="#1973a5" dark class="mb-2" @click="dialog = true">
              {{ actionBoton }}
            </v-btn>
            <!-- CAJA DE TEXTO NOMBRE PACIENTE-->
            <v-col cols="12" sm="12" md="12" v-if="editedItem.documento2">
              <v-text-field label="Paciente" filled disabled v-model="nombrePaciente" height="10px">
              </v-text-field>
            </v-col>
          </v-row>
        </v-form>
        <!-- TABLA RESULTADO-->
        <v-card class="mb-4" v-if="!nombrePaciente">
          <v-tabs v-model="tab" background-color="#1973a5" @change="cambioTab" center-active dark>
            <v-tab value="pendientes">EN PROCESO</v-tab>
            <v-tab value="atendidos">FINALIZADOS</v-tab>
            <!-- OBSERVADOS Y TERMINADOS -->
          </v-tabs>
        </v-card>
        <v-data-table :headers="headers" :items="desserts" class="elevation-1">
          <!-- <template v-slot:item.url="{ value }" v-if="tab == 0">
            <v-btn color="orange" @click="abrirDialog(value)" small text><v-icon>mdi-trash-can</v-icon></v-btn>
          </template>
          <template class="text-center" v-slot:item.url v-else-if="tab == 1">
            <v-icon color="green">mdi-checkbox-marked-circle</v-icon>
          </template> -->

          <template v-slot:item.url="{ item }">
            <!-- <p v-if="item.respuesta  == 'PENDIENTE'">{{ item.respuesta }}</p> -->
            <v-btn v-if="item.respuesta == 'PENDIENTE'" color="orange" @click="abrirDialog(item.url)" small
              text><v-icon>mdi-trash-can</v-icon></v-btn>
            <v-btn v-else-if="item.respuesta == 'ATENDIDO'" small text>
              <v-icon color="green">mdi-check-circle</v-icon>
            </v-btn>
            <v-btn v-else-if="item.respuesta == 'OBSERVADO'" small text>
              <v-icon color="red">mdi-close-circle</v-icon>
            </v-btn>

          </template>

        </v-data-table>
      </v-card>
    </v-container>
    <!-- REGISTRO SOLICITUDES-->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <!--<v-card class="mx-auto my-5">-->
      <v-card class="mx-auto">
        <v-system-bar color="#1973a5" dark>
          <v-flex>
            <center>REGISTRO DE SOLICITUD</center>
          </v-flex>
        </v-system-bar>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="mt-4 container">
            <!-- LISTA DE PACIENTES -->
            <v-col cols="12" sm="12" md="12">
              <v-autocomplete v-model="editedItem.paciente" :rules="[rules.required]" :items="itemsDatosPaciente"
                item-text="nombreCompleto" item-value="paciente" dense label="PACIENTE"></v-autocomplete>
              <!-- <input value=""  type="text" hidden> -->
            </v-col>
            <!-- COMBOBOX TIPO SOLICITUD -->
            <v-col cols="6" sm="6" md="6">
              <v-autocomplete v-model="editedItem.tipoSolicitud" :rules="[rules.required]" :items="itemsTipoSolcitud"
                dense label="Tipo Solicitud"></v-autocomplete>
            </v-col>
            <!-- COMBOBOX NUEVO TURNO -->
            <v-col cols="6" sm="6" md="6">
              <v-autocomplete v-model="editedItem.turno" :rules="[rules.required]" :items="itemsTurno" dense
                label="Nuevo Turno"></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="12" md="12">
              <!-- <h3 class="text-center mb-3">Solicitud de cambio de turno de paciente</h3> -->
              <p>
                Escriba su correo electronico para enviar constancia de envio de
                solicitud.
              </p>
              <v-text-field v-model="editedItem.correo" :rules="[rules.required, rules.email]"
                label="Correo electronico"></v-text-field>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="close"> Cancelar </v-btn>
            <v-btn color="blue darken-1" text @click="save"> Guardar </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
import axios from "axios";

export default {
  data: () => ({
    actionBoton: "AGREGAR SOLICITUD",
    nombrePaciente: [],
    editedItem: {
      //Cupos
      paciente: "",
      frecuencia: "",
      turno: "",
      nombrePaciente: "",
      correo: "",
    },
    defaultItem: {
      paciente: "",
      frecuencia: "",
      turno: "",
    },
    headers: [],
    desserts: [],
    dialog: false,
    valid: true,
    expression: /\w+@\w+\.+[a-z]/,
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      email: (value) => !!/\w+@\w+\.+[a-z]/.test(value) || "Correo invalido",
    },

    itemsDatosPaciente: [],
    itemsTurno: [],
    itemsTipoSolcitud: [],
    nombrePaciente: "",
    tab: 0,
    estadoTab: "PENDIENTE",
    dialogoEliminacion: false,
    dialogCorreo: false,
    correo: "",
    dialogConfirmacion: false,
    mensaje: "Estado de solicitud actualizada con exito.",
  }),
  computed: {},
  watch: {},
  methods: {
    enviarAlCorreo(apepat, apemat, nombre) {
      let data = {
        asunto: "Mensaje de confirmacion",
        mensaje: "hola",
        destinatario: this.editedItem.correo,
        html: `<div style="width:700px;margin: 0 auto;">
                    <div style="width:700px;">
                        <img src="https://inhouse.academicovitem.com/assets/img/logos/essalud-renal.png" width="200" >
                    </div>
                    <div >
                        <h1 style="color:#007AC9;text-transform:uppercase;font-weight:600;font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;text-align:center;">CONFIRMACION DE ENVIO DE SOLICITUD</h1>
                    </div>
                    <p style="text-align:center;font-size:15px;;font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;">Este correo fue generado de forma automática por<strong style="color:#766AE0"> HISAR-SERVICE,</strong><strong style="color:#766AE0"> Por favor no responder.</strong></p>
                    <div style="width:fit-content;margin:0 auto;margin-bottom:5px;border-radius:7px;padding:10px;background-color:#E3DDFB;">  
                        <h3 style="text-align:center;font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;">PACIENTE: ${apepat}  ${apemat} ${nombre}</h3>
                        
                        <p style="text-align:center;font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;color:#000">Tipo de solicitud: ${this.editedItem.tipoSolicitud}</p>
                        <p style="text-align:center;font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;color:#000">Turno: ${this.editedItem.turno}</p>
                    </div>
                    <div style="width:500px;margin:0 auto">
                        <img src="https://blog.vantagecircle.com/content/images/2021/07/Basics-Of-Employee-Engagement-Surveys.png" width="500">
                    </div>
                    <div style="background-color:#007AC9;color:#FFF;padding-top:2px">
                        <p style="padding:5px;text-align:center;font-size:14px;font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif">@HISAR-SERVICE / DSI</p>
                    </div>  
        </div>`,
      };
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .post(RUTA_API + "/enviar-correo-adj/", data, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("exito", res.status);
            });
        });
    },
    guardarCorreo() {
      console.log("enviar correo");
      let data = {
        cas: this.urlCas,
        usuario: this.url,
        correo: this.editedItem.correo,
      };
      // console.log(data)
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .post(RUTA_API + "/correos/", data, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("exito", res.status);
            });
        });
    },
    cambioTab() {
      console.log('Tab: ',this.tab)
      if (this.tab == 0) {
        this.desserts = [];
        this.estadoTab = "PENDIENTE";
        this.solicitudes();
      } else if (this.tab == 1) {
        this.desserts = [];
        this.estadoTab = "ATENDIDO";
        this.solicitudes();
      }
      // if (this.tab == 1) this.estadoTab = "ATENDIDO"
    },
    listarPacientes() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_API + "/asigCuposPac/?search=" + this.urlCas.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.itemsDatosPaciente = [];
              //console.log("data", res.data);
              for (let i = 0; i < res.data.length; i++) {
                this.itemsDatosPaciente.push({
                  nombreCompleto:
                    res.data[i].datosPaciente.ape_pat +
                    " " +
                    res.data[i].datosPaciente.ape_mat +
                    " " +
                    res.data[i].datosPaciente.nombres,
                  paciente: res.data[i].paciente,
                });
              }
              this.dialogDataApi = false;
              console.log(res.status);
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
    buscarPaciente() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/paciente/?search=" + this.urlCas.split("/")[4] + "+" + this.editedItem.documento, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.nombrePaciente =
                res.data[0].ape_pat +
                " " +
                res.data[0].ape_mat +
                " " +
                res.data[0].nombres;
            })
            .catch((res) => {
              console.log(res.status);
            });
        })
        .catch((response) => {
          console.log(response.data);
        });
    },
    comboTipoSolicitud() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/maestro/?search=TS001", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              for (let i = 0; i < res.data.length; i++) {
                this.itemsTipoSolcitud.push(res.data[i].descripMaestro);
              }
            })
            .catch((res) => {
              console.log(res.data);
            });
        })
        .catch((response) => {
          console.log(response.data);
        });
    },
    comboTurnos() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/maestro/?search=TR001", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              for (let i = 0; i < res.data.length; i++) {
                this.itemsTurno.push(res.data[i].descripMaestro);
              }
            })
            .catch((res) => {
              console.log(res.data);
            });
        })
        .catch((response) => {
          console.log(response.data);
        });
    },
    abrirDialog(url) {
      this.dialogoEliminacion = true;
      this.idItem = url.split("/")[4];
      console.log(this.idItem);
    },

    ///
    solicitudes() {
      // this.cabezeraSolicitud();
      this.headers = [
        {
          text: "Apellido Paterno",
          value: "datosPaciente.ape_pat",
        },
        {
          text: "Apellido Materno",
          value: "datosPaciente.ape_mat",
        },
        {
          text: "Nombre",
          value: "datosPaciente.nombres",
        },
        {
          text: "Tipo Solicitud",
          value: "tipoSolicitud",
        },
        {
          text: "Fecha Solicitud",
          value: "fechaSolicitud",
        },
        {
          text: "Nuevo Turno",
          value: "nuevoTurno",
        },
        {
          text: "Respuesta",
          value: "respuesta",
        },
        {
          text: "Motivo",
          value: "motivo",
        },
        {
          text: "Fecha Respuesta",
          value: "fechaRespuesta",
        },
        {
          text: "Acciones",
          value: "url",
        },
      ];
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
              "/solicitud/?search=" +
              this.estadoTab +
              "+" +
              this.urlCas.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              // console.log("Resultado", res.data);
              this.desserts = res.data;
              if (this.estadoTab == "ATENDIDO") {
                axios
                  .get(
                    RUTA_API +
                    "/solicitud/?search=OBSERVADO+" +
                    this.urlCas.split("/")[4],
                    {
                      headers: { Authorization: this.auth },
                    }
                  )
                  .then((res) => {
                    for (let i = 0; i < res.data.length; i++) {
                      this.desserts.push(res.data[i]);
                    }
                    console.log("Resultado de observados: ", res.status);
                  })
                  .catch((res) => {
                    console.log("SSSSS", res.data);
                  });
              }
            })
            .catch((res) => {
              console.log("SSSSS", res.data);
            });
        });
    },

    listarSolicitudes() {
      // this.tab = "ddd"

      // this.desserts = []

      if (this.editedItem.documento2 === "") {
        console.log("Vacio");
        //
        this.tab = 0
        //
      } else {
        // this.tab = 4

        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .get(
                RUTA_API + "/solicitud/?search=" + this.editedItem.documento2 + "+" + this.urlCas.split("/")[4],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("Resultado", res.status);
                //
                this.desserts = []
                this.cabezeraSolicitud();
                //
                this.nombrePaciente =
                  res.data[0].datosPaciente.ape_pat +
                  " " +
                  res.data[0].datosPaciente.ape_mat +
                  " " +
                  res.data[0].datosPaciente.nombres;
                this.desserts = res.data;
             
              })
              .catch((res) => {
                this.desserts = []
                // this.tab = 4
                this.nombrePaciente = "Paciente no encontrado"

                console.log("error::::", res.data);
              });
          })
          .catch((response) => {
            console.log(response.data);
          });
      }
    },
    cabezeraSolicitud() {
      this.headers = [
        {
          text: "Tipo Solicitud",
          value: "tipoSolicitud",
        },
        {
          text: "Fecha Solicitud",
          value: "fechaSolicitud",
        },
        {
          text: "Nuevo Turno",
          value: "nuevoTurno",
        },
        {
          text: "Respuesta",
          value: "respuesta",
        },
        {
          text: "Fecha Respuesta",
          value: "fechaRespuesta",
        },
        {
          text: "Usuario Registro",
          value: "userReg",
        },
        {
          text: "Acciones",
          value: "url",
        },
      ];
    },
    close() {
      this.dialog = false;
      this.editedItem.paciente = "";
      this.editedItem.tipoSolicitud = "";
      this.editedItem.turno = "";
      this.editedItem.correo = "";
    },
    save() {
      console.log("holaaaaa", this.editedItem.correo);
      console.log("holaaaaa", this.expression.test(this.editedItem.correo));

      if (
        !this.editedItem.paciente ||
        !this.editedItem.tipoSolicitud ||
        !this.editedItem.turno ||
        !this.editedItem.correo ||
        this.expression.test(this.editedItem.correo) == false
      ) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        console.log("ok");
        this.dialogDataApi = true;
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_API + "/solicitud/",
                {
                  tipoSolicitud: this.editedItem.tipoSolicitud,
                  fechaSolicitud: new Date(Date.now())
                    .toISOString()
                    .substr(0, 10),
                  nuevoTurno: this.editedItem.turno,
                  userReg: this.usuario + "|" + this.nombre,
                  cas: this.urlCas,
                  paciente: this.editedItem.paciente,
                  respuesta: "PENDIENTE",
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.data);
                this.guardarCorreo();
                this.enviarAlCorreo(
                  res.data.datosPaciente.ape_pat,
                  res.data.datosPaciente.ape_mat,
                  res.data.datosPaciente.nombres
                );
                this.mensaje = "Solicitud agregada con exito."
                this.dialogConfirmacion = true
                this.close();
                //console.log(this.editedItem);
                this.dialogDataApi = false;
                this.desserts = []
                this.estadoTab = "PENDIENTE"
                this.solicitudes()
                // this.dialogCorreo = true;
              })
              .catch((res) => {
                console.log("Error1:", res);
                this.dialogDataApi = false;
                this.mensaje = "Error! Solicitud no ha podido ser agregada."
                this.dialogConfirmacion = true
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
    },
    eliminarSolicitud() {
      let data = {
        respuesta: "ELIMINADO POR IPRESS",
        fechaEdit: new Date(
          Date.now() - new Date().getTimezoneOffset() * 60000
        )
          .toISOString()
          .substr(0, 10),
          userEdit: this.usuario + "|" + this.nombre,
        // motivo: this.motivo
      };
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(RUTA_API + "/solicitud/" + this.idItem + "/", data, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("Resultado: ", res.data);
              this.dialogoEliminacion = false;
              this.mensaje = "Solicitud eliminada con exito."
              this.dialogConfirmacion = true
              // this.editedItem.documento2 = ""
              this.tab = 0
              this.desserts = []
              this.estadoTab = "PENDIENTE"
              this.solicitudes()
              this.nombrePaciente = ""
              this.editedItem.documento2 = ""

            })
            .catch((res) => {
              console.log("Error: ", res.data);
              this.mensaje = "Error! Solicitud no ha sido eliminada."
              this.dialogConfirmacion = true
            });
        });
    },
    edit() { },
    deleteItemConfirm() { },
    closeEdit() { },
    closeDelete() { },
  },
  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
  },
  created() {
    this.solicitudes();
    this.perfil = sessionStorage.getItem("perfil");
    this.nombre = sessionStorage.getItem("nombre");
    this.url = sessionStorage.getItem("url");
    this.usuario = sessionStorage.getItem("usuario");
    this.urlCas = sessionStorage.getItem("urlCas");
    console.log("Url", this.url);
    console.log("Perfil", this.perfil);
    console.log("Nombre", this.nombre);
    console.log("cas", this.urlCas);
    //INICIO DE CONSULTA
    this.comboTipoSolicitud();
    this.comboTurnos();
    this.listarPacientes();
  },
  components: {},
};
</script>


