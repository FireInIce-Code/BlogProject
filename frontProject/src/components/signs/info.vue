<template>
  <div class="row bg">
    <div class="col-3 leftBar text-center rounded">
      <img src="../../assets/usericon.png" width="300" height="300" />
      <h3>{{values.userInfo.nickname}}</h3>
      <h3>{{values.userInfo.qm}}</h3>
      <h3>经验：{{values.userInfo.exp}}</h3>
      <h3>K币：{{values.userInfo.k}}</h3>
      <h3>用户名:{{values.userInfo.username}}</h3>
    </div>
    <div class="col-9 rightBar h-100">
      <div class="text-center h-75 w-75">
        <h2 class="blogTitle">发表的博客</h2>
        <div
          v-for="blog in values.blogs"
          :key="blog"
          class="rounded blog row"
          align="left"
        >
          <div class="col-5">
            <h3>{{blog.title}}[{{blog.tag}}]</h3>
            <h5>Date:{{blog.date}}</h5>
          </div>
          <div class="blog-right">
            <br />
            <router-link v-bind:to="'/blogs/'+blog.id" tag="button" class="btn btn-s">进入</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Axios from "axios";
export default {
  name: "info",
  values: {},
  data() {
    return {
      values: ""
    };
  },
  methods: {
    getData() {
      Axios.get("/api/page/user?id="+(this.$route.params.userId||0))
        .then(
          (response => {
            if(response.data.message!="success"){
                this.$router.push("/user/signIn");
            }else{
                this.values = response.data;
            }
          }).bind(this)
        )
        .catch(console.log);
    }
  },
  mounted() {
    this.getData();
  }
};
</script>
<style scoped>
h3{
  color:dodgerblue;
}
.btn-s{
  background-color: aquamarine;
  color:white;
  border:none;
}
.btn-s:active{
  background-color:rgb(0, 255, 170);
}
.leftBar,.rightBar{
  margin-top: 50px;
}
.leftBar {
  background-color: rgb(240, 248, 255, 0.5);
}
.rightBar {
  margin-top: 80px;
  position: relative;
}
.rightBar > div {
  position: absolute;
  right: 50px;
  background-color: rgb(240, 255, 255, 0.5);
  border-radius: 20px;
  overflow: auto;
  border-radius: 20px;
}
.row.bg {
  height: 100%;
  background-image: url("../../assets/userbg.jpg");
  background-size: 100% 100%;
  overflow: hidden;
}
.blog {
  padding-left: 30px;
  padding-right: 30px;
  margin-left: 20px;
  margin-right: 20px;
  margin-top:20px;
  margin-bottom: 20px;
  position: relative;
  overflow: auto;
  /* background-color: skyblue; */
  color:dodgerblue;
}
.blog-right {
  position: absolute;
  right: 0;
  padding-right: 20px;
}
.blogTitle{
  color:dodgerblue;
}
</style>