<template>
    <div>
        <v-dialog v-model="dialogConfirmacion" max-width="600px">
            <v-card class="mx-auto">
                <!-- <v-icon class="">mdi-close-circle</v-icon> -->
                <v-form ref="form" v-model="valid" lazy-validation>
                    <v-row class="mx-auto container">
                        <v-col></v-col>
                        <v-flex justify-center>
                            <p></p>
                            <v-icon color="green" large>mdi-checkbox-marked-circle</v-icon>
                        </v-flex>
                        <v-col cols="12" sm="12" md="12">
                            <p class="text-center my-0">{{ mensaje }}</p>
                        </v-col>
                    </v-row>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-flex justify-center>
                            <v-btn outlined color="blue darken-1" @click="dialogConfirmacion = false"> ACEPTAR
                            </v-btn>
                        </v-flex>
                    </v-card-actions>
                </v-form>
            </v-card>
        </v-dialog>


        <v-dialog v-model="dialog" max-width="600px" persisten>
            <!-- <p class="text-center">Solicitud de cambio de turno de paciente</p> -->
            <!-- <v-flex>
                <center>Solicitud de cambio de turno de paciente</center>
            </v-flex> -->
            <v-card class="mx-auto">
                <!-- <v-icon class="">mdi-close-circle</v-icon> -->
                <v-form ref="form" v-model="valid" lazy-validation>
                    <v-row class="mt-4 mx-auto container">
                        <v-col cols="12" sm="12" md="12">
                            <h3 class="text-center mb-3">Solicitud de cambio de turno de paciente</h3>
                            <!-- <p class="text-center">¿Esta seguro de aceptar la solicitud de cambio del paciente?</p> -->
                            <v-select @change="cambiarValorEstado" :items="['OBSERVADO', 'ATENDIDO']" v-model="estado"
                                label="Estado de Solicitud" outlined></v-select>
                            <v-textarea outlined label="Motivo" v-if="estado == 'OBSERVADO'" v-model="motivo"></v-textarea>
                        </v-col>
                    </v-row>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <!-- <v-row align="center">
                            <v-col class="d-flex" cols="12" sm="6">
                                <v-select :items="['OBSERVADO','ATENDIDO']" label="ESTADI DE SOLICITUD" outlined></v-select>
                            </v-col>
                        </v-row> -->
                        <v-btn color="blue darken-1" @click="dialog = false, limpiarForm()" text>CANCELAR</v-btn>
                        <v-btn color="blue darken-1" @click="cambiarEstado()" text> ACEPTAR </v-btn>
                        <!-- <v-btn color="blue darken-1" @click="cambiarEstado()" v-if="tab == 0" text> OBSERVAR </v-btn> -->
                    </v-card-actions>
                </v-form>
            </v-card>
        </v-dialog>


        <v-container class="my-5">
            <v-card>
                <v-tabs v-model="tab" background-color="#1973a5" @change="cambioTab" center-active dark>
                    <v-tab value="pendientes">PENDIENTES</v-tab>
                    <v-tab value="pendientes">OBSERVADOS</v-tab>
                    <v-tab value="atendidos">ATENDIDOS</v-tab>
                </v-tabs>
            </v-card>
            <v-data-table :headers="headers" :items="desserts" class="elevation-1 my-2">
                <template v-slot:item.url="{ value }" v-if="tab == 0">
                    <v-btn class="secondary" small @click="atender(value)">ATENDER</v-btn>
                </template>
                <template v-slot:item.url="{ value }" v-else-if="tab == 1">
                    <!-- <v-btn class="secondary" small @click="atender(value)">ATENDER</v-btn> -->
                    <v-icon color="red">mdi-close-circle</v-icon>

                </template>
                <template v-slot:item.url v-else-if="tab == 2">
                    <v-icon color="green">mdi-checkbox-marked-circle</v-icon>
                </template>
                <template v-slot:item.datosPaciente="{ value }">
                    {{ value.ape_pat }} {{ value.ape_mat }} {{ value.nombres }}
                </template>
            </v-data-table>
        </v-container>
    </div>
</template>

<style></style>

<script>
export const USUARIO = process.env.VUE_APP_USERNAME;
export const PASSWORD = process.env.VUE_APP_PASSWORD;
export const RUTA_API = process.env.VUE_APP_API;
import axios from "axios";
import * as XLSX from "xlsx";
export default {
    data: () => ({
        actionBoton: "AGREGAR SOLICITUD",
        nombrePaciente: [],
        defaultItem: {
            paciente: "",
            frecuencia: "",
            turno: "",
        },
        dialog: false,
        tab: 0, //0,1,2
        headers: [
            {
                text: "# Documento",
                value: "datosPaciente.num_doc"
            },
            {
                text: "Paciente",
                value: "datosPaciente"
            },
            {
                text: "Tipo de Solicitud",
                value: "tipoSolicitud",
            },
            {
                text: "Nuevo Turno",
                value: "nuevoTurno",
            },
            {
                text: "Clínica",
                value: "datosCas.descripCas",
            },
            {
                text: "Estado",
                value: "respuesta",
            },
            {
                text: "Motivo",
                value: "motivo"
            },
            {
                text: "Fecha Solicitud",
                value: "fechaSolicitud"
            },
            {
                text: "Fecha Atención",
                value: "fechaRespuesta"
            },
            {
                text: "Acciones",
                value: "url",
            },
        ],
        desserts: [],
        dialog: false,
        valid: true,
        rules: {
            required: (value) => !!value || "Campo Obligatorio.",
        },
        itemsDatosPaciente: [],
        itemsTurno: [],
        itemsTipoSolcitud: [],
        nombrePaciente: "",
        idItem: "",
        ///
        estado: "",
        motivo: "",
        dialogConfirmacion: false,
        mensaje: "Estado de solicitud actualizada con exito.",


        dataToExport: [],
    dataToExport2: [],

    }),
    computed: {},
    watch: {},
    methods: {
        cambiarValorEstado() {
            console.log(this.estado)
            this.motivo = ''
        },
        limpiarForm() {
            this.estado = ""
            this.motivo = ""
        },
        cambioTab() {
            this.desserts = []
            if (this.tab == 1) {
                this.listarSolicitudes("OBSERVADO")
                // this.headers.splice(5,0,{ text:'Motivo',value:'motivo' })
            } else if (this.tab == 2) {
                this.listarSolicitudes("ATENDIDO")
                // this.headers.splice(5,1)
            } else if (this.tab == 0) {
                this.listarSolicitudes("PENDIENTE")
                // this.headers.splice(5,1)

                // this.headers.splice()
            }
        },
        cambiarEstado() {
            // let data
            let data = {
                respuesta: this.estado,
                userEdit: this.usuario + "|" + this.nombre,
                fechaRespuesta: new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().substr(0, 10),
                motivo: this.motivo
            }
            axios.post(RUTA_API + "/api/token/", {
                username: USUARIO,
                password: PASSWORD,
            }).then((response) => {
                this.auth = "Bearer " + response.data.access;
                axios.patch(RUTA_API + "/solicitud/" + this.idItem + "/", data, {
                    headers: { Authorization: this.auth },
                }).then((res) => {
                    this.dialog = false
                    console.log("Resultado: ", res.data);
                    this.dialogConfirmacion = true
                    this.mensaje = "Estado de solicitud actualizada con exito."
                    this.desserts = []
                    this.listarSolicitudes("PENDIENTE")



                    this.limpiarForm()

                }).catch((res) => {
                    console.log('Error: ', res.data);
                    this.dialogConfirmacion = true
                    this.mensaje = "Error! Estado de solicitud no ha podido ser actualizado."
                    this.limpiarForm()
                });
            })
        },
        atender(text) {
            this.dialog = true
            this.idItem = text.split("/")[4]
        },
        listarSolicitudes(estado) {
            axios.post(RUTA_API + "/api/token/", {
                username: USUARIO,
                password: PASSWORD,
            }).then((response) => {
                this.auth = "Bearer " + response.data.access;
                axios.get(RUTA_API + "/solicitud/?search=" + estado, {
                    headers: { Authorization: this.auth },
                }).then((res) => {
                    // console.log("Resultado", res.data);
                    this.desserts = res.data;
                }).catch((res) => {
                    console.log('SSSSS', res.data);
                });
            })
        },
    },
    created() {
        this.listarSolicitudes("PENDIENTE")
        this.perfil = sessionStorage.getItem("perfil");
        this.nombre = sessionStorage.getItem("nombre");
        this.url = sessionStorage.getItem("url");
        this.usuario = sessionStorage.getItem("usuario");
        this.urlCas = sessionStorage.getItem("urlCas");
        console.log("Url", this.url);
        console.log("Perfil", this.perfil);
        console.log("Nombre", this.nombre);
        console.log("cas", this.urlCas);
    }
}

</script>