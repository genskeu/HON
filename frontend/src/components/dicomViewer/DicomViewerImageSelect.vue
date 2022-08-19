<template>
    <!-- image and mask selector -->
    <div class='flex items-center row-span-1 col-span-1 animate-fade-in-up'>
        <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
          title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
            <label class="input-group-text w-35">Viewer {{this.viewerIndex + 1}}</label>
            <select ref='image_select_id'
                class='form-select'
                v-model="stackDisplayed">
                <option></option>
                <option v-for='(stack, name) in stacks' :key='stack.name' :value="stack.cs_stack">
                    {{ name }}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    viewerIndex: Number
  },
  computed: {
    stacks () {
      return this.$store.getters['openStudy/stacks']
    },
    stackDisplayed: {
      get () {
        return this.$store.getters['imageViewers/stackDisplayed'](this.viewerIndex)
      },
      set (stack) {
        // can be deleted after db change
        this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack, index: this.viewerIndex })
      }
    }
  }
}
</script>

<style>

</style>
