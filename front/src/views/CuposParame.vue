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
      v-model="dialogNoPrivilegios"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">¡No tiene permiso para agregar nuevas parametrizaciones!</div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogNoPrivilegios = false">cerrar</v-btn>
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

    <v-container>
      <v-card class="mx-auto my-5" max-width="1000">
        <v-system-bar color="#1973a5" dark>
          PARAMETRIZACION CENTRO DE DIALISIS
        </v-system-bar>
      </v-card>

      <v-card class="mx-auto my-5" max-width="1000">
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
    },
    dialog: false,
    dialogEdit: false,
    formAdmi: false,
    dialogDelete: false,
    dialogEditAdm: false,
    dialogNoEdit: false,
    dialogNoPrivilegios: false,
    vista: "",
    valid: true,
    datosEdit: "",
    actionBoton: "AGREGAR",
    headers: [],
    desserts: [],
    editedIndex: -1,
    dataex: "",
    defaultItem: {
      turno: "",
      frecuencia: "",
      capacidad: Number,
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
              RUTA_API +
                "/parameCentro/" +
                this.datosEdit.split("/")[4] +
                "/",
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
      if (
        !this.editedItem.turno ||
        !this.editedItem.frecuencia ||
        !this.editedItem.capacidad
      ) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        if(this.perfil==0){
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
        }else{
          this.dialogNoPrivilegios=true;
          this.close();
        }
        
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

    ParameCentroInit() {
      this.cabezeraParameCentro();
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
                "/parameCentro/?search=" +
                this.urlCas.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.desserts = res.data;
              this.dialogDataApi = false;
              //this.dataAdmi = res.data[0].url.split("/")[4];
              //this.datosPresHis = res.data[0];
              //console.log("desert", res.data);
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
    console.log("cas", this.urlCas);
    //INICIO DE CONSULTA

    this.ParameCentroInit();
  },

  components: {},
};
</script>


