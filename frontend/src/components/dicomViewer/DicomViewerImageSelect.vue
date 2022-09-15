<template>
    <!-- image and mask selector -->
    <div class='flex items-center row-span-1 col-span-1 animate-fade-in-up'>
        <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
          title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
            <label class="input-group-text w-35">Viewer {{this.viewerIndex + 1}}</label>
            <select ref='image_select_id'
                class='form-select'
                v-model="stackDisplayed">
                <option :value="undefined"></option>
                <option v-for='stack in stacks' :key='stack.name' :value="{ cs_stack: stack.cs_stack, name: stack.name }">
                    {{ stack.name }}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    viewerIndex: Number,
    viewerType: String
  },
  computed: {
    stacks () {
      return this.$store.getters['openStudy/stacks']
    },
    stackDisplayed: {
      get () {
        const stackDisplayed = this.$store.getters['imageViewers/stackDisplayed'](this.viewerIndex, this.viewerType)
        if (stackDisplayed) {
          return { cs_stack: stackDisplayed.csStack, name: stackDisplayed.name }
        } else {
          return undefined
        }
      },
      set (stack) {
        if (stack !== undefined) {
          this.$store.commit('imageViewers/stackDisplayed',
            {
              name: stack.name,
              stackDisplayed: stack.cs_stack,
              index: this.viewerIndex,
              viewertype: this.viewerType
            }
          )
        } else {
        }
      }
    }
  }
}
</script>

<style>

</style>
