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
      v-model="dialogNoEdit"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡No se puede editar, Paciente ya no esta en lista de espera!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogNoEdit = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-card class="mx-auto my-5" max-width="1600">
        <v-system-bar color="#1973a5" dark>
          GESION DE CUPOS - LISTA DE ESPERA
        </v-system-bar>
        <v-row class="start ml-10">
          <v-col cols="12" md="4">
            <v-text-field
              class="mx-auto mt-8"
              v-model="setDni"
              label="BUSCAR"
              required
              :maxlength="maxdat"
              @keyup.enter="buscar"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5" @click="buscar">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5" @click="exportExcel">
              Generar Excel<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>
          </v-col>
          <!--<v-btn class="mt-10" icon color="#1973a5" @click="generatePDF">
              Generar PDF<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>-->
        </v-row>
      </v-card>

      <v-card class="mx-auto my-5" max-width="1600">
        <v-tabs background-color="#1973a5" center-active dark>
          <v-tab @click="listaEsperaInit">Pendientes</v-tab>
          <v-tab @click="listaEsperaAsig">Asignados</v-tab>
        </v-tabs>
      </v-card>

      <v-card class="mx-auto my-5" max-width="1600">
        <v-data-table :headers="headers" :items="desserts" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <!--Registrar-->
              <v-dialog v-model="dialog" max-width="1000px">
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
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="6">
                            <v-menu
                              ref="menu3"
                              v-model="menu3"
                              :rules="[rules.required, rules.counter]"
                              :close-on-content-click="false"
                              transition="scale-transition"
                              offset-y
                              max-width="290px"
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.fechaSolicitud"
                                  label="Fecha de Solicitud"
                                  hint="YYYY/MM/DD formato"
                                  persistent-hint
                                  prepend-icon="mdi-calendar"
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.fechaSolicitud"
                                no-title
                                @input="menu3 = false"
                              ></v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="6">
                            <v-text-field
                              v-model="editedItem.fechaSolicitud"
                              label="Fecha de Solicitud"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.dni"
                              :rules="[rules.required, rules.counter]"
                              label="DNI"
                              :maxlength="maxdat"
                              @keyup.enter="buscarNombrePac"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="6">
                            <v-text-field
                              v-model="editedItem.dni"
                              label="DNI"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="2">
                            <v-btn
                              class="mt-5"
                              icon
                              color="#1973a5"
                              @click="buscarNombrePac"
                            >
                              <v-icon>mdi-magnify</v-icon>
                            </v-btn>
                          </v-col>
                          <v-col
                            v-if="validDni == true"
                            cols="12"
                            sm="12"
                            md="12"
                          >
                            <v-alert type="error">
                              DNI NO ENCONTRADO, REVISAR
                            </v-alert>
                          </v-col>
                          <v-col
                            v-if="perfil == 8 || perfil == 9"
                            cols="12"
                            sm="6"
                            md="6"
                          >
                            <v-text-field
                              v-model="editedItem.nombrePaciente"
                              :rules="[rules.required, rules.counter]"
                              label="nombre Paciente"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefono"
                              :rules="[rules.required, rules.counter]"
                              label="Telefono"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefono"
                              label="Telefono"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefonoDos"
                              label="Telefono 2"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefonoDos"
                              label="Telefono 2"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.casOrigen"
                              label="Ipress de Origen"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.casOrigen"
                              label="Ipress de Origen"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.casDestino"
                              :maxlength="90"
                              :items="itemsClinicas"
                              dense
                              label="Lugar de Destino"
                            ></v-autocomplete>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.casDestino"
                              label="Lugar de Destino"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="6">
                            <v-autocomplete
                              v-model="editedItem.distrito"
                              :items="itemsDistrito"
                              dense
                              label="Distrito"
                              :maxlength="90"
                            ></v-autocomplete>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="6">
                            <v-text-field
                              v-model="editedItem.distrito"
                              label="Distrito"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.turno"
                              :items="itemsTurno"
                              label="Turno"
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.turno"
                              label="Turno"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.referencia"
                              :rules="[rules.required, rules.counter]"
                              label="Referencia"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.referencia"
                              label="Referencia"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.observaciones"
                              label="Observaciones"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.observaciones"
                              label="Observaciones"
                              :maxlength="100"
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
              <v-dialog v-model="dialogEdit" max-width="1000px">
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-title>
                      <span class="text-h5">Editar Lista de Espera</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="6">
                            <v-menu
                              ref="menu3"
                              v-model="menu3"
                              :rules="[rules.required, rules.counter]"
                              :close-on-content-click="false"
                              transition="scale-transition"
                              offset-y
                              max-width="290px"
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.fechaSolicitud"
                                  label="Fecha de Solicitud"
                                  hint="YYYY/MM/DD formato"
                                  persistent-hint
                                  prepend-icon="mdi-calendar"
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.fechaSolicitud"
                                no-title
                                @input="menu3 = false"
                              ></v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="6">
                            <v-text-field
                              v-model="editedItem.fechaSolicitud"
                              label="Fecha de Solicitud"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.dni"
                              :rules="[rules.required, rules.counter]"
                              label="DNI"
                              :maxlength="maxdat"
                              @keyup.enter="buscarNombrePac"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="6">
                            <v-text-field
                              v-model="editedItem.dni"
                              label="DNI"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="2">
                            <v-btn
                              class="mt-5"
                              icon
                              color="#1973a5"
                              @click="buscarNombrePac"
                            >
                              <v-icon>mdi-magnify</v-icon>
                            </v-btn>
                          </v-col>
                          <v-col
                            v-if="perfil == 8 || perfil == 9"
                            cols="12"
                            sm="6"
                            md="6"
                          >
                            <v-text-field
                              v-model="editedItem.nombrePaciente"
                              :rules="[rules.required, rules.counter]"
                              label="nombre Paciente"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefono"
                              :rules="[rules.required, rules.counter]"
                              label="Telefono"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefono"
                              label="Telefono"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefonoDos"
                              label="Telefono 2"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="3" md="3">
                            <v-text-field
                              v-model="editedItem.telefonoDos"
                              label="Telefono 2"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.casOrigen"
                              label="Ipress de Origen"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.casOrigen"
                              label="Ipress de Origen"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-autocomplete
                              v-model="editedItem.casDestino"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsClinicas"
                              dense
                              label="Lugar de Destino"
                            ></v-autocomplete>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.casDestino"
                              label="Lugar de Destino"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="6">
                            <v-autocomplete
                              v-model="editedItem.distrito"
                              :rules="[rules.required, rules.counter]"
                              :items="itemsDistrito"
                              dense
                              label="Distrito"
                            ></v-autocomplete>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="6">
                            <v-text-field
                              v-model="editedItem.distrito"
                              label="Distrito"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.turno"
                              :items="itemsTurno"
                              label="Turno"
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.turno"
                              label="Turno"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.referencia"
                              :rules="[rules.required, rules.counter]"
                              label="Referencia"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.referencia"
                              label="Referencia"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 8" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.observaciones"
                              label="Observaciones"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 9" cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.observaciones"
                              label="Observaciones"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeEdit">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="edit">
                        Editar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="terminar">
                        Terminar
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

import CalendarioAnemia from "./CalendarioAnemia.vue";
import jsPDF from "jspdf";
import "jspdf-autotable";
import * as XLSX from "xlsx";

export default {
  data: () => ({
    //perfil data
    perfil: "",
    nombre: "",
    url: "",
    usuario: "",
    //EXPORT PDF
    dataPdfExport: [],
    dataToExport: [],
    heading: "REPORTE PACIENTES NUTRICIÓN",
    items: [
      { title: "Item 1", body: "I am item 1 body text" },
      { title: "Item 2", body: "I am item 2 body text" },
      { title: "Item 3", body: "I am item 3 body text" },
      { title: "Item 4", body: "I am item 4 body text" },
    ],
    parValores: [],
    //
    dialogDataApi: false,
    dialog: false,
    itemsFrecuencia: ["L-M-V", "M-J-S"],
    itemsVgs: ["A", "B", "C"],
    itemsTurno: ["1er Turno", "2do Turno", "3er Turno", "4to Turno"],
    itemsDiagNut: [
      "Obesidad",
      "Sobrepeso",
      "Normal",
      "Desnutrición Leve",
      "Desnutrición Moderada",
      "Desnutrición Severa",
    ],
    itemsInterNut: [
      "Evaluación y Orientación Nutricional",
      "Seguimiento Nutricional",
      "Monitoreo y Orientación Nutricional",
    ],
    nuevoValid: false,
    datosPresHis: [],
    datosEdit: "",
    dialogEditExclu: false,
    dataAdmin: "",
    datosPaciente: [],
    setDni: "",
    adminForm: 0,
    maxdat: 21,
    valid: true,
    validDni: false,
    medicamentos: ["ERITROPOYETINA", "HIERRO"],
    via: ["SC", "EV"],
    dosisE: [1000, 2000, 3000, 4000, 5000, 6000],
    dosisH: [100, 200, 300, 400, 500, 600, 700, 800],
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    itemsClinicas: [],
    itemsDistrito: [
      "Ancón",
      "Ate Vitarte",
      "Ancón",
      "Barranco",
      "Breña",
      "Carabayllo",
      "Chaclacayo",
      "Chorrillos",
      "Cieneguilla",
      "Comas",
      "El Agustino",
      "Independencia",
      "Jesús María",
      "La Molina",
      "La Victoria",
      "Lima",
      "Lince",
      "Los Olivos",
      "Lurigancho",
      "Lurín",
      "Magdalena del Mar",
      "Miraflores",
      "Pachacamac",
      "Pucusana",
      "Pueblo Libre",
      "Puente Piedra",
      "Punta Hermosa",
      "Punta Negra",
      "Rímac",
      "San Bartolo",
      "San Borja",
      "San Isidro",
      "San Juan de Lurigancho",
      "San Juan de Miraflores",
      "San Luis",
      "San Martín de Porres",
      "San Miguel",
      "Santa Anita",
      "Santa María del Mar",
      "Santa Rosa",
      "Santiago de Surco",
      "Surquillo",
      "Villa El Salvador",
      "Villa María del Triunfo",
      "Callao",
      "Bellavista",
      "Carmen Legua-Reynoso",
      "La Perla",
      "La Punta",
      "Ventanilla",
      "Mi Perú",
      "Cañete",
    ],
    clinicasCarga: null,
    editedItem: {
      //data para Lista de Espera
      fechaSolicitud: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      dni: "",
      nombrePaciente: "",
      urlPaciente: "",
      telefono: "",
      telefonoDos: "",
      casOrigen: "",
      casDestino: "",
      distrito: "",
      referencia: "",
      observaciones: "",
      estado: null,
      dateIngreso: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      dateEvalu: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      frecuencia: "",
      turno: "",
      peso: Number,
      talla: Number,
      imc: 0.0,
      circuBra: Number,
      cmb: Number,
      medCali: Number,
      ept: Number,
      albSerica: Number,
      vgs: "",
      ingestaCalorica: Number,
      ingestaProteica: Number,
      ingestaCaloricaT: Number,
      ingestaProteicaT: Number,
      diagNut: "",
      interNut: "",
    },
    minimo: new Date(
      Date.now() - 432000000 - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .substr(0, 10),
    maximo: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),

    dialogEdit: false,
    formAdmi: false,
    dialogDelete: false,
    dialogEditAdm: false,
    dialogNoEdit: false,
    vista: "",
    actionBoton: "AGREGAR LISTA DE ESPERA",
    headers: [],
    desserts: [],
    editedIndex: -1,
    dataex: "",
    defaultItem: {
      fechaSolicitud: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      dni: "",
      nombrePaciente: "",
      urlPaciente: "",
      telefono: "",
      telefonoDos: "",
      casOrigen: "",
      casDestino: "",
      distrito: "",
      referencia: "",
      observaciones: "",
      estado: null,
      dateIngreso: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      dateEvalu: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      frecuencia: "",
      turno: "",
      peso: Number,
      talla: Number,
      imc: 0.0,
      circuBra: Number,
      cmb: Number,
      medCali: Number,
      ept: Number,
      albSerica: Number,
      vgs: "",
      ingestaCalorica: Number,
      ingestaProteica: Number,
      ingestaCaloricaT: Number,
      ingestaProteicaT: Number,
      diagNut: "",
      interNut: "",
    },
    menu3: false,
    menu2: false,
    menu4: false,
    menu5: false,
    menu6: false,
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
    exportExcel() {
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
            .get(RUTA_API + "/listaEspera/?search=false", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              for (let i = 0; i < res.data.length; i++) {
                //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
                this.dataToExport.push(
                  Object.assign(
                    { contador: i + 1 },
                    { fechaSolicitada: res.data[i].fechaSoli },
                    { Dni: res.data[i].datosPaciente.num_doc },
                    { EdadAños: res.data[i].datosPaciente.edad[0] },
                    { EdadMeses: res.data[i].datosPaciente.edad[1] },
                    { EdadDias: res.data[i].datosPaciente.edad[2] },
                    { apePat: res.data[i].datosPaciente.ape_pat },
                    { ape_mat: res.data[i].datosPaciente.ape_mat },
                    { nombres: res.data[i].datosPaciente.nombres },
                    { Dirección: res.data[i].datosPaciente.direccion },
                    { Distrito: res.data[i].datosPaciente.distrito },
                    { Telefono: res.data[i].telefono },
                    { TelefonoDos: res.data[i].telefonoDos },
                    { Origen: res.data[i].casOrigen },
                    { ClinicaSolicitada: res.data[i].casDestino },
                    { DistritoSolicitado: res.data[i].distrito },
                    { Turno: res.data[i].turno },
                    { Referencia: res.data[i].referencia },
                    { Observaciones: res.data[i].observaciones },
                    { Estado: res.data[i].estado }
                  )
                );
              }

              //this.dataToExport = res.data;
              let data = XLSX.utils.json_to_sheet(this.dataToExport);
              const workbook = XLSX.utils.book_new();
              const filename = "Lista de Espera";
              XLSX.utils.book_append_sheet(workbook, data, filename);
              XLSX.writeFile(workbook, `${filename}.xlsx`);
              this.dialogDataApi = false;
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

    buscarNombrePac() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/asigCuposPac/?search=" + this.editedItem.dni, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("RESPUESTA", res.data);
              if (res.data.length == 0) {
                this.editedItem.casOrigen = "HOSPITAL DE ORIGEN";
                axios
                  .get(RUTA_API + "/paciente/?search=" + this.editedItem.dni, {
                    headers: { Authorization: this.auth },
                  })
                  .then((resPac) => {
                    console.log("RESPUESTA", resPac.data);
                    this.editedItem.nombrePaciente =
                      resPac.data[0].ape_pat +
                      " " +
                      resPac.data[0].ape_mat +
                      " " +
                      resPac.data[0].nombres;
                    this.editedItem.casOrigen =
                      resPac.data[0].datosCasOri.descripCas;
                    this.editedItem.urlPaciente = resPac.data[0].url;
                    this.dialogDataApi = false;
                    this.validDni = false;
                  })
                  .catch((res) => {
                    console.warn("Error:", res);
                    this.validDni = true;
                  });
              } else {
                this.editedItem.nombrePaciente =
                  res.data[0].datosPaciente.ape_pat +
                  " " +
                  res.data[0].datosPaciente.ape_mat +
                  " " +
                  res.data[0].datosPaciente.nombres;
                this.editedItem.urlPaciente = res.data[0].datosPaciente.url;
                this.dialogDataApi = false;
                this.validDni = false;
                this.editedItem.casOrigen =
                  res.data[0].datosPueto.datosCas.descripCas;
              }
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.validDni = true;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },

    listarClinica() {
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
              console.log("clinicas", res.data);
              for (let i = 0; i < res.data.length; i++) {
                this.itemsClinicas.push(res.data[i].descripCas);
              }
            })
            .catch((res) => {
              console.warn("Error:", res.statusText);
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },
    calculoIMC() {
      this.editedItem.imc =
        this.editedItem.peso / (this.editedItem.talla * this.editedItem.talla);
    },
    generatePDF() {
      for (let i = 0; i < this.desserts.length; i++) {
        this.dataPdfExport.push(
          Object.assign(
            {
              datapacfull:
                this.desserts[i].datosPaciente.ape_pat +
                " " +
                this.desserts[i].datosPaciente.ape_mat +
                " " +
                this.desserts[i].datosPaciente.nombres,
            },
            this.desserts[i]
          )
        );
      }

      console.log("dataPdfExport", this.dataPdfExport);
      const columns = [
        { title: "Paciente", dataKey: "datapacfull" },
        { title: "diagNutricional", dataKey: "diagNutricional" },
        { title: "ValGlobalSub", dataKey: "ValGlobalSub" },
        { title: "albSerica", dataKey: "albSerica" },
        { title: "fechaEvaluacion", dataKey: "fechaEvaluacion" },
        { title: "fechaIngreso", dataKey: "fechaIngreso" },
        { title: "frecuencia", dataKey: "frecuencia" },
        { title: "imc", dataKey: "imc" },
        { title: "ingestaCalorica", dataKey: "ingestaCalorica" },
        { title: "ingestaProteica", dataKey: "ingestaProteica" },
        { title: "interveNutricional", dataKey: "interveNutricional" },
        { title: "peso", dataKey: "peso" },
        { title: "porcentajeCMB", dataKey: "porcentajeCMB" },
        { title: "porcentajeEPT", dataKey: "porcentajeEPT" },
        { title: "talla", dataKey: "talla" },
        { title: "turno", dataKey: "turno" },
      ];
      const doc = new jsPDF({
        orientation: "landscape",
        unit: "in",
        format: "letter",
      });
      // text is placed using x, y coordinates
      doc.setFontSize(16).text(this.heading, 0.5, 1.0);
      // create a line under heading
      doc.setLineWidth(0.01).line(0.5, 1.1, 8.0, 1.1);
      // Using autoTable plugin
      doc.autoTable({
        columns,
        body: this.dataPdfExport,
        margin: { left: 0.5, top: 1.25 },
        styles: { fontSize: 5 },
      });
      // Using array of sentences
      /*doc
        .setFont("helvetica")
        .setFontSize(12)
        .text(this.desserts, 0.5, 3.5, { align: "left", maxWidth: "7.5" });
      */
      // Creating footer and saving file
      doc
        .setFont("times")
        .setFontSize(11)
        //.setFontStyle("italic")
        .setTextColor(0, 0, 255)
        .text(
          "Este reporte debe ser firmado y entregado, siguiendo el flujo normal",
          0.5,
          doc.internal.pageSize.height - 0.5
        );
      doc.save(`${this.heading}.pdf`);
      console.log(this.desserts[0].datosPaciente.nombres, "aqui tas");
    },

    initialize() {
      this.desserts = [];
    },

    buscar() {
      this.desserts = this.desserts.filter(
        (e) =>
          e.datosPaciente.nombres
            .toUpperCase()
            .includes(this.setDni.toUpperCase()) ||
          e.datosPaciente.num_doc
            .toUpperCase()
            .includes(this.setDni.toUpperCase()) ||
          e.datosPaciente.ape_pat
            .toUpperCase()
            .includes(this.setDni.toUpperCase()) ||
          e.datosPaciente.ape_mat
            .toUpperCase()
            .includes(this.setDni.toUpperCase())
      );
    },

    cabezeraNut() {
      this.headers = [
        { text: "Turno", value: "turno" },
        {
          text: "Frecuencia",
          align: "start",
          sortable: false,
          value: "frecuencia",
        },
        { text: "Fecha Ingreso", value: "fechaIngreso" },
        { text: "Fecha Evaluacion", value: "fechaEvaluacion" },
        { text: "Peso", value: "peso" },
        { text: "Talla", value: "talla" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    editItem(item) {
      console.log("item", item);

      this.editedItem.fechaSolicitud = item.fechaSoli;
      this.editedItem.dni = item.datosPaciente.num_doc;
      this.editedItem.urlPaciente = item.datosPaciente.url;
      this.editedItem.nombrePaciente =
        item.datosPaciente.nombres +
        " " +
        item.datosPaciente.ape_pat +
        " " +
        item.datosPaciente.ape_mat;
      this.editedItem.urlPaciente = item.datosPaciente.url;
      this.editedItem.telefono = item.telefono;
      this.editedItem.telefonoDos = item.telefonoDos;
      this.editedItem.casOrigen = item.casOrigen;
      this.editedItem.casDestino = item.casDestino;
      this.editedItem.distrito = item.distrito;
      this.editedItem.turno = item.turno;
      this.editedItem.referencia = item.referencia;
      this.editedItem.observaciones = item.observaciones;
      this.datosEdit = item.url;
      //this.editedItem.estado = item.estado;
      if (item.estado == false) {
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

    deleteItemConfirm() {
      console.log("data pa eliminar", this.editedItem);
      if (this.editedItem.usuario == this.url) {
        console.log("hola");
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .delete(
                RUTA_API + "/nutricion/" + this.editedItem.url.split("/")[4],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("se elimino");
                this.dialogDelete = false;
                this.nut();
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
      } else {
        console.log("no da pe");
        this.dialogDelete = false;
        this.dialogAvisoEliminar = true;
      }
      //this.desserts.splice(this.editedIndex, 1);

      //this.closeDelete();
    },

    closeFormAdmin() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    terminar() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_API + "/listaEspera/" + this.datosEdit.split("/")[4] + "/",
              {
                estado: true,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.dialogDataApi = true;
              console.log("exito", res.status);
              this.close();
              this.listaEsperaInit();
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

    edit() {
      console.log("esto es para editar", this.editedItem);
      //if (this.editedItem.usuario == this.url) {

      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_API + "/listaEspera/" + this.datosEdit.split("/")[4] + "/",
              {
                fechaSoli: this.editedItem.fechaSolicitud,
                paciente: this.editedItem.urlPaciente,
                telefono: this.editedItem.telefono,
                telefonoDos: this.editItem.telefonoDos,
                casOrigen: this.editedItem.casOrigen,
                casDestino: this.editedItem.casDestino,
                distrito: this.editedItem.distrito,
                turno: this.editedItem.turno,
                referencia: this.editedItem.referencia,
                observaciones: this.editedItem.observaciones,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.dialogDataApi = true;
              console.log("exito", res.status);
              this.close();
              this.listaEsperaInit();
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
      /*} else {
        this.dialogEdit = false;
        this.dialogAvisoEditar = true;
      }*/
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
        !this.editedItem.fechaSolicitud ||
        !this.editedItem.dni ||
        !this.editedItem.nombrePaciente ||
        !this.editedItem.telefono ||
        !this.editedItem.casOrigen ||
        !this.editedItem.casDestino ||
        !this.editedItem.distrito
        //!this.editedItem.ept ||
        //!this.editedItem.turno ||
        //!this.editedItem.vgs ||
        //!this.editedItem.referencia
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
                RUTA_API + "/listaEspera/",
                {
                  fechaSoli: this.editedItem.fechaSolicitud,
                  paciente: this.editedItem.urlPaciente,
                  telefono: this.editedItem.telefono,
                  telefonoDos: this.editedItem.telefonoDos,
                  casOrigen: this.editedItem.casOrigen,
                  casDestino: this.editedItem.casDestino,
                  distrito: this.editedItem.distrito,
                  turno: this.editedItem.turno,
                  referencia: this.editedItem.referencia,
                  observaciones: this.editedItem.observaciones,
                  estado: false,
                  user_reg: this.usuario + "|" + this.nombre,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                console.log(this.editedItem);
                this.listaEsperaInit();
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

    nut() {
      //this.adminForm = "0";
      //this.vista = "Prescipción Anemia";
      this.cabezeraNut();
      //this.actionBoton = "Registro Prescripción";
      this.dialogDataApi = true;

      axios
        .post(RUTA_API + "/APICNSR/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_API +
                "/nutricion/?search=" +
                this.datosPaciente[0].url.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.desserts = res.data;
              this.dialogDataApi = false;
              //this.dataAdmi = res.data[0].url.split("/")[4];
              //this.datosPresHis = res.data[0];
              console.log("desert", res.data);
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
    nutricion() {},

    cabezeraListaEspera() {
      this.headers = [
        { text: "Fecha Soli", value: "fechaSoli" },
        {
          text: "Dni",
          align: "start",
          sortable: false,
          value: "datosPaciente.num_doc",
        },
        { text: "Apellido Pat", value: "datosPaciente.ape_pat" },
        { text: "Apellido Mat", value: "datosPaciente.ape_mat" },
        { text: "Nombre", value: "datosPaciente.nombres" },
        { text: "Telefono", value: "telefono" },
        { text: "Telefono 2", value: "telefonoDos" },
        { text: "Origen", value: "casOrigen" },
        { text: "Clinica Solicitada", value: "casDestino" },
        { text: "Distrito Solicitado", value: "distrito" },
        { text: "Turno", value: "turno" },
        { text: "Referencia", value: "referencia" },
        { text: "Observaciones", value: "observaciones" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    listaEsperaInit() {
      this.cabezeraListaEspera();
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/listaEspera/?search=false", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.desserts = res.data;
              this.dialogDataApi = false;
              //this.dataAdmi = res.data[0].url.split("/")[4];
              //this.datosPresHis = res.data[0];
              console.log("desert", res.data);
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
    listaEsperaAsig() {
      this.cabezeraListaEspera();
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: USUARIO,
          password: PASSWORD,
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/listaEspera/?search=true", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.desserts = res.data;
              this.dialogDataApi = false;
              //this.dataAdmi = res.data[0].url.split("/")[4];
              //this.datosPresHis = res.data[0];
              console.log("desert", res.data);
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
    //INICIO DE CONSULTA

    this.listaEsperaInit();
    this.listarClinica();
  },

  components: {
    CalendarioAnemia,
  },
};
</script>


