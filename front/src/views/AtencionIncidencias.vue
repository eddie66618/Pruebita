<template>
  <div>
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
      v-model="dialogAvisoAsignacion"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¿Estas Seguro de Asignarte este Ticket/Incidencia?
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="editItemAsignacion">Aceptar</v-btn>
          <v-btn text @click="dialogAvisoAsignacion = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAvisoErrorAsignacion"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡No puedes atender este Incidente, se encunetra asigando a otra
            persona!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAvisoErrorAsignacion = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-card class="mx-auto my-5" max-width="1200">
        <v-system-bar color="#1973a5" dark>
          INCIDENCIAS - DIVISION DE SOPORTE INFORMATICO
        </v-system-bar>
        <v-row class="start ml-10">
          <v-col cols="12" md="4">
            <v-text-field
              class="mx-auto mt-8"
              label="Número de Documento"
              required
              :maxlength="10"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
      <v-card class="mx-auto my-5" max-width="1200">
        <v-toolbar>
          <v-tabs dark background-color="#1973a5" grow>
            <v-tab
              @click="incidenciasPendientes"
              v-if="contenidoPendiente == 0"
            >
              <v-badge color="pink" content="0"> Proceso </v-badge>
            </v-tab>
            <v-tab
              @click="incidenciasPendientes"
              v-if="contenidoPendiente != 0"
            >
              <v-badge color="pink" :content="contenidoPendiente">
                Pendientes
              </v-badge>
            </v-tab>
            <v-tab @click="incidenciasProceso" v-if="contenidoProceso == 0">
              <v-badge color="orange" content="0"> Proceso </v-badge>
            </v-tab>
            <v-tab @click="incidenciasProceso" v-if="contenidoProceso != 0">
              <v-badge color="orange" :content="contenidoProceso">
                Proceso
              </v-badge>
            </v-tab>
            <v-tab @click="incidenciasTerminado" v-if="contenidoTerminado == 0">
              <v-badge color="green" content="0"> Proceso </v-badge>
            </v-tab>
            <v-tab @click="incidenciasTerminado" v-if="contenidoTerminado != 0">
              <v-badge color="green" :content="contenidoTerminado">
                Terminado
              </v-badge>
            </v-tab>
          </v-tabs>
        </v-toolbar>
      </v-card>

      <v-card v-if="adminForm == '0'" class="mx-auto my-5" max-width="1200">
        <v-data-table
          :headers="headers"
          :items="desserts"
          sort-by="calories"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>LISTA DE INCIDENCIAS PENDIENTES</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="800px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="#1973a5"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    Agregar Incidencia
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">AGREGAR INCIDENCIA</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-autocomplete
                            v-model="value"
                            :rules="[rules.required]"
                            :items="itemsPersonal"
                            dense
                            filled
                            solo
                          ></v-autocomplete>
                          <v-textarea
                            v-model="editedItem.detalleProblema"
                            outlined
                            :rules="[rules.required]"
                            name="input-7-4"
                            label="Detalle de problema"
                            :maxlength="980"
                          ></v-textarea>
                          <v-combobox
                            v-model="editedItem.personaAsig"
                            :items="itemsPersonalDsi"
                            label="Personal Asignado"
                            outlined
                            dense
                            :maxlength="70"
                            :rules="[rules.required]"
                          ></v-combobox>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="dialog = false">
                      Cancelar
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="save">
                      Agregar
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete"
                      >Cancel</v-btn
                    >
                    <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-account-plus-outline
            </v-icon>
          </template>
        </v-data-table>
      </v-card>

      <!--Proceso-->

      <v-card v-if="adminForm == '1'" class="mx-auto my-5" max-width="1200">
        <v-data-table
          :headers="headersProceso"
          :items="dessertsProceso"
          sort-by="calories"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>LISTA DE INCIDENCIAS EN PROCESO</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialogProceso" max-width="700px">
                <template v-slot:activator="{}">
                  <v-btn> </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-combobox
                            v-model="editedItem.clasiSolucion"
                            :items="items"
                            label="Clasificación de la Solución"
                            multiple
                            outlined
                            dense
                            :maxlength="980"
                            :rules="[rules.required]"
                          ></v-combobox>
                          <v-textarea
                            v-model="editedItem.detalleSolucion"
                            outlined
                            name="input-7-4"
                            label="Detalle de Solución"
                            :rules="[rules.required]"
                          ></v-textarea>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">
                      Cancelar
                    </v-btn>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="editAccionProceso"
                    >
                      Guardar
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete"
                      >Cancel</v-btn
                    >
                    <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItemProceso(item)">
              mdi-send-lock-outline
            </v-icon>
          </template>
        </v-data-table>
      </v-card>

      <!--Terminado-->

      <v-card v-if="adminForm == '2'" class="mx-auto my-5" max-width="1200">
        <v-data-table
          :headers="headersTerminado"
          :items="dessertsTerminado"
          sort-by="calories"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>LISTA DE INCIDENCIAS TERMINADAS</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialogProceso" max-width="700px">
                <template v-slot:activator="{}">
                  <v-btn> </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="12" md="12">
                          <v-combobox
                            v-model="editedItem.clasiSolucion"
                            :items="items"
                            label="Clasificación de la Solución"
                            multiple
                            outlined
                            dense
                            :maxlength="980"
                            :rules="[rules.required]"
                          ></v-combobox>
                          <v-textarea
                            v-model="editedItem.detalleSolucion"
                            outlined
                            name="input-7-4"
                            label="Detalle de Solución"
                            :rules="[rules.required]"
                          ></v-textarea>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">
                      Cancelar
                    </v-btn>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="editAccionProceso"
                    >
                      Guardar
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete"
                      >Cancel</v-btn
                    >
                    <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItemProceso(item)">
              mdi-send-lock-outline
            </v-icon>
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
export const RUTA_SERVIDOR = process.env.VUE_APP_RUTA_API;
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;

export default {
  data: () => ({
    //cambo items
    items: ["HARDWARE","SOFTWARE","ESSI","OTROS"],
    itemsPersonal: [],
    itemsPersonalDsi: [
      "46184379-ARIAS CANCHIHUAMAN KEVIN JOEL",
      "07622610-CARRASCO FERNANDEZ JULIO ENRIQUE",
      "25739053-OCHOA BERROA MARCELA VERONICA",
      "10669299-OCAMPO AGUILAR EUGENIA VIOLETA",
      "07973782-JUNCO	PAREDES	CARMEN MARIA",
    ],
    value: null,
    //Administracion de resultados
    adminForm: "",
    //data de sesion
    perfil: "",
    nombre: "",
    usuario: "",
    //variables para edicion
    urlAsignacion: "",
    incidenciasTotal: [],
    usuarioNombre: "",
    //DATA DATA TABLE
    dialog: false,
    dialogDelete: false,
    dialogProceso: false,
    dialogAvisoErrorAsignacion: false,
    //validaciones
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    headers: [
      {
        text: "Número Ticket",
        align: "start",
        sortable: false,
        value: "numTicket",
      },
      { text: "Personal", value: "personalSoli" },
      { text: "Dependencia", value: "datosPersonal.datosDependencia.descDep" },
      { text: "Problema", value: "problema" },
      { text: "Fecha Solicitud", value: "fechaSolicutud" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    //Proceso
    headersProceso: [
      {
        text: "Número Ticket",
        align: "start",
        sortable: false,
        value: "numTicket",
      },
      { text: "Personal", value: "personalSoli" },
      { text: "Dependencia", value: "datosPersonal.datosDependencia.descDep" },
      { text: "Problema", value: "problema" },
      { text: "Fecha Solicitud", value: "fechaSolicutud" },
      { text: "Personal Asignado", value: "userReg" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    //Terminado
    headersTerminado: [
      {
        text: "Número Ticket",
        align: "start",
        sortable: false,
        value: "numTicket",
      },
      { text: "Personal", value: "personalSoli" },
      { text: "Dependencia", value: "datosPersonal.datosDependencia.descDep" },
      { text: "Problema", value: "problema" },
      { text: "Solución", value: "solucion" },
      { text: "Fecha Solicitud", value: "fechaSolicutud" },
      { text: "Personal Asignado", value: "userReg" },
      //{ text: "Actions", value: "actions", sortable: false },
    ],
    desserts: [],
    dessertsProceso: [],
    dessertsTerminado: [],
    editedIndex: -1,
    editedItem: {
      clasiSolucion: "",
      detalleSolucion: "",
      detalleProblema: "",
      personaAsig: "",
    },
    defaultItem: {
      clasiSolucion: "",
      detalleSolucion: "",
      detalleProblema: "",
      personaAsig: "",
    },
    //VARIOS
    value: 2,
    contenidoPendiente: "",
    contenidoProceso: "",
    contenidoTerminado: "",
    //dialogos
    dialogDataApi: false,
    dialogAvisoAsignacion: false,
  }),
  methods: {
    //Consulta de incidencias pendientes
    listarPersonal() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/personal/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("data listada", res.data);
              for (let i = 0; i < res.data.length; i++) {
                this.itemsPersonal.push(
                  res.data[i].apePatPer +
                    " " +
                    res.data[i].apeMatPer +
                    " " +
                    res.data[i].nomPer +
                    "-" +
                    res.data[i].dniPer +
                    "-" +
                    res.data[i].url.split("/")[4]
                );
              }
              console.log("data listada", this.itemsPersonal);
            })
            .catch((res) => {
              console.log("Error:", res);
            });
        })
        .catch((response) => {
          console.log("Error:", response);
        });
    },

    incidenciasPendientes() {
      this.adminForm = "0";
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/incidenciaDsi/?search=PENDIENTE", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.desserts = [];
              for (let i = 0; i < res.data.length; i++) {
                this.desserts.push(
                  Object.assign(
                    {
                      personalSoli:
                        res.data[i].datosPersonal.apePatPer +
                        " " +
                        res.data[i].datosPersonal.apeMatPer +
                        " " +
                        res.data[i].datosPersonal.nomPer,
                    },
                    {
                      fechaSolicutud: res.data[i].fecha_reg.split("T")[0],
                    },
                    res.data[i]
                  )
                );
              }
              //this.desserts = res.data;
              console.log("dataIncidencias", this.desserts);
              this.dialogDataApi = false;
            })
            .catch((res) => {
              console.log("error", res.data);
            });
        })
        .catch((response) => {
          console.log("error", response.data);
        });
    },
    incidenciasProceso() {
      this.adminForm = "1";
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/incidenciaDsi/?search=PROCESO", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.dessertsProceso = [];
              for (let i = 0; i < res.data.length; i++) {
                this.dessertsProceso.push(
                  Object.assign(
                    {
                      personalSoli:
                        res.data[i].datosPersonal.apePatPer +
                        " " +
                        res.data[i].datosPersonal.apeMatPer +
                        " " +
                        res.data[i].datosPersonal.nomPer,
                    },
                    {
                      fechaSolicutud: res.data[i].fecha_reg.split("T")[0],
                    },
                    res.data[i]
                  )
                );
              }
              //this.dessertsProceso = res.data;
              console.log("dataIncidencias", this.dessertsProceso);
              this.dialogDataApi = false;
            })
            .catch((res) => {
              console.log("error", res.data);
            });
        })
        .catch((response) => {
          console.log("error", response.data);
        });
    },
    incidenciasTerminado() {
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/incidenciaDsi/?search=TERMINADO", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.dessertsTerminado = [];
              for (let i = 0; i < res.data.length; i++) {
                this.dessertsTerminado.push(
                  Object.assign(
                    {
                      personalSoli:
                        res.data[i].datosPersonal.apePatPer +
                        " " +
                        res.data[i].datosPersonal.apeMatPer +
                        " " +
                        res.data[i].datosPersonal.nomPer,
                    },
                    {
                      fechaSolicutud: res.data[i].fecha_reg.split("T")[0],
                    },
                    res.data[i]
                  )
                );
              }
              //this.dessertsTerminado = res.data;
              this.adminForm = 2;
              console.log("dataIncidencias", this.dessertsTerminado);
              this.dialogDataApi = false;
            })
            .catch((res) => {
              console.log("error", res.data);
            });
        })
        .catch((response) => {
          console.log("error", response.data);
        });
    },
    //Consulta Cantidad de incidencias
    incidencias() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/incidenciaDsi/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.incidenciasTotal = res.data;
              const resDataPendiete = res.data.filter(
                (e) => e.datosEstado.descripMaestro === "PENDIENTE"
              ).length;
              this.contenidoPendiente = resDataPendiete;
              const resDataProceso = res.data.filter(
                (e) => e.datosEstado.descripMaestro === "PROCESO"
              ).length;
              this.contenidoProceso = resDataProceso;
              const resDataTerminado = res.data.filter(
                (e) => e.datosEstado.descripMaestro === "TERMINADO"
              ).length;
              this.contenidoTerminado = resDataTerminado;
              console.log("data", res.data);
            })
            .catch((res) => {
              console.log("error", res.data);
            });
        })
        .catch((response) => {
          console.log("error", response.data);
        });
    },
    //TABLE
    initialize() {
      this.desserts = [];
    },

    editItemAsignacion(item) {
      //this.dialogAvisoAsignacion = true;
      console.log("data item", item);
      console.log("usuario", this.usuario);
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
                "/incidenciaDsi/" +
                this.urlAsignacion.split("/")[4] +
                "/",
              {
                estado: RUTA_API.substring(0,29) + "/maestro/3/",
                userReg: this.usuario + "-" + this.nombre,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("exito", res.status);
              this.dialogAvisoAsignacion = false;
              this.incidenciasPendientes();
              this.incidencias();
              //this.dialogAvisoAsignacion = false;
            })
            .catch((res) => {
              console.log("Error:", res);
              //this.dialogEdit = false;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },

    editItem(item) {
      this.dialogAvisoAsignacion = true;
      console.log("url", item.url.split("/")[4]);
      this.urlAsignacion = item.url;
      console.log("this url", this.urlAsignacion);
      /*this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;*/
    },

    editItemProceso(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);

      console.log("data editemProceso", this.editedItem);
      this.urlAsignacion = item.url;
      this.usuarioNombre = item.userReg;
      if (item.userReg.split("-")[0] == this.usuario) {
        this.dialogProceso = true;
      } else {
        this.dialogAvisoErrorAsignacion = true;
      }
    },

    editAccionProceso() {
      console.log("click");
      if (!this.editedItem.clasiSolucion || !this.editedItem.detalleSolucion) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        console.log("clasificacion", this.editedItem.clasiSolucion);
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
                  "/incidenciaDsi/" +
                  this.urlAsignacion.split("/")[4] +
                  "/",
                {
                  estado: RUTA_API.substring(0,29) + "/maestro/4/",
                  clasiSolu: this.editedItem.clasiSolucion.toString(),
                  solucion: this.editedItem.detalleSolucion,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.dialogAvisoAsignacion = false;
                this.incidenciasProceso();
                this.incidencias();
                this.close();
                //this.dialogAvisoAsignacion = false;
              })
              .catch((res) => {
                console.warn("Error:", res);
                //this.dialogEdit = false;
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
    },

    deleteItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.desserts.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialogProceso = false;
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
      if (!this.value || !this.editedItem.detalleProblema) {
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
                RUTA_API + "/incidenciaDsi/",
                {
                  personal:
                    RUTA_API.substring(0,29) +
                    "/personal/" +
                    this.value.split("-")[2] +
                    "/",
                  problema: this.editedItem.detalleProblema,
                  userReg: this.editedItem.personaAsig,
                  numTicket:
                    "DSI" +
                    this.value.split("-")[1] +
                    "T" +
                    (this.incidenciasTotal.length + 1),
                  estado: RUTA_API.substring(0,29) + "/maestro/3/",
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.dialog = false;
                this.incidenciasPendientes();
                this.incidencias();
              })
              .catch((res) => {
                console.log("Error:", res);
              });
          })
          .catch((response) => {
            console.log("Error 2:", response);
          });
      }
    },
  },

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Solción del Problema" : "Edit Item";
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
    console.log("Url", this.url);
    console.log("Perfil", this.perfil);
    console.log("Nombre", this.nombre);
    //Consulta Cantidad de incidencias
    this.incidencias();
    this.initialize();
    this.incidenciasPendientes();
    this.listarPersonal();
    this.editedItem.personaAsig =
      sessionStorage.getItem("usuario") +
      "-" +
      sessionStorage.getItem("nombre");
    this.defaultItem.personaAsig =
      sessionStorage.getItem("usuario") +
      "-" +
      sessionStorage.getItem("nombre");
  },
};
</script>