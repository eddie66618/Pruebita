<template>
  <div>
    <v-container>
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
      <v-card class="mx-auto my-5" max-width="1000">
        <v-system-bar color="#1973a5" dark>
          REPORTE DE ASISTENCIA DE PACIENTES
        </v-system-bar>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="mt-4 container">
            <v-col cols="12" sm="6" md="6">
              <v-menu
                ref="menu1"
                v-model="menu1"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="date"
                    label="Fecha Desde"
                    hint="YYYY/MM/DD formato"
                    persistent-hint
                    prepend-icon="mdi-calendar"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="date"
                  no-title
                  @input="menu1 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-menu
                ref="menu2"
                v-model="menu2"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="dateHasta"
                    label="Fecha Hasta"
                    hint="YYYY/MM/DD formato"
                    persistent-hint
                    prepend-icon="mdi-calendar"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="dateHasta"
                  no-title
                  @input="menu2 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" md="4"></v-col>
            <v-col cols="12" md="4">
              <v-btn class="mt-10" icon color="#1973a5" @click="generatePDF">
                Generar PDF<v-icon>mdi-arrow-down-bold-box</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
import jsPDF from "jspdf";
import "jspdf-autotable";

export default {
  data: () => ({
    //DATAPARA REPORTE
    dataReporteAsistencia: [],
    dataReporteAsistenciaAdicional: [],
    //Dialogos
    dialogDataApi: false,
    //exportado pdf
    heading: "REPORTE ASISTENCIA",
    //data de fechas
    dateHoy: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    dateHasta: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    menu1: false,
    menu2: false,
    actionBoton: "AGREGAR",
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
    ////acreditacion
    vigenciaPac: "",
    capAdscPac: "",
    datosAcred: [],
    datosAcredAd: [],
  }),

  computed: {},

  watch: {},
  methods: {
    // FUNCION ACREDITACION
    /*async acredAdicional() {
      let respuesta = await new Promise((resolve, reject) => {
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
                  this.urlCas.split("/")[4],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                res.data = res.data.filter(
                  (e) =>
                    e.fecha_reg >= this.date && e.fecha_reg <= this.dateHasta
                );
                if (res.data.length > 0) {
                  for (let i = 0; i < res.data.length; i++) {
                    axios
                      .post(
                        RUTA_API + "/users/",
                        {
                          codOpcion: "1",
                          codTipDoc: "1",
                          numDoc: res.data[i].datosPaciente.num_doc,
                          fecNacimiento:
                            res.data[i].datosPaciente.fecha_nac.split("-")[2] +
                            "/" +
                            res.data[i].datosPaciente.fecha_nac.split("-")[1] +
                            "/" +
                            res.data[i].datosPaciente.fecha_nac.split("-")[0],
                        },
                        {
                          headers: { Authorization: this.auth },
                        }
                      )
                      .then((respuesta) => {
                        resolve(
                          //respuesta.data.vDataItem[0],
                          (this.datosAcredAd[i] = respuesta.data.vDataItem[0])
                        );
                      })
                      .catch((error) => {
                        reject(error);
                      });
                  }
                } else {
                  resolve((this.datosAcredAd = []));
                }
              })
              .catch((ans) => {
                reject(ans);
              });
          });
      });
    },
    async acreditacion() {
      let respuesta = await new Promise((resolve, reject) => {
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
                  "/asisPacDiario/?search=" +
                  this.urlCas.split("/")[4],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dataReporteAsistencia = [];
                console.log("prueba", res.data);
                res.data = res.data.filter(
                  (e) =>
                    e.fecha_reg >= this.date && e.fecha_reg <= this.dateHasta
                );
                if (res.data.length > 0) {
                  for (let i = 0; i < res.data.length; i++) {
                    axios
                      .post(
                        RUTA_API + "/users/",
                        {
                          codOpcion: "1",
                          codTipDoc: "1",
                          numDoc:
                            res.data[i].datosAsigCuposPac.datosPaciente.num_doc,
                          fecNacimiento:
                            res.data[
                              i
                            ].datosAsigCuposPac.datosPaciente.fecha_nac.split(
                              "-"
                            )[2] +
                            "/" +
                            res.data[
                              i
                            ].datosAsigCuposPac.datosPaciente.fecha_nac.split(
                              "-"
                            )[1] +
                            "/" +
                            res.data[
                              i
                            ].datosAsigCuposPac.datosPaciente.fecha_nac.split(
                              "-"
                            )[0],
                        },
                        {
                          headers: { Authorization: this.auth },
                        }
                      )
                      .then((respuesta) => {
                        resolve(
                          //respuesta.data.vDataItem[0],
                          (this.datosAcred[i] = respuesta.data.vDataItem[0])
                        );
                      })
                      .catch((error) => {
                        console.log(error);
                      });
                  }
                } else {
                  resolve((this.datosAcred = []));
                }
              })
              .catch((ans) => {
                reject(ans);
              });
          });
      });
    },*/

    // FUNCION ACREDITACION
    generatePDF() {
      this.dialogDataApi = true;
      //await this.acreditacion();
      //await this.acredAdicional();
      //console.log("DATOS ACREEDDD", this.datosAcred);
      //console.log('DAOTS ADICIONAL',this.datosAcredAd[0])
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;

          axios
            .get(
              RUTA_API + "/asisPacDiario/?search=" + this.urlCas.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.dataReporteAsistencia = [];
              console.log("prueba", res.data);
              res.data = res.data.filter(
                (e) => e.fecha_reg >= this.date && e.fecha_reg <= this.dateHasta
              );
              for (let i = 0; i < res.data.length; i++) {
                this.dataReporteAsistencia.push(
                  Object.assign(
                    { contador: i + 1 },
                    {
                      nombreCompleto:
                        res.data[i].datosAsigCuposPac.datosPaciente.ape_pat +
                        " " +
                        res.data[i].datosAsigCuposPac.datosPaciente.ape_mat +
                        " " +
                        res.data[i].datosAsigCuposPac.datosPaciente.nombres,
                    },
                    { estadoAsistencia: res.data[i].estadoAsistencia },
                    { estadoAcredi: res.data[i].estadoAcredi },
                    { observaFalta: res.data[i].observaFalta },
                    { fecha: res.data[i].fecha_reg },
                    { vigSeguro: res.data[i].vigSeguro },
                    { casAsd: res.data[i].casAsd }
                  )
                );
              }

              console.log("desde-hasta", this.date + " " + this.dateHasta);
              console.log("dataReporteAsistencial", this.dataReporteAsistencia);
              axios
                .get(
                  RUTA_API +
                    "/asisPacDiarioAdicional/?search=" +
                    this.urlCas.split("/")[4],
                  {
                    headers: { Authorization: this.auth },
                  }
                )
                .then((resAdicional) => {
                  this.dataReporteAsistenciaAdicional = [];

                  resAdicional.data = resAdicional.data.filter(
                    (e) =>
                      e.fecha_reg >= this.date && e.fecha_reg <= this.dateHasta
                  );
                  console.log("resAdicional", resAdicional.data);
                  for (let i = 0; i < resAdicional.data.length; i++) {
                    this.dataReporteAsistenciaAdicional.push(
                      Object.assign(
                        { contador: i + 1 },
                        { fecha: resAdicional.data[i].fecha_reg },
                        {
                          nombreCompleto:
                            resAdicional.data[i].datosPaciente.ape_pat +
                            " " +
                            resAdicional.data[i].datosPaciente.ape_mat +
                            " " +
                            resAdicional.data[i].datosPaciente.nombres,
                        },
                        { sala: resAdicional.data[i].sala },
                        {
                          frecuencia: resAdicional.data[i].frecuencia,
                        },
                        {
                          turno: resAdicional.data[i].turno,
                        },
                        {
                          observaFalta: resAdicional.data[i].motivo,
                        }
                      )
                    );
                  }
                  const doc = new jsPDF({
                    //orientation: "landscape",
                    unit: "in",
                    format: "letter",
                  });
                  var finalY = doc.lastAutoTable.finalY || 0.2;
                  doc.setFontSize(16).text(this.heading, 3.5, finalY + 0.1);
                  doc
                    .setFontSize(12)
                    .text("Hemodialisis Asistencia", 0.5, finalY + 0.3);
                  doc.autoTable({
                    startY: finalY + 0.5,
                    columns: [
                      { title: "Número", dataKey: "contador" },
                      { title: "Fecha", dataKey: "fecha" },
                      { title: "Nombre Completo", dataKey: "nombreCompleto" },
                      {
                        title: "Estado Asistencia",
                        dataKey: "estadoAsistencia",
                      },
                      { title: "Estado Acreditación", dataKey: "estadoAcredi" },
                      { title: "Motivo", dataKey: "observaFalta" },
                      { title: "CAS Adscripcion", dataKey: "casAsd" },
                      { title: "VIgencia Acreditacion", dataKey: "vigSeguro" },
                    ],
                    body: this.dataReporteAsistencia,
                    margin: { left: 0.5 },
                    styles: { fontSize: 5 },
                  });

                  var finalY = doc.lastAutoTable.finalY || 0.5;
                  doc
                    .setFontSize(12)
                    .text("Hemodialisis Adiconales", 0.5, finalY + 0.4);
                  doc.autoTable({
                    startY: finalY + 0.5,
                    columns: [
                      { title: "Número", dataKey: "contador" },
                      { title: "Fecha", dataKey: "fecha" },
                      { title: "Nombre Completo", dataKey: "nombreCompleto" },
                      { title: "Frecuencia", dataKey: "frecuencia" },
                      { title: "Turno", dataKey: "turno" },
                      { title: "Motivo", dataKey: "observaFalta" },
                    ],
                    body: this.dataReporteAsistenciaAdicional,
                    margin: { left: 0.5 },
                    styles: { fontSize: 5 },
                  });
                  doc
                    .setFont("times")
                    .setFontSize(10)
                    //.setFontStyle("italic")
                    .text(
                      "Reporte Generado por: HISAR " + this.dateHoy,
                      5.5,
                      doc.internal.pageSize.height - 0.5
                    );
                  doc.save(`${this.heading + " " + this.dateHoy}.pdf`);
                  this.dialogDataApi = false;
                  /*console.log("dessert", this.desserts);
                  console.log("resCuposAsig", resCuposAsig.data);
                  this.desserts = resCuposAsig.data;*/
                })
                .catch((resAdicional) => {
                  console.warn("Error:", resAdicional);
                  //this.dialog = false;
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


