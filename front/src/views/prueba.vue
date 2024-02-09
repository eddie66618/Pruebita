<template>
  <div>
    <table>
      <tr>
        <td><button @click="Economical">Economical</button></td>
        <td>
          <button @click="Custum">Custum</button>
        </td>
      </tr>
    </table>
    <table>
      <tr>
        <td v-if="ver==true">
          <input
            type="number"
            id="conditional"
            name="conditional"
            required
            minlength="4"
            maxlength="8"
            size="2"
            autocomplete="off"
          />
        </td>
      </tr>
    </table>
    <table>
      <tr>
        <td>LENGTH</td>
        <td>QUANTITY</td>
        <td>WEIGHT</td>
      </tr>
      <tr>
        <td>6500</td>
        <td>
          <input
            type="number"
            id="quantity"
            name="name"
            required
            autocomplete="off"
          />
        </td>
        <td><span id="result"></span></td>
      </tr>
    </table>
  </div>
</template>
<script>

export default {
  data() {
    return {
      valor1: 15,
      valor2: 10,
      ver: false,
    };
  },
  methods: {
    Economical() {
        const result = this.valor1 + this.valor2
        console.log("result",result)
        this.ver = false
    },
    Custum(){
        this.ver = true
    }
  },
  mounted() {},
  created() {},
  components: {},
};
</script>