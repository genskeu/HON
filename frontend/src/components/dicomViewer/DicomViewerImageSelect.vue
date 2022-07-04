<template>
    <!-- image and mask selector -->
    <div class='flex items-center row-span-1 col-span-1 animate-fade-in-up'>
        <div class='flex grow items-center mr-2'>
            <label class='block text-sm font-medium'>Select your Image:
            </label>
            <select ref='image_select_id'
                class='border grow text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5'
                v-model="stackDisplayed">
                <option></option>
                <option v-for='stack in stacks' :key='stack.name' :value="stack">
                    {{ stack.name }}
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
