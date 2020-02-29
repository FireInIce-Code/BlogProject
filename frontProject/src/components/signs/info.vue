<template>
  <div></div>
</template>
<script>
import Axios from "axios";
export default {
  name: "info",
  values: {},
  getData() {
    Axios.get("/api/page/user").then(response => {
      this.values = response.data();
    });
  },
  data() {
    this.getData();
    console.log(this.values);
    return this.values;
  },
  method: {}
};
</script>
<style>
</style>