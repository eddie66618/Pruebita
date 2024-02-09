<template>
  <div>
    <NavBar />
    <div class="row">
      <div class="col-sm-2">
        <v-card class="mx-auto" width="100%" height="100vh" tile>
          <v-navigation-drawer permanent>
            <v-list>
              <v-list-item>
                <v-list-item-avatar> </v-list-item-avatar>
              </v-list-item>

              <v-list-item link>
                <v-list-item-content>
                  <v-list-item-title class="text-h6"> CNSR </v-list-item-title>
                  <v-list-item-subtitle>ESSALUD</v-list-item-subtitle>
                  <v-list-item-subtitle>{{nombre}}</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  <v-icon>mdi-menu-down</v-icon>
                </v-list-item-action>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list nav dense>
              <v-list-item-group v-model="selectedItem" color="primary">
                <v-list-item v-if="perfil==1 || perfil==2">
                  <v-list-item-icon>
                    <v-icon v-text="items2[0].icon"></v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title v-text="items2[0].text"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="perfil==1 || perfil==2">
                  <v-list-item-icon>
                    <v-icon v-text="items2[1].icon"></v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title v-text="items2[1].text"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="perfil==1">
                  <v-list-item-icon>
                    <v-icon v-text="items2[2].icon"></v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title v-text="items2[2].text"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="perfil==1 || perfil==2">
                  <v-list-item-icon>
                    <v-icon v-text="items2[3].icon"></v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title v-text="items2[3].text"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-navigation-drawer>
        </v-card>
      </div>
      <div v-if="selectedItem == 0" class="col-sm-10"><CExternaAnem /></div>
      <div v-if="selectedItem == 1" class="col-sm-10"><CExternaNut /></div>
      <div v-if="selectedItem == 2 && perfil == 1" class="col-sm-10"><ValorGloSub /></div>
      <div v-if="selectedItem == 2 && perfil == 1" class="col-sm-10"><Reportes /></div>
      <div v-if="selectedItem == 2 && perfil == 2" class="col-sm-10"><Reportes /></div>
      <div v-if="selectedItem == 3" class="col-sm-10"><Reportes /></div>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/navbar/NavBar.vue";
import CExternaNut from "./CExternaNut.vue";
import CExternaAnem from "./CExternaAnem.vue";
import CalendarioAnemia from "./CalendarioAnemia.vue";
import ValorGloSub from "./ValorGloSub.vue";
import Reportes from "./Reportes.vue";

export default {
  data() {
    return {
      perfil: "",
      nombre: "",
      selectedItem: null,
      items2: [
        { text: "Anemia", icon: "mdi-folder" },
        { text: "Nutrición", icon: "mdi-folder" },
        { text: "VGS", icon: "mdi-folder" },
        { text: "Reportes", icon: "mdi-folder" },
      ],
    };
  },
  methods: {},
  mounted() {
    if (!sessionStorage.getItem("keyValue")) {
      this.$router.push("/");
    }
  },
  created() {
    this.perfil = sessionStorage.getItem("perfil");
    this.nombre = sessionStorage.getItem("nombre");
    console.log("Perfil", this.perfil);
    console.log("nombre", this.nombre);
  },
  components: {
    NavBar,
    CExternaNut,
    CExternaAnem,
    CalendarioAnemia,
    ValorGloSub,
    Reportes,
  },
};
</script>