<template>
  <Context>
    <ul class="context__menu">
      <li>
        <a @click=";[$emit('create-row'), hide()]">
          <i class="context__menu-icon fas fa-fw fa-plus"></i>
          Create row
        </a>
      </li>
      <li v-if="option !== null">
        <a
          ref="updateContextLink"
          @click="$refs.updateContext.toggle($refs.updateContextLink)"
        >
          <i class="context__menu-icon fas fa-fw fa-pen"></i>
          Edit stack
        </a>
        <KanbanViewUpdateStackContext
          ref="updateContext"
          :option="option"
          :fields="fields"
          :primary="primary"
          :store-prefix="storePrefix"
          @saved="hide()"
        ></KanbanViewUpdateStackContext>
      </li>
      <li v-if="option !== null">
        <a @click="$refs.deleteModal.show()">
          <i class="context__menu-icon fas fa-fw fa-trash-alt"></i>
          Delete stack
        </a>
      </li>
    </ul>
    <Modal v-if="option !== null" ref="deleteModal">
      <h2 class="box__title">Delete {{ option.value }}</h2>
      <Error :error="error"></Error>
      <div>
        <p>
          Are you sure that you want to delete stack {{ option.value }}?
          Deleting the stack results in deleting the select option of the single
          select field, which might result into data loss because row values are
          going to be set to empty.
        </p>
        <div class="actions">
          <div class="align-right">
            <a
              class="button button--large button--error"
              :class="{ 'button--loading': loading }"
              :disabled="loading"
              @click="deleteStack()"
            >
              Delete {{ option.value }}
            </a>
          </div>
        </div>
      </div>
    </Modal>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import error from '@baserow/modules/core/mixins/error'
import KanbanViewUpdateStackContext from '@baserow_premium/components/views/kanban/KanbanViewUpdateStackContext'

export default {
  name: 'KanbanViewStackContext',
  components: { KanbanViewUpdateStackContext },
  mixins: [context, error],
  props: {
    option: {
      validator: (prop) => typeof prop === 'object' || prop === null,
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
    storePrefix: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async deleteStack() {
      this.loading = true

      try {
        const doUpdate = await this.$store.dispatch(
          this.storePrefix + 'view/kanban/deleteStack',
          {
            optionId: this.option.id,
            fields: this.fields,
            primary: this.primary,
            deferredFieldUpdate: true,
          }
        )
        await this.$emit('refresh', {
          callback: () => {
            doUpdate()
            this.loading = false
          },
        })
      } catch (error) {
        this.handleError(error)
        this.loading = false
      }
    },
  },
}
</script>
