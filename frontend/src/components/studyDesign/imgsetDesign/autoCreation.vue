<template>
  <div>
    <!-- heading -->
    <div class="row">
      <div class="col-2 my-auto mx-auto">
        <button class="btn btn-secondary btn-lg" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
          :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
        </button>
      </div>

      <div class="col-10">
        <h2 class="accordion-header">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#images_create_auto" aria-expanded="true" aria-controls="images_create_auto">
            Auto-Creation
          </button>
        </h2>
      </div>
    </div>
    <!-- content -->
    <div id="images_create_auto" class="collapse">
      <!-- imgset type -->
      <div class="input-group w-100">
        <label class="input-group-text w-50">Img-Set Type</label>
        <select class="form-select" ref="imgsetType">
          <option value="standard">standard</option>
          <!-- <option value="afc">alternative forced choice</option> -->
        </select>
      </div>
      <!-- order -->
      <div class="input-group w-100">
        <label class="input-group-text w-50">Img-Set Order</label>
        <select class="form-select" ref="imgsetOrder">
          <option value="ordered">ordered</option>
          <!-- <option value="random">random</option> -->
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
      <!-- viewport settings -->
      <div id="viewport_settings_container_auto" class="w-100 mt-1"
        title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images. Each viewport can be controlled individually.">
        <div class="row mx-auto">
          <button class="text-start btn btn-light input-group-text bg-gray-300" data-bs-toggle="collapse"
            data-bs-target="#viewport_settings_auto" aria-expanded="true" aria-controls="viewport_settings_auto">
            <div class="mr-auto" id="imgset_btn">Viewer Settings</div>
          </button>
        </div>
        <div id="viewport_settings_auto" class="collapse show">
          <!-- <div v-if="refviewerNumb" class="input-group-text">
            <h5 class="mx-auto">Reference-Images</h5>
          </div>
          <div v-if="refviewerNumb"> -->
            <!-- windowing -->
            <!-- <div class="mx-auto">
              <div class="input-group mx-auto">
                <label class="input-group-text w-20">WW/WC</label>
                <input type="Number" step="any" min="0" class="form-control ww viewport_prop" placeholder="WW"
                  v-model.number="refViewerSettings.windowWidth" />
                <input type="Number" step="any" class="form-control wc viewport_prop" placeholder="WC"
                  v-model.number="refViewerSettings.windowCenter" />
              </div>
            </div> -->

            <!-- window zoom -->
            <!-- <div class="mx-auto">
              <div class="input-group">
                <label class="input-group-text w-20">Zoom</label>
                <input type="Number" step="0.1" min="0.1" class="form-control zoom viewport_prop" placeholder="Zoom"
                  v-model.number="refViewerSettings.scale" />
              </div>
            </div> -->

            <!-- window position -->
            <!-- <div class="mx-auto">
              <div class="input-group">
                <label class="input-group-text w-20">Pos</label>
                <input type="Number" step="any" class="form-control pos_x viewport_prop" placeholder="x"
                  v-model.number="refViewerSettings.posX" />
                <input type="Number" step="any" class="form-control pos_y viewport_prop" placeholder="y"
                  v-model.number="refViewerSettings.posY" />
              </div>
            </div> -->

            <!-- rotation -->
            <!-- <div class="mx-auto">
              <div class="input-group">
                <label class="input-group-text w-20">Rotation</label>
                <input type="Number" step="1" class="form-control pos_y viewport_prop" placeholder="rotation"
                  v-model.number="refViewerSettings.rotation" />
              </div>
            </div>
          </div>
          <div v-if="refviewerNumb" class="input-group-text">
            <h5 class="mx-auto">Images</h5>
          </div> -->
          <div>
            <!-- windowing -->
            <div class="mx-auto">
              <div class="input-group mx-auto">
                <label class="input-group-text tw-w-20">WW/WC</label>
                <input type="Number" step="any" min="0" class="form-control ww viewport_prop" placeholder="WW"
                  v-model.number="viewerSettings.windowWidth" />
                <input type="Number" step="any" class="form-control wc viewport_prop" placeholder="WC"
                  v-model.number="viewerSettings.windowCenter" />
              </div>
            </div>

            <!-- window zoom -->
            <div class="mx-auto">
              <div class="input-group">
                <label class="input-group-text tw-w-20">Zoom</label>
                <input type="Number" step="0.1" min="0.1" class="form-control zoom viewport_prop" placeholder="Zoom"
                  v-model.number="viewerSettings.scale" />
              </div>
            </div>

            <!-- window position -->
            <div class="mx-auto">
              <div class="input-group">
                <label class="input-group-text tw-w-20">Pos</label>
                <input type="Number" step="any" class="form-control pos_x viewport_prop" placeholder="x"
                  v-model.number="viewerSettings.posX" />
                <input type="Number" step="any" class="form-control pos_y viewport_prop" placeholder="y"
                  v-model.number="viewerSettings.posY" />
              </div>
            </div>

            <!-- rotation -->
            <div class="mx-auto">
              <div class="input-group">
                <label class="input-group-text tw-w-20">Rotation</label>
                <input type="Number" step="1" class="form-control pos_y viewport_prop" placeholder="rotation"
                  v-model.number="viewerSettings.rotation" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- btns -->
      <div class="mt-1">
        <button @click="createImgsets" class="text-start w-100 btn btn-success imgset_btn" value="generate imgsets"
          id="btn_auto_imgset">
          Create Image-Sets
        </button>
        <div v-if="imgsets.length" class="row mx-auto">
        <button class="text-start btn-light btn" @click="updateImgsets">Update all Image-Sets
        </button>
      </div>
      <div v-if="imgsets.length" class="row mx-auto">
        <button class="text-start btn-danger btn" @click="deleteImgsets">Delete all Image-Sets
        </button>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import cornerstone from 'cornerstone-core'

export default {
  name: 'ImgsetControlAuto',
  components: {
  },
  data () {
    return {
      imagesetAddPosition: 1,
      popoverTitle: 'Section Info',
      popoverText: 'This section can be used to automatically add all uploaded images to Image-Sets as well as update or delete all imgsets created so far. Settings such as image position, windowing and zoom level can be controlled via the Viewer Settings Menu.',
      viewerSettings: {
        windowWidth: null,
        windowCenter: null,
        scale: null,
        posX: null,
        posY: null,
        rotation: null
      },
      refViewerSettings: {
        windowWidth: null,
        windowCenter: null,
        scale: null,
        posX: null,
        posY: null,
        rotation: null
      }
    }
  },
  computed: {
    imgsets () {
      return this.$store.getters['currentStudy/imgsets']
    },
    viewerNumb () {
      return this.$store.getters['currentStudy/viewerNumb']
    },
    refviewerNumb () {
      return this.$store.getters['currentStudy/refviewerNumb']
    },
    imageViewers () {
      return this.$store.getters['imageViewers/viewers']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    },
    afcCreateAuto () {
      if (this.$refs.imgsetType) {
        return this.$refs.imgsetType.value === 'afc'
      }
      return false
    },
    stacks () {
      return this.$store.getters['currentStudy/stacks']
    }
  },
  methods: {
    deleteImgsets () {
      const studyId = this.$route.params.id
      this.$store.dispatch('currentStudy/deleteAllImgsets', studyId)
    },
    createImgsets () {
      const studyId = this.$route.params.id
      const element = cornerstone.getEnabledElements()[0].element
      const imageId = this.stacks[0].cs_stack.imageIds[0]

      if (this.viewerSettings.windowCenter || this.viewerSettings.windowWidth || this.viewerSettings.scale || this.viewerSettings.rotation || this.viewerSettings.posX || this.viewerSettings.posY) {
        cornerstone.loadImage(imageId)
        .then((image) => {
          var viewport = cornerstone.getDefaultViewportForImage(element, image)
          viewport.voi.windowWidth = this.viewerSettings.windowWidth ? this.viewerSettings.windowWidth : viewport.voi.windowWidth
          viewport.voi.windowCenter = this.viewerSettings.windowCenter ? this.viewerSettings.windowCenter : viewport.voi.windowCenter
          viewport.scale = this.viewerSettings.scale ? this.viewerSettings.scale : viewport.scale
          viewport.rotation = this.viewerSettings.rotation ? this.viewerSettings.rotation : viewport.rotation
          viewport.translation.x = this.viewerSettings.posX ? this.viewerSettings.posX : viewport.translation.x
          viewport.translation.y = this.viewerSettings.posY ? this.viewerSettings.posY : viewport.translation.y
          this.$store.dispatch('currentStudy/createImgsetsAuto',
            {
              studyId: studyId,
              viewport: viewport
            })
        })
      } else {
        this.$store.dispatch('currentStudy/createImgsetsAuto',
            {
              studyId: studyId,
              viewport: null
            })
      }
    },
    updateImgsets () {
      const studyId = this.$route.params.id
      this.$store.dispatch('currentStudy/updateAllImgsets',
        {
          studyId: studyId,
          viewport: this.viewerSettings
        })
    }
  }
}

</script>

<style>

</style>
