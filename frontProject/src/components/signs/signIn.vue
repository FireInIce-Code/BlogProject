<template>
  <div align="center">
    <form method="POST" action="/api/user/signIn">
      <h3 class="text-primary">登录</h3>
      <span class="text-primary">用户名:</span>
      <input
        type="text"
        id="username"
        name="username"
        class="form-control"
        style="display:inline"
        @change="username=$event.target.value"
      />
      <br />
      <br />
      <span class="text-primary">密码:</span>
      <input
        type="password"
        id="password"
        name="password"
        class="form-control"
        style="display:inline"
        @change="password=$event.target.value"
      />
      <br />
      <br />
      <input type="button" class="btn btn-info" @click="getData()" value="获取验证码" />
      <div id="codeBox" v-show="isCodeBoxShow">
        <br />
        <img id="codeImg" />
        <br />
        <span class="text-primary">验证码(请尽快填写,此验证码将在一分钟后失效,看不清可以重新获取验证码):</span>
        <input
          type="text"
          id="code"
          name="code"
          class="form-control"
          style="inline"
          @change="code=$event.target.value"
        />
        <br />
        <input type="button" class="btn btn-success" value="登录" @click="login();" />
      </div>
      <br>
      <router-link to="/user/signUp">还没有账户?去注册!</router-link>
    </form>
    <b-modal id="modal" ref="modal" title="提示" hide-footer>
      <h3>{{this.info}}</h3>
      <br />
      <br />
      <b-button block @click="hide()">确定</b-button>
    </b-modal>
  </div>
</template>
<script>
import Axios from "axios";

export default {
  name: "signIn",
  isCodeBoxShow: false,
  showModal: false,
  username: "",
  password: "",
  code: "",
  info: "",
  success:false,
  data() {
    return {
      isCodeBoxShow: this.CodeBoxShow,
      showModal: this.showModal,
      info: this.info
    };
  },
  methods: {
    alert(text) {
      this.info = text;
      this.$refs["modal"].show();
    },
    getData() {
      var username = document.getElementById("username").value;
      if (username == "") {
        this.alert("你要先填上用户名哦.");
        return;
      }
      const api = "/api/code";
      Axios.get(api, {
        params: {
          username: username
        }
      }).then(response => {
        if (response.data.message == "username wrong") {
          this.alert("检查一下,用户名是不是填错了?");
        } else {
          this.isCodeBoxShow = true;
          var img = document.getElementById("codeImg");
          img.src = "data:image/jpeg;base64," + response.data;
        }
      });
    },
    login() {
      const api = "/api/user/signIn";
      var pwd = this.$md5(this.password);
      Axios.post(api, {
        username: this.username,
        code: this.code,
        password: pwd
      }).then(response => {
        if (response.data.message == "code wrong") {
          this.alert(
            "验证码错误,你确定你不是机器人吗?(不是可以重新获取并填写)"
          );
        } else if (response.data.message == "faild") {
          this.alert("检查一下,用户名或密码填错了呢!");
        } else if (response.data.message == "success") {
          this.success=true;
          this.alert("登录成功!");
        } else if (response.data.message == "loginned") {
          this.alert("你已经登录过了!");
          this.success=true;
        } else{
          this.alert("出了点问题呢:" + response.data.message);
        }
      });
    },
    hide() {
      this.$bvModal.hide("modal");
      if(this.success){
        this.$router.push("/info");
        window.location.reload();
      }
    }
  },
  mounted() {}
};
</script>
<style scoped>
input.form-control {
  width: 130px;
  height: 30px;
}
</style>