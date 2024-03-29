<template>
  <SidebarApplication
    :group="group"
    :application="application"
    @selected="selected"
  >
    <template #context>
      <li>
        <nuxt-link
          :to="{
            name: 'database-api-docs-detail',
            params: {
              databaseId: application.id,
            },
          }"
        >
          <i class="context__menu-icon fas fa-fw fa-book"></i>
          {{ $t('sidebar.viewAPI') }}
        </nuxt-link>
      </li>
    </template>
    <template v-if="application._.selected" #body>
      <ul class="tree__subs">
        <SidebarItem
          v-for="table in orderedTables"
          :key="table.id"
          v-sortable="{
            id: table.id,
            update: orderTables,
            marginLeft: 34,
            marginRight: 10,
            marginTop: -1.5,
          }"
          :database="application"
          :table="table"
        ></SidebarItem>
      </ul>
      <a class="tree__sub-add" @click="$refs.createTableModal.show()">
        <i class="fas fa-plus"></i>
        {{ $t('sidebar.createTable') }}
      </a>
      <CreateTableModal
        ref="createTableModal"
        :application="application"
      ></CreateTableModal>
    </template>
  </SidebarApplication>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'
import SidebarItem from '@baserow/modules/database/components/sidebar/SidebarItem'
import CreateTableModal from '@baserow/modules/database/components/table/CreateTableModal'
import SidebarApplication from '@baserow/modules/core/components/sidebar/SidebarApplication'

export default {
  name: 'Sidebar',
  components: { SidebarApplication, SidebarItem, CreateTableModal },
  props: {
    application: {
      type: Object,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },
  computed: {
    orderedTables() {
      return this.application.tables
        .map((table) => table)
        .sort((a, b) => a.order - b.order)
    },
  },
  methods: {
    async selected(application) {
      try {
        await this.$store.dispatch('application/select', application)
      } catch (error) {
        notifyIf(error, 'group')
      }
    },
    async orderTables(order, oldOrder) {
      try {
        await this.$store.dispatch('table/order', {
          database: this.application,
          order,
          oldOrder,
        })
      } catch (error) {
        notifyIf(error, 'table')
      }
    },
  },
}
</script>

<i18n>
{
  "en":{
    "sidebar": {
      "viewAPI": "View API Docs",
      "createTable": "Create table"
    }
  },
  "fr":{
    "sidebar": {
      "viewAPI": "Documentation de l'API",
      "createTable": "Ajouter une table"
    }
  }
}
</i18n>
