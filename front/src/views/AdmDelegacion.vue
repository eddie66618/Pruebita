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
          MONITOREO Y SEGUIMIENTO DE COMPRAS DELEGADAS Y LOCALES
        </v-system-bar>
        <v-row class="start mt-5 ml-5">
          <v-col cols="12" md="5">
            <v-menu
              v-model="menuBusquedaDesde"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="dateBusquedaDesde"
                  label="Fecha Busqueda Desde"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dateBusquedaDesde"
                @input="menuBusquedaDesde = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" md="5"
            ><v-menu
              v-model="menuBusquedaHasta"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="dateBusquedaHasta"
                  label="Fecha Busqueda Hasta"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dateBusquedaHasta"
                @input="menuBusquedaHasta = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" md="1">
            <v-btn color="#1973a5" dark class="mb-2" @click="buscarPorFecha">
              Buscar
            </v-btn>
          </v-col>
        </v-row>
      </v-card>

      <v-card class="mx-auto my-5" max-width="900">
        <v-tabs background-color="#1973a5" center-active dark>
          <v-tab>Delegación</v-tab>
        </v-tabs>
      </v-card>

      <v-card class="mx-auto my-5" max-width="900">
        <v-data-table :headers="headers" :items="desserts" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <!--Registrar-->

              <v-col cols="12" md="4">
                <v-btn
                  class=""
                  icon
                  color="#1973a5"
                  @click="exportExcelDelegaciones"
                >
                  Generar Excel<v-icon>mdi-arrow-down-bold-box</v-icon>
                </v-btn>
              </v-col>
              <v-dialog v-model="dialog" max-width="700px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="#1973a5"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                    v-if="perfil == 4"
                  >
                    {{ actionBoton }}
                  </v-btn>
                </template>
                <v-card>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-card-title>
                      <span>Registro Bienes Estratégicos</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu3"
                              v-model="menu3"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateDelegacion"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateDelegacion"
                                  label="Fecha de Delegación"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateDelegacion"
                                no-title
                                scrollable
                                :min="minimo"
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
                                    $refs.menu3.save(editedItem.dateDelegacion)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perDel"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Delegación"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.solped"
                              :rules="[rules.required, rules.counter]"
                              label="Solicitud Pedido"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.posiFinaciera"
                              :rules="[rules.required, rules.counter]"
                              label="Posición Financiera"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="validCodigoSap == true"
                            cols="12"
                            sm="12"
                            md="12"
                          >
                            <v-alert type="error">
                              CODIGO SAP NO ENCONTRADO
                            </v-alert>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.codsap"
                              :rules="[rules.required, rules.counter]"
                              label="Codigo SAP"
                              :maxlength="maxdat"
                              type="number"
                              @keyup.enter="BuscarCodSap"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="1">
                            <v-btn
                              class=""
                              icon
                              color="#1973a5"
                              @click="BuscarCodSap"
                              ><v-icon>mdi-magnify</v-icon>
                            </v-btn>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="5">
                            <v-text-field
                              v-model="editedItem.producto"
                              disabled
                              label="Producto"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.tipoBienEstra"
                              label="Tipo Bien"
                              disabled
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.unidadMed"
                              :items="itemsUm"
                              :rules="[rules.required]"
                              label="Unidad Medida"
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.cantidad"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.valorTotal"
                              :rules="[rules.required, rules.counter]"
                              label="Valor Total"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu4"
                              v-model="menu4"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateDerivacion"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateDerivacion"
                                  label="Fecha de Derivación"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateDerivacion"
                                no-title
                                scrollable
                                :min="minimo"
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
                                    $refs.menu4.save(editedItem.dateDerivacion)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu5"
                              v-model="menu5"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateRequerimiento"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateRequerimiento"
                                  label="Fecha de Requerimiento"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateRequerimiento"
                                no-title
                                scrollable
                                :min="minimo"
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
                                    $refs.menu5.save(
                                      editedItem.dateRequerimiento
                                    )
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perSol"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Solicitado"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu6"
                              v-model="menu6"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateLogistica"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateLogistica"
                                  label="Fecha Logistica"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateLogistica"
                                no-title
                                scrollable
                                :min="minimo"
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
                                    $refs.menu6.save(editedItem.dateLogistica)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ordenCompra"
                              :rules="[rules.required, rules.counter]"
                              label="N° O/C"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.monto"
                              :rules="[rules.required, rules.counter]"
                              label="Monto"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu7"
                              v-model="menu7"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateIngreso"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateIngreso"
                                  label="Fecha Ingreso Almacen"
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
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu7 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu7.save(editedItem.dateIngreso)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu8"
                              v-model="menu8"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.datePago"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.datePago"
                                  label="Fecha Pago"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.datePago"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu8 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu8.save(editedItem.dateIngreso)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.anulacion"
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
                      <span class="text-h5">Editar Delegación</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu9"
                              v-model="menu9"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateDelegacion"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateDelegacion"
                                  label="Fecha de Delegación"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateDelegacion"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu9 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu9.save(editedItem.dateDelegacion)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateDelegacion"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Delegación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateDelegacion"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Delegación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateDelegacion"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Delegación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perDel"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Delegación"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perDel"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Delegación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perDel"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Delegación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perDel"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Delegación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.solped"
                              :rules="[rules.required, rules.counter]"
                              label="Solicitud Pedido"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.solped"
                              :rules="[rules.required, rules.counter]"
                              label="Solicitud Pedido"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.solped"
                              :rules="[rules.required, rules.counter]"
                              label="Solicitud Pedido"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.solped"
                              :rules="[rules.required, rules.counter]"
                              label="Solicitud Pedido"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.posiFinaciera"
                              :rules="[rules.required, rules.counter]"
                              label="Posición Financiera"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="perfil == 5 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.posiFinaciera"
                              :rules="[rules.required, rules.counter]"
                              label="Posición Financiera"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.codsap"
                              :rules="[rules.required, rules.counter]"
                              label="Codigo SAP"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="1">
                            <v-btn
                              class=""
                              icon
                              color="#1973a5"
                              @click="BuscarCodSap"
                              ><v-icon>mdi-magnify</v-icon>
                            </v-btn>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.codsap"
                              :rules="[rules.required, rules.counter]"
                              label="Codigo SAP"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.codsap"
                              :rules="[rules.required, rules.counter]"
                              label="Codigo SAP"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.codsap"
                              :rules="[rules.required, rules.counter]"
                              label="Codigo SAP"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="5">
                            <v-text-field
                              v-model="editedItem.producto"
                              :rules="[rules.required, rules.counter]"
                              label="Producto"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.producto"
                              :rules="[rules.required, rules.counter]"
                              label="Producto"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.producto"
                              :rules="[rules.required, rules.counter]"
                              label="Producto"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.producto"
                              :rules="[rules.required, rules.counter]"
                              label="Producto"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.tipoBienEstra"
                              :rules="[rules.required, rules.counter]"
                              label="Tipo Bien"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="perfil == 5 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.tipoBienEstra"
                              :rules="[rules.required, rules.counter]"
                              label="Tipo Bien"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.unidadMed"
                              :items="itemsUm"
                              :rules="[rules.required]"
                              label="Unidad Medida"
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.unidadMed"
                              :items="itemsUm"
                              :rules="[rules.required]"
                              label="Unidad Medida"
                              disabled
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.unidadMed"
                              :items="itemsUm"
                              :rules="[rules.required]"
                              label="Unidad Medida"
                              disabled
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.unidadMed"
                              :items="itemsUm"
                              :rules="[rules.required]"
                              label="Unidad Medida"
                              disabled
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.cantidad"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.cantidad"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.cantidad"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.cantidad"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.valorTotal"
                              :rules="[rules.required, rules.counter]"
                              label="Valor Total"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="perfil == 5 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.valorTotal"
                              :rules="[rules.required, rules.counter]"
                              label="Valor Total"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu10"
                              v-model="menu10"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateDerivacion"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateDerivacion"
                                  label="Fecha de Derivación"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateDerivacion"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu10 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu10.save(editedItem.dateDerivacion)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateDerivacion"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Derivación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateDerivacion"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Derivación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateDerivacion"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Derivación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.anulacion"
                              :rules="[rules.required, rules.counter]"
                              label="Observación"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.anulacion"
                              :rules="[rules.required, rules.counter]"
                              label="Observación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.anulacion"
                              :rules="[rules.required, rules.counter]"
                              label="Observación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.anulacion"
                              :rules="[rules.required, rules.counter]"
                              label="Observación"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu11"
                              v-model="menu11"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateRequerimiento"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateRequerimiento"
                                  label="Fecha de Requerimiento"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateRequerimiento"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu11 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu11.save(
                                      editedItem.dateRequerimiento
                                    )
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateRequerimiento"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Requerimiento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateRequerimiento"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Requerimiento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateRequerimiento"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha de Requerimiento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perSol"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Solicitado"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perSol"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Solicitado"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perSol"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Solicitado"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.perSol"
                              :rules="[rules.required, rules.counter]"
                              label="Periodo Solicitado"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-select
                              v-model="editedItem.tipoDoc"
                              :items="itemsTipoDoc"
                              :rules="[rules.required]"
                              label="Tipo Documento"
                            ></v-select>
                          </v-col>
                          <v-col
                            v-if="perfil == 4 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-select
                              v-model="editedItem.tipoDoc"
                              :items="itemsTipoDoc"
                              :rules="[rules.required]"
                              label="Tipo Documento"
                              disabled
                            ></v-select>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.numDoc"
                              :rules="[rules.required, rules.counter]"
                              label="Nº Documento"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="perfil == 4 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.numDoc"
                              :rules="[rules.required, rules.counter]"
                              label="Nº Documento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.cantiRequeridaUsu"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad Requerida"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="perfil == 4 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.cantiRequeridaUsu"
                              :rules="[rules.required, rules.counter]"
                              label="Cantidad Requerida"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.obsUsu"
                              :rules="[rules.required, rules.counter]"
                              label="Obs. Usuaria"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col
                            v-if="perfil == 4 || perfil == 6 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.obsUsu"
                              :rules="[rules.required, rules.counter]"
                              label="Obs. Usuaria"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu12"
                              v-model="menu12"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateLogistica"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateLogistica"
                                  label="Fecha Recep. Requerimiento"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.dateLogistica"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu12 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu12.save(editedItem.dateLogistica)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateLogistica"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Recep. Requerimiento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateLogistica"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Recep. Requerimiento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateLogistica"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Recep. Requerimiento"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ordenCompra"
                              :rules="[rules.required, rules.counter]"
                              label="N° O/C"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ordenCompra"
                              :rules="[rules.required, rules.counter]"
                              label="N° O/C"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ordenCompra"
                              :rules="[rules.required, rules.counter]"
                              label="N° O/C"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.ordenCompra"
                              :rules="[rules.required, rules.counter]"
                              label="N° O/C"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu15"
                              v-model="menu15"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.fechaEmiOrden"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.fechaEmiOrden"
                                  label="Fecha Emi. Orden"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.fechaEmiOrden"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu15 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu15.save(editedItem.fechaEmiOrden)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col
                            v-if="perfil == 5 || perfil == 4 || perfil == 7"
                            cols="12"
                            sm="6"
                            md="3"
                          >
                            <v-text-field
                              v-model="editedItem.fechaEmiOrden"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Emi. Orden"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.monto"
                              :rules="[rules.required, rules.counter]"
                              label="Monto O/C"
                              :maxlength="maxdat"
                              type="number"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.monto"
                              :rules="[rules.required, rules.counter]"
                              label="Monto O/C"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.monto"
                              :rules="[rules.required, rules.counter]"
                              label="Monto O/C"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.monto"
                              :rules="[rules.required, rules.counter]"
                              label="Monto O/C"
                              :maxlength="maxdat"
                              type="number"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu13"
                              v-model="menu13"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.dateIngreso"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.dateIngreso"
                                  label="Fecha Ingreso Almacen"
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
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu13 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu13.save(editedItem.dateIngreso)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateIngreso"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Ingreso Almacen"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateIngreso"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Ingreso Almacen"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.dateIngreso"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Ingreso Almacen"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.observaLogistica"
                              :rules="[rules.required, rules.counter]"
                              label="Obsr. Log"
                              :maxlength="maxdat"
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 7" cols="12" sm="6" md="3">
                            <v-menu
                              ref="menu14"
                              v-model="menu14"
                              :close-on-content-click="false"
                              :return-value.sync="editedItem.datePago"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="editedItem.datePago"
                                  label="Fecha Pago"
                                  prepend-icon="mdi-calendar"
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="editedItem.datePago"
                                no-title
                                scrollable
                                :min="minimo"
                                :max="maximo"
                              >
                                <v-spacer></v-spacer>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="menu14 = false"
                                >
                                  Cancel
                                </v-btn>
                                <v-btn
                                  text
                                  color="primary"
                                  @click="
                                    $refs.menu14.save(editedItem.datePago)
                                  "
                                >
                                  OK
                                </v-btn>
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                          <v-col v-if="perfil == 5" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.datePago"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Pago"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 6" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.datePago"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Pago"
                              :maxlength="maxdat"
                              disabled
                            ></v-text-field>
                          </v-col>
                          <v-col v-if="perfil == 4" cols="12" sm="6" md="3">
                            <v-text-field
                              v-model="editedItem.datePago"
                              :rules="[rules.required, rules.counter]"
                              label="Fecha Pago"
                              :maxlength="maxdat"
                              disabled
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
            <v-icon v-if="perfil == 4" small @click="deleteItem(item)">
              mdi-delete
            </v-icon>
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
import ExportExcel from "./ExportarExcel.vue";
import * as XLSX from "xlsx";
import CalendarioAnemia from "./CalendarioAnemia.vue";
import jsPDF from "jspdf";
import "jspdf-autotable";

export default {
  data: () => ({
    dataExportBE: null,
    //fecha para busqueda
    menuBusquedaDesde: false,
    menuBusquedaHasta: false,
    dateBusquedaDesde: "2023-01-01",
    dateBusquedaHasta: new Date(
      Date.now() - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .substr(0, 10),
    //perfil data
    perfil: "",
    nombre: "",
    usuario: "",
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
    //
    dialogDataApi: false,
    dialogAviso: false,
    dialogAvisoEliminar: false,
    dialogAvisoEditar: false,
    dialog: false,
    itemsFrecuencia: ["L-M-V", "M-J-S"],
    itemsTurno: ["1er Turno", "2do Turno", "3er Turno", "4to Turno"],
    itemsUm: ["TB", "G", "UN", "AM", "PBA", "CM3", "FR", "ROL", "AM", "CP"],
    itemsTipoDoc: ["Nota", "Memorando", "Informe", "Hoja de envio", "Proveido"],
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
      peso: Number,
      talla: Number,
      solped: Number,
      codsap: Number,
      producto: "",
      unidadMed: "",
      cantidad: Number,
      dateDelegacion: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      perDel: "",
      dateDerivacion: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      dateRequerimiento: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      perSol: "",
      tipoDoc: "",
      numDoc: "",
      dateLogistica: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      ordenCompra: Number,
      monto: Number,
      datePago: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      anulacion: "",
      posiFinaciera: "",
      tipoBienEstra: "",
      valorTotal: "",
      fechaEmiOrden: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      observaLogistica: "",
      cantiRequeridaUsu: "",
      obsUsu: "",
      imc: 0.0,
      cmb: Number,
      ept: Number,
      albSerica: Number,
      vgs: "",
      ingestaCalorica: Number,
      ingestaProteica: Number,
      diagNut: "",
      interNut: "",
    },
    minimo: new Date(
      Date.now() - 432000000000 - new Date().getTimezoneOffset() * 60000
    )
      .toISOString()
      .substr(0, 10),
    maximo: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),

    dialogEdit: false,
    formAdmi: false,
    validCodigoSap: false,
    dialogDelete: false,
    dialogEditAdm: false,
    vista: "",
    actionBoton: "AGREGAR BIEN",
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
      peso: Number,
      talla: Number,
      solped: Number,
      codsap: Number,
      producto: "",
      unidadMed: "",
      cantidad: Number,
      dateDelegacion: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      perDel: "",
      dateDerivacion: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      dateRequerimiento: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      perSol: "",
      tipoDoc: "",
      numDoc: "",
      dateLogistica: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      ordenCompra: Number,
      monto: Number,
      datePago: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      anulacion: "",
      posiFinaciera: "",
      tipoBienEstra: "",
      valorTotal: "",
      fechaEmiOrden: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      observaLogistica: "",
      cantiRequeridaUsu: "",
      obsUsu: "",
      imc: 0.0,
      cmb: Number,
      ept: Number,
      albSerica: Number,
      vgs: "",
      ingestaCalorica: Number,
      ingestaProteica: Number,
      diagNut: "",
      interNut: "",
    },
    menu3: false,
    menu2: false,
    menu4: false,
    menu5: false,
    menu6: false,
    menu7: false,
    menu8: false,
    menu9: false,
    menu10: false,
    menu11: false,
    menu12: false,
    menu13: false,
    menu14: false,
    menu15: false,
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
    buscarPorFecha() {
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/delegaciones/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.desserts = res.data.filter(
                (e) =>
                  e.fechaDelegacion >= this.dateBusquedaDesde &&
                  e.fechaDelegacion <= this.dateBusquedaHasta
              );
              this.dialogDataApi = false;
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
      //if (this.setDni == "") {
      // this.dialogAviso = true;
      //} else {
      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
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
              this.datosPaciente.length != 0
                ? this.nut()
                : //(this.dialogDataApi = false),
                  (this.dialogAviso = true);
              //,
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
      //}
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

    cabezeraDelegaciones() {
      this.headers = [
        { text: "solPed", value: "solPed" },
        {
          text: "producto",
          align: "start",
          sortable: false,
          value: "producto",
        },
        { text: "unidadMedida", value: "unidadMedida" },
        { text: "fechaDelegacion", value: "fechaDelegacion" },
        { text: "fechaDerivacion", value: "fechaDerivacion" },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },

    editItem(item) {
      console.log("item", item);
      //this.botonEditar = "1";
      //this.editedIndex;
      //this.editedIndex = this.desserts.indexOf(item);
      /*this.editedItem.date = item.fechaPres;*/
      this.editedItem.solped = item.solPed;
      this.editedItem.codsap = item.codigoSap;
      this.editedItem.producto = item.producto;
      this.editedItem.unidadMed = item.unidadMedida;
      this.editedItem.cantidad = item.cantidad;
      this.editedItem.dateDelegacion = item.fechaDelegacion;
      this.editedItem.perDel = item.pediodoDelegacion;
      this.editedItem.dateDerivacion = item.fechaDerivacion;
      this.editedItem.dateRequerimiento = item.fechaRequerimiento;
      this.editedItem.perSol = item.periodoSolicitado;
      this.editedItem.dateLogistica = item.fechaLogistica;
      this.editedItem.ordenCompra = item.numOrdenCompra;
      this.editedItem.monto = item.monto;
      this.editedItem.dateIngreso = item.fechaIngresoAlmacen;
      this.editedItem.datePago = item.fechaPago;
      this.editedItem.anulacion = item.anulacionPedido;
      this.editedItem.posiFinaciera = item.posiFinaciera;
      this.editedItem.tipoBienEstra = item.tipoBienEstra;
      this.editedItem.valorTotal = item.valorTotal;
      this.editedItem.fechaEmiOrden = item.fechaEmiOrden;
      this.editedItem.observaLogistica = item.observaLogistica;
      this.editedItem.tipoDoc = item.tipoDoc;
      this.editedItem.numDoc = item.numDoc;
      this.editedItem.cantiRequeridaUsu = item.cantiRequeridaUsu;
      this.editedItem.obsUsu = item.obsUsu;
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
      console.log("USUARIO", this.editedItem.userOpc.split("-")[0]);
      console.log("usuario en sesion", this.usuario);
      if (this.editedItem.userOpc.split("-")[0] == this.usuario) {
        console.log("ingresoooo");
        axios
          .post(RUTA_API + "/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .delete(
                RUTA_API + "/delegaciones/" + this.editedItem.url.split("/")[4],
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                console.log("se elimino");
                this.dialogDelete = false;
                this.delegaciones();
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
      /*console.log("esto es para editar", this.editedItem);
      if (this.editedItem.usuario == this.url) {*/
      if (this.perfil == 4) {
        axios
          .post(RUTA_API + "/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .patch(
                RUTA_API +
                  "/delegaciones/" +
                  this.datosEdit.split("/")[4] +
                  "/",
                {
                  solPed: this.editedItem.solped,
                  codigoSap: this.editedItem.codsap,
                  producto: this.editedItem.producto,
                  unidadMedida: this.editedItem.unidadMed,
                  cantidad: this.editedItem.cantidad,
                  fechaDelegacion: this.editedItem.dateDelegacion,
                  pediodoDelegacion: this.editedItem.perDel,
                  fechaDerivacion: this.editedItem.dateDerivacion,
                  anulacionPedido: this.editedItem.anulacion,
                  userOpc: this.usuario + "-" + this.nombre,
                  posiFinaciera: this.editedItem.posiFinaciera,
                  tipoBienEstra: this.editedItem.tipoBienEstra,
                  valorTotal: this.editedItem.valorTotal,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dialogDataApi = true;
                console.log("exito", res.status);
                this.close();
                this.delegaciones();
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
      } else if (this.perfil == 5) {
        axios
          .post(RUTA_API + "/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .patch(
                RUTA_API +
                  "/delegaciones/" +
                  this.datosEdit.split("/")[4] +
                  "/",
                {
                  fechaRequerimiento: this.editedItem.dateRequerimiento,
                  periodoSolicitado: this.editedItem.perSol,
                  userUsuario: this.usuario + "-" + this.nombre,
                  tipoDoc: this.editedItem.tipoDoc,
                  numDoc: this.editedItem.numDoc,
                  cantiRequeridaUsu: this.editedItem.cantiRequeridaUsu,
                  obsUsu: this.editedItem.obsUsu,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dialogDataApi = true;
                console.log("exito", res.status);
                this.close();
                this.delegaciones();
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
      } else if (this.perfil == 6) {
        axios
          .post(RUTA_API + "/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .patch(
                RUTA_API +
                  "/delegaciones/" +
                  this.datosEdit.split("/")[4] +
                  "/",
                {
                  fechaLogistica: this.editedItem.dateLogistica,
                  numOrdenCompra: this.editedItem.ordenCompra,
                  fechaEmiOrden: this.editedItem.fechaEmiOrden,
                  monto: this.editedItem.monto,
                  fechaIngresoAlmacen: this.editedItem.dateLogistica,
                  observaLogistica: this.editedItem.observaLogistica,
                  userLogistica: this.usuario + "-" + this.nombre,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dialogDataApi = true;
                console.log("exito", res.status);
                this.close();
                this.delegaciones();
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
      } else if (this.perfil == 7) {
        axios
          .post(RUTA_API + "/api/token/", {
            username: "cnsr",
            password: "123456",
          })
          .then((response) => {
            this.auth = "Bearer " + response.data.access;
            axios
              .patch(
                RUTA_API +
                  "/delegaciones/" +
                  this.datosEdit.split("/")[4] +
                  "/",
                {
                  fechaPago: this.editedItem.datePago,
                  userFinanzas: this.usuario + "-" + this.nombre,
                },
                {
                  headers: { Authorization: this.auth },
                }
              )
              .then((res) => {
                this.dialogDataApi = true;
                console.log("exito", res.status);
                this.close();
                this.delegaciones();
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
      }
      /*
      } else {
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

    BuscarCodSap() {
      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/mestroSap/?search=" + this.editedItem.codsap, {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("sap", res.data);
              console.log("sap", this.editedItem.codsap);
              this.editedItem.producto = res.data[0].desProducto;
              this.editedItem.tipoBienEstra = res.data[0].tipoBienes;
              this.validCodigoSap = false;
            })
            .catch((res) => {
              console.warn("Error:", res);
              this.validCodigoSap = true;
            });
        })
        .catch((response) => {
          response === 404
            ? console.warn("lo sientimos no tenemos servicios")
            : console.warn("Error:", response);
        });
    },

    save() {
      console.log("click");
      /*if (
        !this.editedItem.turno ||
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
        !this.editedItem.interNut
      ) {
        this.$refs.form.validate();
        console.log("validate");
      } else {*/
      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .post(
              RUTA_API + "/delegaciones/",
              {
                solPed: this.editedItem.solped,
                codigoSap: this.editedItem.codsap,
                producto: this.editedItem.producto,
                unidadMedida: this.editedItem.unidadMed,
                cantidad: this.editedItem.cantidad,
                fechaDelegacion: this.editedItem.dateDelegacion,
                pediodoDelegacion: this.editedItem.perDel,
                fechaDerivacion: this.editedItem.dateDerivacion,
                //fechaRequerimiento: this.editedItem.dateRequerimiento,
                //periodoSolicitado: this.editedItem.perSol,
                //fechaLogistica: this.editedItem.dateLogistica,
                //numOrdenCompra: this.editedItem.ordenCompra,
                //monto: this.editedItem.monto,
                //fechaIngresoAlmacen: this.editedItem.dateLogistica,
                //fechaPago: this.editedItem.datePago,
                anulacionPedido: this.editedItem.anulacion,
                userOpc: this.usuario + "-" + this.nombre,
                userUsuario: "USRER",
                userLogistica: "LOG",
                userFinanzas: "FINANZAS",
                estado: "1",
                posiFinaciera: this.editedItem.posiFinaciera,
                tipoBienEstra: this.editedItem.tipoBienEstra,
                valorTotal: this.editedItem.valorTotal,
              },
              {
                headers: { Authorization: this.auth },
              }
            )
            .then((res) => {
              console.log("exito", res.status);
              this.close();
              console.log(this.editedItem);
              this.delegaciones();
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
      //}
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
          username: "cnsr",
          password: "123456",
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
    delegaciones() {
      //this.adminForm = "0";
      //this.vista = "Prescipción Anemia";
      this.cabezeraDelegaciones();
      //this.actionBoton = "Registro Prescripción";
      this.dialogDataApi = true;

      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/delegaciones/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              this.desserts = res.data.filter(
                (e) =>
                  e.fechaDelegacion >= this.dateBusquedaDesde &&
                  e.fechaDelegacion <= this.dateBusquedaHasta
              );
              this.dialogDataApi = false;
              //this.dataAdmi = res.data[0].url.split("/")[4];
              //this.datosPresHis = res.data[0];
              console.log("desert", res.data);
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
    },

    exportExcelDelegaciones() {
      this.dataExportBE = [];
      this.dialogDataApi = true;
      axios
        .post(RUTA_API + "/api/token/", {
          username: "cnsr",
          password: "123456",
        })
        .then((response) => {
          this.auth = "Bearer " + response.data.access;
          axios
            .get(RUTA_API + "/delegaciones/", {
              headers: { Authorization: this.auth },
            })
            .then((res) => {
              console.log("delegaciones", res.data);
              for (let i = 0; i < res.data.length; i++) {
                this.dataExportBE.push(Object.assign(
                  { contador: i + 1 },
                  { fechaDelegacion: res.data[i].fechaDelegacion},
                  { pediodoDelegacion: res.data[i].pediodoDelegacion},
                  { solPed: res.data[i].solPed},
                  { posiFinaciera: res.data[i].posiFinaciera},
                  { codigoSap: res.data[i].codigoSap},
                  { producto: res.data[i].producto},
                  { tipoBienEstra: res.data[i].tipoBienEstra},
                  { unidadMedida: res.data[i].unidadMedida},
                  { cantidad: res.data[i].cantidad},
                  { valorTotal: res.data[i].valorTotal},
                  { obsUsu: res.data[i].obsUsu},
                  { fechaRequerimiento: res.data[i].fechaRequerimiento},
                  { periodoSolicitado: res.data[i].periodoSolicitado},
                  { tipoDoc: res.data[i].tipoDoc},
                  { numDoc: res.data[i].numDoc},
                  { cantiRequeridaUsu: res.data[i].cantiRequeridaUsu},
                  { fechaRequerimiento: res.data[i].fechaRequerimiento},
                  { numOrdenCompra: res.data[i].numOrdenCompra},
                  { fechaLogistica: res.data[i].fechaLogistica},
                  { fechaEmiOrden: res.data[i].fechaEmiOrden},
                  { monto: res.data[i].monto},
                  { fechaIngresoAlmacen: res.data[i].fechaIngresoAlmacen},
                  { observaLogistica: res.data[i].observaLogistica},
                  { fechaPago: res.data[i].fechaPago},
                  { userOpc: res.data[i].userOpc},    
                  { userUsuario: res.data[i].userUsuario},   
                  { userLogistica: res.data[i].userLogistica},   
                  { userFinanzas: res.data[i].userFinanzas},  
                  ));
              }
              let data = XLSX.utils.json_to_sheet(this.dataExportBE);
              const workbook = XLSX.utils.book_new();
              const filename = "Exportado";
              XLSX.utils.book_append_sheet(workbook, data, filename);
              XLSX.writeFile(workbook, `${filename} BienesEstrategicos.xlsx`);
              this.dialogDataApi= false;
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
    this.usuario = sessionStorage.getItem("usuario");
    console.log("Url", this.url);
    console.log("Perfil", this.perfil);
    console.log("Nombre", this.nombre);
    console.log("usuario", this.usuario);
    this.delegaciones();
  },

  components: {
    CalendarioAnemia,
  },
};
</script>

