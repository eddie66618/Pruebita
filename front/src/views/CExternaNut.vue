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
      v-model="dialogAviso"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡Paciente no se encuentra registrado!, ponerse en contacto con el
            admistrador de sistema Telf: 988 578 051 o ingresar al siguiente
            enlace:
            <a href="https://wa.me/message/3NEVQVLLDQV3O1" target="_blank"
              >Envía un mensaje a Centro Nacional De Salud Renal - DSI por
              WhatsApp.</a
            >
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAviso = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAvisoNULL"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡NO PUEDE ESTAR EL CAMPO DOCUMENTO DE INDENTIDAD VACIO!
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAvisoNULL = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogError"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">¡Lo siento, se cometio un error!</div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogError = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAvisoEliminar"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡Solo puede ser eliminado por la persona que resgistro¡.
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAvisoEliminar = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      transition="dialog-bottom-transition"
      max-width="600"
      v-model="dialogAvisoEditar"
    >
      <v-card>
        <v-toolbar color="#1973a5" dark>¡Aviso Importante!</v-toolbar>
        <v-card-text>
          <div class="text-h4 pa-5">
            ¡Solo puede ser editado por la persona que resgistro!.
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAvisoEditar = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-card class="mx-auto my-5" max-width="900">
        <v-system-bar color="#1973a5" dark>
          DATOS DE PACIENTE - CONTROL NUTRICIONAL CLINICAS CONTRATADOS
        </v-system-bar>
        <v-row class="start ml-10">
          <v-col cols="12" md="4">
            <v-text-field
              class="mx-auto mt-8"
              v-model="setDni"
              label="Número de Documento"
              required
              :maxlength="10"
              @keyup.enter="buscarPacicente"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5" @click="buscarPacicente">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
          <v-col v-if="desserts.length != 0" cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5" @click="generatePDF">
              Generar PDF<v-icon>mdi-arrow-down-bold-box</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <!--
          <v-row justify="center">
            <v-col cols="12" md="3">
              <v-text-field label="Apellido Paterno" required></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field label="Apellido Materno" required></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field label="Nombres" required></v-text-field>
            </v-col>
            <v-col cols="12" md="1">
              <v-btn class="mt-3" icon color="#1973a5">
                <v-icon>mdi-magnify</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          -->
      </v-card>

      <v-card
        class="mx-auto my-5"
        max-width="900"
        v-if="datosPaciente.length != 0"
      >
        <v-tabs background-color="#1973a5" center-active dark>
          <v-tab @click="nutricion">Nutrición</v-tab>
        </v-tabs>
      </v-card>

      <v-card
        class="mx-auto my-5"
        max-width="900"
        v-if="datosPaciente.length != 0"
      >
        <v-data-table :headers="headers" :items="desserts" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title v-if="datosPaciente.length != 0">
                {{
                  datosPaciente[0].nombres +
                  " " +
                  datosPaciente[0].ape_pat +
                  " " +
                  datosPaciente[0].ape_mat
                }}
                | {{ vista }}</v-toolbar-title
              >
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <!--Registrar-->
              <v-dialog v-model="dialog" max-width="700px">
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
                    <v-card-title>
                      <!--<div cols="12" sm="6" md="6" class="">
                        <v-checkbox v-model="nuevoValid"></v-checkbox>
                      </div>
                      <span>Click si el paciente es nuevo</span>-->
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu3"
                              v-model="menu3"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateIngreso"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateIngreso"
                                  label="Fecha de Ingreso"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateIngreso"
                                no-title
                                scrollable
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu3 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu3.save(editedItem.dateIngreso)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu4"
                              v-model="menu4"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateEvalu"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateEvalu"
                                  label="Fecha de Evaluacion Nutricional"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateEvalu"
                                no-title
                                scrollable
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu4 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu4.save(editedItem.dateEvalu)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.frecuencia"
                              :items="itemsFrecuencia"
                              label="Frecuencia"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.turno"
                              :items="itemsTurno"
                              label="Turno"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-select
                              v-model="editedItem.tipoPaciente"
                              :items="itemsTipoPaciente"
                              :rules="[rules.required]"
                              label="Tipo Paciente"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.peso"
                              :rules="[rules.required]"
                              label="Peso (Kilogramos)"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.talla"
                              :rules="[rules.required]"
                              label="Talla (Metros)"
                              :maxlength="15"
                              type="number"
                              @keyup.enter="calculoIMC"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.circuBra"
                              :rules="[rules.required]"
                              label="Circunferencia Braquial"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.medCali"
                              label="Pliege Tricipital"
                              :rules="[rules.required]"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.albSerica"
                              :rules="[rules.required]"
                              label="ALB Sérica"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.vgs"
                              label="MIS"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ingestaCaloricaT"
                              :rules="[rules.required]"
                              label="Ingesta Calorica Total"
                              :maxlength="40"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ingestaProteicaT"
                              :rules="[rules.required]"
                              label="Ingesta Proteica Total"
                              :maxlength="40"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.diagNut"
                              label="Diagnostico Nutricional"
                              :items="itemsDiagNut"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.interNut"
                              :items="itemsInterNut"
                              label="Intervención Nutricional"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.obsNutricion"
                              label="Observacion Nutricional"
                              :maxlength="100"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12"
                            ><v-divider inset></v-divider
                          ></v-col>
                          <v-col cols="12" sm="4" md="3"
                            >Edad: {{ parValores[0].edad }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >Sexo: {{ parValores[0].sexo }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >CB: {{ parValores[0].cb }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >CMB: {{ parValores[0].cmb }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >PT: {{ parValores[0].pt }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >IMC:
                            {{(
                    editedItem.peso /
                    (editedItem.talla * editedItem.talla)
                  ).toFixed(2),}}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >%CMB:
                            {{(
                    ((editedItem.circuBra -
                      3.14 * (editedItem.medCali / 10)) /
                      parValores[0].cmb) *
                    100
                  ).toFixed(2),}}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >%EPT:
                            {{(
                    (editedItem.medCali * 100) /
                    parValores[0].pt
                  ).toFixed(2),}}</v-col
                          >
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
              <v-dialog v-model="dialogEdit" max-width="700px">
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-title>
                      <span class="text-h5">Editar Nutrición</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu5"
                              v-model="menu5"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateIngreso"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateIngreso"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateIngreso"
                                no-title
                                scrollable
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu5 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu5.save(editedItem.dateIngreso)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu6"
                              v-model="menu6"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateEvalu"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateEvalu"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateEvalu"
                                no-title
                                scrollable
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu6 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu6.save(editedItem.dateEvalu)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.frecuencia"
                              :items="itemsFrecuencia"
                              :rules="[rules.required]"
                              label="Frecuencia"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.turno"
                              :items="itemsTurno"
                              :rules="[rules.required]"
                              label="Turno"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-select
                              v-model="editedItem.tipoPaciente"
                              :items="itemsTipoPaciente"
                              :rules="[rules.required]"
                              label="Tipo Paciente"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.peso"
                              :rules="[rules.required]"
                              label="Peso (Kilogramos)"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.talla"
                              :rules="[rules.required]"
                              label="Talla (Metros)"
                              :maxlength="15"
                              type="number"
                              @keyup.enter="calculoIMC"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.circuBra"
                              :rules="[rules.required]"
                              label="Circunferencia Braquial"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.medCali"
                              label="Pliege Tricipital"
                              :rules="[rules.required]"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.albSerica"
                              :rules="[rules.required]"
                              label="ALB Sérica"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.vgs"
                              :rules="[rules.required]"
                              label="MIS"
                              :maxlength="15"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ingestaCaloricaT"
                              :rules="[rules.required]"
                              label="Ingesta Calorica Total"
                              :maxlength="40"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ingestaProteicaT"
                              :rules="[rules.required]"
                              label="Ingesta Proteica Total"
                              :maxlength="40"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.diagNut"
                              :rules="[rules.required]"
                              label="Diagnostico Nutricional"
                              :items="itemsDiagNut"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.interNut"
                              :items="itemsInterNut"
                              :rules="[rules.required]"
                              label="Intervención Nutricional"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.obsNutricion"
                              label="Observacion Nutricional"
                              :maxlength="100"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="4" md="3"
                            >Edad: {{ parValores[0].edad }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >Sexo: {{ parValores[0].sexo }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >CB: {{ parValores[0].cb }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >CMB: {{ parValores[0].cmb }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >PT: {{ parValores[0].pt }}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >%IMC:
                            {{(
                    editedItem.peso /
                    (editedItem.talla * editedItem.talla)
                  ).toFixed(2),}}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >%CMB:
                            {{(
                    ((editedItem.circuBra -
                      3.14 * (editedItem.medCali / 10)) /
                      parValores[0].cmb) *
                    100
                  ).toFixed(2),}}</v-col
                          >
                          <v-col cols="12" sm="4" md="3"
                            >%EPT:
                            {{(
                    (editedItem.medCali * 100) /
                    parValores[0].pt
                  ).toFixed(2),}}</v-col
                          >
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
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
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

export default {
  data: () => ({
    //perfil data
    perfil: "",
    nombre: "",
    url: "",
    //EXPORT PDF
    dataPdfExport: [],
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
    dialogAviso: false,
    dialogAvisoEliminar: false,
    dialogAvisoEditar: false,
    dialogAvisoNULL: false,
    dialogError: false,
    dialog: false,
    itemsFrecuencia: ["L-M-V", "M-J-S"],
    itemsTurno: ["1er Turno", "2do Turno", "3er Turno", "4to Turno"],
    itemsTipoPaciente: [
      "CASO PROBLEMA",
      "PACIENTE NUEVO",
      "PACIENTE CONTINUADOR",
    ],
    itemsDiagNut: [
      "Obesidad",
      "Sobrepeso",
      "Normal",
      "Desnutrición Leve",
      "Desnutrición Moderada",
      "Desnutrición Severa",
    ],
    /*itemsInterNut: [
      "Evaluación y Orientación Nutricional - NUEVO",
      "Seguimiento Nutricional - NORMAL/SOBRESO/OBESIDAD",
      "Monitoreo y Orientación Nutricional- DESNUTRICION LEVE/MODERADO/SEVERO",
    ],*/
    itemsInterNut: [
      "Evaluación y Orientación Nutricional",
      "Seguimiento Nutricional",
      "Monitoreo y Orientación Nutricional",
    ],
    nuevoValid: true,
    datosPresHis: [],
    datosEdit: "",
    dialogEditExclu: false,
    dataAdmin: "",
    datosPaciente: [],
    setDni: "",
    adminForm: 0,
    maxdat: 21,
    valid: true,
    medicamentos: ["ERITROPOYETINA", "HIERRO"],
    via: ["SC", "EV"],
    dosisE: [1000, 2000, 3000, 4000, 5000, 6000],
    dosisH: [100, 200, 300, 400, 500, 600, 700, 800],
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    editedItem: {
      dateIngreso: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      dateEvalu: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      frecuencia: "",
      turno: "",
      tipoPaciente: "",
      peso: Number,
      talla: Number,
      imc: 0.0,
      circuBra: Number,
      cmb: Number,
      medCali: Number,
      ept: Number,
      albSerica: Number,
      vgs: "NA",
      ingestaCalorica: Number,
      ingestaProteica: Number,
      ingestaCaloricaT: Number,
      ingestaProteicaT: Number,
      diagNut: "",
      interNut: "",
      obsNutricion: "",
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
    vista: "",
    actionBoton: "AGREGAR NUTRICIÓN",
    headers: [],
    desserts: [],
    editedIndex: -1,
    dataex: "",
    defaultItem: {
      dateIngreso: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      dateEvalu: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      frecuencia: "",
      turno: "",
      tipoPaciente: "",
      peso: Number,
      talla: Number,
      imc: 0.0,
      circuBra: Number,
      cmb: Number,
      medCali: Number,
      ept: Number,
      albSerica: Number,
      vgs: "NA",
      ingestaCalorica: Number,
      ingestaProteica: Number,
      ingestaCaloricaT: Number,
      ingestaProteicaT: Number,
      diagNut: "",
      interNut: "",
      obsNutricion: "",
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

  created() {
    //this.initialize()
    //this.actionBoton='pres'
  },

  methods: {
    calculoIMC() {
      this.editedItem.imc =
        this.editedItem.peso / (this.editedItem.talla * this.editedItem.talla);
    },
    generatePDF() {
      console.log("datos deseert elemt", this.desserts);
      for (let i = 0; i < this.desserts.length; i++) {
        //this.dataPdfExport.push(this.desserts[i].datosPaciente.nombres,this.desserts[i]);
        this.dataPdfExport.push(
          Object.assign(
            {
              datapacfull:
                this.desserts[i].datosPaciente.nombres +
                " " +
                this.desserts[i].datosPaciente.ape_pat +
                " " +
                this.desserts[i].datosPaciente.ape_mat,
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

    buscarPacicente() {
      //this.desserts=[]
      //this.editedItem=[]
      //console.log(this.setDni);
      //this.adminForm = "";
      if (this.setDni == "") {
        this.dialogAvisoNULL = true;
      } else {
        axios
          .post(RUTA_API + "/api/token/", {
            username: USUARIO,
            password: PASSWORD,
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .get(RUTA_API + "/paciente/?search=" + this.setDni, {
                headers: { Authorization: this.auth },
              })
              .then((res) => {
                this.datosPaciente = res.data;
                console.log("datosPaciente", this.datosPaciente);
                //console.log("valores par",res.data[0].edad[0] + "," + res.data[0].sexo);
                this.datosPaciente.length != 0
                  ? this.nut()
                  : (this.dialogAviso = true); //(this.dialogDataApi = false),
                //(this.dialogAviso = true);
                //,
                //this.pres()
                ///////aqui valor par////
                axios
                  .get(
                    RUTA_API +
                      "/parNutricion/?search=" +
                      res.data[0].edad[0] +
                      "," +
                      res.data[0].sexo,
                    {
                      headers: { Authorization: this.auth },
                    }
                  )
                  .then((res1) => {
                    this.parValores = res1.data;
                    console.log("valores par", this.parValores);
                  })
                  .catch((res1) => {
                    console.warn("Error:", res1);
                    this.dialog = false;
                  });
                ////fin de par///
              })
              .catch((res) => {
                console.warn("Error:", res);
                this.dialog = false;
                console.log("ingresa a no encontrado pacinte");
                this.dialogAviso = true;
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      }
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
      //this.botonEditar = "1";
      //this.editedIndex;
      //this.editedIndex = this.desserts.indexOf(item);
      /*this.editedItem.date = item.fechaPres;*/
      this.editedItem.dateIngreso = item.fechaIngreso;
      this.editedItem.dateEvalu = item.fechaEvaluacion;
      this.editedItem.frecuencia = item.frecuencia;
      this.editedItem.turno = item.turno;
      this.editedItem.tipoPaciente = item.tipoPaciente;
      this.editedItem.peso = item.peso;
      this.editedItem.talla = item.talla;
      this.editedItem.imc = item.imc;
      (this.editedItem.circuBra = item.circuBra),
        (this.editedItem.cmb = item.porcentajeCMB);
      this.editedItem.medCali = item.medCali;
      this.editedItem.ept = item.porcentajeEPT;
      this.editedItem.albSerica = item.albSerica;
      this.editedItem.vgs = item.ValGlobalSub;
      this.editedItem.ingestaCalorica = item.ingestaCalorica;
      this.editedItem.ingestaProteica = item.ingestaProteica;
      this.editedItem.ingestaCaloricaT = item.ingestaCaloricaT;
      this.editedItem.ingestaProteicaT = item.ingestaProteicaT;
      this.editedItem.diagNut = item.diagNutricional;
      this.editedItem.interNut = item.interveNutricional;
      this.editedItem.usuario = item.usuario;
      this.editedItem.obsNutricion = item.obsNutricion;
      /*this.editedItem.name = item.nomNefro;
      this.editedItem.dos = item.dosisPres;
      this.editedItem.dosHierro = item.dosisHiePres;
      this.editedItem.med = item.medPres;
      this.editedItem.medHierro = item.medHiePres;
      this.editedItem.via = item.viaAdmPres;
      this.editedItem.viaHierro = item.viaAdmHiePres;*/
      //this.editedItem = Object.assign({}, item);
      console.log("editedItem", this.editedItem);
      this.dialogEdit = true;
      this.datosEdit = item.url;
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
                RUTA_API +
                  "/nutricion/" +
                  this.editedItem.url.split("/")[4],
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

    edit() {
      console.log("esto es para editar", this.editedItem);
      if (this.editedItem.usuario == this.url) {
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
                  "/nutricion/" +
                  this.datosEdit.split("/")[4] +
                  "/",
                {
                  paciente: this.datosPaciente[0].url,
                  turno: this.editedItem.turno,
                  frecuencia: this.editedItem.frecuencia,
                  fechaIngreso: this.editedItem.dateIngreso,
                  fechaEvaluacion: this.editedItem.dateEvalu,
                  tipoPaciente: this.editedItem.tipoPaciente,
                  peso: this.editedItem.peso,
                  talla: this.editedItem.talla,
                  imc: (
                    this.editedItem.peso /
                    (this.editedItem.talla * this.editedItem.talla)
                  ).toFixed(2),
                  circuBra: this.editedItem.circuBra,
                  //esto es para allar el cb
                  //porcentajeCMB: (this.editedItem.circuBra*100)/this.parValores[0].cb,
                  porcentajeCMB: (
                    ((this.editedItem.circuBra -
                      3.14 * (this.editedItem.medCali / 10)) /
                      this.parValores[0].cmb) *
                    100
                  ).toFixed(2),
                  medCali: this.editedItem.medCali,
                  porcentajeEPT: (
                    (this.editedItem.medCali * 100) /
                    this.parValores[0].pt
                  ).toFixed(2),
                  albSerica: this.editedItem.albSerica,
                  ValGlobalSub: this.editedItem.vgs,
                  ingestaCaloricaT: this.editedItem.ingestaCaloricaT,
                  ingestaProteicaT: this.editedItem.ingestaProteicaT,
                  ingestaCalorica: (
                    this.editedItem.ingestaCaloricaT / this.editedItem.peso
                  ).toFixed(2),
                  ingestaProteica: (
                    this.editedItem.ingestaProteicaT / this.editedItem.peso
                  ).toFixed(2),
                  diagNutricional: this.editedItem.diagNut,
                  interveNutricional: this.editedItem.interNut,
                  usuario: this.url,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dialogDataApi = true;
                console.log("exito", res.status);
                this.close();
                this.nut();
                this.dialogEdit = false;
              })
              .catch((res) => {
                console.warn("Error:", res);
                //this.dialogEdit = false;
              });
          })
          .catch((response) => {
            response === 404
              ? console.warn("lo sientimos no tenemos servicios")
              : console.warn("Error:", response);
          });
      } else {
        this.dialogEdit = false;
        this.dialogAvisoEditar = true;
      }
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
        /*!this.editedItem.turno ||
        !this.editedItem.frecuencia ||
        !this.editedItem.dateIngreso ||
        !this.editedItem.dateEvalu ||
        !this.editedItem.peso ||
        !this.editedItem.talla ||
        !this.editedItem.cmb ||
        //!this.editedItem.ept ||
        !this.editedItem.albSerica ||
        //!this.editedItem.vgs ||
        !this.editedItem.ingestaCalorica ||
        !this.editedItem.ingestaProteica ||
        !this.editedItem.diagNut ||
        !this.editedItem.interNut*/
        !this.editedItem.tipoPaciente
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
                RUTA_API + "/nutricion/",
                {
                  paciente: this.datosPaciente[0].url,
                  turno: this.editedItem.turno,
                  frecuencia: this.editedItem.frecuencia,
                  fechaIngreso: this.editedItem.dateIngreso,
                  fechaEvaluacion: this.editedItem.dateEvalu,
                  tipoPaciente: this.editedItem.tipoPaciente,
                  peso: this.editedItem.peso,
                  talla: this.editedItem.talla,
                  imc: (
                    this.editedItem.peso /
                    (this.editedItem.talla * this.editedItem.talla)
                  ).toFixed(2),
                  circuBra: this.editedItem.circuBra,
                  //esto es para allar el cb
                  //porcentajeCMB: (this.editedItem.circuBra*100)/this.parValores[0].cb,
                  porcentajeCMB: (
                    ((this.editedItem.circuBra -
                      3.14 * (this.editedItem.medCali / 10)) /
                      this.parValores[0].cmb) *
                    100
                  ).toFixed(2),
                  medCali: this.editedItem.medCali,
                  porcentajeEPT: (
                    (this.editedItem.medCali * 100) /
                    this.parValores[0].pt
                  ).toFixed(2),
                  albSerica: this.editedItem.albSerica,
                  ValGlobalSub: this.editedItem.vgs,
                  ingestaCaloricaT: this.editedItem.ingestaCaloricaT,
                  ingestaProteicaT: this.editedItem.ingestaProteicaT,
                  ingestaCalorica: (
                    this.editedItem.ingestaCaloricaT / this.editedItem.peso
                  ).toFixed(2),
                  ingestaProteica: (
                    this.editedItem.ingestaProteicaT / this.editedItem.peso
                  ).toFixed(2),
                  diagNutricional: this.editedItem.diagNut,
                  interveNutricional: this.editedItem.interNut,
                  obsNutricion : this.editedItem.obsNutricion,
                  usuario: this.url,
                  pacNuevo: this.nuevoValid,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                console.log(this.editedItem);
                this.nut();
              })
              .catch((res) => {
                console.log("Error:", res);
                this.dialogError = true;
                //this.dialog = false;
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
    nutricion() {
      console.log("nutricion");
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
    console.log("Url", this.url);
    console.log("Perfil", this.perfil);
    console.log("Nombre", this.nombre);
  },

  components: {
    CalendarioAnemia,
  },
};
</script>

