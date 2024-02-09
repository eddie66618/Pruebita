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
      v-model="dialogAsistenciaDoble"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            !No se puede registrar, el paciente ya tiene asistencia!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAsistenciaDoble = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-card class="mx-auto my-5" max-width="1100">
        <v-system-bar color="#1973a5" dark> Asistencia Adicional </v-system-bar>
      </v-card>
      <v-card class="mx-auto my-5" max-width="1100">
        <v-data-table :headers="headers" :items="desserts" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <!--Registrar-->
              <v-dialog v-model="dialog" max-width="600px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="#1973a5"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ actionBoton }}
                  </v-btn>
                </template>
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-title>
                      <span class="text-h5">Agregar Asistencia</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.paciente"
                              :rules="[rules.required]"
                              :items="itemsDatosPaciente"
                              item-text="nombreCompleto"
                              item-value="paciente"
                              dense
                              label="PACIENTE"
                            ></v-autocomplete>
                          </v-col>
                          <v-col v-if="urlCas.split('/')[4]==1" cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.sala"
                              :rules="[rules.required]"
                              :items="itemsSala"
                              dense
                              label="SALA"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.frecuencia"
                              :rules="[rules.required]"
                              :items="itemsFrecuencia"
                              dense
                              label="FRECUENCIA"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.turno"
                              :rules="[rules.required]"
                              :items="itemsTurno"
                              dense
                              label="TURNO"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.motivo"
                              :rules="[rules.required]"
                              label="MOTIVO"
                              :maxlength="80"
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
                      <span class="text-h5">Editar Asistencia Adicional</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.paciente"
                              :rules="[rules.required, rules.counter]"
                              label="nombreCompleto"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="urlCas.split('/')[4]==1" cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.sala"
                              :rules="[rules.required]"
                              :items="itemsSala"
                              dense
                              label="SALA"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.frecuencia"
                              :rules="[rules.required]"
                              :items="itemsFrecuencia"
                              dense
                              label="FRECUENCIA"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.turno"
                              :rules="[rules.required]"
                              :items="itemsTurno"
                              dense
                              label="TURNO"
                            ></v-autocomplete>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.motivo"
                              :rules="[rules.required]"
                              label="MOTIVO"
                              :maxlength="80"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="red darken-1" text @click="closeEdit">
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
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <!--<v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>-->
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </div>
</template>

<script>
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
import axios from "axios";

export default {
  data: () => ({
    actionBoton: "AGREGAR HEMODIALISIS",
    itemsDatosPaciente: [],
    datosEdit: "",
    editedItem: {
      //Cupos
      paciente: "",
      frecuencia: "",
      turno: "",
      motivo: "",
      sala:"",
    },
    defaultItem: {
      paciente: "",
      frecuencia: "",
      turno: "",
      motivo: "",
      sala:"",
    },
    headers: [],
    desserts: [],
    dialogDataApi: false,
    dialog: false,
    dialogEdit: false,
    dialogDelete: false,
    dialogAsistenciaDoble: false,
    valid: true,
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    itemsTurno: ["TURNO 1", "TURNO 2", "TURNO 3", "TURNO 4"],
    itemsFrecuencia: ["LUN-MIE-VIE", "MAR-JUE-SAB"],
    itemsSala: ["SALA1","SALA2","SALA3","SALA4"]
  }),

  computed: {},

  watch: {},
  methods: {
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    cabezeraHemoAdicional() {
      this.headers = [
        {
          text: "Nombre",
          value: "datosPaciente.nombres",
        },
        {
          text: "Apellido Paterno",
          value: "datosPaciente.ape_pat",
        },
        {
          text: "Apellido materno",
          value: "datosPaciente.ape_mat",
        },
        {
          text: "Estado Asistencia",
          align: "start",
          sortable: false,
          value: "estadoAsistencia",
        },
        { text: "Sala", value: "sala" },
        { text: "Frecuencia", value: "frecuencia" },
        { text: "Turno", value: "turno" },
        { text: "Motivo", value: "motivo" },
        { text: "fecha Registro", value: "fecha_reg" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    listaHemoAdicional() {
      this.dialogDataApi = true;
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
                "/asisPacDiarioAdicional/?search=" +
                this.urlCas.split("/")[4] +
                "," +
                new Date().toISOString().substr(0, 10),
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.desserts = res.data;
              console.log("dessert", res.data);
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

    buscarPacienteAsig() {
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
              console.log("data", res.data);
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
    save() {
      console.log("click");
      if (
        !this.editedItem.paciente ||
        !this.editedItem.frecuencia ||
        !this.editedItem.turno ||
        !this.editedItem.motivo
      ) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
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
                RUTA_API + "/asisPacDiarioAdicional/",
                {
                  paciente: this.editedItem.paciente,
                  cas: this.urlCas,
                  sala: this.editedItem.sala,
                  turno: this.editedItem.turno,
                  frecuencia: this.editedItem.frecuencia,
                  estadoAsistencia: "ASISTIO",
                  usuario_reg: this.usuario + "|" + this.nombre,
                  validacionAsistencia:
                    new Date(
                      Date.now() - new Date().getTimezoneOffset() * 60000
                    )
                      .toISOString()
                      .substr(0, 10) +
                    "|" +
                    this.editedItem.paciente.split("/")[4],
                  motivo: this.editedItem.motivo,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                //console.log(this.editedItem);
                this.listaHemoAdicional();
                this.dialogDataApi = false;
              })
              .catch((res) => {
                console.log("Error1:", res);
                this.dialogDataApi = false;
                this.dialogAsistenciaDoble = true;
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
    },
    edit() {
      console.log("editar");
      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_API +
                "/asisPacDiarioAdicional/" +
                this.datosEdit.split("/")[4] +
                "/",
              {
                sala: this.editedItem.sala,
                turno: this.editedItem.turno,
                frecuencia: this.editedItem.frecuencia,
                estadoAsistencia: "ASISTIO",
                usuario_reg: this.usuario + "|" + this.nombre,
                motivo: this.editedItem.motivo,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("exito", res.status);
              this.dialogEdit = false;
              this.dialogDataApi = true;
              this.listaHemoAdicional();
            })
            .catch((res) => {
              console.warn("Error1:", res);
            });
        })
        .catch((response) => {
          console.log("Error2", response);
        });
    },
    editItem(item) {
      console.log("editutem", item);
      this.editedItem.paciente =
        item.datosPaciente.nombres +
        " " +
        item.datosPaciente.ape_pat +
        " " +
        item.datosPaciente.ape_mat;
      this.editedItem.frecuencia = item.frecuencia;
      this.editedItem.sala = item.sala;
      this.editedItem.turno = item.turno;
      this.editedItem.motivo = item.motivo;
      this.datosEdit = item.url;
      this.dialogEdit = true;
    },
    deleteItemConfirm() {},
    deleteItem(item) {
      console.log("deleteitem", item);
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
    this.buscarPacienteAsig();
    this.listaHemoAdicional();
    this.cabezeraHemoAdicional();
  },

  components: {},
};
</script>


