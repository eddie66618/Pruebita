<template>
  <div>
    <NavBar />
    <div class="d-flex flex-column justify-space-between align-center">
      <v-card class="mx-auto my-12" max-width="374">
        <div class="text-center mt-10">
          <h1>Cambiar Contraseña</h1>
        </div>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-col cols="12" md="12">
                <v-text-field
                  prepend-icon="mdi-lock"
                  v-model="contraActual"
                  :rules="nameRules"
                  label="contraseña Actual"
                  type="password"
                  required
                  autocomplete="off"
                  @keypress="actualizar"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="12">
                <v-text-field
                  prepend-icon="mdi-lock"
                  v-model="contraNueva1"
                  :rules="nameRules"
                  label="Nueva Constraseña"
                  type="password"
                  autocomplete="off"
                  required
                  @keypress="actualizar"
                  @keyup.enter="ingresar"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="12">
                <v-text-field
                  prepend-icon="mdi-lock"
                  v-model="contraNueva2"
                  :rules="nameRules"
                  label="Repetir Nueva Constraseña"
                  type="password"
                  autocomplete="off"
                  required
                  @keypress="actualizar"
                  @keyup.enter="cambiarContra"
                ></v-text-field>
              </v-col>
            </v-row>
            <div class="text-center mt-10 mb-5">
              <v-btn depressed color="primary" large @click="cambiarContra">
                Cambiar Contraseña
              </v-btn>
              <v-dialog v-model="dialog" hide-overlay persistent width="300">
                <v-card color="primary" dark>
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
            </div>
            <v-alert
              border="top"
              color="red"
              dismissible
              outlined
              text
              :value="value"
              type="warning"
            >
              Usuario o Contraseña incorrectos
            </v-alert>
            <v-alert
              border="top"
              color="green"
              dismissible
              outlined
              text
              :value="valueGreen"
              type="warning"
            >
              Se actualizo la clave correctamente
            </v-alert>
            <v-alert
              border="top"
              color="red"
              dismissible
              outlined
              text
              :value="valueError"
              type="warning"
            >
              ¡Error!,Revise los datos ingresados
            </v-alert>
          </v-container>
        </v-form>
      </v-card>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/navbar/NavBar.vue";
import axios from "axios";
export const RUTA_SERVIDOR = process.env.VUE_APP_RUTA_API;
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;

export default {
  data() {
    return {
      perfil: "",
      nombre: "",
      url: "",
      usuario: "",
      dialog: false,
      valid: false,
      contraActual: "",
      contraNueva1: "",
      contraNueva2: "",
      value: false,
      valueGreen: false,
      valueError: false,
      nameRules: [
        (v) => !!v || "*Campo obligatorio",
        (v) => v.length <= 10 || "*Maximo 10 caracteres",
      ],
    };
  },
  methods: {
    cambiarContra() {
      this.dialog = true;
      this.value = false;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/usuario/?search=" + this.usuario, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("respuesta", res.data);
              this.dialog = false;
              if (
                this.usuario == res.data[0].usuario &&
                this.contraActual == res.data[0].clave &&
                this.contraNueva1 == this.contraNueva2
              ) {
                axios
                  .patch(
                    RUTA_API +
                      "/usuario/" +
                      res.data[0].url.split("/")[4] +
                      "/",
                    {
                      num_doc: res.data[0].num_doc,
                      nombre: res.data[0].nombre,
                      cas: res.data[0].cas,
                      usuario: res.data[0].usuario,
                      clave: this.contraNueva2,
                      perfil: res.data[0].perfil,
                    },
                    {
                      headers: { Authorization: this.auth },
                    }
                  )
                  .then((res1) => {
                    conosole.log("clave cambiada");
                    this.valueGreen = true;
                  })
                  .catch((res1) => {
                    console.warn("Error:", res);
                    this.valueGreen = true;
                    this.value = false;
                    this.valueError = false;
                  });
              } else {
                this.valueError = true;
              }
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.dialog = false;
              this.value = true;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
          this.value = true;
        });
    },
    actualizar() {
      this.value = false;
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
    console.log("Perfil", this.perfil);
    console.log("nombre", this.nombre);
    console.log("url", this.url);
    console.log("usuario", this.usuario);
  },
  components: {
    NavBar,
  },
};
</script>