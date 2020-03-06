<template>
  <div class="bg">
    <div class="content" align="center">
      <h1 class="text-primary">我的文章</h1>
      <hr width="80%" />
      <h3 class="d-inline text-primary">分类:&nbsp;&nbsp;&nbsp;&nbsp;</h3>
      <select ref="select" class="form-control" v-model="tag" @change="changeTag">
        <option selected="selected">所有</option>
        <option v-for="item in sortItems" :key="item">{{item}}</option>
      </select>
      <ul class="list-group blog-list" align="left">
        <div
          class="list-group-item list-group-item-action row"
          v-for="blog in blogs"
          :key="blog"
          align="left"
        >
          <div class="col-9 d-inline" align="left">
            {{blog.title}}
            <br />
            Date:{{blog.date}}
          </div>
          <div class="offset-6 col-6" align="right">
            <router-link class="btn btn-success button" v-bind:to="'/blogs/'+blog.id" tag="div">查看</router-link>
            <router-link
              class="btn btn-warning button"
              v-bind:to="'/write/'+replaceStr(blog.title)"
              tag="div"
            >编辑</router-link>
            <button class="btn btn-danger button" v-bind:id="'delBlog'+blog.id" @click="delBlog($event)">删除</button>
          </div>
        </div>
      </ul>
    </div>
    <br />
    <br />
  </div>
</template>

<script>
import Axios from "axios";
export default {
  data() {
    return {
      tag: "",
      sortItems: [],
      allblogs: [],
      blogs: []
    };
  },
  methods: {
    getData() {
      Axios.get("/api/page/user").then(response => {
        var data = response.data;
        if (data.message == "no signIn") {
          this.$router.push("/user/signIn");
          return;
        }
        this.allblogs = data.blogs;
        this.changeTag();
      });
      Axios.get("/api/sortItems").then(response => {
        var data = response.data;
        this.sortItems = data.sortItems;
      });
    },
    changeTag(event) {
      var tag = this.tag;
      if (tag == "所有") {
        this.blogs = this.allblogs;
      } else {
        this.blogs = [];
        for (var i = 0; i < this.allblogs.length; i++) {
          if (this.allblogs[i].tag == tag) {
            this.blogs.push(this.allblogs[i]);
          }
        }
      }
    },
    delBlog(e){
      var id=parseInt(e.target.id.slice(7));
      Axios.post("/api/edit/del?id="+id);
      this.getData();
    },
    replaceStr(str) {
      return str
        .replace(/:/g, "%3A")
        .replace(/\//g, "%2F")
        .replace(/\?/g, "%3F")
        .replace(/=/g, "%3D")
        .replace(/\+/g, "%2B")
        .replace(/&/g, "%26")
        .replace(/ /g, "%20")
        .replace(/#/g, "%23");
    }
  },
  mounted() {
    this.tag = "所有";
    this.getData();
  }
};
</script>

<style scoped>
.bg {
  background-color: aliceblue;
  min-height: 100%;
  margin-top: 0;
  padding-top: 1px;
}
.content {
  margin-top: 100px;
}
select.form-control {
  display: inline-block;
  width: 400px;
  height: 60px;
  font-size: 40px;
  padding-top: 0px;
  padding-bottom: 0px;
}
.blog-list {
  height: 600px;
  width: 70%;
  overflow: auto;
}
.blog-list > div {
  background-color: rgb(137, 212, 255);
  color: white;
}
.blog-list > div:hover {
  background-color: rgb(0, 140, 255);
  color: white;
}
</style>