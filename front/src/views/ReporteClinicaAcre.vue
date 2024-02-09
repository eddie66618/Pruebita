<template>
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
    <v-card class="mx-auto my-5" max-width="900">
      <v-tabs background-color="#1973a5" center-active dark>
        <v-tab @click="adminForm = 0">PACIENTES POR CLÍNICA</v-tab>
        <!--<v-tab @click="adminForm = 1">Anemia</v-tab>-->
      </v-tabs>
    </v-card>
    <v-card class="mx-auto my-5" max-width="900" v-if="adminForm == 0">
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-system-bar color="#1973a5" dark>
          Reportes de Pacientes Por Clínica
        </v-system-bar>
        <v-row class="mt-4 container">
          <v-col cols="12" sm="12" md="12">
            <v-autocomplete
              v-model="urlClinica"
              :rules="[rules.required]"
              :items="itemsClinicas"
              item-text="descripCas"
              item-value="url"
              dense
              solo
              filled
              label="Por Clinica"
            ></v-autocomplete>
          </v-col>
          <!--<v-col cols="12" sm="6" md="6">
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
          </v-col>-->
          <v-col cols="12" md="6"></v-col>
          <v-col cols="12" md="6">
            <v-btn class="mt-10" icon color="#1973a5" @click="exportExcel">
              Generar Excel<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>
          </v-col>
          <!--<v-col cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5" @click="generatePDF">
              Generar PDF<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>
          </v-col>-->
        </v-row>
      </v-form>
    </v-card>

    <!--Reporte de Anemia-->

    <v-card class="mx-auto my-5" max-width="900" v-if="adminForm == 1">
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-system-bar color="#1973a5" dark> Reporte Anemia </v-system-bar>
        <v-row class="mt-4 container">
          <v-col cols="12" sm="12" md="12">
            <v-autocomplete
              v-model="valueClinicasAnemia"
              :items="itemsClinicas"
              :rules="[rules.required]"
              solo
              filled
              label="Seleccine una Clinica"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" sm="6" md="6">
            <v-menu
              ref="menu3"
              v-model="menu3"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="dateInicialAnemia"
                  label="Fecha Desde"
                  hint="YYYY/MM/DD formato"
                  persistent-hint
                  prepend-icon="mdi-calendar"
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dateInicialAnemia"
                no-title
                @input="menu3 = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" sm="6" md="6">
            <v-menu
              ref="menu4"
              v-model="menu4"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="dateHastaAnemia"
                  label="Fecha Hasta"
                  hint="YYYY/MM/DD formato"
                  persistent-hint
                  prepend-icon="mdi-calendar"
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dateHastaAnemia"
                no-title
                @input="menu4 = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" md="4"></v-col>
          <v-col cols="12" md="4">
            <v-btn
              class="mt-10"
              icon
              color="#1973a5"
              @click="exportExcelAnemia"
            >
              Generar Excel<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn
              class="mt-10"
              icon
              color="#1973a5"
              @click="generatePDFAnemia"
            >
              Generar PDF<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
export const RUTA_SERVIDOR = process.env.VUE_APP_RUTA_API;
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
export const RUTA_CENTRAL = process.env.VUE_APP_CENTRAL;
export const USUARIO_CENTRAL = process.env.VUE_APP_CENTRAL_USERNAME;
export const PASSWORD_CENTRAL = process.env.VUE_APP_CENTRAL_PASSWORD;

import ExportExcel from "./ExportarExcel.vue";
import * as XLSX from "xlsx";
import jsPDF from "jspdf";
import "jspdf-autotable";

export default {
  data: () => ({
    adminForm: 0,
    dialogDataApi: false,
    selectedPesta: "",
    valid: true,
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
    },
    dataToExport: [],
    dataToExport2: [],
    dataToExportAnemia: [],
    dataToExportAdmin: [],
    dataToExportExclu: [],
    dataNutriServ: [],
    dataNutriDefault: [],
    dataPdfExport: [],
    dataPdfExportPacNuevo: [],
    dataPdfExportAnemia: [],
    dataPdfExportAdmin: [],
    dataPdfExportExclu: [],
    heading: "INFORME MENSUAL DE NUTRICIÓN",
    select: [],
    itemsClinicas: [],
    urlClinica: "",
    valueClinicasAnemia: null,
    valueClinicas: null,
    dateHoy: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    date: new Date(
      Date.now() - 2592000000 - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .substr(0, 10),
    dateHasta: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    dateInicialAnemia: new Date(
      Date.now() - 2592000000 - new Date().getTimezoneOffset() * 6000
    )
      .toISOString()
      .substr(0, 10),
    dateHastaAnemia: new Date(
      Date.now() - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .substr(0, 10),
    menu: false,
    modal: false,
    modalHasta: false,
    menu4: false,
    menu3: false,
    menu2: false,
    menu1: false,
  }),

  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    },
  },

  watch: {
    date(val) {
      this.dateFormatted = this.formatDate(this.date);
    },
  },

  created() {
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

  methods: {
    formatDate(date) {
      if (!date) return null;

      const [year, month, day] = date.split("-");
      return `${month}/${day}/${year}`;
    },
    parseDate(date) {
      if (!date) return null;

      const [month, day, year] = date.split("/");
      return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
    },
    exportExcel() {
      this.dataToExport2 = [];
      this.dataToExport = [];
      this.dialogDataApi = true;
      if (this.urlClinica === "") {
        console.log("no a seleccionado ninguan clinica");
        this.$refs.form.validate();
      } else {
        this.dialogDataApi = true;
        this.dataToExport = [];
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
                  "/asigCuposPac/?search=" +
                  this.urlClinica.split("/")[4] +
                  ",true",
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("value clinica", this.urlClinica);
                console.log("respuesta", res.data);

                for (let i = 0; i < res.data.length; i++) {
                  this.dataToExport.push(
                    Object.assign(
                      { contador: i + 1 },
                      { tipoDoc:  res.data[i].datosPaciente.tipo_doc },
                      { Dni: res.data[i].datosPaciente.num_doc },
                      {
                        Nombre:
                          res.data[i].datosPaciente.nombres +
                          " " +
                          res.data[i].datosPaciente.ape_pat +
                          " " +
                          res.data[i].datosPaciente.ape_mat,
                      },
                      {
                        Edad:
                          res.data[i].datosPaciente.edad[0] +
                          " a " +
                          res.data[i].datosPaciente.edad[1] +
                          " m",
                      },
                      {
                        FechaNacimiento: res.data[i].datosPaciente.fecha_nac,
                      }
                    )
                  );
                }
                let cont = 0;
                for (let i = 0; i < this.dataToExport.length; i++) {
                  axios
                    .post(RUTA_API + "/api/token/", {
                      username: USUARIO,
                      password: PASSWORD,
                    })
                    .then((response) => {
                      this.auth = "Bearer " + response.data.access;
                      axios
                        .post(
                          RUTA_API + "/users/",
                          {
                            codOpcion: "1",
                            codTipDoc:
                              this.dataToExport[i].tipoDoc.split("/")[4] == 5 ? "1" : "2",
                            numDoc: this.dataToExport[i].Dni,
                            fecNacimiento:
                              this.dataToExport[i].FechaNacimiento.split(
                                "-"
                              )[2] +
                              "/" +
                              this.dataToExport[i].FechaNacimiento.split(
                                "-"
                              )[1] +
                              "/" +
                              this.dataToExport[i].FechaNacimiento.split(
                                "-"
                              )[0],
                          },
                          {
                            headers: { Authorization: this.auth },
                          }
                        )
                        .then((response) => {
                          //servicio nuevo de Acreditación
                         
                            
                              cont++;
                              this.dataToExport2.push(
                                Object.assign(
                                  { Dni: res.data[i].datosPaciente.num_doc },
                                  {
                                    Autogenerado:
                                      response.data.vDataItem[0].autogenerado,
                                  },
                                  {
                                    Clinica:
                                      res.data[i].datosPueto.datosCas
                                        .descripCas,
                                  },
                                  {
                                    Nombre:
                                      res.data[i].datosPaciente.ape_pat +
                                      " " +
                                      res.data[i].datosPaciente.ape_mat +
                                      " " +
                                      res.data[i].datosPaciente.nombres,
                                  },
                                  {
                                    Edad:
                                      res.data[i].datosPaciente.edad[0] +
                                      " a " +
                                      res.data[i].datosPaciente.edad[1] +
                                      " m",
                                  },
                                  {
                                    FechaNacimiento:
                                      res.data[i].datosPaciente.fecha_nac,
                                  },
                                  {
                                    Turno: res.data[i].datosPueto.turno,
                                  },
                                  {
                                    Frecuencia:
                                      res.data[i].datosPueto.frecuencia,
                                  },
                                  {
                                    Acreditado:
                                      response.data.vDataItem[0]
                                        .flagIndicadorActivo,
                                  },
                                  {
                                    FecVigHasta:
                                      response.data.vDataItem[0].fecVigHasta,
                                  },
                                  {
                                    Error: response.data.desError,
                                  }
                                )
                              );
                              if (this.dataToExport.length == cont) {
                                this.generarExcel(this.dataToExport2);
                                this.dialogDataApi = false;
                              }
              
                          //fin de nuevo servicio de acreditación
                        })
                        .catch((error) => {
                          console.log("Error on Authentication", error);
                        });
                    })
                    .catch((response) => {
                      response === 404
                        ? console.warn("lo sientimos no tenemos servicios")
                        : console.warn("Error:", response);
                    });
                }
                //if (this.dataToExport.length == cont) {
                //this.generarExcel(this.dataToExport);
                //}
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

    generarExcel(dataExport) {
      let data = XLSX.utils.json_to_sheet(dataExport);
      const workbook = XLSX.utils.book_new();
      const filename = "Exportado";
      XLSX.utils.book_append_sheet(workbook, data, filename);
      XLSX.writeFile(workbook, `${dataExport[0].Clinica}.xlsx`);
    },

    generatePDF() {
      if (this.valueClinicas === null) {
        console.log("no a seleccionado ninguan clinica");
        this.$refs.form.validate();
      } else {
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
                  "/nutricion/?search=" +
                  this.valueClinicas.split("-")[0],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                //this.dataNutriServ = res.data;
                console.log("serv", res.data);
                const result = res.data.filter((e) => e.pacNuevo == false);
                const resultNoNUevo = result.filter(
                  (e) =>
                    e.fechaEvaluacion >= this.date &&
                    e.fechaEvaluacion <= this.dateHasta
                );
                let resultPacNuevo = [];
                resultPacNuevo = res.data.filter((e) => e.pacNuevo == true);
                let resultPacN = [];
                resultPacN = resultPacNuevo.filter(
                  (e) =>
                    e.fechaEvaluacion >= this.date &&
                    e.fechaEvaluacion <= this.dateHasta
                );
                console.log("serv-noNuevo", result);
                console.log("servPacNuevo", resultPacNuevo);
                console.log("resultPacN", resultPacN);
                console.log("date Fecha", this.dateHasta);
                console.log("resultPacN", resultPacN);

                for (let i = 0; i < resultNoNUevo.length; i++) {
                  //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                  this.dataPdfExport.push(
                    Object.assign(
                      { contador: i + 1 },
                      {
                        dni: resultNoNUevo[i].datosPaciente.num_doc,
                      },
                      {
                        nombrePaciente:
                          resultNoNUevo[i].datosPaciente.nombres +
                          " " +
                          resultNoNUevo[i].datosPaciente.ape_pat +
                          " " +
                          resultNoNUevo[i].datosPaciente.ape_mat,
                      },
                      {
                        edad:
                          resultNoNUevo[i].datosPaciente.edad[0] +
                          " a " +
                          resultNoNUevo[i].datosPaciente.edad[1] +
                          " m",
                      },
                      resultNoNUevo[i]
                    )
                  );
                }
                for (let y = 0; y < resultPacN.length; y++) {
                  //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                  this.dataPdfExportPacNuevo.push(
                    Object.assign(
                      { contador: y + 1 },
                      {
                        dni: resultPacN[y].datosPaciente.num_doc,
                      },
                      {
                        nombrePaciente:
                          resultPacN[y].datosPaciente.nombres +
                          " " +
                          resultPacN[y].datosPaciente.ape_pat +
                          " " +
                          resultPacN[y].datosPaciente.ape_mat,
                      },
                      {
                        edad:
                          resultPacN[y].datosPaciente.edad[0] +
                          " a " +
                          resultPacN[y].datosPaciente.edad[1] +
                          " m",
                      },
                      resultPacN[y]
                    )
                  );
                }
                console.log("dataPdfExport", this.dataPdfExport);
                const columns = [];
                console.log(
                  "dataPdfExportPacNuevo",
                  this.dataPdfExportPacNuevo
                );

                const doc = new jsPDF({
                  orientation: "landscape",
                  unit: "in",
                  format: "letter",
                });
                // text is placed using x, y coordinates
                var finalY = doc.lastAutoTable.finalY || 0.5;
                doc.setFontSize(16).text(this.heading, 3.5, finalY);
                doc
                  .setFontSize(10)
                  .text(
                    "Centro Contratado: " + this.valueClinicas,
                    0.5,
                    finalY + 0.35
                  );
                doc
                  .setFontSize(10)
                  .text(
                    "Nutricionista a Cargo: " +
                      sessionStorage.getItem("nombre"),
                    0.5,
                    finalY + 0.55
                  );
                doc
                  .setFontSize(10)
                  .text(
                    "Mes: " + "Del " + this.date + " Al " + this.dateHasta,
                    0.5,
                    finalY + 0.74
                  );
                doc
                  .setFontSize(10)
                  .text(
                    "Fecha de Reporte: " + this.dateHoy,
                    6.0,
                    finalY + 0.74
                  );
                // create a line under heading
                doc
                  .setLineWidth(0.01)
                  .line(0.5, finalY + 0.85, 10.0, finalY + 0.85);
                doc
                  .setFontSize(10)
                  .text(
                    "Reporte de Pacientes Casos Problemas",
                    0.5,
                    finalY + 1
                  );
                doc
                  .setFontSize(8)
                  .text(
                    "N Pacientes casos problema (con diagnóstico de desnutrición) en el mes: " +
                      resultPacN.filter(
                        (e) => e.tipoPaciente === "CASO PROBLEMA"
                      ).length,
                    0.5,
                    finalY + 1.17
                  );
                doc
                  .setFontSize(8)
                  .text(
                    "N Pacientes Nuevos: " +
                      resultPacN.filter(
                        (e) => e.tipoPaciente === "PACIENTE NUEVO"
                      ).length,
                    5.5,
                    finalY + 1.17
                  );
                doc
                  .setFontSize(8)
                  .text(
                    "N Pacientes Continuadores: " +
                      resultPacN.filter(
                        (e) => e.tipoPaciente === "PACIENTE CONTINUADOR"
                      ).length,
                    8,
                    finalY + 1.17
                  );
                /*doc
                  .setFontSize(8)
                  .text("N Pacientes con DPE en el mes: ", 5.0, finalY + 1.12);*/
                // Using autoTable plugin
                doc.autoTable({
                  startY: finalY + 1.3,
                  columns: [
                    { title: "N", dataKey: "contador" },
                    { title: "Dni", dataKey: "dni" },
                    { title: "Paciente", dataKey: "nombrePaciente" },
                    { title: "Frecuencia", dataKey: "frecuencia" },
                    { title: "Turno", dataKey: "turno" },
                    { title: "Edad", dataKey: "edad" },
                    { title: "Tipo Paciente", dataKey: "tipoPaciente" },
                    { title: "Fecha Ingreso", dataKey: "fechaIngreso" },
                    { title: "Fecha Evaluacion", dataKey: "fechaEvaluacion" },
                    { title: "Peso", dataKey: "peso" },
                    { title: "Talla", dataKey: "talla" },
                    { title: "Imc", dataKey: "imc" },
                    { title: "%CMB", dataKey: "porcentajeCMB" },
                    { title: "%EPT", dataKey: "porcentajeEPT" },
                    { title: "Alb. Serica", dataKey: "albSerica" },
                    { title: "MIS", dataKey: "ValGlobalSub" },
                    { title: "Ingesta Calorica", dataKey: "ingestaCalorica" },
                    { title: "IngestaProteica", dataKey: "ingestaProteica" },
                    { title: "Diag. Nutricional", dataKey: "diagNutricional" },
                    {
                      title: "interveNutricional",
                      dataKey: "interveNutricional",
                    },
                    { title: "OBS", dataKey: "obsNutricion" },
                  ],
                  body: this.dataPdfExportPacNuevo,
                  margin: { left: 0.5, top: 1.87 },
                  styles: { fontSize: 5 },
                });
                this.dataPdfExport = [];
                finalY = doc.lastAutoTable.finalY;
                /*doc
                  .setFontSize(8)
                  .text("Reporte pacientes Nuevos", 0.5, finalY + 0.2);
                doc
                  .setFontSize(8)
                  .text(
                    "N pacientes nuevos evaluados en el mes: " +
                      resultPacN.length,
                    0.5,
                    finalY + 0.33
                  );
                console.log("comlumnssss", columns);
                doc.autoTable({
                  startY: finalY + 0.4,
                  columns: [
                    { title: "N", dataKey: "contador" },
                    { title: "Dni", dataKey: "dni" },
                    { title: "Paciente", dataKey: "nombrePaciente" },
                    { title: "Frecuencia", dataKey: "frecuencia" },
                    { title: "Turno", dataKey: "turno" },
                    { title: "Edad", dataKey: "edad" },
                    { title: "Fecha Ingreso", dataKey: "fechaIngreso" },
                    { title: "Fecha Evaluacion", dataKey: "fechaEvaluacion" },
                    { title: "Peso", dataKey: "peso" },
                    { title: "Talla", dataKey: "talla" },
                    { title: "Imc", dataKey: "imc" },
                    { title: "%CMB", dataKey: "porcentajeCMB" },
                    { title: "%EPT", dataKey: "porcentajeEPT" },
                    { title: "Alb. Serica", dataKey: "albSerica" },
                    { title: "Val. Global. Sub", dataKey: "ValGlobalSub" },
                    { title: "Ingesta Calorica", dataKey: "ingestaCalorica" },
                    { title: "IngestaProteica", dataKey: "ingestaProteica" },
                    { title: "Diag. Nutricional", dataKey: "diagNutricional" },
                    {
                      title: "interveNutricional",
                      dataKey: "interveNutricional",
                    },
                  ],
                  body: this.dataPdfExportPacNuevo,
                  margin: { left: 0.5, top: 1.87 },
                  styles: { fontSize: 5 },
                });
                this.dataPdfExportPacNuevo = [];
                // Using array of sentences
                /*doc
                  .setFont("helvetica")
                  .setFontSize(12)
                  .text(this.desserts, 0.5, 3.5, { align: "left", maxWidth: "7.5" });
                */
                // Creating footer and saving file
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text("Obesidad", 0.5, doc.internal.pageSize.height - 2.2);
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      resultPacN.filter((e) => e.diagNutricional === "Obesidad")
                        .length,
                    2.5,
                    doc.internal.pageSize.height - 2.2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (
                        (resultPacN.filter(
                          (e) => e.diagNutricional === "Obesidad"
                        ).length /
                          (resultPacN.filter(
                            (e) => e.diagNutricional === "Obesidad"
                          ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Sobrepeso"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Normal"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Leve"
                            ).length +
                            resultPacN.filter(
                              (e) =>
                                e.diagNutricional === "Desnutrición Moderada"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Severa"
                            ).length)) *
                        100
                      ).toFixed(2) +
                      "%",
                    3,
                    doc.internal.pageSize.height - 2.2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text("Sobrepeso", 0.5, doc.internal.pageSize.height - 2);
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      resultPacN.filter(
                        (e) => e.diagNutricional === "Sobrepeso"
                      ).length,
                    2.5,
                    doc.internal.pageSize.height - 2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (
                        (resultPacN.filter(
                          (e) => e.diagNutricional === "Sobrepeso"
                        ).length /
                          (resultPacN.filter(
                            (e) => e.diagNutricional === "Obesidad"
                          ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Sobrepeso"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Normal"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Leve"
                            ).length +
                            resultPacN.filter(
                              (e) =>
                                e.diagNutricional === "Desnutrición Moderada"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Severa"
                            ).length)) *
                        100
                      ).toFixed(2) +
                      "%",
                    3,
                    doc.internal.pageSize.height - 2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text("Normal", 0.5, doc.internal.pageSize.height - 1.8);
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      resultPacN.filter((e) => e.diagNutricional === "Normal")
                        .length,
                    2.5,
                    doc.internal.pageSize.height - 1.8
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (
                        (resultPacN.filter(
                          (e) => e.diagNutricional === "Normal"
                        ).length /
                          (resultPacN.filter(
                            (e) => e.diagNutricional === "Obesidad"
                          ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Sobrepeso"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Normal"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Leve"
                            ).length +
                            resultPacN.filter(
                              (e) =>
                                e.diagNutricional === "Desnutrición Moderada"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Severa"
                            ).length)) *
                        100
                      ).toFixed(2) +
                      "%",
                    3,
                    doc.internal.pageSize.height - 1.8
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "Desnutricion Leve",
                    0.5,
                    doc.internal.pageSize.height - 1.6
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      resultPacN.filter(
                        (e) => e.diagNutricional === "Desnutrición Leve"
                      ).length,
                    2.5,
                    doc.internal.pageSize.height - 1.6
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (
                        (resultPacN.filter(
                          (e) => e.diagNutricional === "Desnutrición Leve"
                        ).length /
                          (resultPacN.filter(
                            (e) => e.diagNutricional === "Obesidad"
                          ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Sobrepeso"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Normal"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Leve"
                            ).length +
                            resultPacN.filter(
                              (e) =>
                                e.diagNutricional === "Desnutrición Moderada"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Severa"
                            ).length)) *
                        100
                      ).toFixed(2) +
                      "%",
                    3,
                    doc.internal.pageSize.height - 1.6
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "Desnutricion Moderada",
                    0.5,
                    doc.internal.pageSize.height - 1.4
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      resultPacN.filter(
                        (e) => e.diagNutricional === "Desnutrición Moderada"
                      ).length,
                    2.5,
                    doc.internal.pageSize.height - 1.4
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (
                        (resultPacN.filter(
                          (e) => e.diagNutricional === "Desnutrición Moderada"
                        ).length /
                          (resultPacN.filter(
                            (e) => e.diagNutricional === "Obesidad"
                          ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Sobrepeso"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Normal"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Leve"
                            ).length +
                            resultPacN.filter(
                              (e) =>
                                e.diagNutricional === "Desnutrición Moderada"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Severa"
                            ).length)) *
                        100
                      ).toFixed(2) +
                      "%",
                    3,
                    doc.internal.pageSize.height - 1.4
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "Desnutricion Severa",
                    0.5,
                    doc.internal.pageSize.height - 1.2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      resultPacN.filter(
                        (e) => e.diagNutricional === "Desnutrición Severa"
                      ).length,
                    2.5,
                    doc.internal.pageSize.height - 1.2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (
                        (resultPacN.filter(
                          (e) => e.diagNutricional === "Desnutrición Severa"
                        ).length /
                          (resultPacN.filter(
                            (e) => e.diagNutricional === "Obesidad"
                          ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Sobrepeso"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Normal"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Leve"
                            ).length +
                            resultPacN.filter(
                              (e) =>
                                e.diagNutricional === "Desnutrición Moderada"
                            ).length +
                            resultPacN.filter(
                              (e) => e.diagNutricional === "Desnutrición Severa"
                            ).length)) *
                        100
                      ).toFixed(2) +
                      "%",
                    3,
                    doc.internal.pageSize.height - 1.2
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text("Total", 0.5, doc.internal.pageSize.height - 1);
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text(
                    "" +
                      (resultPacN.filter(
                        (e) => e.diagNutricional === "Obesidad"
                      ).length +
                        resultPacN.filter(
                          (e) => e.diagNutricional === "Sobrepeso"
                        ).length +
                        resultPacN.filter((e) => e.diagNutricional === "Normal")
                          .length +
                        resultPacN.filter(
                          (e) => e.diagNutricional === "Desnutrición Leve"
                        ).length +
                        resultPacN.filter(
                          (e) => e.diagNutricional === "Desnutrición Moderada"
                        ).length +
                        resultPacN.filter(
                          (e) => e.diagNutricional === "Desnutrición Severa"
                        ).length),
                    2.5,
                    doc.internal.pageSize.height - 1
                  );
                doc
                  .setFont("times")
                  .setFontSize(7)
                  //.setFontStyle("italic")
                  .text("100%", 3, doc.internal.pageSize.height - 1);
                doc
                  .setFont("times")
                  .setFontSize(10)
                  //.setFontStyle("italic")
                  .text(
                    "Firma y sello Nutricionista",
                    6,
                    doc.internal.pageSize.height - 0.7
                  );
                doc
                  .setFont("times")
                  .setFontSize(10)
                  //.setFontStyle("italic")
                  .text(
                    "C.N.P. N°____",
                    6.5,
                    doc.internal.pageSize.height - 0.5
                  );
                doc.save(`${this.heading}.pdf`);
                //console.log(this.desserts[0].datosPaciente.nombres, "aqui tas");
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

        //delete this.dataPdfExport
      }
    },
    //DE AQUI EN ADELANTE ANEMIA REPORTES
    exportExcelAnemia() {
      if (this.valueClinicasAnemia === null) {
        console.log("no a seleccionado ninguan clinica");
        this.$refs.form.validate();
      } else {
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
                  "/presAnemia/?search=" +
                  this.valueClinicasAnemia.split("-")[0],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("data presAnemia", res.data);

                for (let i = 0; i < res.data.length; i++) {
                  //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                  this.dataToExportAnemia.push(
                    Object.assign(
                      { contador: i + 1 },
                      { Dni: res.data[i].datosPaciente.num_doc },
                      {
                        Nombre:
                          res.data[i].datosPaciente.nombres +
                          " " +
                          res.data[i].datosPaciente.ape_pat +
                          " " +
                          res.data[i].datosPaciente.ape_mat,
                      },
                      {
                        edad:
                          res.data[i].datosPaciente.edad[0] +
                          " a " +
                          res.data[i].datosPaciente.edad[1] +
                          " m",
                      },
                      {
                        NomNefro: res.data[i].nomNefro,
                      },
                      {
                        FechaPres: res.data[i].fechaPres,
                      },
                      {
                        MedPres: res.data[i].medPres,
                      },
                      {
                        DosisPresMensual: res.data[i].dosisPres,
                      },
                      {
                        MedHiePres: res.data[i].medHiePres,
                      },
                      {
                        DosisHiePresSemanal: res.data[i].dosisHiePres,
                      },
                      {
                        Registro:
                          res.data[i].datosUsuario.num_doc +
                          "-" +
                          res.data[i].datosUsuario.nombre,
                      },
                      {
                        Clinica: res.data[i].datosUsuario.datosCas.descripCas,
                      },
                      {
                        CasOrigen:
                          res.data[i].datosPaciente.datosCasOri.descripCas,
                      }
                    )
                  );
                }
                console.log("resulAnemia", this.dataToExportAnemia);
                const resultFechaAnemia = this.dataToExportAnemia.filter(
                  (e) =>
                    e.FechaPres >= this.dateInicialAnemia &&
                    e.FechaPres <= this.dateHastaAnemia
                );
                console.log("resultFechaAnemia", resultFechaAnemia);
                let data = XLSX.utils.json_to_sheet(resultFechaAnemia);
                const workbook = XLSX.utils.book_new();
                const filename = "Exportado";
                XLSX.utils.book_append_sheet(workbook, data, filename);
                XLSX.writeFile(workbook, `${filename} Prescripcion.xlsx`);

                this.dataToExportAnemia = [];
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

        //delete this.dataPdfExport
      }

      //Administración Anemia

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
                "/adminAnemia/?search=" +
                this.valueClinicasAnemia.split("-")[0],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((resAdmin) => {
              console.log("data adminAnemia", resAdmin.data);
              for (let i = 0; i < resAdmin.data.length; i++) {
                //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                this.dataToExportAdmin.push(
                  Object.assign(
                    { contador: i + 1 },
                    { Dni: resAdmin.data[i].datosPres.datosPaciente.num_doc },
                    {
                      Nombre:
                        resAdmin.data[i].datosPres.datosPaciente.nombres +
                        " " +
                        resAdmin.data[i].datosPres.datosPaciente.ape_pat +
                        " " +
                        resAdmin.data[i].datosPres.datosPaciente.ape_mat,
                    },
                    {
                      edad:
                        resAdmin.data[i].datosPres.datosPaciente.edad[0] +
                        " a " +
                        resAdmin.data[i].datosPres.datosPaciente.edad[1] +
                        " m",
                    },
                    { FechaAdmi: resAdmin.data[i].fechaAdmi },
                    { NomEnfer: resAdmin.data[i].nomEnfer },
                    { MedAdmi: resAdmin.data[i].medAdmi },
                    { ViaAdm: resAdmin.data[i].viaAdm },
                    { DosisAdmi: resAdmin.data[i].dosisAdmi },
                    { MedHieAdmi: resAdmin.data[i].medHieAdmi },
                    { ViaAdmHierro: resAdmin.data[i].viaAdmHierro },
                    { DosisHieAdmi: resAdmin.data[i].dosisHieAdmi },
                    {
                      Registro:
                        resAdmin.data[i].datosUsuario.num_doc +
                        "-" +
                        resAdmin.data[i].datosUsuario.nombre,
                    },
                    {
                      Clinica:
                        resAdmin.data[i].datosUsuario.datosCas.descripCas,
                    },
                    {
                      CasOrigen:
                        resAdmin.data[i].datosPres.datosPaciente.datosCasOri
                          .descripCas,
                    }
                  )
                );
              }
              console.log("resulAnemia", this.dataToExportAdmin);
              const resultFechaAdmin = this.dataToExportAdmin.filter(
                (e) =>
                  e.FechaAdmi >= this.dateInicialAnemia &&
                  e.FechaAdmi <= this.dateHastaAnemia
              );
              console.log("resultFechaAnemia", resultFechaAdmin);
              let data = XLSX.utils.json_to_sheet(resultFechaAdmin);
              const workbook = XLSX.utils.book_new();
              const filename = "Exportado";
              XLSX.utils.book_append_sheet(workbook, data, filename);
              XLSX.writeFile(workbook, `${filename} Administracion.xlsx`);

              this.dataToExportAdmin = [];
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

      //Administración exclusion

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
                "/exclusionAnemia/?search=" +
                this.valueClinicasAnemia.split("-")[0],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((resExclu) => {
              console.log("data excluAnemia", resExclu.data);
              for (let i = 0; i < resExclu.data.length; i++) {
                //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                this.dataToExportExclu.push(
                  Object.assign(
                    { contador: i + 1 },
                    { Dni: resExclu.data[i].datosPaciente.num_doc },
                    {
                      Nombre:
                        resExclu.data[i].datosPaciente.nombres +
                        " " +
                        resExclu.data[i].datosPaciente.ape_pat +
                        " " +
                        resExclu.data[i].datosPaciente.ape_mat,
                    },
                    {
                      edad:
                        resExclu.data[i].datosPaciente.edad[0] +
                        " a " +
                        resExclu.data[i].datosPaciente.edad[1] +
                        " m",
                    },
                    { FechaExclu: resExclu.data[i].fechaExclu },
                    { RazonExclu: resExclu.data[i].razonExclu },
                    { ObservaExclu: resExclu.data[i].ObservaExclu },
                    {
                      Clinica:
                        resExclu.data[i].datosUsuario.datosCas.descripCas,
                    },
                    {
                      CasOrigen:
                        resExclu.data[i].datosPaciente.datosCasOri.descripCas,
                    }
                  )
                );
              }
              console.log("excluAnemia", this.dataToExportExclu);
              const resultFechaExclu = this.dataToExportExclu.filter(
                (e) =>
                  e.FechaExclu >= this.dateInicialAnemia &&
                  e.FechaExclu <= this.dateHastaAnemia
              );
              console.log("resultFechaAnemia", resultFechaExclu);
              let data = XLSX.utils.json_to_sheet(resultFechaExclu);
              const workbook = XLSX.utils.book_new();
              const filename = "Exportado";
              XLSX.utils.book_append_sheet(workbook, data, filename);
              XLSX.writeFile(workbook, `${filename} Exclusion.xlsx`);

              this.dataToExportAdmin = [];
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

    generatePDFAnemia() {
      if (this.valueClinicasAnemia === null) {
        console.log("no a seleccionado ninguan clinica");
        this.$refs.form.validate();
      } else {
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
                  "/presAnemia/?search=" +
                  this.valueClinicasAnemia.split("-")[0],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                axios
                  .get(
                    RUTA_API +
                      "/adminAnemia/?search=" +
                      this.valueClinicasAnemia.split("-")[0],
                    {
                      headers: { Authorization: this.auth },
                    }
                  )
                  .then((resAdm) => {
                    axios
                      .get(
                        RUTA_API +
                          "/exclusionAnemia/?search=" +
                          this.valueClinicasAnemia.split("-")[0],
                        {
                          headers: { Authorization: this.auth },
                        }
                      )
                      .then((resExclu) => {
                        //Inicio de reporte PDF
                        //this.dataNutriServ = res.data;
                        console.log("servPresAnemia", res.data);
                        const result = res.data.filter(
                          (e) =>
                            e.fechaPres >= this.dateInicialAnemia &&
                            e.fechaPres <= this.dateHastaAnemia
                        );
                        console.log("resultado filtrando fecha", result);

                        for (let i = 0; i < result.length; i++) {
                          //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                          this.dataPdfExportAnemia.push(
                            Object.assign(
                              { contador: i + 1 },
                              {
                                dni: result[i].datosPaciente.num_doc,
                              },
                              {
                                nombrePaciente:
                                  result[i].datosPaciente.nombres +
                                  " " +
                                  result[i].datosPaciente.ape_pat +
                                  " " +
                                  result[i].datosPaciente.ape_mat,
                              },
                              {
                                edad:
                                  result[i].datosPaciente.edad[0] +
                                  " a " +
                                  result[i].datosPaciente.edad[1] +
                                  " m",
                              },
                              {
                                Clinica:
                                  result[i].datosUsuario.datosCas.descripCas,
                              },
                              {
                                CasOrigen:
                                  result[i].datosPaciente.datosCasOri
                                    .descripCas,
                              },
                              result[i]
                            )
                          );
                        }

                        console.log(
                          "dataPdfExportAnemia",
                          this.dataPdfExportAnemia
                        );
                        const columns = [];
                        const doc = new jsPDF({
                          orientation: "landscape",
                          unit: "in",
                          format: "letter",
                        });
                        // text is placed using x, y coordinates
                        var finalY = doc.lastAutoTable.finalY || 0.5;
                        doc
                          .setFontSize(16)
                          .text("Reporte Anemia por Clínica", 3.5, finalY);
                        doc
                          .setFontSize(10)
                          .text(
                            "Centro Contratado: " + this.valueClinicasAnemia,
                            0.5,
                            finalY + 0.35
                          );
                        doc
                          .setFontSize(10)
                          .text(
                            "Mes: " +
                              "Del " +
                              this.dateInicialAnemia +
                              " Al " +
                              this.dateHastaAnemia,
                            0.5,
                            finalY + 0.64
                          );
                        doc
                          .setFontSize(10)
                          .text(
                            "Fecha de Reporte: " + this.dateHoy,
                            6.0,
                            finalY + 0.64
                          );
                        // create a line under heading
                        doc
                          .setLineWidth(0.01)
                          .line(0.5, finalY + 0.75, 10.0, finalY + 0.75);
                        doc
                          .setFontSize(8)
                          .text(
                            "Lista de Prescripciones de Anemia",
                            0.5,
                            finalY + 0.95
                          );
                        doc
                          .setFontSize(8)
                          .text(
                            "N° Prescripciones: " + result.length,
                            0.5,
                            finalY + 1.1
                          );
                        // Using autoTable plugin
                        doc.autoTable({
                          startY: finalY + 1.15,
                          columns: [
                            { title: "N", dataKey: "contador" },
                            { title: "Dni", dataKey: "dni" },
                            { title: "Paciente", dataKey: "nombrePaciente" },
                            { title: "nomNefro", dataKey: "nomNefro" },
                            { title: "fechaPres", dataKey: "fechaPres" },
                            { title: "medPres", dataKey: "medPres" },
                            { title: "viaAdmPres", dataKey: "viaAdmPres" },
                            { title: "dosisPres", dataKey: "dosisPres" },
                            { title: "medHiePres", dataKey: "medHiePres" },
                            {
                              title: "viaAdmHiePres",
                              dataKey: "viaAdmHiePres",
                            },
                            { title: "dosisHiePres", dataKey: "dosisHiePres" },
                            { title: "Clinica", dataKey: "Clinica" },
                            { title: "CasOrigen", dataKey: "CasOrigen" },
                          ],
                          //startY: 10,
                          body: this.dataPdfExportAnemia,
                          margin: { left: 0.5, top: 1.87 },
                          styles: { fontSize: 6 },
                        });
                        finalY = doc.lastAutoTable.finalY;
                        doc
                          .setFontSize(8)
                          .text(
                            "Lista de Administraciones de Anemia ",
                            0.5,
                            finalY + 0.2
                          );
                        const resultAdm = resAdm.data.filter(
                          (e) =>
                            e.fechaAdmi >= this.dateInicialAnemia &&
                            e.fechaAdmi <= this.dateHastaAnemia
                        );
                        doc
                          .setFontSize(8)
                          .text(
                            "N° Administraciones: " + resultAdm.length,
                            0.5,
                            finalY + 0.35
                          );
                        console.log("Administracion servicio", resAdm.data);

                        for (let i = 0; i < resultAdm.length; i++) {
                          //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                          this.dataPdfExportAdmin.push(
                            Object.assign(
                              { contador: i + 1 },
                              {
                                dni: resultAdm[i].datosPres.datosPaciente
                                  .num_doc,
                              },
                              {
                                nombrePaciente:
                                  resultAdm[i].datosPres.datosPaciente.nombres +
                                  " " +
                                  resultAdm[i].datosPres.datosPaciente.ape_pat +
                                  " " +
                                  resultAdm[i].datosPres.datosPaciente.ape_mat,
                              },
                              {
                                edad:
                                  resultAdm[i].datosPres.datosPaciente.edad[0] +
                                  " a " +
                                  resultAdm[i].datosPres.datosPaciente.edad[1] +
                                  " m",
                              },
                              {
                                Clinica:
                                  resultAdm[i].datosUsuario.datosCas.descripCas,
                              },
                              {
                                CasOrigen:
                                  resultAdm[i].datosPres.datosPaciente
                                    .datosCasOri.descripCas,
                              },
                              resultAdm[i]
                            )
                          );
                        }
                        console.log("Administracion Filtrado Fecha", resultAdm);
                        console.log("dataPdfAdmin", this.dataPdfExportAdmin);
                        //console.log("comlumnssss", columns);
                        doc.autoTable({
                          startY: finalY + 0.4,
                          columns: [
                            { title: "N", dataKey: "contador" },
                            { title: "Dni", dataKey: "dni" },
                            { title: "Paciente", dataKey: "nombrePaciente" },
                            { title: "nomEnfer", dataKey: "nomEnfer" },
                            { title: "fechaAdmi", dataKey: "fechaAdmi" },
                            { title: "medAdmi", dataKey: "medAdmi" },
                            { title: "viaAdm", dataKey: "viaAdm" },
                            { title: "dosisAdmi", dataKey: "dosisAdmi" },
                            { title: "medHieAdmi", dataKey: "medHieAdmi" },
                            { title: "viaAdmHierro", dataKey: "viaAdmHierro" },
                            { title: "dosisHieAdmi", dataKey: "dosisHieAdmi" },
                            { title: "Clinica", dataKey: "Clinica" },
                            { title: "CasOrigen", dataKey: "CasOrigen" },
                          ],
                          body: this.dataPdfExportAdmin,
                          margin: { left: 0.5, top: 1.87 },
                          styles: { fontSize: 5 },
                        });
                        finalY = doc.lastAutoTable.finalY;
                        console.log("Exclusión servicio", resExclu.data);
                        doc
                          .setFontSize(8)
                          .text(
                            "Lista de Exclusión de Anemia",
                            0.5,
                            finalY + 0.2
                          );
                        const resultExclu = resExclu.data.filter(
                          (e) =>
                            e.fechaExclu >= this.dateInicialAnemia &&
                            e.fechaExclu <= this.dateHastaAnemia
                        );
                        doc
                          .setFontSize(8)
                          .text(
                            "N° Exclusiónes: " + resultExclu.length,
                            0.5,
                            finalY + 0.35
                          );

                        for (let i = 0; i < resultExclu.length; i++) {
                          //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                          this.dataPdfExportExclu.push(
                            Object.assign(
                              { contador: i + 1 },
                              {
                                dni: resultExclu[i].datosPaciente.num_doc,
                              },
                              {
                                nombrePaciente:
                                  resultExclu[i].datosPaciente.nombres +
                                  " " +
                                  resultExclu[i].datosPaciente.ape_pat +
                                  " " +
                                  resultExclu[i].datosPaciente.ape_mat,
                              },
                              {
                                edad:
                                  resultExclu[i].datosPaciente.edad[0] +
                                  " a " +
                                  resultExclu[i].datosPaciente.edad[1] +
                                  " m",
                              },
                              {
                                Clinica:
                                  resultExclu[i].datosUsuario.datosCas
                                    .descripCas,
                              },
                              {
                                CasOrigen:
                                  resultExclu[i].datosPaciente.datosCasOri
                                    .descripCas,
                              },
                              resultExclu[i]
                            )
                          );
                        }
                        console.log("Exclusion Filtrado Fecha", resultExclu);
                        console.log("dataPdfExclu", this.dataPdfExportExclu);
                        //console.log("comlumnssss", columns);
                        doc.autoTable({
                          startY: finalY + 0.4,
                          columns: [
                            { title: "N", dataKey: "contador" },
                            { title: "Dni", dataKey: "dni" },
                            { title: "Paciente", dataKey: "nombrePaciente" },
                            { title: "fechaExclu", dataKey: "fechaExclu" },
                            { title: "razonExclu", dataKey: "razonExclu" },
                            { title: "ObservaExclu", dataKey: "ObservaExclu" },
                            { title: "Clinica", dataKey: "Clinica" },
                            { title: "CasOrigen", dataKey: "CasOrigen" },
                          ],
                          body: this.dataPdfExportExclu,
                          margin: { left: 0.5, top: 1.87 },
                          styles: { fontSize: 5 },
                        });
                        this.dataPdfExportExclu = [];
                        this.dataPdfExportAnemia = [];
                        this.dataPdfExportAdmin = [];
                        // Using array of sentences
                        /*doc
                  .setFont("helvetica")
                  .setFontSize(12)
                  .text(this.desserts, 0.5, 3.5, { align: "left", maxWidth: "7.5" });
                */
                        // Creating footer and saving file
                        /*doc
                  .setFont("times")
                  .setFontSize(10)
                  //.setFontStyle("italic")
                  .text(
                    "Firma y sello Nutricionista",
                    6,
                    doc.internal.pageSize.height - 0.7
                  );
                doc
                  .setFont("times")
                  .setFontSize(10)
                  //.setFontStyle("italic")
                  .text(
                    "C.N.P. N°____",
                    6.5,
                    doc.internal.pageSize.height - 0.5
                  );*/
                        doc.save(`${this.heading}.pdf`);
                        //console.log(this.desserts[0].datosPaciente.nombres, "aqui tas");
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

        //delete this.dataPdfExport
      }
    },
  },

  mounted() {},

  components: {
    ExportExcel,
  },
};
</script>

