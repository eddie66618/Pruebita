<template>
  <v-card class="mx-auto" max-width="244">
    <div v-if="this.img === '1'">
      <v-img :src="require('../../assets/adm.jpg')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '2'">
      <v-img :src="require('../../assets/cexterna.jpg')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '3'">
      <v-img :src="require('../../assets/lab.jpg')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '4'">
      <v-img
        :src="require('../../assets/seguridad.jpg')"
        height="120px"
      ></v-img>
    </div>
    <div v-if="this.img === '5'">
      <v-img :src="require('../../assets/labesca.png')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '6'">
      <v-img :src="require('../../assets/archivo.png')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '7'">
      <v-img
        :src="require('../../assets/dialisisMaq.jpeg')"
        height="120px"
      ></v-img>
    </div>
    <div v-if="this.img === '8'">
      <v-img :src="require('../../assets/bienes.png')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '9'">
      <v-img :src="require('../../assets/cupos.png')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '10'">
      <v-img :src="require('../../assets/transfer.png')" height="120px"></v-img>
    </div>
    <div v-if="this.img === '11'">
      <v-img
        :src="require('../../assets/incidencias.png')"
        height="120px"
      ></v-img>
    </div>
    <div v-if="this.img === '12'">
      <v-img
        :src="require('../../assets/cuposClinicas.png')"
        height="120px"
      ></v-img>
    </div>
    <v-card-title> {{ img }}-{{ title }} </v-card-title>

    <v-card-subtitle>
      {{ detalle_titulo }}
    </v-card-subtitle>

    <v-card-actions>
      <v-btn color="#1973a5" text outlined @click="ingresar"> Ingresar </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    ingresar() {
      if (this.img === "1") {
        console.log("ingresando a", this.img);
      }
      if (this.img === "2") {
        this.$router.push("/ConsultaExterna");
      }
      if (this.img === "3") {
        this.$router.push("/AyudaDiag");
      }
      if (this.img === "4") {
        this.$router.push("/Seguridad");
      }
      if (this.img === "5") {
        this.$router.push("/Escaneados");
      }
      if (this.img === "6") {
        this.$router.push("/Archivo");
      }
      if (this.img === "8") {
        this.$router.push("/Bienes");
      }
      if (this.img === "9") {
        this.$router.push("/Cupos");
      }
      if (this.img === "10") {
        this.$router.push("/DocuContratados");
      }
      if (this.img === "11") {
        this.$router.push("/Incidencias");
      }
      if (this.img === "12") {
        this.$router.push("/CuposIpress");
      }
    },
  },
  props: {
    title: String,
    img: String,
    detalle_titulo: String,
  },
};
</script>