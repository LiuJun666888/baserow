<template>
  <ul v-if="!tableLoading" class="header__filter header__filter--full-width">
    <li class="header__filter-item">
      <a
        ref="stackedContextLink"
        class="header__filter-link"
        @click="
          $refs.stackedContext.toggle(
            $refs.stackedContextLink,
            'bottom',
            'left',
            4
          )
        "
      >
        <i class="header__filter-icon fas fa-chevron-circle-down"></i>
        <span class="header__filter-name">
          <template v-if="view.single_select_field === null">Stack by</template
          ><template v-else>Stacked by {{ stackedByFieldName }}</template></span
        >
      </a>
      <Context ref="stackedContext">
        <KanbanViewStackedBy
          :table="table"
          :view="view"
          :fields="fields"
          :primary="primary"
          :read-only="readOnly"
          :store-prefix="storePrefix"
          @refresh="$emit('refresh', $event)"
        ></KanbanViewStackedBy>
      </Context>
    </li>
    <li v-if="singleSelectFieldId !== -1" class="header__filter-item">
      <a
        ref="customizeContextLink"
        class="header__filter-link"
        @click="
          $refs.customizeContext.toggle(
            $refs.customizeContextLink,
            'bottom',
            'left',
            4
          )
        "
      >
        <i class="header__filter-icon fas fa-cog"></i>
        <span class="header__filter-name">Customize cards</span>
      </a>
      <ViewFieldsContext
        ref="customizeContext"
        :fields="allFields"
        :read-only="readOnly"
        :field-options="fieldOptions"
        @update-all-field-options="updateAllFieldOptions"
        @update-field-options-of-field="updateFieldOptionsOfField"
        @update-order="orderFieldOptions"
      ></ViewFieldsContext>
    </li>
  </ul>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import { notifyIf } from '@baserow/modules/core/utils/error'
import ViewFieldsContext from '@baserow/modules/database/components/view/ViewFieldsContext'
import KanbanViewStackedBy from '@baserow_premium/components/views/kanban/KanbanViewStackedBy'
import kanbanViewHelper from '@baserow_premium/mixins/kanbanViewHelper'

export default {
  name: 'KanbanViewHeader',
  components: { KanbanViewStackedBy, ViewFieldsContext },
  mixins: [kanbanViewHelper],
  props: {
    database: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    primary: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    stackedByFieldName() {
      const allFields = [this.primary].concat(this.fields)
      for (let i = 0; i < allFields.length; i++) {
        if (allFields[i].id === this.view.single_select_field) {
          return allFields[i].name
        }
      }
      return ''
    },
    allFields() {
      return [this.primary].concat(this.fields)
    },
    ...mapState({
      tableLoading: (state) => state.table.loading,
    }),
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        singleSelectFieldId:
          this.$options.propsData.storePrefix +
          'view/kanban/getSingleSelectFieldId',
      }),
    }
  },
  methods: {
    async updateAllFieldOptions({ newFieldOptions, oldFieldOptions }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/kanban/updateAllFieldOptions',
          {
            newFieldOptions,
            oldFieldOptions,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateFieldOptionsOfField({ field, values, oldValues }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/kanban/updateFieldOptionsOfField',
          {
            field,
            values,
            oldValues,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async orderFieldOptions({ order }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/kanban/updateFieldOptionsOrder',
          {
            order,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  },
}
</script>
