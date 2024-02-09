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
      persistent
      v-model="dialogAsigPaciente"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>Asignar Puesto</v-toolbar>
        <v-container class="mt-5">
          <v-row>
            <v-col cols="12" sm="12" md="12">
              <v-autocomplete
                v-model="editedItem.urlPaciente"
                :rules="[rules.required]"
                :items="itemsDatosPaciente"
                item-text="nombreCompleto"
                item-value="url"
                dense
                label="PACIENTE"
              ></v-autocomplete>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions class="justify-end">
          <v-btn text @click="asignarCupoPaciente">Aceptar</v-btn>
          <v-btn text @click="dialogAsigPaciente = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDetalleCupos" hide-overlay persistent width="1000">
      <v-toolbar color="#1973a5" dark
        ><v-row
          ><v-col cols="12" sm="9" md="9"
            >Cupos Libres de la Clinica {{ nombreClinicaDetalle }}</v-col
          >
          <v-col cols="12" sm="3" md="3"
            ><v-btn
              color="#1973a5"
              dark
              class="justify-content-end"
              @click="dialogDetalleCupos = false"
            >
              CERRAR
            </v-btn></v-col
          ></v-row
        ></v-toolbar
      >
      <v-card class="mx-auto" max-width="1000">
        <v-data-table
          :items-per-page="5"
          :headers="headers"
          :items="desserts"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <!--Registrar-->
              <v-dialog v-model="dialog" max-width="600px">
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.turno"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsTurno"
                              dense
                              label="TURNO"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.frecuencia"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsFrecuencia"
                              dense
                              label="FRECUENCIA"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.capacidad"
                              :rules="[rules.required, rules.counter]"
                              label="CAPACIDAD"
                              :maxlength="8"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="close">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="save">
                        Guardar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <!--editar-->
              <v-dialog v-model="dialogEdit" max-width="600px">
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-title>
                      <span class="text-h5">Editar el estado de turno</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <span class="text-h5"
                              >¿Esta seguro de desactivar este turno?</span
                            >
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="red darken-1"
                        text
                        @click="dialogEdit = false"
                      >
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="edit">
                        Aceptar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Esta seguro de eliminar registro?</v-card-title
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
            <v-icon small class="mr-2" @click="itemAsigCuposPac(item)">
              mdi-account
            </v-icon>
            <!--<v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>-->
          </template>
        </v-data-table>
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
      v-model="dialogParametrizado"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            No se puede asignar pacientes a esta clinica, revise la
            parametrización
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogParametrizado = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogNoAsignacion"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            No es posible otorgar Cupo - ¡Paciene con Cupo Vigente!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogNoAsignacion = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-card class="mx-auto my-5" max-width="1000">
        <v-system-bar color="#1973a5" dark>
          ASIGNACIÓN DE CUPOS - IPRESS CONTRATADAS
        </v-system-bar>
        <v-row class="mt-2 ml-15">
          <!--<v-col cols="12" sm="6" md="6">
            <v-autocomplete
              v-model="editedItem.urlDistrito"
              :rules="[rules.required]"
              :items="itemsClinicas"
              item-text="distrito"
              item-value="url"
              dense
              label="Por Distrito"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn
              class="mt-2"
              icon
              color="#1973a5"
              @click="buscarClinicaDistrito"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>-->
          <v-col cols="12" sm="6" md="6">
            <v-autocomplete
              v-model="editedItem.urlClinica"
              :rules="[rules.required]"
              :items="itemsClinicas"
              item-text="descripCas"
              item-value="url"
              dense
              label="Por Clinica"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn
              class="mt-2 mb-5"
              icon
              color="#1973a5"
              @click="buscarClinica"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card>

      <v-card class="mx-auto my-5" max-width="1000">
        <v-data-table
          :headers="headersClinica"
          :items="dessertsClinica"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <!--Registrar-->
              <v-dialog v-model="dialog" max-width="600px">
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.turno"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsTurno"
                              dense
                              label="TURNO"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.frecuencia"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsFrecuencia"
                              dense
                              label="FRECUENCIA"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.capacidad"
                              :rules="[rules.required, rules.counter]"
                              label="CAPACIDAD"
                              :maxlength="8"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="close">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="save">
                        Guardar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <!--editar-->
              <v-dialog v-model="dialogGuaradoCorrecto" max-width="600px">
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-title>
                      <span class="text-h5">!MENSAJE IMPORTANTE¡</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <span class="text-h5"
                              >SE GRABO CORRECTAMENTE EL CUPO</span
                            >
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="dialogGuaradoCorrecto = false"
                      >
                        Aceptar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Esta seguro de eliminar registro?</v-card-title
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
            <v-icon small class="mr-2" @click="buscarCuposClinica(item)">
              mdi-account
            </v-icon>
            <!--<v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>-->
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
    //cupos
    itemsTurno: ["TURNO 1", "TURNO 2", "TURNO 3", "TURNO 4"],
    itemsFrecuencia: ["LUN-MIE-VIE", "MAR-JUE-SAB"],
    itemsEstado: ["true", "false"],
    itemsClinicas: [],
    itemsClinicasDistritos: [],
    itemsDistrito: [],
    itemsDatosPaciente: [],
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
      capacidad: Number,
      urlClinica: "",
      urlPaciente: "",
      urlPuesto: "",
      urlDistrito: "",
    },
    dialogParametrizado: false,
    dialog: false,
    dialogEdit: false,
    formAdmi: false,
    dialogDelete: false,
    dialogEditAdm: false,
    dialogNoEdit: false,
    dialogDataApi: false,
    dialogDetalleCupos: false,
    dialogAsigPaciente: false,
    dialogGuaradoCorrecto: false,
    dialogNoAsignacion: false,
    vista: "",
    valid: true,
    datosEdit: "",
    actionBoton: "AGREGAR",
    headers: [],
    headersCuposLibres: [],
    headersClinica: [],
    desserts: [],
    dessertsCuposLibres: [],
    dessertsClinica: [],
    editedIndex: -1,
    dataex: "",
    nombreClinicaDetalle: "",
    defaultItem: {
      turno: "",
      frecuencia: "",
      capacidad: Number,
      urlClinica: "",
      urlPaciente: "",
      urlPuesto: "",
      urlDistrito: "",
    },
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
      this.dialogEdit = true;
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
              this.ParameCentroInit();
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
                console.log("editedItem", this.editedItem.turno);

                axios
                  .post(RUTA_API + "/api/token/", {
                    username: USUARIO,
                    password: PASSWORD,
                  })
                  .then((response) => {
                    this.auth = "Bearer " + response.data.access;
                    for (let i = 0; i < this.editedItem.capacidad; i++) {
                      axios
                        .post(
                          RUTA_API + "/parameCentroPuesto/",
                          {
                            cas: this.urlCas,
                            turno: this.editedItem.turno,
                            frecuencia: this.editedItem.frecuencia,
                            tipoPuesto: "NORMAL",
                            numeroPuesto: i + 1,
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
                        })
                        .catch((res) => {
                          console.log("Error:", res);
                          this.dialog = false;
                        });
                    }
                  })
                  .catch((response) => {
                    response === 404
                      ? console.warn("lo sientimos no tenemos servicios")
                      : console.warn("Error:", response);
                  });

                this.ParameCentroInit();
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
        { text: "Tipo Puesto", value: "tipoPuesto" },
        { text: "Número Puesto", value: "numeroPuesto" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    cabezeraCuposClinica() {
      this.headersClinica = [
        { text: "Clinica", value: "clinica" },
        {
          text: "Cupos Totales",
          align: "start",
          sortable: false,
          value: "cuposTotales",
        },
        { text: "Cupos Ocupados", value: "cuposAsignados" },
        { text: "Cupos Disponibles", value: "cuposNoAsignados" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    clinicasInit() {
      //this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/cas/?search=2,true", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.itemsClinicas = res.data;
              this.dialogDataApi = false;
              //this.itemsClinicasDistritos =
              console.log("itemsClinicas", this.itemsClinicas);
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

    buscarClinica() {
      this.liberarCupo();
      console.log("prueba", this.editedItem.urlClinica);
      this.dessertsClinica = [];
      this.dialogDataApi = true;
      this.cabezeraCuposClinica();
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
                "/parameCentroPuesto/?search=" +
                this.editedItem.urlClinica.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              axios
                .get(
                  RUTA_API +
                    "/asigCuposPac/?search=" +
                    this.editedItem.urlClinica.split("/")[4] +
                    ",true",
                  {
                    headers: { Authorization: this.auth },
                  }
                )
                .then((resCuposAsig) => {
                  if (resCuposAsig.data.length != 0) {
                    console.log("resCuposAsig", resCuposAsig.data);
                    const resultNoAsig = res.data.filter(
                      (e) =>
                        !resCuposAsig.data.some((i) =>
                          i.parameCentroPuesto.includes(e.url)
                        )
                    );
                    this.dessertsClinica.push(
                      Object.assign(
                        {
                          clinica:
                            resCuposAsig.data[0].datosPueto.datosCas.descripCas,
                        },
                        { urlClinica: resCuposAsig.data[0].datosPueto.cas },
                        { cuposTotales: res.data.length },
                        { cuposAsignados: resCuposAsig.data.length },
                        { cuposNoAsignados: resultNoAsig.length }
                      )
                    );
                    this.nombreClinicaDetalle =
                      resCuposAsig.data[0].datosPueto.datosCas.descripCas;
                    console.log("data total cupos", res.data);
                    console.log("data asignados", resCuposAsig.data);
                    console.log("resultNoAsig", this.dessertsClinica);
                    this.dialogDataApi = false;
                    //this.dialogDetalleCupos = true;
                  } else {
                    console.log(
                      "esta clinica no tiene nungun paciente asignado"
                    );
                    console.log("resCuposAsig", resCuposAsig.data);
                    this.dessertsClinica.push(
                      Object.assign(
                        {
                          clinica: this.editedItem.urlClinica,
                        },
                        { cuposTotales: res.data.length },
                        { cuposAsignados: 0 },
                        { cuposNoAsignados: 0 }
                      )
                    );
                    this.dialogDataApi = false;
                  }
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
    buscarClinicaDistrito() {
      console.log("prueba", this.editedItem.distrito);
    },

    buscarPaciente() {
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/paciente/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              for (let i = 0; i < res.data.length; i++) {
                this.itemsDatosPaciente.push(
                  Object.assign(
                    {
                      nombreCompleto:
                        res.data[i].ape_pat +
                        " " +
                        res.data[i].ape_mat +
                        " " +
                        res.data[i].nombres,
                    },
                    { url: res.data[i].url + "|" + res.data[i].num_doc }
                  )
                );
              }
              console.log("datosPaciente", this.itemsDatosPaciente);
              this.dialogDataApi = false;
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

    buscarCuposClinica(item) {
      console.log("detalleCipos", item);
      this.dialogDataApi = true;
      if (item.cuposTotales == 0) {
        console.log("no tiene parametrizacion");
        this.dialogParametrizado = true;
        this.dialogDataApi = false;
      } else {
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
                  "/parameCentroPuesto/?search=" +
                  item.urlClinica.split("/")[4],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                axios
                  .get(
                    RUTA_API +
                      "/asigCuposPac/?search=" +
                      item.urlClinica.split("/")[4] +
                      ",true",
                    {
                      headers: { Authorization: this.auth },
                    }
                  )
                  .then((resCuposAsig) => {
                    console.log("data buscar clinica", res.data);
                    console.log("data asignados", resCuposAsig.data);
                    const resultNoAsig = res.data.filter(
                      (e) =>
                        !resCuposAsig.data.some((i) =>
                          i.parameCentroPuesto.includes(e.url)
                        )
                    );
                    if (item.urlClinica.split("/")[4] == 1) {
                      this.headers.unshift({ text: "Sala", value: "sala" });
                      this.desserts = [];
                      for (let i = 0; i < resultNoAsig.length; i++) {
                        if (
                          (resultNoAsig[i].numeroPuesto > 0) &
                          (resultNoAsig[i].numeroPuesto <= 10)
                        ) {
                          const sala = "Sala1";
                          this.desserts.push(
                            Object.assign({
                              cas: resultNoAsig[i].cas,
                              datosCas: resultNoAsig[i].datosCas,
                              estado: resultNoAsig[i].estado,
                              fecha_reg: resultNoAsig[i].fecha_reg,
                              frecuencia: resultNoAsig[i].frecuencia,
                              numeroPuesto: resultNoAsig[i].numeroPuesto,
                              tipoPuesto: resultNoAsig[i].tipoPuesto,
                              turno: resultNoAsig[i].turno,
                              url: resultNoAsig[i].url,
                              usuario_reg: resultNoAsig[i].usuario_reg,
                              sala: sala,
                            })
                          );
                        }
                        if (
                          (resultNoAsig[i].numeroPuesto > 10) &
                          (resultNoAsig[i].numeroPuesto <= 20)
                        ) {
                          const sala = "Sala2";
                          this.desserts.push(
                            Object.assign({
                              cas: resultNoAsig[i].cas,
                              datosCas: resultNoAsig[i].datosCas,
                              estado: resultNoAsig[i].estado,
                              fecha_reg: resultNoAsig[i].fecha_reg,
                              frecuencia: resultNoAsig[i].frecuencia,
                              numeroPuesto: resultNoAsig[i].numeroPuesto,
                              tipoPuesto: resultNoAsig[i].tipoPuesto,
                              turno: resultNoAsig[i].turno,
                              url: resultNoAsig[i].url,
                              usuario_reg: resultNoAsig[i].usuario_reg,
                              sala: sala,
                            })
                          );
                        }
                        if (
                          (resultNoAsig[i].numeroPuesto > 20) &
                          (resultNoAsig[i].numeroPuesto <= 30)
                        ) {
                          const sala = "Sala3";
                          this.desserts.push(
                            Object.assign({
                              cas: resultNoAsig[i].cas,
                              datosCas: resultNoAsig[i].datosCas,
                              estado: resultNoAsig[i].estado,
                              fecha_reg: resultNoAsig[i].fecha_reg,
                              frecuencia: resultNoAsig[i].frecuencia,
                              numeroPuesto: resultNoAsig[i].numeroPuesto,
                              tipoPuesto: resultNoAsig[i].tipoPuesto,
                              turno: resultNoAsig[i].turno,
                              url: resultNoAsig[i].url,
                              usuario_reg: resultNoAsig[i].usuario_reg,
                              sala: sala,
                            })
                          );
                        }
                        if (
                          (resultNoAsig[i].numeroPuesto > 30) &
                          (resultNoAsig[i].numeroPuesto <= 40)
                        ) {
                          const sala = "Sala4";
                          this.desserts.push(
                            Object.assign({
                              cas: resultNoAsig[i].cas,
                              datosCas: resultNoAsig[i].datosCas,
                              estado: resultNoAsig[i].estado,
                              fecha_reg: resultNoAsig[i].fecha_reg,
                              frecuencia: resultNoAsig[i].frecuencia,
                              numeroPuesto: resultNoAsig[i].numeroPuesto,
                              tipoPuesto: resultNoAsig[i].tipoPuesto,
                              turno: resultNoAsig[i].turno,
                              url: resultNoAsig[i].url,
                              usuario_reg: resultNoAsig[i].usuario_reg,
                              sala: sala,
                            })
                          );
                        }
                        console.log(
                          "resCuposAsig[i].numeroPuesto",
                          resultNoAsig[i].numeroPuesto
                        );
                      }
                      console.log("heders", this.headers);

                      //this.desserts = resultNoAsig;
                      console.log("resultNoAsig", this.desserts);
                      this.dialogDataApi = false;
                      this.dialogDetalleCupos = true;
                    } else {
                      console.log("heders", this.headers);
                      this.desserts = resultNoAsig;
                      console.log("resultNoAsig", this.desserts);
                      this.dialogDataApi = false;
                      this.dialogDetalleCupos = true;
                    }
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
      }
    },

    itemAsigCuposPac(item) {
      this.dialogAsigPaciente = true;
      console.log("item de asig cupos", item);
      this.editedItem.urlPuesto = item.url;
      this.editedItem.urlPaciente = [];
    },

    asignarCupoPaciente() {
      console.log("ya casi", this.editedItem.urlPuesto);
      console.log("ya casi 2", this.editedItem.urlPaciente);
      console.log("ya casi 2", this.itemsDatosPaciente);

      console.log("click");
      this.dialogDataApi = true;
      if (!this.editedItem.urlPaciente) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        //datos
        axios
          .get(
            RUTA_API +
              "/asigCuposPac/?search=" +
              this.editedItem.urlPaciente.split("|")[1] +
              ",true",
            {
              headers: { Authorization: this.auth },
            }
          )
          .then((res) => {
            console.log("datooo", res.data.length);
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
                      RUTA_API + "/asigCuposPac/",
                      {
                        paciente: this.editedItem.urlPaciente.split("|")[0],
                        parameCentroPuesto: this.editedItem.urlPuesto,
                        usuario_reg: this.usuario + "|" + this.nombre,
                        estado: true,
                        fechaAsigCupo: new Date(
                          Date.now() - new Date().getTimezoneOffset() * 60000
                        )
                          .toISOString()
                          .substr(0, 10),
                      },
                      {
                        headers: { Authorization: this.auth },
                      }
                    )
                    .then((res) => {
                      console.log("exito", res.status);
                      this.dialogDataApi = false;
                      this.editedItem.urlPaciente = [];
                      this.dialogAsigPaciente = false;
                      this.dialogDetalleCupos = false;
                      this.buscarClinica();
                      this.dialogGuaradoCorrecto = true;
                    })
                    .catch((res) => {
                      console.log("exito", res.status);
                      console.log("Error:", res);
                      this.dialogNoAsignacion = true;
                      this.dialogDataApi = false;
                      this.dialogAsigPaciente = false;
                      this.dialogDetalleCupos = false;
                      this.dialog = false;
                      this.buscarClinica();
                    });
                })
                .catch((response) => {
                  console.log("exito", response.status);
                });
            } else {
              console.log("Error:", res);
              this.dialogNoAsignacion = true;
              this.dialogDataApi = false;
              this.dialogAsigPaciente = false;
              this.dialogDetalleCupos = false;
              this.dialog = false;
              this.buscarClinica();
            }
          })
          .catch((res) => {
            console.warn("Error:", res);
            this.dialog = false;
          });
      }
    },

    liberarCupo() {
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
                "/asisPacDiario/?search=FALTO," +
                this.editedItem.urlClinica.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("asistenciaPacDiario", res.data);
              for (let i = 0; i < res.data.length; i++) {
                let quinceDias = 1000 * 60 * 60 * 24 * 15;

                if (
                  new Date(
                    Date.now() -
                      quinceDias -
                      new Date().getTimezoneOffset() * 60000
                  )
                    .toISOString()
                    .substr(0, 10) >
                    res.data[i].fecha_reg ==
                  true
                ) {
                  console.log(
                    "liberarCupos",
                    new Date(
                      Date.now() -
                        quinceDias -
                        new Date().getTimezoneOffset() * 60000
                    )
                      .toISOString()
                      .substr(0, 10) > res.data[i].fecha_reg
                  );
                }
              }
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
    console.log("cas", this.urlCas);
    //INICIO DE CONSULTA

    this.clinicasInit();
    this.buscarPaciente();
  },

  components: {},
};
</script>


