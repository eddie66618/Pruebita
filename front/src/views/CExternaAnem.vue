<template>
  <div>
    <div class="text-center">
      <v-dialog v-model="dialogCalendar" class="col-sm-12">
        <v-card>
          <v-card-title class="col-md-12 text-h5 grey lighten-2">
            <span class="col-md-11">CALENDARIO</span>
            <v-btn
              class="col-md-1"
              color="primary"
              text
              @click="dialogCalendar = false"
            >
              X (Cerrar)
            </v-btn>
          </v-card-title>

          <div class="col-sm-12">
            <CalendarioAnemia :pres="desserts" :adm="desserts1" />
          </div>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="dialogCalendar = false">
              Cerrar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
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
            ¡Paciente no se encuentra registrado!, ponerce en contacto con el
            admistrador de sistema.
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialogAviso = false">cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-container>
      <v-card class="mx-auto my-5" max-width="900">
        <v-system-bar color="#1973a5" dark>
          DATOS DE PACIENTE - CONTROL DE ANEMIA CLINICAS CONTRATADOS
        </v-system-bar>
        <v-row justify="center">
          <v-col cols="12" md="3">
            <v-text-field
              class="mx-auto mt-8"
              v-model="setDni"
              label="N° de documento"
              required
              :maxlength="8"
              @keyup.enter="buscarPacicente"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn class="mt-10" icon color="#1973a5" @click="buscarPacicente">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="12" md="3">
            <v-btn
              v-if="datosPaciente.length != 0"
              class="mt-10"
              icon
              color="#1973a5"
              @click="activarCalendario"
            >
              Calendario Anemia
              <v-icon>mdi-calendar</v-icon>
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
        v-if="(adminForm == '0' || adminForm == '1' || adminForm == '2') && datosPaciente.length != 0"
      >
        <v-tabs background-color="#1973a5" center-active dark>
          <v-tab @click="pres">Prescripción</v-tab>
          <v-tab @click="adm">Administración</v-tab>
          <v-tab @click="exclu">Exclusión (MES)</v-tab>
        </v-tabs>
      </v-card>

      <v-card class="mx-auto my-5" max-width="900" v-if="adminForm == '0' && datosPaciente.length != 0">
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
                      <span class="text-h5">{{
                        "Registro de Prescripción Mensual"
                      }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-menu
                              ref="menu"
                              v-model="menu"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.date"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.date"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.date"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="$refs.menu.save(editedItem.date)"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="8">
                            <v-text-field
                              v-model="editedItem.name"
                              :rules="[rules.required, rules.counter]"
                              label="Nombre Nefrólogo"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.med"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dos"
                              :items="dosisE"
                              :rules="[rules.required]"
                              label="Dosis (UI) Semanal"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.via"
                              :rules="[rules.required, rules.counter]"
                              :items="via"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.medHierro"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dosHierro"
                              :items="dosisH"
                              :rules="[rules.required]"
                              label="Dosis (UI) Mensual"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.viaHierro"
                              :rules="[rules.required, rules.counter]"
                              :items="via[1]"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
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
                      <span class="text-h5">{{ actionBoton }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-menu
                              ref="menu2"
                              v-model="menu2"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.date"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.date"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.date"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu2 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="$refs.menu2.save(editedItem.date)"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="8">
                            <v-text-field
                              v-model="editedItem.name"
                              :rules="[rules.required, rules.counter]"
                              label="Nombre Nefrólogo"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.med"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dos"
                              :items="dosisE"
                              :rules="[rules.required]"
                              label="Dosis (UI) Semanal"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.via"
                              :rules="[rules.required, rules.counter]"
                              :items="via"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.medHierro"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dosHierro"
                              :items="dosisH"
                              :rules="[rules.required]"
                              label="Dosis (UI) Mensual"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.viaHierro"
                              :rules="[rules.required, rules.counter]"
                              :items="via[1]"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
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
                    >Esta seguro de eliminar la Prescipción?</v-card-title
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

      <v-card class="mx-auto my-5" max-width="900" v-if="adminForm == '1'">
        <v-data-table :headers="headers" :items="desserts1" class="elevation-1">
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
                      <span class="text-h4">{{ actionBoton }} </span>
                    </v-card-title>
                    <v-card>
                      <v-col cols="12" sm="12" md="12"> </v-col>
                      <v-col cols="12" sm="12" md="12">
                        <span class="text-h6">Médico Prescribe: </span>
                        <span>{{ datosPresHis.nomNefro }}</span>
                      </v-col>
                      <v-col cols="12" sm="12" md="12">
                        <span class="text-h6">Dosis Eritropoyetina:</span>
                        <span>{{ datosPresHis.dosisPres }} UI Semanal</span>
                        <span class="text-h6">Dosis Hierro: </span>
                        <span> {{ datosPresHis.dosisHiePres }} UI Mensual</span>
                      </v-col>
                    </v-card>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-menu
                              ref="menu"
                              v-model="menu"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.date"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.date"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.date"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="$refs.menu.save(editedItem.date)"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="8">
                            <v-text-field
                              v-model="editedItem.name"
                              :rules="[rules.required, rules.counter]"
                              label="Nombre Completo Enfermera"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.med"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dos"
                              :items="dosisE"
                              :rules="[rules.required]"
                              label="Dosis (UI)-Administrada"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.via"
                              :rules="[rules.required, rules.counter]"
                              :items="via"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.medHierro"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dosHierro"
                              :items="dosisH"
                              :rules="[rules.required]"
                              label="Dosis (UI)-Administrada"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.viaHierro"
                              :rules="[rules.required, rules.counter]"
                              :items="via[1]"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeFormAdmin">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="saveFormAdmin">
                        Guardar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <!--Editar administracion-->
              <v-dialog v-model="dialogEditAdm" max-width="700px">
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
                      <span class="text-h5">{{ actionBoton }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-menu
                              ref="menu2"
                              v-model="menu2"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.date"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.date"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.date"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu2 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="$refs.menu2.save(editedItem.date)"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="8">
                            <v-text-field
                              v-model="editedItem.name"
                              :rules="[rules.required, rules.counter]"
                              label="Nombre Completo Enfermera"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.med"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dos"
                              :items="dosisE"
                              :rules="[rules.required]"
                              label="Dosis (UI)-Administrada"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.via"
                              :rules="[rules.required, rules.counter]"
                              :items="via"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field
                              v-model="editedItem.medHierro"
                              label="Medicamento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.dosHierro"
                              :items="dosisH"
                              :rules="[rules.required]"
                              label="Dosis (UI)-Administrada"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                            <v-select
                              v-model="editedItem.viaHierro"
                              :rules="[rules.required, rules.counter]"
                              :items="via[1]"
                              label="Via Administración"
                            ></v-select>
                          </v-col>
                          <!--HIERRO-->
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="closeEditFormAdmin"
                      >
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="editarAdm">
                        Editar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <!--fin de edicion de administracion-->
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Esta seguro de eliminar la Prescipción?</v-card-title
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
            <v-icon small class="mr-2" @click="editItemAdm(item)">
              mdi-pencil
            </v-icon>
            <!--<v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>-->
          </template>
        </v-data-table>
      </v-card>

      <v-card class="mx-auto my-5" max-width="900" v-if="adminForm == '2'">
        <v-data-table :headers="headers" :items="desserts2" class="elevation-1">
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
                      <span class="text-h5">{{ actionBoton }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-menu
                              ref="menu"
                              v-model="menu"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.date"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.date"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.date"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="$refs.menu.save(editedItem.date)"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="8">
                            <v-text-field
                              v-model="editedItem.razonExclu"
                              :rules="[rules.required, rules.counter]"
                              label="Razón o Motivo"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.observa"
                              :rules="[rules.required, rules.counter]"
                              label="Observación"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeFormAdmin">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="saveFormExclu">
                        Guardar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <!--Editar Eclusion-->
              <v-dialog v-model="dialogEditExclu" max-width="700px">
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
                      <span class="text-h5">{{ actionBoton }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-menu
                              ref="menu2"
                              v-model="menu2"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.date"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.date"
                                  label="Fecha"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.date"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu2 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="$refs.menu2.save(editedItem.date)"
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col cols="12" sm="6" md="8">
                            <v-text-field
                              v-model="editedItem.razonExclu"
                              :rules="[rules.required, rules.counter]"
                              label="Razón o Motivo"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.observa"
                              :rules="[rules.required, rules.counter]"
                              label="Observación"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeFormExclu">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue darken-1" text @click="editExclu">
                        editar
                      </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-dialog>
              <!--fin de edicion de administracion-->
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Esta seguro de eliminar la Prescipción?</v-card-title
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
            <v-icon small class="mr-2" @click="editItemExclu(item)">
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
import CalendarioAnemia from "./CalendarioAnemia.vue";

export default {
  data: () => ({
    perfil: "",
    nombre: "",
    url:"",
    dialogCalendar: false,
    datosPresHis: [],
    datosEdit: "",
    dialogEditExclu: false,
    dialogAviso: false,
    dataAdmin: "",
    datosPaciente: [],
    setDni: "",
    adminForm: 0,
    dialogDataApi: false,
    maxdat: 21,
    valid: true,
    medicamentos: ["ERITROPOYETINA", "HIERRO"],
    via: ["SC", "EV"],
    dosisE: [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000],
    dosisH: [100, 200, 300, 400, 500, 600, 700, 800],
    rules: {
      required: (value) => !!value || "Campo Obligatorio.",
      counter: (value) => value.length <= 20 || "Max 20 characters",
    },
    date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    menu: false,
    modal: false,
    menu2: false,
    minimo: new Date(
      Date.now() - 432000000 - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .substr(0, 10),
    maximo: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    dialog: false,
    dialogEdit: false,
    formAdmi: false,
    dialogDelete: false,
    dialogEditAdm: false,
    vista: "",
    actionBoton: "nueva",
    headers: [],
    desserts: [],
    desserts1: [],
    desserts2: [],
    editedIndex: -1,
    editedItem: {
      date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      name: "",
      med: "ERITROPOYETINA",
      dos: "",
      medHierro: "HIERRO",
      dosHierro: "",
      viaHierro: "",
      via: "",
      razonExclu: "",
      observa: "",
    },
    dataex: "",
    defaultItem: {
      date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      name: "",
      med: "ERITROPOYETINA",
      dos: "",
      medHierro: "HIERRO",
      dosHierro: "",
      viaHierro: "",
      via: "",
      razonExclu: "",
      observa: "",
    },
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
    this.perfil = sessionStorage.getItem("perfil");
    this.nombre = sessionStorage.getItem("nombre");
    this.url = sessionStorage.getItem("url");
    console.log("Url", this.url);
    console.log("Perfil", this.perfil);
    console.log("Nombre", this.nombre);
  },

  methods: {
    initialize() {
      this.desserts = [];
    },

    buscarPacicente() {
      //this.desserts=[]
      //this.editedItem=[]
      console.log(this.setDni);
      this.adminForm = "";
      if (this.setDni == "") {
        this.dialogAviso = true;
      } else {
        axios
          .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .get(RUTA_SERVIDOR + "/APICNSR/paciente/?search=" + this.setDni, {
                headers: { Authorization: this.auth },
              })
              .then((res) => {
                this.datosPaciente = res.data;
                console.log("datosPaciente", this.datosPaciente);
                this.datosPaciente.length != 0
                  ? (this.adm(), this.pres())
                  : ((this.dialogDataApi = false),
                    (this.aviso = "Datos de paciente no encontrados"),
                    (this.dialogAviso = true));
                //this.pres()
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

    cabezeraPres() {
      this.headers = [
        { text: "Fecha", value: "fechaPres" },
        {
          text: "Nombre Apellido Nefrologo",
          align: "start",
          sortable: false,
          value: "nomNefro",
        },
        { text: "ERITROPOYETINA (UI)", value: "dosisPres" },
        { text: "Via ERITRO", value: "viaAdmPres" },
        { text: "HIERRO (UI)", value: "dosisHiePres" },
        { text: "Via HIERRO", value: "viaAdmHiePres" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    cabezeraAdm() {
      this.headers = [
        { text: "Fecha", value: "fechaAdmi" },
        {
          text: "Nombre Apellido Enfermera",
          align: "start",
          sortable: false,
          value: "nomEnfer",
        },
        { text: "ERITROPOYETINA", value: "dosisAdmi" },
        { text: "Via", value: "viaAdm" },
        { text: "HIERRO", value: "dosisHieAdmi" },
        { text: "Via", value: "viaAdmHierro" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    cabezeraExclu() {
      this.headers = [
        { text: "Fecha", value: "fechaExclu" },
        {
          text: "Razón o Motivo",
          align: "start",
          sortable: false,
          value: "razonExclu",
        },
        { text: "Observaciones", value: "ObservaExclu" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    cabezeraMov() {
      this.headers = [
        { text: "Fecha", value: "calories" },
        {
          text: "Razón o Motivo",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "Motivo", value: "calories" },
        { text: "Observación", value: "calories" },
      ];
    },

    editItem(item) {
      console.log("item", item);
      //this.botonEditar = "1";
      //this.editedIndex;
      //this.editedIndex = this.desserts.indexOf(item);
      this.editedItem.date = item.fechaPres;
      this.editedItem.name = item.nomNefro;
      this.editedItem.dos = item.dosisPres;
      this.editedItem.dosHierro = item.dosisHiePres;
      this.editedItem.med = item.medPres;
      this.editedItem.medHierro = item.medHiePres;
      this.editedItem.via = item.viaAdmPres;
      this.editedItem.viaHierro = item.viaAdmHiePres;
      //this.editedItem = Object.assign({}, item);
      console.log("editedItem", this.editedItem);
      this.dialogEdit = true;
      this.datosEdit = item.url;
    },

    editItemAdm(item) {
      console.log("item", item);
      //this.botonEditar = "1";
      //this.editedIndex;
      //this.editedIndex = this.desserts.indexOf(item);
      this.editedItem.date = item.fechaAdmi;
      this.editedItem.name = item.nomEnfer;
      this.editedItem.dos = item.dosisAdmi;
      this.editedItem.dosHierro = item.dosisHieAdmi;
      this.editedItem.med = item.medAdmi;
      this.editedItem.medHierro = item.medHieAdmi;
      this.editedItem.via = item.viaAdm;
      this.editedItem.viaHierro = item.viaAdmHierro;
      //this.editedItem = Object.assign({}, item);
      //console.log("editedItem", this.editedItem);
      this.dialogEditAdm = true;
      this.datosEdit = item.url;
    },

    editItemExclu(item) {
      console.log("item", item);
      //this.botonEditar = "1";
      //this.editedIndex;
      //this.editedIndex = this.desserts.indexOf(item);
      this.editedItem.fechaExclu = item.fechaExclu;
      this.editedItem.razonExclu = item.razonExclu;
      this.editedItem.observa = item.ObservaExclu;
      //this.editedItem = Object.assign({}, item);
      console.log("editedItem", this.editedItem);
      this.dialogEditExclu = true;
      this.datosEdit = item.url;
    },

    deleteItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.desserts.splice(this.editedIndex, 1);

      this.closeDelete();
    },

    closeFormAdmin() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeEditFormAdmin() {
      this.dialogEditAdm = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeFormExclu() {
      this.dialogEditExclu = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    edit() {
      console.log("esto es para editar", this.datosEdit.split("/")[4]);
      axios
        .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_SERVIDOR +
                "/presAnemia/" +
                this.datosEdit.split("/")[4] +
                "/",
              {
                fechaPres: this.editedItem.date,
                nomNefro: this.editedItem.name,
                medPres: this.editedItem.med,
                dosisPres: this.editedItem.dos,
                medHiePres: this.editedItem.medHierro,
                dosisHiePres: this.editedItem.dosHierro,
                viaAdmPres: this.editedItem.via,
                viaAdmHiePres: this.editedItem.viaHierro,
                usuario: this.url
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.dialogDataApi = true;
              console.log("exito", res.status);
              this.close();
              this.pres();
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

    editarAdm() {
      axios
        .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_SERVIDOR +
                "/adminAnemia/" +
                this.datosEdit.split("/")[4] +
                "/",
              {
                fechaAdmi: this.editedItem.date,
                nomEnfer: this.editedItem.name,
                medAdmi: this.editedItem.med,
                dosisAdmi: this.editedItem.dos,
                medHiePres: this.editedItem.medHierro,
                dosisHieAdmi: this.editedItem.dosHierro,
                viaAdm: this.editedItem.via,
                viaAdmHierro: this.editedItem.viaHierro,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("exito", res.status);
              this.dialogDataApi = true;
              this.close();
              this.adm();
              this.dialogEditAdm = false;
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.dialogEditAdm = false;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },

    editExclu(item) {
      console.log("esto es para editar", item);
      console.log("esto exclu", this.editedItem);
      console.log("esto paciente", this.datosPaciente);

      axios
        .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .patch(
              RUTA_SERVIDOR +
                "/exclusionAnemia/1/",
              {
                fechaExclu: this.editedItem.fechaExclu,
                razonExclu: this.editedItem.razonExclu,
                ObservaExclu: this.editedItem.observa,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("exito", res.status);
              this.dialogDataApi = true;
              this.close();
              this.exclu();
              this.dialogEditExclu = false;
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

    saveFormAdmin() {
      console.log("click");
      if (
        !this.editedItem.name ||
        !this.editedItem.med ||
        !this.editedItem.dos ||
        !this.editedItem.via ||
        !this.editedItem.dosHierro ||
        !this.editedItem.viaHierro ||
        !this.editedItem.medHierro
      ) {
        this.$refs.form.validate();
      } else {
        console.log("administra", this.editedItem);
        axios
          .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_SERVIDOR + "/APICNSR/adminAnemia/",
                {
                  presAnemia:
                    RUTA_SERVIDOR + "/APICNSR/presAnemia/" + this.dataAdmi + "/",
                  fechaAdmi: this.editedItem.date,
                  nomEnfer: this.editedItem.name,
                  medAdmi: this.editedItem.med,
                  dosisAdmi: this.editedItem.dos,
                  medHieAdmi: this.editedItem.medHierro,
                  dosisHieAdmi: this.editedItem.dosHierro,
                  viaAdm: this.editedItem.via,
                  viaAdmHierro: this.editedItem.viaHierro,
                  usuario: this.url
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                this.adm();
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
      //console.log('holaaaaaaaa',this.editedItem)
    },

    save() {
      console.log("click");
      if (
        !this.editedItem.name ||
        !this.editedItem.med ||
        !this.editedItem.dos ||
        !this.editedItem.via ||
        !this.editedItem.dosHierro ||
        !this.editedItem.viaHierro ||
        !this.editedItem.medHierro
      ) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        axios
          .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_SERVIDOR + "/APICNSR/presAnemia/",
                {
                  paciente: this.datosPaciente[0].url,
                  fechaPres: this.editedItem.date,
                  nomNefro: this.editedItem.name,
                  medPres: this.editedItem.med,
                  dosisPres: this.editedItem.dos,
                  medHiePres: this.editedItem.medHierro,
                  dosisHiePres: this.editedItem.dosHierro,
                  viaAdmPres: this.editedItem.via,
                  viaAdmHiePres: this.editedItem.viaHierro,
                  usuario: this.url
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                this.pres();
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
      //console.log('holaaaaaaaa',this.editedItem)
    },

    saveFormExclu() {
      console.log("click");
      console.log(this.datosPaciente[0].url);
      console.log(this.editedItem);
      if (!this.editedItem.razonExclu || !this.editedItem.observa) {
        this.$refs.form.validate();
        console.log("validate");
      } else {
        axios
          .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .post(
                RUTA_SERVIDOR + "/APICNSR/exclusionAnemia/",
                {
                  paciente: this.datosPaciente[0].url,
                  fechaExclu: this.editedItem.date,
                  razonExclu: this.editedItem.razonExclu,
                  ObservaExclu: this.editedItem.observa,
                  usuario: this.url
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("exito", res.status);
                this.close();
                this.exclu();
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

    pres() {
      this.adminForm = "0";
      this.vista = "Prescipción Anemia";
      this.cabezeraPres();
      this.actionBoton = "Registro Prescripción";
      this.dialogDataApi = true;

      axios
        .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_SERVIDOR +
                "/presAnemia/?search=" +
                this.datosPaciente[0].url.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.desserts = res.data;
              this.dialogDataApi = false;
              this.dataAdmi = res.data[0].url.split("/")[4];
              this.datosPresHis = res.data[0];
              console.log(res.data);
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

    adm() {
      this.adminForm = "1";
      this.vista = "Administración Anemia";
      this.cabezeraAdm();
      this.actionBoton = "Registro Admistración";
      this.dialogDataApi = true;
      //consulta api datos Prescripcion
      console.log("datos desert1", this.desserts1);
      axios
        .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_SERVIDOR +
                "/adminAnemia/?search=" +
                this.datosPaciente[0].url.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.desserts1 = res.data;
              //console.log(this.dataAdmi);
              console.log("datosAministra", this.desserts1);
              //this.datosPresHis = this.desserts[0].datosPres
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

    exclu() {
      this.adminForm = "2";
      this.vista = "Exclusion Protocolo";
      this.cabezeraExclu();
      this.initialize();
      this.actionBoton = "Registro Exclusión";
      this.dialogDataApi = true;
      axios
        .post(RUTA_SERVIDOR + "/APICNSR/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(
              RUTA_SERVIDOR +
                "/exclusionAnemia/?search=" +
                this.datosPaciente[0].url.split("/")[4],
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              this.desserts2 = res.data;
              //console.log(this.dataAdmi);
              console.log("datosAministra", this.desserts);
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

    mov() {
      this.vista = "Movimiento de paciente";
      this.cabezeraMov();
      this.actionBoton = "Registro Movimiento";
    },

    activarCalendario() {
      this.dialogCalendar = true;
    },
  },

  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
  },

  components: {
    CalendarioAnemia,
  },
};
</script>

