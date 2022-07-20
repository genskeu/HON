<template>
  <div>
    <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Imgset Active</label>
        <select class='form-select' v-model="imgsetActive">
            <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{imgset.position}}</option>
        </select>
    </div>
        <div class="row mx-auto">
            <button value="append imgset" class="imgset_btn btn-success btn" id="add_imgset"
                title="add image-set to the end of the study">append imgset</button>
        </div>
        <div class="row mx-auto">
            <input value="insert imgset" class="imgset_btn btn-success btn" id="insert_imgset"
                title="inserts image-set at the currently selected position" />
        </div>
        <div class="row mx-auto">
            <input value="update imgset" class="imgset_btn btn-light btn" id="upd_imgset"
                title="update currently selected image-set" />
        </div>
        <div class="row mx-auto">
            <input value="delete imgset" class="imgset_btn btn-danger btn" id="del_imgset"
                title="delete currently selected image-set" />
        </div>
        <div class="row mx-auto">
            <input value="delete all imgsets" class="imgset_btn btn-danger btn" id="del_all_imgsets" />
        </div>
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
          // ensure same structure as select menu values
          stack.cs_stack.name = stack.name
          this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack.cs_stack, index: index })
        })
      }
    }
  }
}
</script>

<style>

</style>
