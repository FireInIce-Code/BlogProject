<template>
  <div class="bg" align="center">
    <div class="content" align="center">
      <h3 class="text-primary">{{tag}}专栏</h3>
      <hr width="100%" class="text-primary bg-primary" />
      <div v-for="blog in blogs" :key="blog" class="rounded blog row" align="left">
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
</template>

<script>
import Axios from "axios";
export default {
  data() {
    return {
      tag: "",
      blogs: []
    };
  },
  methods: {
    getData() {
      this.tag = this.$route.params.tag;
      Axios.get("/api/page/tag?tagName=" + this.tag).then(response => {
        var data = response.data;
        if (data.message == "none") {
          this.$route.push("/404");
        } else if (data.message == "success") {
          this.blogs = data.blogs;
        }
      });
    }
  },
  mounted() {
    this.getData();
  }
};
</script>

<style scoped>
.bg {
  height: 100%;
  width: 100%;
  padding-top: 1px;
  background-color: beige;
}
.content {
  margin-top: 100px;
  width:80%;
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
  background-color: rgb(174, 232, 255);
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
.btn-s{
  background-color: aquamarine;
  color:white;
  border:none;
}
.btn-s:hover{
    color:white;
}
.btn-s:active{
  background-color:rgb(0, 255, 170);
}
</style>