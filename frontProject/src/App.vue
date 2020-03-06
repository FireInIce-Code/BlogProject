<template>
  <div id="app">
    <nav class="navbar navbar-expand-sm bg-light fixed-top">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/" tag="button" class="nav-link text-light btn btn-primary navBtn">回到首页</router-link>
        </li>
        <li class="nav-item">
          <router-link
            to="/write"
            tag="button"
            class="nav-link text-light btn btn-primary navBtn"
          >文章管理</router-link>
        </li>
        <li class="nav-item">
          <button
            class="nav-link text-primary newBlogBtn text-light btn btn-primary navBtn"
            @click="newBlog()"
          >新的文章</button>
        </li>
      </ul>
      <div v-if="logined" class="navbar-nav ml-auto">
        <li class="nav-item">
          <router-link
            to="/info"
            tag="a"
            class="nav-link text-primary text-light btn btn-primary navBtn"
          >用户中心</router-link>
        </li>
        <li class="nav-item">
          <button
            class="nav-link text-primary newBlogBtn text-light btn btn-primary navBtn"
            @click="exit()"
          >退出登录</button>
        </li>
      </div>
      <div v-else class="navbar-nav ml-auto">
        <router-link
          to="/user/signIn"
          tag="a"
          class="nav-link text-primary text-light btn btn-primary navBtn"
        >登录</router-link>
      </div>
    </nav>
    <router-view />
    <b-modal id="newBlog" ref="newBlog" title="新建文章" @ok="blogSubmit()">
      <h4>标题:</h4>
      <b-form-input v-model="blogTitle"></b-form-input>
      <h4>分类:</h4>
      <select class="form-control d-block" v-model="blogSelect">
        <option v-for="item in sortItems" :key="item">{{item}}</option>
      </select>
    </b-modal>
  </div>
</template>

<script>
import Axios from "axios";
export default {
  name: "App",
  data() {
    return {
      logined: false,
      user: null,
      sortItems: [],
      blogTitle: "",
      blogSelect: ""
    };
  },
  methods: {
    getData() {
      Axios.get("/api/page/user").then(response => {
        if (response.data.message == "no signIn") {
          this.logined = false;
        } else {
          this.logined = true;
          this.user = response.data.userInfo;
        }
      });
      Axios.get("/api/sortItems").then(response => {
        if (response.data.message == "success") {
          this.sortItems = response.data.sortItems;
        }
      });
    },
    newBlog() {
      this.$refs.newBlog.show();
    },
    blogSubmit() {
      Axios.post("/api/blog/new", {
        tag: this.sortItems.indexOf(this.blogSelect),
        inner: " ",
        title: this.blogTitle
      })
        .then(response => {
          console.log(response.data);
        })
        .catch(console.log);
      this.$router.push("/write/" + this.blogTitle);
    },
    exit() {
      Axios.post("/api/user/signOut");
      this.$router.push("/user/signIn");
      window.location.reload();
    }
  },
  mounted() {
    this.getData();
  }
};
</script>

<style scoped>
#app {
  width: 100%;
  height:100%;
}
.newBlogBtn {
  cursor: pointer;
}
.navBtn {
  margin-left: 20px;
}
</style>