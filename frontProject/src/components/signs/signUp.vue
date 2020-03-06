<template>
  <div align="center">
    <form method="POST" action="/api/user/signIn">
      <h3 class="text-primary">注册</h3>
      <span class="text-primary">&nbsp;&nbsp;&nbsp;&nbsp;用户名:</span>
      <input
        type="text"
        id="username"
        name="username"
        class="form-control"
        style="display:inline"
        @change="username=$event.target.value"
      />
      <br /><br />
      <span class="text-primary">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;密码:</span>
      <input
        type="password"
        id="password"
        name="password"
        class="form-control"
        style="display:inline"
        @change="password=$event.target.value"
      />
      <br /><br />
      <span class="text-primary">确认密码:</span>
      <input
        type="password"
        id="confirmPassword"
        class="form-control"
        style="display:inline"
        @change="confirmPassword=$event.target.value"
      />
      <br /><br />
      <span class="text-primary">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;昵称:</span>
      <input
        type="text"
        id="nickname"
        name="nickname"
        class="form-control"
        style="display:inline"
        @change="nickname=$event.target.value"
      />
      <br /><br />
      <input type="button" class="btn btn-info" @click="getData()" value="获取验证码" />
      <div id="codeBox" v-show="isCodeBoxShow"><br />
        <img id="codeImg" />
        <br />
        <span class="text-primary">
          验证码(请尽快填写,此验证码将在一分钟后失效,看不清可以重新获):
        </span>
        <input
          type="text"
          id="code"
          name="code"
          class="form-control"
          style="inline"
          @change="code=$event.target.value"
        /><br />
        <input type="button" class="btn btn-success" value="注册" @click="signUp();" />
      </div>
      <br>
      <router-link to="/user/signIn">已经有账户?去登陆!</router-link>
    </form>
    <b-modal id="modal" ref="modal" title="提示" hide-footer>
      <h3>{{info}}</h3>
      <br />
      <br />
      <b-button block @click="$bvModal.hide('modal');">确定</b-button>
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
  nickname:"",
  password: "",
  confirmPassword:"",
  code: "",
  info:"",
  data() {
    return {
      isCodeBoxShow: this.CodeBoxShow,
      showModal: this.showModal,
      info:this.info
    };
  },
  methods: {
    alert(text) {
        this.info=text;
        this.$refs["modal"].show();
    },
    getData() {
      var username = document.getElementById("username").value;
      if (username == "") {
        this.alert("请先输入用户名");
        return;
      }
      const api = "/api/code";
      Axios.get(api, {
        params: {
          username: username,
          method:"singUp"
        }
      }).then(response => {
        this.isCodeBoxShow = true;
        var img = document.getElementById("codeImg");
        img.src = "data:image/jpeg;base64," + response.data;
      });
    },
    signUp() {
      const api = "/api/user/signUp";
      if(this.password!=this.confirmPassword){
          this.alert("两次密码输入不同呢!");
          return;
      }
      var pwd = this.$md5(this.password);
      Axios.post(api, {
        username: this.username,
        code: this.code,
        password: pwd,
        nickname:this.nickname
      }).then(response=>{
        if(response.data.message=="code wrong"){
          this.alert("验证码不对呢,你确定你不是机器人吗?!");
        }else if(response.data.message=="username repeat"){
          this.alert("您的用户名太抢手了,来晚了一步呢.");
        }else if(response.data.message=="success"){
          this.alert("恭喜你,注册成功!")
          this.$router.push("/user");
          window.location.reload();
        }else{
          this.alert(response.data.message);
        }
      });
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