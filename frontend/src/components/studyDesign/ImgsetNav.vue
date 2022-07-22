<template>
  <div>
    <div class="row mx-auto mt-2" id="imgset_settings_title">
      <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#imgset_settings"
        aria-expanded="true">
        <h4 class="w-100 mt-1">Imagesets &#9776;</h4>
      </button>
    </div>
    <div id="imgset_settings" class="collapse show">
        <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
          title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
          <label class="input-group-text">Load Imgset</label>
          <select class='form-select' v-model="imgsetActive">
            <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{ imgset.position }}</option>
          </select>
        </div>
        <div class="row mx-auto">
          <input value="delete all imgsets" class="imgset_btn btn-danger btn" id="del_all_imgsets" />
        </div>
      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_displayed"
          aria-expanded="true" aria-controls="images_displayed"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Images displayed</h5>
        </button>
      </div>

      <div id="images_displayed" class="collapse">
        <div v-for="index in viewerNumb" :key="index">
          <DicomViewerImageSelect :viewer-index="index-1"></DicomViewerImageSelect>
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_create_man"
          aria-expanded="true" aria-controls="images_create_man"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (manual)</h5>
        </button>
      </div>
      <div id="images_create_man" class="collapse">
        <div class="row mx-auto">
          <button value="append imgset" class="imgset_btn btn-success btn" id="add_imgset"
            title="add image-set to the end of the study">add new imgset</button>
        </div>
        <div class="row mx-auto">
          <input value="update loaded imgset" class="imgset_btn btn-light btn" id="upd_imgset"
            title="update currently selected image-set" />
        </div>
        <div class="row mx-auto">
          <input value="delete loaded imgset" class="imgset_btn btn-danger btn" id="del_imgset"
            title="delete currently selected image-set" />
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_create_auto"
          aria-expanded="true" aria-controls="images_create_auto"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (auto)</h5>
        </button>
      </div>
      <div id="images_create_auto" class="collapse">
      </div>

    </div>
  </div>
</template>

<script>
import DicomViewerImageSelect from '@/components/dicomViewer/DicomViewerImageSelect.vue'

export default {
  name: 'ImgsetControl',
  components: {
    DicomViewerImageSelect
  },
  data () {
    return {
      imgsetActive: undefined
    }
  },
  computed: {
    imgsets () {
      return this.$store.getters['openStudy/imgsets']
    },
    viewerNumb () {
      return this.$store.getters['openStudy/viewerNumb']
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
