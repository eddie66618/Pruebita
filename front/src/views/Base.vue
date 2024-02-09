<template>
  <div>
    <v-container>
      <v-card class="mx-auto my-5" max-width="1000">
        <v-system-bar color="#1973a5" dark>
          Asistencia Emergencia
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
                              v-model="editedItem.paciente"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsTurno"
                              dense
                              label="PACIENTE"
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
                              v-model="editedItem.turno"
                              :rules="[rules.required, rules.counter]"
                              label="TURNO"
                              :maxlength="8"
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
export default {
  data: () => ({
    actionBoton: "AGREGAR HEMODIALISIS ADICIONAL",
    editedItem: {
      //Cupos
      paciente: "",
      frecuencia: "",
      turno: "",
    },
    defaultItem: {
      paciente: "",
      frecuencia: "",
      turno: "",
    },
    headers: [],
    desserts: [],
    dialog: false,
    dialogEdit: false,
    dialogDelete: false,
    valid: true,
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    itemsTurno: ["TURNO 1", "TURNO 2", "TURNO 3", "TURNO 4"],
    itemsFrecuencia: ["LUN-MIE-VIE", "MAR-JUE-SAB"],
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
    save() {
      console.log("guardar");
    },
    edit() {
      console.log("editar");
    },
    deleteItemConfirm() {},
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
  },

  components: {},
};
</script>


