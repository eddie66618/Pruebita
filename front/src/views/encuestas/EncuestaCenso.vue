<template>
  <div class="principal">
    <div class="msg-bienv">
      <p>Bienvenido {{ usuarioLogin }}</p>
      <button class="btn-logout" @click="logout">CERRAR SESION</button>
    </div>
    <div class="content-pacientes">
      <h1>CENSO A PACIENTES RENALES 2023</h1>
      <ul class="options" @click="obtenerClase">
        <li class="list-element active">AGREGAR PACIENTE</li>
        <li class="list-element">PACIENTES REGISTRADOS</li>
      </ul>
      <div v-show="showForm">
        <div class="form" v-show="mostrarForm">
          <h4
            style="
              text-align: center;
              font-size: 16px;
              text-transform: uppercase;
            "
          >
            Ingrese informacion de paciente
          </h4>
          <div class="input-div">
            <div class="div" id="input-clinica">
              <v-autocomplete
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
              <h5>DNI</h5>
              <input
                type="text"
                class="input"
                id="input-dni"
                maxlength="8"
                v-model="dni"
              />
            </div>
          </div>
          <div class="input-div">
            <div class="div">
              <h5 class="input-h5">Paciente</h5>
              <input
                type="text"
                class="input"
                id="input-user"
                v-model="paciente"
                disabled
              />
            </div>
          </div>
          <div class="input-div">
            <div class="div">
              <h5>Telefono</h5>
              <input
                type="text"
                maxlength="9"
                class="input"
                id="input-telefono"
                v-model="telefono"
              />
            </div>
          </div>
          <div class="input-div">
            <div class="div">
              <h5>Telefono 2</h5>
              <input
                type="text"
                maxlength="9"
                class="input"
                id="input-user"
                v-model="telefono2"
              />
            </div>
          </div>
          <div class="input-div">
            <div class="div">
              <!--<h5 class="input-h5">Departamento</h5>
                            <input type="text" class="input" v-model="departamento" disabled>-->
              <v-autocomplete
                :items="departamento"
                v-model="departamentoEleg"
                outlined
                label="Departamento"
                @change="mostrarOpciones"
              ></v-autocomplete>
            </div>
          </div>
          <div class="input-div">
            <div class="div" id="input-provdist">
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
                maxlength="150"
                class="input"
                id="input-direccion"
                v-model="direccion"
              />
            </div>
          </div>
          <div class="input-div">
            <div class="div">
              <h5>Referencia</h5>
              <input
                type="text"
                maxlength="150"
                class="input"
                id="input-referencia"
                v-model="referencia"
              />
            </div>
          </div>
          <div class="input-div">
            <div class="div">
              <h5>Geolocalizacion (Latitud, Longitud)</h5>
              <input
                type="text"
                class="input"
                id="input-geo"
                v-model="geoCoord"
              />
            </div>
          </div>
          <div style="width: 100%">
            <button class="btn-add-pacientes" @click="registrarPaciente">
              REGISTRAR
            </button>
          </div>
        </div>
        <div class="mensaje-success" v-show="successMsg">
          <p>Paciente {{ paciente }} registrado</p>
          <button class="btn-paciente-registrado" @click="mostrarFormulario">
            REGISTRAR OTRO PACIENTE
          </button>
        </div>
      </div>

      <div class="content-pacientes-registro" v-show="showResults">
        <table class="tabla" v-if="listRegistrosFiltered">
          <thead>
            <td>Fecha de Registro</td>
            <td>DNI</td>
            <td>PACIENTE</td>
            <td>ACCIONES</td>
          </thead>
          <tbody>
            <tr v-for="f in listRegistrosFiltered" :key="f.url">
              <td>{{ f.fechaReg }}</td>
              <td>{{ f.datosPaciente.num_doc }}</td>
              <td>
                {{
                  f.datosPaciente.nombres +
                  " " +
                  f.datosPaciente.ape_pat +
                  " " +
                  f.datosPaciente.ape_mat
                }}
              </td>
              <td>
                <button class="btn-info" @click="verDetalles(f.url)">
                  <font-awesome-icon
                    :icon="['fas', 'eye']"
                    style="color: #ffffff"
                  />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="!listRegistrosFiltered">
          <p style="text-align: center">
            No tiene registro de datos de pacientes
          </p>
        </div>
      </div>
      <div class="msg-error" v-show="errorclient">
        ERROR: Paciente ya registrado
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
.options {
  display: flex;
  list-style-type: none;
  justify-content: space-around;
  width: 100vw;
  padding: 0 10px;
}

.options li {
  width: 45vw;
  padding: 10px;
  text-align: center;
}

li.active {
  background-color: #000;
  color: #fff;
}

.mensaje-success {
  margin: 10px;
  background-color: #c0f4cc;
  color: green;
  border: 1px solid green;
  text-align: center;
  padding: 2px;
}

.btn-add-pacientes {
  font-size: 15px;
  background-color: #a1ce57;
  width: 100%;
  padding: 4px;
  color: white;
  border-radius: 10px;
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

a {
  display: block;
  text-align: right;
  text-decoration: none;
  color: #999;
  font-size: 0.9rem;
  transition: 0.3s;
}

/*
.input-input:focus+ .input-label,
.input-input:not(:placeholder-shown)+.input-label {
    transform: translateY(-12px) scale(.7);
    transform-origin: left top;
    font-size: 22px;
}*/

/*
select{
    width: 48vw;
    text-indent: 10px;
    background-color: #FFF;
}
select:focus{
    outline: 1px solid #007ac9;
}*/
.content-pacientes h1 {
  padding: 10px;
  color: #007ac9;
}

.content-pacientes-registro {
  margin-top: 10px;
  padding: 10px;
}

.tabla {
  border: 1px solid #ccc;
  table-layout: auto;
}

.tabla thead {
  font-weight: bold;
  font-size: 22px;
  text-align: center;
  background-color: #007ac9;
  color: white;
}

.tabla tbody {
  text-align: center;
}

.btn-add,
.btn-add-datos-paciente {
  background-color: #578dde;
  color: white;
  padding: 10px;
  border-radius: 10px;
  height: fit-content;
}

.btn-info {
  background-color: #00a79c;
  padding: 5px;
  border-radius: 5px;
}

.btn-edit,
.btn-eliminar {
  padding: 10px;
  border-radius: 5px;
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
.btn-edit {
  background-color: #dabc53;
}

.btn-eliminar {
  background-color: #e9696c;
  color: white;
}

.btn-add:hover,
.btn-edit:hover,
.btn-eliminar:hover,
.btn-search:hover {
  opacity: 0.8;
}

.form {
  width: 95vw;
  margin: 10px auto;
  border: 1px solid #ccc;
  box-shadow: 1px 1px 1px 1px #ccc;
  border-radius: 10px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  /*background-color: rgba(0,122,201,0.11)*/
}

/*
.form-input {
    display: flex;
    align-items: center;
    gap: 10px;
}*/

/*.input {
    border: 1px solid #ccc;
    background-color: #fff;
}

.input:focus {
    outline: 1px solid #007ac9;
}

.form-input label {
    width: 26vw;
}
*/
.btn-search {
  background-color: #a1ce57;
  padding: 1px;
  width: 30px;
}
#optiones {
  display: none;
}

.btn-paciente-registrado{
    color: #fff;
    background-color:green;
    padding:1.5% 2%;
    border-radius: 10px;
}


@media screen and (max-width: 600px) {
  .form {
    font-size: 15px;
  }

  .content-pacientes {
    width: 100vw;
  }

  .content-pacientes h1 {
    text-align: center;
  }

  .content-pacientes-registro {
    overflow-y: scroll;
  }

  .tabla thead td,
  .tabla tbody td {
    padding: 12px;
  }

  .tabla thead {
    font-size: 12px;
  }

  .tabla tbody {
    font-size: 11px;
  }

  .btn-add {
    width: 95vw;
    display: block;
    margin: 0 auto;
  }

  .btn-add-datos-paciente {
    display: block;
    /* margin: 0 auto;*/
    background-color: #a1ce57;
    font-size: 11px;
    padding: 5px;
    width: 50%;
  }

  .btn-add,
  .btn-edit,
  .btn-eliminar {
    padding: 5px;
    font-size: 11px;
  }

  .btn-edit,
  .btn-eliminar {
    margin-bottom: 5px;
  }
  
}
</style>

<script>
import axios from "axios";

export const RUTA_SERVIDOR = process.env.VUE_APP_RUTA_API;
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
export const RUTA_SERVIDOR_HISAR = process.env.VUE_APP_RUTA_HISAR;

export default {
  data() {
    return {
      //user login data
      dniUsuarioLogin: sessionStorage.dniUsuario,
      usuarioLogin: sessionStorage.nombre,
      errorclient: false,
      mostrarForm: true,
      dni: "",
      paciente: "No paciente identificado",
      provincias: null,
      clinicas: null,
      distritos: null,
      departamento: "LIMA",
      distrito: "",
      departamento: ["LIMA", "CALLAO"],
      clinicasFiltered: [],
      provinciasFiltered: [],
      distritosFiltered: null,
      successMsg: false,
      listRegistros: null,
      listRegistrosFiltered: null,
      departamentoEleg: "LIMA",
      //
      showForm: true,
      showResults: false,
      //valores a guardar
      telefono: "",
      telefono2: "",
      pacienteUrl: "",
      direccion: "",
      referencia: "",
      geoCoord: "",
      clinic: "",
      dep: "",
    };
  },
  watch: {
    dni: function () {
      if (this.dni.length == 8) {
        this.getPaciente(this.dni);
      }
    },
  },
  methods: {
    mostrarFormulario() {
      this.successMsg = false;
      this.mostrarForm = true;
    },
    mostrarOpciones() {
      this.getProvincias();
    },
    logout() {
      sessionStorage.clear();
      this.$router.push("/");
    },
    getItemText(item) {
      return `${item.provincia}, ${item.distrito}`;
    },
    obtenerClase(e) {
      for (const li of document.querySelectorAll("li.active")) {
        li.classList.remove("active");
      }
      e.target.classList.add("active");
      if (e.target.innerText == "AGREGAR PACIENTE") {
        this.showForm = true;
        this.showResults = false;
      } else if (e.target.innerText == "PACIENTES REGISTRADOS") {
        this.showForm = false;
        this.showResults = true;
      }
    },
    verDetalles(url) {
      this.$router.push(`/censo/${url.split("/")[4]}`);
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
              this.provinciasFiltered = this.provincias.filter(
                (e) => e.departamento === this.departamentoEleg
              );
              //this.provinciasFiltered = this.provincias.filter((e) => e.departamento == "LIMA")
            })
            .catch((res) => {
              console.warn("error: ", res);
            });
        });
    },
    getRegistrosPacientes() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/pacienteLocalizacion/?search="+this.dniUsuarioLogin, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              //console.log(res.data)
              this.listRegistrosFiltered = res.data;
              /*this.listRegistrosFiltered = this.listRegistros.filter(
                (e) => e.userReg === this.dniUsuarioLogin
              );*/
              if (this.listRegistrosFiltered.length == 0) {
                this.listRegistrosFiltered = null;
              }
              //this.provincias = res.data
              //this.provinciasFiltered = this.provincias.filter((e)=>e.departamento=="LIMA")
            })
            .catch((res) => {
              console.warn("error: ", res);
            });
        });
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
    getClinicas() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          console.log("resdata", response);
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/cas/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("resdata", res.data);
              this.clinicas = res.data;
              this.clinicasFiltered = this.clinicas.filter(
                (e) => e.tipoCas == "2" && e.estado == true
              );
            })
            .catch((res) => {
              console.log("resdata", res.data);
              console.warn("error: ", res);
            });
        });
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
    verificarValorSelect(valor, id) {
      if (valor === "") {
        document.getElementById(id).focus();
      }
    },
    registrarPaciente() {
      let inp = document.querySelectorAll("fieldset");
      inp.forEach((inp) => {
        if (
          inp.parentNode.parentNode.getElementsByTagName("input")[1].value == ""
        ) {
          inp.style.color = "red";
          console.log(
            inp.parentNode.parentNode.getElementsByTagName("input")[1].value
          );
        } else {
          inp.style.color = "#ccc";
        }
      });

      this.verificarValor(this.dni, "input-dni");
      this.verificarValorSelect(this.clinic, "input-clinica");
      //this.verificarValor(this.clinic,"input-clinica")
      this.verificarValor(this.telefono, "input-telefono");
      this.verificarValor(this.dep, "input-provdist");
      ///this.verificarValor(this.clinicaUrl,"clinicaSelected")
      this.verificarValor(this.direccion, "input-direccion");
      //this.verificarValor(this.referencia,"input-referencia")
      this.verificarValor(this.geoCoord, "input-geo");
      //this.verificarValor(this.provinciaDistritoSelected,"provinciaSelected")

      let latitud = this.geoCoord.split(",")[0];
      let longitud = this.geoCoord.split(",")[1];

      if (
        this.pacienteUrl != "" &&
        this.dni != "" &&
        this.telefono != "" &&
        this.direccion != "" &&
        this.geoCoord != ""
      ) {
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

        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(RUTA_API + "/pacienteLocalizacion/", datos, {
                headers: { Authorization: this.auth },
              })
              .then((res) => {
                //console.log(res)
                this.successMsg = true;
                this.mostrarForm = false;
                //setTimeout(() => (this.successMsg = false), 2000);
                this.dni = "";
                (this.clinic = ""),
                  (this.telefono = ""),
                  (this.telefono2 = ""),
                  (this.pacienteUrl = ""),
                  (this.dep = ""),
                  (this.direccion = ""),
                  (this.referencia = ""),
                  (this.geoCoord = "");
                this.paciente = "";
              })
              .catch(({ response }) => {
                if (response.status === 400) {
                  this.errorclient = true;
                  setTimeout(() => (this.errorclient = false), 2500);
                }
              });
          });
      } else {
        console.log("complete los datos");
      }
    },
    mostrarModal() {
      this.mostrarForm = !this.mostrarForm;
    },
  },
  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
    const inputs = document.querySelectorAll(".input");

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
    this.getRegistrosPacientes();
    ///
  },
};
</script>
