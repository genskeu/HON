<template>
  <div>
    <div class="row mx-auto mt-2" id="imgset_settings_title">
      <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#imgset_settings"
        aria-expanded="true">
        <h4 class="w-100 mt-1">Image Sets &#9776;</h4>
      </button>
    </div>
    <div id="imgset_settings" class="collapse show">
      <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Image Set Displayed</label>
        <select class='form-select' v-model="imgsetActive">
          <option :value="undefined"></option>
          <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{ imgset.position + 1 }}</option>
        </select>
        <label class="input-group-text">/{{ imgsets.length }}</label>
      </div>
      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_displayed"
          aria-expanded="true" aria-controls="images_displayed"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Images displayed</h5>
        </button>
      </div>

      <div id="images_displayed" class="collapse show">
        <div v-if="refviewerNumb" class="input-group-text">
          <h5 class="mx-auto">Reference-Images</h5>
        </div>
        <div v-for="index in refviewerNumb" :key="index">
          <DicomViewerImageSelect :viewer-index="index - 1"></DicomViewerImageSelect>
        </div>
        <div v-if="refviewerNumb" class="input-group-text">
          <h5 class="mx-auto">Images</h5>
        </div>
        <div v-for="index in viewerNumb" :key="index">
          <DicomViewerImageSelect :viewer-index="refviewerNumb + index - 1"></DicomViewerImageSelect>
        </div>
      </div>
      <!-- default viewport settings -->
      <div id="viewport_settings_container" class="w-100 mt-1" title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images.
                        Each viewport can be controlled individually.
                        To globally control viewport settings use the defaults submenu.">
        <div class="row mt-1 mx-auto">
          <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#viewport_settings"
            aria-expanded="true" aria-controls="viewport_settings">
            <h4 class="w-100 mt-1" id="imgset_btn">Viewer Settings</h4>
          </button>
        </div>
      </div>
      <div id="viewport_settings" class="collapse">
        <div id="viewports_man_container" v-for="(viewer, index) in imageViewers" :key="index">
          <DicomViewportControl :target-viewer="index"></DicomViewportControl>
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <!-- <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_create_man"
          aria-expanded="true" aria-controls="images_create_man"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (manual)</h5>
        </button> -->
      </div>
      <div id="images_create_man" class="collapse show">
        <div class="row mx-auto">
          <button class="imgset_btn btn-success btn mb-1" id="add_imgset" title="add image-set to the end of the study"
            @click="addImgset">add new imgset
          </button>
        </div>
        <div v-if="imgsetActive" class="row mx-auto">
          <button value="update loaded imgset" class="imgset_btn btn-light btn mb-1" id="upd_imgset"
            title="update currently selected image-set">update loaded imgset
          </button>
        </div>
        <div v-if="imgsetActive" class="row mx-auto">
          <button value="delete loaded imgset" class="imgset_btn btn-danger btn mb-1" id="del_imgset"
            title="delete currently selected image-set">delete loaded imgset
          </button>
        </div>
        <div v-if="imgsets.length" class="row mx-auto">
          <button value="delete all imgsets" class="imgset_btn btn-danger btn mb-1" id="del_all_imgsets">delete all
            imgsets
          </button>
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
        <!-- study type -->
        <div class="input-group w-100">
          <label class="input-group-text w-50">Imgset Type</label>
          <select class="form-select" ref="imgsetType">
            <option value="standard">standard</option>
            <option value="afc">alternative forced choice</option>
          </select>
        </div>
        <!-- order -->
        <div class="input-group w-100">
          <label class="input-group-text w-50">Imgset Order</label>
          <select class="form-select" ref="imgsetOrder">
            <option value="ordered">ordered</option>
            <option value="random">random</option>
          </select>
        </div>
        <!-- signal info -->
        <div v-if="afcCreateAuto" class="input-group w-100">
          <label class="input-group-text">Signal Present Pattern:</label>
          <select class="form-select pattern_imgset_auto" id="pos_pattern" placeholder="pattern pos class">
            <option></option>
          </select>
        </div>
        <div v-if="afcCreateAuto" class="input-group w-100">
          <label class="input-group-text">Signal Absent Pattern:</label>
          <select class="form-select pattern_imgset_auto" id="neg_pattern" placeholder="pattern neg class">
            <option></option>
          </select>
        </div>
        <div class="mt-1">
        <button @click="createImgsetsAuto" class="w-100 btn btn-success imgset_btn" value="generate imgsets" id="btn_auto_imgset">
          Create Imgsets
        </button>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
import DicomViewerImageSelect from '@/components/dicomViewer/DicomViewerImageSelect.vue'
import DicomViewportControl from '@/components/dicomViewer/DicomViewportControl.vue'

export default {
  name: 'ImgsetControl',
  components: {
    DicomViewerImageSelect,
    DicomViewportControl
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
    },
    refviewerNumb () {
      return this.$store.getters['openStudy/refviewerNumb']
    },
    imageViewers () {
      return this.$store.getters['imageViewers/cornerstoneViewers']
    },
    afcCreateAuto () {
      if (this.$refs.imgsetType) {
        return this.$refs.imgsetType.value === 'afc'
      }
      return false
    }
  },
  watch: {
    imgsetActive: {
      handler (newImgset) {
        newImgset.imageStacks.forEach((stack, index) => {
          // ensure same structure as select menu values
          stack.csStack.name = stack.name
          this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack.csStack, index: index })
        })
      }
    }
  },
  methods: {
    addImgset () {
      const imgset = this.$store.getters['imageViewers/getImgset']
      if (this.imgsetActive === undefined) {
        imgset.position = this.imgsets.length
      } else {
        imgset.position = this.imgsetActive.position
      }
      this.$store.commit('openStudy/addImgset', imgset)
      this.imgsetActive = imgset
    },
    updateImgset () {

    },
    deleteImgset () {

    },
    deleteImgsets () {

    },
    createImgsetsAuto () {
      this.$store.commit('openStudy/createImgsetsAuto', {})
    }
  }
}
</script>

<style>
</style>
