import Vue from "vue";
import Router from "vue-router";
import signs from "@/components/signs/signs";
import signIn from "@/components/signs/signIn";
import signUp from "@/components/signs/signUp";
import info from "@/components/signs/info";
import home from "@/components/blogs/home";
import write from "@/components/blogs/write";
import newBlog from "@/components/blogs/newBlog"

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: home
    },
    {
      path:"/write",
      name:"write",
      component:write
    },
    {
      path:"/newBlog",
      name:"newBlog",
      component:newBlog
    },
    {
      path: "/user",
      name: "signs",
      component: signs,
      children: [
        {
          path: "signIn",
          name: "signIn",
          component: signIn
        },
        {
          path: "signUp",
          name: "signUp",
          component: signUp
        }
      ]
    },
    {
      path: "/info",
      name: "info",
      component: info
    }
  ]
});
