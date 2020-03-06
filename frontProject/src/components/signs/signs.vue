<template>
  <div class="signs-bg">
    <div class="signs-box col-3 offset-7 card">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>
export default {
  name: "signs",
  mounted(){
  }
};
</script>
<style scoped>
.signs-bg {
  width: 100%;
  height: 100%;
  background-size: 100% 100%;
  background-image: url("../../assets/loginbg.jpg");
}
.signs-box {
  top: 100px;
  border-radius: 40px;
  background-color: skyblue;
  padding: 20px;
}
</style>