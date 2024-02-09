<template>
  <div class="principal">
    <div class="msg-bienv">
      <p>Bienvenido {{ usuarioLogin }}</p>
      <button class="btn-logout" @click="logout">CERRAR SESION</button>
    </div>
    <h1 style="text-align: center; color: #07c">
      CENSO A PACIENTES RENALES 2023
    </h1>
    <button class="btn-atras" @click="atras">
      <font-awesome-icon :icon="['fas', 'arrow-left']" style="color: #ffffff" />
      Atras
    </button>
    <div class="msg-edit" v-show="msg_edit">Ya puede editar el registro</div>
    <div class="msg-edit" v-show="pacAct">Datos actualizados de paciente</div>
    <div class="form">
      <h4 style="text-transform: uppercase; text-align: center">
        Detalles de Registro de Paciente
      </h4>
      <div class="input-div">
        <div class="div">
          <v-autocomplete
            id="input-user"
            :items="clinicasFiltered"
            item-text="descripCas"
            item-value="url"
            v-model="clinic"
            outlined
            label="Clinica"
          ></v-autocomplete>
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">DNI</h5>
          <input
            type="text"
            class="input"
            id="input-dni"
            maxlength="8"
            v-model="dni"
            disabled
          />
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">Paciente</h5>
          <input
            type="text"
            class="inputss"
            id="input-userss"
            v-model="paciente"
            disabled
          />
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">Telefono</h5>
          <input
            type="text"
            class="input"
            maxlength="9"
            id="input-telefono"
            v-model="telefono"
            disabled
          />
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">Telefono 2</h5>
          <input
            type="text"
            class="input"
            maxlength="9"
            id="input-user"
            v-model="telefono2"
            disabled
          />
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <!--<h5 class="input-h5">Departamento</h5>
                    <input type="text" class="inputss" v-model="departamento" disabled>-->
          <v-autocomplete
            id="input-user"
            :items="departamento"
            v-model="departamentoEleg"
            outlined
            label="Departamento"
            @change="mostrarOpciones"
          ></v-autocomplete>
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <v-autocomplete
            :items="provinciasFiltered"
            :item-text="getItemText"
            item-value="url"
            v-model="dep"
            outlined
            label="Provincia / Distrito"
          ></v-autocomplete>
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">Direccion</h5>
          <input
            type="text"
            class="input"
            maxlength="150"
            id="input-direccion"
            v-model="direccion"
            disabled
          />
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">Referencia</h5>
          <input
            type="text"
            class="input"
            maxlength="150"
            id="input-referencia"
            v-model="referencia"
            disabled
          />
        </div>
      </div>
      <div class="input-div">
        <div class="div">
          <h5 class="input-h5">Geolocalizacion (Latitud, Longitud)</h5>
          <input
            type="text"
            class="input"
            id="input-user"
            v-model="geoCoord"
            disabled
          />
        </div>
      </div>
      <div class="btns-cont">
        <button class="btn-edit" @click="editarPac">EDITAR</button>
        <button class="btn-save" id="btn-save" @click="guardarCambios">
          GUARDAR
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.msg-bienv {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin: 10px;
}
.msg-error {
  text-align: center;
  background-color: #fab9b5;
  color: red;
  border: 1px solid red;
  padding: 10px 0;
  margin: 3vw;
}
.principal {
  margin: 10px;
}
.form {
  padding-top: 10px;
}
.msg-edit {
  margin-top: 12px;
  background-color: #c0f4cc;
  color: green;
  border: 1px solid green;
  text-align: center;
  padding: 2px;
}
.btn-edit,
.btn-eliminar,
.btn-save {
  padding: 5px;
  border-radius: 5px;
}
.btns-cont {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.btn-save {
  background-color: #007ac9;
  color: #fff;
}
.btn-edit {
  background-color: #00a79c;
  color: #fff;
}
.btn-logout {
  font-size: 14px;
  background-color: #e35c5c;
  display: block;
  margin-left: auto;
  color: #ffff;
  padding: 7px 5px;
  border-radius: 7px;
}
.btn-atras {
  background-color: #dad220;
  color: #fff;
  border-radius: 5px;
  padding: 5px;
}
.btn-atras:hover,
.btn-edit:hover,
.btn-save:hover {
  opacity: 0.7;
}

.input-div > .div > .input-h5 {
  position: relative;
  top: 10px;
}
select {
  border: 1px solid #ccc;
  width: 100%;
  height: 100%;
}
.input-div {
  margin-bottom: 10px;
}
.input-div > div {
  position: relative;
  height: 55px;
  background-color: #f5f5f5;
}

.input-div > div > h5 {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #000;
  font-weight: normal;
  font-size: 15px;
  transition: 0.3s;
}

.input-div:before,
.input-div:after {
  content: "";
  position: absolute;
  bottom: -2px;
  width: 0%;
  height: 2px;
  transition: 0.4s;
}

.input-div:before {
  right: 50%;
}

.input-div:after {
  left: 50%;
}

.input-div.focus:before,
.input-div.focus:after {
  width: 50%;
}

.input-div.focus > div > h5 {
  top: 10px;
  font-size: 15px;
}

.input-div.focus > .i > i {
  color: #3678b0;
}

.input-div > div > input,
select {
  position: absolute;
  left: 0;
  top: 0;
  text-indent: 10px;
  width: 100%;
  height: 100%;
  border: 1px solid #ccc;
  outline: none;
  background: none;
  padding-top: 10px;
  font-size: 15px;
  color: #555;
}
</style>

<script>
import axios from "axios";

export const RUTA_SERVIDOR = process.env.VUE_APP_RUTA_API;
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;

export default {
  props: ["id"],
  data() {
    return {
      //user login data
      dniUsuarioLogin: sessionStorage.dniUsuario,
      usuarioLogin: sessionStorage.nombre,
      clinicasFiltered: [],
      msg_edit: false,
      dni: "",
      paciente: "No hay paciente",
      telefono: "",
      telefono2: "",
      departamento: "LIMA",
      provinciasFiltered: [],
      distritosFiltered: [],
      direccion: "",
      referencia: "",
      geoCoord: "",
      clinicaselect: "",
      provinciaselect: "",
      clinic: "",
      dep: "",
      pacAct: false,
      departamento: ["LIMA", "CALLAO"],
      departamentoEleg: "",
    };
  },
  watch: {
    dni: function () {
      if (this.dni.length == 8) {
        this.getPaciente(this.dni);
      } else {
        this.paciente = "";
      }
    },
  },
  methods: {
    mostrarOpciones() {
      this.getProvincias();
    },
    logout() {
      sessionStorage.clear();
      this.$router.push("/");
    },
    verificarValor(valor, id) {
      if (valor == "") {
        let inp = document.getElementById(id);
        inp.style.border = "1.5px solid red";
      } else {
        let inp = document.getElementById(id);
        inp.style.border = "1.5px solid #ccc";
      }
    },
    getItemText(item) {
      return `${item.provincia}, ${item.distrito}`;
    },
    atras() {
      this.$router.push("/censo");
    },
    getPaciente(dnipac) {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/paciente/?search=" + dnipac, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.pacienteUrl = res.data[0].url;
              this.paciente =
                res.data[0].nombres +
                " " +
                res.data[0].ape_pat +
                " " +
                res.data[0].ape_mat;
            })
            .catch((res) => {
              this.paciente = "No existe paciente";
              console.warn("error: ", res);
            });
        });
    },
    getData() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/pacienteLocalizacion/" + this.id + "/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              ///console.log(res.data)
              this.dni = res.data.datosPaciente.num_doc;
              this.clinic = res.data.datosCas.url;
              //this.clinic = res.data.datosCas.descripCas
              this.telefono = res.data.telefono;
              this.telefono2 = res.data.telefonoAlterno;
              this.departamentoEleg = res.data.datosUbigeo.departamento
              this.dep = res.data.datosUbigeo.url;
              this.direccion = res.data.direccion;
              this.referencia = res.data.referencia;
              this.geoCoord = res.data.latitud + ", " + res.data.longitud;
              //this.listRegistros = res.data
              //this.provincias = res.data
              //this.provinciasFiltered = this.provincias.filter((e)=>e.departamento=="LIMA")
            })
            .catch((res) => {
              console.warn("error: ", res);
            });
        });
    },

    editarPac() {
      let inp = document.querySelectorAll(".input");
      inp.forEach((input) => (input.disabled = false));
      this.msg_edit = true;
      setTimeout(() => {
        this.msg_edit = false;
      }, 1500);
    },
    guardarCambios() {
      this.verificarValor(this.dni, "input-dni");
      this.verificarValor(this.telefono, "input-telefono");
      this.verificarValor(this.direccion, "input-direccion");
      this.verificarValor(this.referencia, "input-referencia");

      let latitud = this.geoCoord.split(",")[0];
      let longitud = this.geoCoord.split(",")[1];
      let datos = {
        cas: this.clinic,
        paciente: this.pacienteUrl,
        ubigeo: this.dep,
        direccion: this.direccion.trim().toUpperCase(),
        referencia: this.referencia.trim().toUpperCase(),
        telefono: this.telefono.trim(),
        telefonoAlterno: this.telefono2.trim(),
        latitud: latitud,
        longitud: longitud,
        cordePac:
          "SRID=4326;POINT (" +
          this.geoCoord.split(",")[1].trim() +
          " " +
          this.geoCoord.split(",")[0].trim() +
          ")",
        userReg: sessionStorage.dniUsuario,
      };
      console.log(datos);
      if (
        this.pacienteUrl != "" &&
        this.dni != "" &&
        this.telefono != "" &&
        this.direccion != "" &&
        this.geoCoord != ""
      ) {
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .patch(
                RUTA_API + "/pacienteLocalizacion/" + this.id + "/",
                datos,
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("Exito actualizando estado de Mensaje", res.status);
                this.pacAct = true;
                setTimeout(() => (this.pacAct = false), 2000);
              })
              .catch((res) => {
                console.warn("Error:", res);
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("Lo sentimos no tenemos servicios")
              : console.warn("Error:", response);
          });
        //this.$router.push("/detallesol/" + `${url.split("/")[4]}`);
      }
    },
    getProvincias() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/ubigeo/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.provincias = res.data;
              this.provinciasFiltered = this.provincias.filter((e)=>e.departamento==this.departamentoEleg)
            })
            .catch((res) => {
              console.warn("error: ", res);
            });
        });
    },
    getClinicas() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/cas/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.clinicas = res.data;
              this.clinicasFiltered = this.clinicas.filter(
                (e) => e.tipoCas == "2" && e.estado == true
              );
            })
            .catch((res) => {
              console.warn("error: ", res);
            });
        });
    },
  },
  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
    const inputs = this.$el.querySelectorAll(".input");
    inputs.forEach((input) => {
      input.addEventListener("focus", function () {
        let parent = input.parentNode.parentNode;
        parent.classList.add("focus");
      });
      input.addEventListener("blur", function () {
        let parent = input.parentNode.parentNode;
        if (input.value == "") {
          parent.classList.remove("focus");
        }
      });
    });
    this.getClinicas();
    this.getProvincias();
    this.getData();
  },
};
</script>