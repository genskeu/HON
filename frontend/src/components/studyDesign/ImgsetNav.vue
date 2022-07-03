<template>
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Imgset Active</label>
        <select class='form-select' v-model="imgsetActive">
            <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{imgset.position}}</option>
        </select>
    </div>
</template>

<script>
export default {
  name: 'ImgsetControl',
  data () {
    return {
      imgsetActive: undefined
    }
  },
  computed: {
    imgsets () {
      return this.$store.getters['openStudy/imgsets']
    }
  },
  watch: {
    imgsetActive: {
      handler (newImgset) {
        newImgset.image_stacks.forEach((stack, index) => {
          stack.cs_stack.imageIds[0] = stack.cs_stack.imageIds[0].replace('127.0.0.1', 'localhost:5000')
          // debugger // eslint-disable-line no-debugger
          this.$store.commit('cornerstoneViewers/imageDisplayed', { imageDisplayed: [stack.cs_stack.imageIds, stack.cs_stack], index: index })
        })
      }
    }
  }
}
</script>

<style>

</style>
