<template>
  <v-card class="mx-auto" width="256" tile>
    <v-navigation-drawer permanent>
      <v-list>
        <v-list-item>
          <v-list-item-avatar>
            <v-img :src="require('../../assets/logo_mini.png')"></v-img>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item link>
          <v-list-item-content>
            <v-list-item-title class="text-h6"> CNSR </v-list-item-title>
            <v-list-item-subtitle
              >ESSALUD {{ selectedItem }}</v-list-item-subtitle
            >
          </v-list-item-content>

          <v-list-item-action>
            <v-icon>mdi-menu-down</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list nav dense>
        <v-list-item-group v-model="selectedItem" color="primary">
          <v-list-item v-for="(item, i) in items" :key="i">
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
export default {
  name: "navBarV",
  data: () => ({
    selectedItem: 0,
    items: [
      { text: "Anemia", icon: "mdi-folder" },
      { text: "Nutrición", icon: "mdi-folder" },
    ],
  }),
  props: {
    arbolCod: {
      type: Function,
      default: null,
    },
  },
  methods: {},
};
</script>