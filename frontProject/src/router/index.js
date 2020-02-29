import Vue from "vue";
import Router from "vue-router";
import signs from "@/components/signs/signs";
import signIn from "@/components/signs/signIn";
import signUp from "@/components/signs/signUp";
import info from "@/components/signs/info"

Vue.use(Router);

export default new Router({
  routes: [{
    path: "/user",
    name: "signs",
    component: signs,
    children: [{
        path: "signIn",
        name: "signIn",
        component: signIn
      },
      {
        path: "signUp",
        name: "signUp",
        component: signUp
      },
    ],
  },
  {
    path:"/info",
    name:"info",
    component: info
  }
]
});
