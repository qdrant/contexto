<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title> Contexto.me Solver </q-toolbar-title>

        <div>Qdrant</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";
import EssentialLink from "components/EssentialLink.vue";

const linksList = [
  {
    title: "Docs",
    caption: "qdrant.tech/documentation",
    icon: "school",
    link: "https://qdrant.tech/documentation",
  },
  {
    title: "Qdrant",
    caption: "qdrant.tech",
    icon: "public",
    link: "https://qdrant.tech",
  },
  {
    title: "GitHub - Qdrant",
    caption: "github.com/qdrant/qdrant",
    icon: "code",
    link: "https://github.com/qdrant/qdrant",
  },
  {
    title: "Discord Chat Channel",
    caption: "qdrant.to/discord",
    icon: "chat",
    link: "https://qdrant.to/discord",
  },
  {
    title: "Twitter",
    caption: "@qdrant_engine",
    icon: "rss_feed",
    link: "https://twitter.com/qdrant_engine",
  },
];

export default defineComponent({
  name: "MainLayout",

  components: {
    EssentialLink,
  },

  setup() {
    const leftDrawerOpen = ref(false);

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
});
</script>
