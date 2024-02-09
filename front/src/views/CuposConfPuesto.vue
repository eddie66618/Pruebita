<template>
  <div>
    <v-bottom-navigation :value="value" class="" color="primary" horizontal>
      <v-container class="">
        <v-row>
          <v-col v-if="urlCas.split('/')[4] == '1'" cols="12" sm="6" md="3">
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
      persistent
      v-model="dialogEditPuesto"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark
          >Editar Puesto {{ editedItem.numeroPuesto }}</v-toolbar
        >
        <v-container class="mt-5">
          <v-row>
            <v-col cols="12" sm="12" md="12">
              <v-autocomplete
                v-model="editedItem.tipoPuesto"
                :rules="[rules.required, rules.counter]"
                :items="itemsPuesto"
                dense
                label="PUESTO"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="12" md="12">
              <v-radio-group v-model="editedItem.estado" row>
                <v-radio label="Activo" value="true"></v-radio>
                <v-radio label="Inactivo" value="false"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions class="justify-end">
          <v-btn text @click="cambioPuesto">Aceptar</v-btn>
          <v-btn text @click="dialogEditPuesto = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-row>
        <v-col
          :key="indice"
          v-for="(contadorRes, indice) in contadorConf"
          cols="12"
          sm="2"
          md="2"
        >
          <v-card class="mx-auto" max-width="250">
            <v-card-text v-if="contadorRes.tipoPuesto == 'NEGATIVO'">
              <div>PUESTO {{ contadorRes.numeroPuesto }}</div>
              <p class="text-h5 text--primary">{{ contadorRes.tipoPuesto }}</p>
              <p
                v-if="contadorRes.estado == true"
                class="text-h5 text--primary"
              >
                ACTIVO
              </p>
              <p v-else class="text-h5 red--text">INACTIVO</p>
            </v-card-text>
            <v-card-text v-else>
              <div class="orange--text">
                PUESTO {{ contadorRes.numeroPuesto }}
              </div>
              <p class="text-h5 orange--text">{{ contadorRes.tipoPuesto }}</p>
              <p
                v-if="contadorRes.estado == true"
                class="text-h5 text--primary"
              >
                ACTIVO
              </p>
              <p v-else class="text-h5 red--text">INACTIVO</p>
            </v-card-text>
            <v-card-actions>
              <v-btn
                @click="configItem(contadorRes)"
                text
                color="deep-purple accent-4"
                elevation="2"
              >
                Configurar
              </v-btn>
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

export default {
  data: () => ({
    value: 1,
    //cupos
    itemsTurno: ["TURNO 1", "TURNO 2", "TURNO 3", "TURNO 4"],
    itemsFrecuencia: ["LUN-MIE-VIE", "MAR-JUE-SAB"],
    itemsSala: ["SALA1", "SALA2", "SALA3", "SALA4"],
    itemsEstado: ["true", "false"],
    itemsPuesto: ["NEGATIVO", "B POSITIVO", "C POSITIVO"],
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
    },
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
    },
    dialog: false,
    dialogEdit: false,
    formAdmi: false,
    dialogDelete: false,
    dialogEditAdm: false,
    dialogNoEdit: false,
    dialogDataApi: false,
    dialogEditPuesto: false,
    vista: "",
    valid: true,
    datosEdit: "",
    actionBoton: "AGREGAR",
    contadorConf: [],
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
              this.dialogEditPuesto = false;
              this.ParameCentroPuestoInit();
              this.ejecutarTurno();
              //.dialogEdit = false;
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
      console.log("item", item);
      this.dialogEditPuesto = true;
      this.editedItem.numeroPuesto = item.numeroPuesto;
      this.editedItem.tipoPuesto = item.tipoPuesto;
      this.editedItem.estado = item.estado.toString();
      this.datosEditPuesto = item.url;
    },

    ejecutarTurno() {
      console.log("cas", this.desserts);
      if (this.urlCas.split("/")[4] == "1") {
        if (this.editedItem.sala == "SALA1") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.turno == this.editedItem.turno &&
              e.frecuencia == this.editedItem.frecuencia &&
              e.numeroPuesto > 0 &&
              e.numeroPuesto <= 10
          );
          resultTurno.sort((x, y) => x.numeroPuesto - y.numeroPuesto);
          this.contadorConf = resultTurno;
          console.log("contador",this.contadorConf)
        }
        if (this.editedItem.sala == "SALA2") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.turno == this.editedItem.turno &&
              e.frecuencia == this.editedItem.frecuencia &&
              e.numeroPuesto > 10 &&
              e.numeroPuesto <= 20
          );
          resultTurno.sort((x, y) => x.numeroPuesto - y.numeroPuesto);
          this.contadorConf = resultTurno;
        }
        if (this.editedItem.sala == "SALA3") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.turno == this.editedItem.turno &&
              e.frecuencia == this.editedItem.frecuencia &&
              e.numeroPuesto > 20 &&
              e.numeroPuesto <= 30
          );
          resultTurno.sort((x, y) => x.numeroPuesto - y.numeroPuesto);
          this.contadorConf = resultTurno;
        }
        if (this.editedItem.sala == "SALA4") {
          const resultTurno = this.desserts.filter(
            (e) =>
              e.turno == this.editedItem.turno &&
              e.frecuencia == this.editedItem.frecuencia &&
              e.numeroPuesto > 30 &&
              e.numeroPuesto <= 40
          );
          resultTurno.sort((x, y) => x.numeroPuesto - y.numeroPuesto);
          this.contadorConf = resultTurno;
        }
      } else {
        console.log(this.desserts, "desserts");
        const resultTurno = this.desserts.filter(
          (e) =>
            e.turno == this.editedItem.turno &&
            e.frecuencia == this.editedItem.frecuencia
        );
        //console.log("resultTurno", resultTurno);
        resultTurno.sort((x, y) => x.numeroPuesto - y.numeroPuesto);
        this.contadorConf = resultTurno;
        console.log("contadorConf", this.contadorConf);
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
      //this.cabezeraParameCentro();
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
                "/parameCentroPuesto/?search=" +
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
              console.log("parametrosPuesto", res.data);
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
    this.ParameCentroPuestoInit();
  },

  components: {},
};
</script>


