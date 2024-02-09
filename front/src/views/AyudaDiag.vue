<template>
  <div>
  <NavBar/>
  <div class="d-flex justify-center mb-10 mt-10">
    <v-card>
      <v-form >
        <v-container>
          <v-row>
            <v-col
              cols="12"
              md="12"
            >
              <v-text-field
                v-model="buscarDni"
                label="Dni Paciente"
                required
              ></v-text-field>
              <v-btn 
              color="primary"
              @click="getLabResultado">
              BUSCAR
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card>
  </div>
  <div class="d-flex justify-center">
    <v-card>
    <v-card-title>
      Resultado - {{nombre}}
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :search="search"
    >
    <template v-slot:[`item.calories`]="{ item }">
      <v-chip
        :color="getColor(item.calories)"
        dark
      >
        {{ item.calories }}
      </v-chip>
    </template>
    </v-data-table>
  </v-card>
  </div>
  </div>
</template>

<script>
  import NavBar from '../components/navbar/NavBar.vue'
  import NavBarVertical from '../components/navbar/NavBarVertical.vue'
  import axios from 'axios'

  export default {
    data(){
      return{
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        menu: false,
        modal: false,
        menu2: false,  
        search: '',
        buscarDni: '',
        headers: [
          { text: 'N°', value: 'key' },
          {
            text: 'Apellido Paterno',
            align: 'start',
            sortable: false,
            value: 'datosPaciente.soleqppacapepat',
            auth: '',
          },
          { text: 'Apellido Materno', value: 'datosPaciente.soleqppacapemat' },
          { text: 'Nombre', value: 'datosPaciente.soleqppacprinom' },
          { text: 'Examen', value: 'soleqpcpscod' },
          { text: 'Fecha y Hora Examen', value: 'datosPaciente.soleqpcrefec' },
          { text: 'Resultado', value: '' },
        ],
          desserts: [],
      }
    },
    mounted() {
      if(!localStorage.getItem('keyValue')){
       this.$router.push('/')
      }
    },
    methods: {
       getColor (calories) {
        if (calories > 400) return 'red'
        else if (calories > 200) return 'orange'
        else return 'green'
      },
      getLabResultado(){
         axios.post('http://10.0.52.70:8080/api/token/',{
                    "username": "cnsr",
                    "password": "123456"
        })
        .then(
        (response)=>{
        this.auth="Bearer "+response.data.access
        console.log(this.buscarDni)
        //SolexaLAbCps
        axios.get('http://10.0.52.70:8080/SolexaLAbCps/?search='+this.buscarDni,
        {
          headers:{'Authorization': this.auth},
        }
        )
        .then(
          (res)=>{
            this.desserts=res.data
            console.log(this.desserts)
          }
        )
        .catch(
          (res)=>{
            console.warn('Error:', res)
          }
        )
        }
        )
        .catch(
        (response)=>{
          response===404 ? console.warn('lo sientimos no tenemos servicios') :console.warn('Error:' ,response)
        }
        )  
       }
    },
    created(){
      //this.getLabResultado()
        this.nombre = localStorage.getItem('nombre');
    },
    components: {
    NavBar,
    NavBarVertical,
    },
  }
</script>
