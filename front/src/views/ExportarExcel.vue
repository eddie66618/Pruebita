<template>
  <v-btn color="blue darken-1" text @click="exportExcel">OK</v-btn>
  
</template>
<script>
import * as XLSX from 'xlsx';

export default {
    
  data: () => ({
    props: ['dataExcel'],
  }),
  methods: {
    exportExcel: function () {
        console.log(this.dataExcel)
      let data = XLSX.utils.json_to_sheet(this.dataExcel);
      const workbook = XLSX.utils.book_new();
      const filename = "devschile-admins";
      XLSX.utils.book_append_sheet(workbook, data, filename);
      XLSX.writeFile(workbook, `${filename}.xlsx`);
    },
  },
};
</script>