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

    <v-container>
      <v-card class="mx-auto my-5" max-width="1000">
        <v-system-bar color="#1973a5" dark>
          LISTA DE PACIENTES QUE PIERDEN CUPOS
        </v-system-bar>
        <v-row class="mt-2 ml-15">
          <v-col cols="12" sm="6" md="6">
            <v-text-field
              class="mx-auto mt-2"
              v-model="setDni"
              label="Número de Documento"
              required
              :maxlength="10"
              @keyup.enter="buscarPacicente"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="6">
            <v-btn
              class="mt-2 mb-5"
              icon
              color="#1973a5"
              @click="buscarPacicente"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card>

      <v-card class="mx-auto my-5" max-width="1000">
        <v-data-table :headers="headers" :items="desserts" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
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
          <!--<template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="eliminarAsig(item)">
              mdi-account
            </v-icon>
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
          </template>-->
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
    //RECORD CUPOS POR PACIENTE
    setDni: "",
    //cupos

    //perfil data
    perfil: "",
    nombre: "",
    url: "",
    usuario: "",
    //Datos de formulario

    dialogDelete: false,

    dialogDataApi: false,

    headers: [],
    desserts: [],
    editedIndex: -1,
    dataex: "",
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
    liberarCuposInit() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/asisPacDiario/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("exito", res.data);
              this.cabezeraLiberarCupos();
              this.desserts = res.data;
              /*
              let data = res.data;
              for (let i = 0; i < data.length; i++) {
                
                for (let x = 0; x < data.length; x++) {
                  if(data[i].validacionAsistencia.split("|")[1]==data[x].validacionAsistencia.split("|")[1]){
                    console.log("resultado",data[x].validacionAsistencia.split("|")[1])
                  }
                }

              }*/
              var arrayRespuesta = [
                {
                  Nombre: "Fulano Detal",
                  Descripcion: "Un string explicando a qué se dedica",
                  Ciudad: { distrito: "CIUDAD 1" },
                },
                {
                  Nombre: "Otro Fulano",
                  Descripcion:
                    "String diferente que tambien describe su trabajo",
                  Ciudad: { distrito: "CIUDAD 1" },
                },
                {
                  Nombre: "Tercer Fulano",
                  Descripcion: "Su trabajo en donde sea que este",
                  Ciudad: { distrito: "CIUDAD 2" },
                },
              ];
              let data = res.data;
              var nuevoArray = [];
              var arrayTemporal = [];
              for (var i = 0; i < data.length; i++) {
                arrayTemporal = nuevoArray.filter(
                  (resp) =>
                    resp["DNI"] ==
                    data[i].datosAsigCuposPac.datosPaciente["num_doc"]
                );
                if (arrayTemporal.length > 0) {
                  nuevoArray[nuevoArray.indexOf(arrayTemporal[0])][
                    "Asistencia"
                  ].push({
                    estado: data[i]["estadoAsistencia"],
                    fecha: data[i]["fecha_reg"],
                  });
                } else {
                  nuevoArray.push({
                    DNI: data[i].datosAsigCuposPac.datosPaciente["num_doc"],
                    Asistencia: [
                      {
                        estado: data[i]["estadoAsistencia"],
                        fecha: data[i]["fecha_reg"],
                      },
                    ],
                  });
                }
              }
              console.log(nuevoArray);
              
            })
            .catch((res) => {
              console.log("ERROR", res);
            });
        })
        .catch((response) => {
          console.log("ERROR", response);
        });
    },

    cabezeraLiberarCupos() {
      this.headers = [
        { text: "Nombres", value: "datosAsigCuposPac.datosPaciente.nombres" },
        {
          text: "Apellido Paterno",
          value: "datosAsigCuposPac.datosPaciente.ape_pat",
        },
        {
          text: "Apellido Materno",
          value: "datosAsigCuposPac.datosPaciente.ape_mat",
        },
        {
          text: "Clínica",
          value: "datosAsigCuposPac.datosPueto.datosCas.descripCas",
        },
        { text: "Estado", value: "estadoAsistencia" },
        { text: "Fecha De inacistencia", value: "fecha_reg" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    buscarPacicente() {
      this.cabezeraLiberarCupos();
      console.log("buscar paciente");
    },

    initialize() {
      this.desserts = [];
    },

    editItem(item) {},

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

    edit() {},

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

    this.liberarCuposInit();
  },

  components: {},
};
</script>



